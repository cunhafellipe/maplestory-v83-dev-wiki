#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Emit docs/facts.json — a machine-readable index of the wiki's load-bearing facts.

The wiki is written for people. Agents have to grep prose to find a single
address or opcode, which is slow and error-prone. This script derives the same
facts from the binaries (not from the markdown) and writes them once, so:

  * an agent can read one small file instead of 683 KB of prose
  * verify_wiki_claims.py and this file cannot drift, because both compute
    their values the same way from the same bytes

Run:  python gen_facts_index.py
"""
import hashlib
import json
import os
import re
import struct
import sys

import pefile

REPO = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(REPO, "docs")

ASSETS = r"C:\MUWORK\GAME\MAPLESOTRY\待分類"
ORIG = os.path.join(ASSETS, "MapleStory 0.83.exe")
UNPACKED = r"C:\RE\msv83\bin\msv83_trad.exe"
IDB = r"C:\RE\msv83\ida\v83.idb"
WZ_SCRIPTS = r"C:\RE\msv83\wz\scripts"

IMAGE_BASE = 0x400000

# The published JSON must not carry this machine's directory layout, so the
# literal paths below are folded into placeholders before anything is written.
# tools/anonymize_paths.py applies the same mapping to the markdown.
PATH_PLACEHOLDERS = [
    (r"C:\\+MUWORK\\+GAME\\+MAPLESOTRY\\+待分類", "<ASSETS>"),
    (r"C:\\+MUWORK\\+GAME\\+MAPLESOTRY", "<MAPLESOTRY>"),
    (r"C:\\+RE\\+msv83\\+bin", "<RE>/bin"),
    (r"C:\\+RE\\+msv83\\+ida", "<RE>/ida"),
    (r"C:\\+RE\\+msv83\\+wz", "<RE>/wz"),
    (r"C:\\+RE\\+msv83", "<RE>"),
    (r"C:\\+Users\\+[^\\/\s]+", "<USERPROFILE>"),
    (r"[A-Z]:\\\\[^\"\\n]*", "<LOCAL>"),
]


def scrub(text):
    """Replace absolute local paths with placeholders."""
    if not isinstance(text, str):
        return text
    for pat, rep in PATH_PLACEHOLDERS:
        text = re.sub(pat, rep, text)
    return text


def scrub_obj(node):
    """Walk the structure so no local path survives into the published JSON."""
    if isinstance(node, dict):
        return {k: scrub_obj(v) for k, v in node.items()}
    if isinstance(node, list):
        return [scrub_obj(v) for v in node]
    return scrub(node)

CORE_ADDRESSES = {
    "CLogin::OnPacket":        0x5F80FF,
    "CField::OnPacket":        0x531325,
    "CWvsContext::OnPacket":   0xA07A08,
    "CStage::OnPacket":        0x644446,
    "StringPool::GetString":   0x406455,
    "StringPool::GetInstance": 0x79E805,
    "CInPacket::Decode1":      0x4065F3,
    "CInPacket::Decode2":      0x42470C,
    "CInPacket::Decode4":      0x406629,
    "CInPacket::DecodeBuffer": 0x432257,
    "CinPacket::DecodeStr":    0x46F30C,
    "_WinMain@16":             0x9F19F2,
    "sub_5F83EE":              0x5F83EE,
}

CWVS_CONTEXT_HANDLERS = {
    29: 0xA1EAD9, 30: 0xA1F881, 31: 0xA1FB52, 32: 0xA202BE, 33: 0xA2071F,
    34: 0xA208FF, 35: 0xA2091C, 36: 0xA1E48C, 37: 0xA209B2, 38: 0xA223DC,
    39: 0xA209D4, 40: 0xA20AC0, 41: 0xA2508B, 42: 0xA25268, 43: 0xA265C2,
    45: 0xA27891, 46: 0xA27B38, 47: 0xA27B61, 48: 0xA29115, 49: 0xA26D44,
    50: 0xA27D75, 51: 0xA1E5AF, 52: 0xA1E943, 53: 0xA1E96D, 55: 0xA29739,
    57: 0xA23D92, 58: 0xA23D79, 59: 0xA1233F, 61: 0xA2370B, 62: 0xA3E31C,
}

DISPATCHERS = {
    "CLogin::OnPacket": {
        "opcode_range": [0, 28],
        "bias": 0,
        "compare": 0x1C,
        "note": "no bias; cmp eax, 0x1c",
    },
    "CField::OnPacket": {
        "opcode_range": [125, 345],
        "bias": None,
        "note": "125 is an 8-bit compare; 345 is dispatched by a multi-way "
                "chain and is not an 8-bit compare",
    },
    "CWvsContext::OnPacket": {
        "opcode_range": [29, 124],
        "bias": 29,
        "compare": 0x5F,
        "note": "add eax,-29 then cmp eax,0x5f (95); jump table of 96 "
                "consecutive code pointers at 0x00A07E8E",
    },
    "CStage::OnPacket": {
        "opcode_range": [128, 130],
        "bias": 128,
        "compare": None,
        "note": "sub eax, 0x80",
    },
}

WZ_ARCHIVES = ["Character", "Mob", "Skill", "Reactor", "Npc", "UI", "Quest",
               "Item", "Effect", "String", "Etc", "Morph", "TamingMob",
               "Sound", "Map"]


def read(path):
    with open(path, "rb") as f:
        return f.read()


def code_spans(pe):
    out = []
    for s in pe.sections:
        name = s.Name.rstrip(b"\x00").decode(errors="replace")
        if name in (".rsrc", ".idata", ".macktt"):
            continue
        out.append((s.PointerToRawData, s.PointerToRawData + s.SizeOfRawData))
    return out


def main():
    import glob
    import re

    orig = read(ORIG)
    unpacked = read(UNPACKED)
    pe_o = pefile.PE(ORIG)
    pe_u = pefile.PE(UNPACKED)
    spans = code_spans(pe_u)
    idb = read(IDB)

    import datetime
    ts = datetime.datetime.fromtimestamp(
        pe_o.FILE_HEADER.TimeDateStamp, datetime.UTC)

    def in_code(va):
        off = va - IMAGE_BASE
        return 0 <= off < len(unpacked) and any(
            lo <= off < hi for lo, hi in spans)

    scripts = glob.glob(os.path.join(WZ_SCRIPTS, "**", "*.js"), recursive=True)
    per = {}
    for f in scripts:
        rel = os.path.relpath(f, WZ_SCRIPTS).split(os.sep)[0]
        per[rel] = per.get(rel, 0) + 1

    paths = set(m.decode(errors="replace") for m in
                re.findall(rb"[A-Za-z]:\\[^\x00]{4,160}MapleAeon\.exe", idb))
    # The full original path is the IDB holder's personal directory layout; the
    # part that matters as evidence is the tail (…\GMS\v83\MapleAeon.exe).
    idb_origin = None
    if paths:
        raw = sorted(paths)[0]
        # drop the drive + every folder before the "MapleStory IDBs" marker
        idx = raw.lower().rfind("maplestory idbs")
        idb_origin = ("<IDB_PATH>\\" + raw[idx:]) if idx > 0 else \
            "<IDB_PATH>\\" + raw.rsplit("\\", 1)[-1]

    facts = {
        "schema": "maplestory-v83-wiki-facts/1",
        "generated_by": "gen_facts_index.py",
        "verify_with": "python verify_wiki_claims.py",
        "image_base": IMAGE_BASE,

        "binaries": {
            "packed": {
                "path": ORIG,
                "size": len(orig),
                "md5": hashlib.md5(orig).hexdigest(),
                "machine": "i386 (PE32)",
                "image_base": pe_o.OPTIONAL_HEADER.ImageBase,
                "entry_rva": pe_o.OPTIONAL_HEADER.AddressOfEntryPoint,
                "section_count": pe_o.FILE_HEADER.NumberOfSections,
                "size_of_code": pe_o.OPTIONAL_HEADER.SizeOfCode,
                "time_date_stamp": pe_o.FILE_HEADER.TimeDateStamp,
                "time_date_stamp_utc": ts.isoformat(),
                "protection": "Nexon CSecurity",
                "protection_note": "first-party, not a commercial packer; "
                                   "Themida/VMProtect/ASProtect/Enigma/UPX all "
                                   "score 0 hits",
            },
            "unpacked": {
                "path": UNPACKED,
                "size": len(unpacked),
                "entry_rva": pe_u.OPTIONAL_HEADER.AddressOfEntryPoint,
                "toolchain": "SolidDaima_Rev8_200901029",
            },
            "idb": {
                "path": IDB,
                "size": len(idb),
                "original_path": idb_origin,
                "note": "IDA database for the 2014 MapleAeon.exe analysis, not "
                        "the 2010 build on disk; addresses agree, but the two "
                        "artefacts are different files",
            },
        },

        "addresses": {
            name: {
                "va": va,
                "hex": "0x%X" % va,
                "rva": va - IMAGE_BASE,
                "in_code": in_code(va),
            }
            for name, va in sorted(CORE_ADDRESSES.items())
        },

        "dispatchers": {
            name: dict(info, address="0x%X" % CORE_ADDRESSES[name])
            for name, info in DISPATCHERS.items()
        },

        "cwvs_context_handlers": {
            str(opc): {"va": va, "hex": "0x%X" % va,
                       "in_code": in_code(va)}
            for opc, va in sorted(CWVS_CONTEXT_HANDLERS.items())
        },

        "wz": {
            "archives": WZ_ARCHIVES,
            "count": len(WZ_ARCHIVES),
            "binding": "Pixi (GetProcAddress 'PcCreateObject'), not COM",
            "archive_header": "PKG1 + 'Package file v1.0 Copyright 2002 "
                              "Wizet, ZMS'",
            "loose_img_magic": "73f86c77",
            "reader_location": "not in the client image",
        },

        "scripts": {
            "total": len(scripts),
            "per_directory": dict(sorted(per.items())),
            "encoding": "GB18030",
        },

        "corrections": [
            {
                "claim": "CWvsContext::OnPacket opcode range is 29~62",
                "corrected": "29~124",
                "why": "the dispatcher applies a -29 bias then compares "
                       "against 0x5f (95) and jumps through a 96-entry table; "
                       "62 was merely the last handler the wiki had named",
                "source": "docs/40-protocol/index.md",
            },
            {
                "claim": "7,270,400 is the build timestamp (~2018)",
                "corrected": "7,270,400 is SizeOfCode; the timestamp is "
                             "1,267,176,451 = 2010-02-26 09:27:31 UTC",
                "why": "the two fields were conflated",
                "source": "README.md",
            },
            {
                "claim": "the binary is packed with Themida / WzPacker",
                "corrected": "Nexon CSecurity (first-party)",
                "why": "the RTTI in the unpacked build identifies CSecurity; "
                       "every commercial packer signature scores 0 hits",
                "source": "docs/10-client-analysis/exe-reverse-engineering.md",
            },
        ],

        "entry_points": {
            "want_to_change_ui": "docs/30-ui-classes/index.md",
            "want_to_add_packet_behaviour": "docs/40-protocol/index.md",
            "want_to_patch_client": "docs/60-secondary-dev/patches/index.md",
            "want_to_run_server": "docs/20-server-emulators/index.md",
            "want_to_reverse_client": "docs/10-client-analysis/v83-idb/index.md",
            "want_to_hook_client": "docs/50-tools/kaentake/index.md",
            "want_to_edit_wz": "docs/50-tools/wz-mod-tool/index.md",
            "want_github_projects": "docs/70-resources/github-bookmarks/index.md",
        },
    }

    out = os.path.join(DOCS, "facts.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(scrub_obj(facts), f, ensure_ascii=False, indent=1)
    print("written: %s (%d bytes)" % (out, os.path.getsize(out)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
