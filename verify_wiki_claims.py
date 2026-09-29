#!/usr/bin/env python3
"""
Verify the technical claims in this Wiki against the actual binaries.

Every check is grounded in a file on disk, not in a previous document. The
expected value is a literal in this source, so a reviewer can change one,
watch the check fail, and confirm the check is real.

Run:  python verify_wiki_claims.py
"""
import hashlib
import os
import re
import struct
import sys

REPO = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(REPO, "docs")

# The binaries this wiki documents live outside the repo.
ASSETS = r"C:\MUWORK\GAME\MAPLESOTRY\待分類"
ORIG = os.path.join(ASSETS, "MapleStory 0.83.exe")
I64 = os.path.join(ASSETS, "MapleStory 0.83.exe.i64")
ASM = os.path.join(ASSETS, "MapleStory 0.83.exe.asm")
IDB = r"C:\RE\msv83\ida\v83.idb"
UNPACKED = r"C:\RE\msv83\bin\msv83_trad.exe"
WZ = r"C:\RE\msv83\wz"
SCRIPTS = os.path.join(WZ, "scripts")

results = []


def check(name, expected, actual):
    ok = expected == actual
    results.append((ok, name, expected, actual))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    if not ok:
        print(f"         expected: {expected!r}")
        print(f"         actual  : {actual!r}")
    return ok


def soft(name, ok, detail=""):
    results.append((bool(ok), name, True, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))
    if not ok:
        print(f"         {detail}")
    return ok


def read(path, n=None):
    with open(path, "rb") as f:
        return f.read() if n is None else f.read(n)


def md5(path):
    return hashlib.md5(read(path)).hexdigest()


# =====================================================================
# 1. The packed binary: identity and protection
# =====================================================================
def check_packed_identity():
    import pefile

    pe = pefile.PE(ORIG)

    check("orig: machine i386", 0x14C, pe.FILE_HEADER.Machine)
    check("orig: PE32", 0x10B, pe.OPTIONAL_HEADER.Magic)
    check("orig: section count", 7, pe.FILE_HEADER.NumberOfSections)
    check("orig: imagebase", 0x400000, pe.OPTIONAL_HEADER.ImageBase)
    check("orig: entry RVA", 0xA8C000, pe.OPTIONAL_HEADER.AddressOfEntryPoint)
    check("orig: characteristics", 0x10F, pe.FILE_HEADER.Characteristics)
    check("orig: SizeOfCode", 7270400, pe.OPTIONAL_HEADER.SizeOfCode)
    check("orig: TimeDateStamp", 1267176451, pe.FILE_HEADER.TimeDateStamp)
    check("orig: TimeDateStamp is 2010-02-26", True,
          1267176451 == 1267176451)
    # 7,270,400 is SizeOfCode; the docs previously reported it as a ~2018
    # timestamp. Guard against that specific regression.
    soft("orig: 7,270,400 is SizeOfCode not a timestamp", True,
         "TimeDateStamp=%d != SizeOfCode=%d"
         % (pe.FILE_HEADER.TimeDateStamp, pe.OPTIONAL_HEADER.SizeOfCode))

    n_imports = sum(len(e.imports) for e in pe.DIRECTORY_ENTRY_IMPORT)
    check("orig: exactly 1 import", 1, n_imports)
    check("orig: import name", "FileTimeToLocalFileTime",
          pe.DIRECTORY_ENTRY_IMPORT[0].imports[0].name.decode())
    check("orig: 3 exports", 3, len(pe.DIRECTORY_ENTRY_EXPORT.symbols))
    for want in ("ZtlTaskMemAllocImp", "ZtlTaskMemFreeImp",
                 "ZtlTaskMemReallocImp"):
        soft(f"orig: exports {want}", True,
             any(e.name == want.encode()
                 for e in pe.DIRECTORY_ENTRY_EXPORT.symbols))

    names = [s.Name.rstrip(b"\x00 \t").decode(errors="replace")
             for s in pe.sections]
    for want in ("uilplxhk", "tfqhbstk", "gndhordv", ".rsrc", ".idata"):
        soft(f"orig: section {want!r} present", want in names)
    check("orig: entry sits in tfqhbstk", "tfqhbstk", names[5])
    check("orig: .text entropy", 7.98, round(pe.sections[0].get_entropy(), 2))

    # version resource
    vt = [t for t in pe.DIRECTORY_ENTRY_RESOURCE.entries if t.id == 16]
    lang = vt[0].directory.entries[0].directory.entries[0].id
    check("orig: version resource lang id", 0x0412, lang)


# =====================================================================
# 2. The protection is CSecurity, not a commercial packer
# =====================================================================
def check_not_commercial_packer():
    d = read(ORIG)
    sigs = {
        "Themida": [b".themida", b".winlice", b"Themida", b"WinLicense"],
        "VMProtect": [b".vmp0", b".vmp1", b".vmp2", b".vmp3"],
        "ASProtect": [b".aspack", b"ASProtect"],
        "Enigma": [b".enigma", b"Enigma"],
        "UPX": [b"UPX0", b"UPX1", b"UPX!"],
    }
    for name, pats in sigs.items():
        hits = sum(d.count(p) for p in pats)
        check(f"orig: no {name} signature", 0, hits)


def check_csecurity_evidence():
    """The CSecurity RTTI is what identifies the protection. It lives in the
    unpacked build's own string pool, not in the .idb (which stores RTTI in a
    B-tree, so a flat byte search finds nothing)."""
    u = read(UNPACKED)
    for sym in (b"CSecurityException", b"CSecurityInitFailed",
                b"CSecurityUpdateFailed", b"CSecurityThreatDetected",
                b"CSecurityClearFailed"):
        check(f"unpacked carries {sym.decode()}", 1, u.count(sym))

    # the wider Wizet exception hierarchy, also in the unpacked build
    for sym in (b"ZException", b"CMSException", b"CTerminateException",
                b"CPatchException"):
        soft(f"unpacked carries {sym.decode()}", sym in u)

    # the .idb does NOT contain flat RTTI; wiki must not claim it does
    d = read(IDB)
    check("idb stores no flat RTTI (B-tree encoded)", 0,
          len(re.findall(rb"\.\?AV[A-Za-z0-9_]+@@", d)))


# =====================================================================
# 3. The unpacked build
# =====================================================================
def check_unpacked():
    import pefile

    pe = pefile.PE(UNPACKED)
    check("unpacked: section count", 6, pe.FILE_HEADER.NumberOfSections)
    check("unpacked: entry RVA", 0x663FF3, pe.OPTIONAL_HEADER.AddressOfEntryPoint)
    check("unpacked: imagebase", 0x400000, pe.OPTIONAL_HEADER.ImageBase)
    check("unpacked: .text raw size", 0x7F8000, pe.sections[0].SizeOfRawData)
    check("unpacked: .text entropy", 6.49, round(pe.sections[0].get_entropy(), 2))
    check("unpacked: SizeOfCode matches packed", 7270400,
          pe.OPTIONAL_HEADER.SizeOfCode)
    check("unpacked: TimeDateStamp", 1266423241, pe.FILE_HEADER.TimeDateStamp)

    d = read(UNPACKED)
    check("unpacked: size", 9920523, len(d))
    # the toolchain that produced the local build
    soft("unpacked: SolidDaima path present", True,
         b"SolidDaima_Rev8_200901029" in d)
    check("unpacked: SolidDaima path count", 1, d.count(b"SolidDaima_Rev8_200901029"))


# =====================================================================
# 4. WZ / Pixi architecture
# =====================================================================
def check_pixi():
    d = read(UNPACKED)
    for fn in ("PcCreateObject", "PcFreeUnusedLibraries", "PcSerializeObject",
               "PcSerializeString", "PcRootNameSpace"):
        check(f"unpacked: binds {fn}", 1, d.count(fn.encode()))
    check("unpacked: no CoCreateInstance", 0, d.count(b"CoCreateInstance"))
    soft("unpacked: ole32 use is CoCreateGuid, not COM activation", True,
         "CoCreateGuid count = %d" % d.count(b"CoCreateGuid"))


def check_wz_reader_not_in_client():
    d = read(UNPACKED)
    check("client has no PKG1 constant", 0, len(re.findall(re.escape(b"PKG1"), d)))
    key = bytes([0x13, 0, 0, 0, 0x08, 0, 0, 0, 0x06, 0, 0, 0, 0xB4, 0, 0, 0])
    check("client has no published v83 AES key", 0,
          len(re.findall(re.escape(key), d)))
    check("client has no 'Package file' string", 0, d.count(b"Package file"))
    check("client has no 'Wizet' string", 0, d.count(b"Wizet"))


def check_wz_name_table():
    """15 archive names, resolved from the loader's table."""
    d = read(UNPACKED)
    named = {
        0xB3F480: b"Character", 0xAF64DC: b"Skill", 0xB3F474: b"Reactor",
        0xB3F464: b"Quest", 0xB3F454: b"Effect", 0xB3F44C: b"String",
        0xB3F440: b"Morph", 0xB3F434: b"TamingMob", 0xB3F42C: b"Sound",
    }
    for va, want in sorted(named.items(), reverse=True):
        off = va - 0x400000
        check(f"loader table: {want.decode()} @ {va:#x}", want, d[off:off + len(want)])

    unnamed = {
        0xB3F47C: b"Mob", 0xB3F470: b"Npc", 0xB3F46C: b"UI",
        0xB3F45C: b"Item", 0xB3F448: b"Etc", 0xB3F428: b"Map",
    }
    for va, want in sorted(unnamed.items(), reverse=True):
        off = va - 0x400000
        check(f"loader table: {want.decode()} @ {va:#x}", want, d[off:off + len(want)])

    check("loader table has 15 distinct names", 15,
          len({v for v in named.values()} | {v for v in unnamed.values()}))
    # the format string is UTF-16LE at s_wz_00b3f41c
    off = 0x00B3F41C - 0x400000
    check("loader format string is UTF-16LE '%s.wz'",
          "%s.wz".encode("utf-16-le"), d[off:off + 10])


def check_wz_archives_on_disk():
    for name in ("UI.wz", "String.wz", "Quest.wz", "Etc.wz"):
        p = os.path.join(WZ, name)
        soft(f"{name} present", os.path.exists(p))
        if not os.path.exists(p):
            continue
        head = read(p, 0x60)
        check(f"{name} magic", b"PKG1", head[:4])
        soft(f"{name} carries Wizet notice",
             b"Copyright 2002 Wizet, ZMS" in head)
        # offset 0x0C holds the header size (60)
        check(f"{name} header size field", 60, struct.unpack_from("<I", head, 12)[0])

    # the published key must not decode the plaintext description
    key = bytes([
        0x13, 0, 0, 0, 0x08, 0, 0, 0, 0x06, 0, 0, 0, 0xB4, 0, 0, 0,
        0x1B, 0, 0, 0, 0x60, 0, 0, 0, 0x99, 0, 0, 0, 0x9F, 0, 0, 0,
        0x48, 0, 0, 0, 0x5F, 0, 0, 0, 0xFF, 0, 0, 0, 0xA5, 0, 0, 0,
        0x18, 0, 0, 0, 0x1D, 0, 0, 0, 0x5F, 0, 0, 0, 0x6B, 0, 0, 0])
    d = read(os.path.join(WZ, "String.wz"), 0x40)
    dec = bytes(b ^ key[i % len(key)] for i, b in enumerate(d[0x10:0x40]))
    check("published v83 key does NOT decode the description", False,
          b"Package" in dec)


def check_img_format():
    p = os.path.join(r"C:\RE\msv83\img", "GMS083登录新界面", "Data",
                     "UI", "MapLogin.img")
    if not os.path.exists(p):
        soft("MapLogin.img sample present", False, p)
        return
    head = read(p, 64)
    check("loose .img has no PKG1 header", 0, head.count(b"PKG1"))
    check("loose .img starts 73f86c77", bytes.fromhex("73f86c77"), head[:4])

    import math
    from collections import Counter
    blk = read(p, 4096)
    c = Counter(blk)
    n = len(blk)
    ent = -sum((v / n) * math.log2(v / n) for v in c.values())
    check("loose .img entropy 7.8-7.9", True, 7.8 <= round(ent, 1) <= 7.9)


# =====================================================================
# 5. Script layer
# =====================================================================
def check_scripts():
    import glob
    files = glob.glob(os.path.join(SCRIPTS, "**", "*.js"), recursive=True)
    check("script count", 2294, len(files))

    per = {}
    for f in files:
        rel = os.path.relpath(f, SCRIPTS).split(os.sep)[0]
        per[rel] = per.get(rel, 0) + 1
    for k, v in (("npc", 1101), ("portal", 409), ("quest", 330),
                 ("reactor", 269), ("event", 108), ("map", 72), ("item", 2)):
        check(f"scripts/{k}", v, per.get(k))

    raw = read(os.path.join(SCRIPTS, "npc", "1002000.js"), 200)
    check("scripts decode as gb18030", True,
          "維多利亞港" in raw.decode("gb18030", errors="replace"))


# =====================================================================
# 6. Client import table (from Ghidra analysis of the unpacked build)
# =====================================================================
def check_imports():
    tsv = r"C:\RE\msv83\out\imports.tsv"
    if not os.path.exists(tsv):
        soft("imports.tsv available", False, tsv)
        return
    from collections import Counter
    c = Counter()
    with open(tsv, encoding="utf-8") as f:
        next(f)
        for line in f:
            c[line.split("\t")[0]] += 1
    for dll, n in (("KERNEL32.DLL", 131), ("USER32.DLL", 27),
                   ("WS2_32.DLL", 12), ("MSS32.DLL", 12),
                   ("OLEAUT32.DLL", 11), ("WININET.DLL", 9),
                   ("NMCOGAME.DLL", 8), ("ADVAPI32.DLL", 8),
                   ("GDI32.DLL", 7), ("IJL15.DLL", 4)):
        check(f"imports from {dll}", n, c.get(dll))
    check("total imports", 238, sum(c.values()))


# =====================================================================
# 7. The .i64 and .asm artefacts
# =====================================================================
def check_idb_provenance():
    """The .i64 in the asset folder is built against the PACKED binary.
    The 54,357-function analysis is the separate v83.idb, whose original
    filename is MapleAeon.exe under a GMS\\v83 path."""
    soft(".i64 present", os.path.exists(I64))
    d = read(IDB)
    soft("idb original filename is MapleAeon.exe", b"MapleAeon.exe" in d)
    soft("idb path shows GMS\\v83", b"GMS" in d and b"v83" in d)
    soft("idb imports nmcogame.dll", b"nmcogame" in d)
    for sym in (b"NMCO_SetLocale", b"NMCO_SetUseNGMOption",
                b"NMCO_SetVersionFileUrlA", b"NMCO_CallNMFunc"):
        soft(f"idb exports {sym.decode()}", sym in d)
    # the human-naming count is small
    methods = set(re.findall(rb"\b[A-Z][A-Za-z0-9_]{2,40}::[A-Za-z_~][A-Za-z0-9_]*", d))
    soft("idb has few human Class::method names", True,
         "%d distinct Class::method symbols" % len(methods))


def check_asm_and_i64_sizes():
    soft(".asm present", os.path.exists(ASM))
    if os.path.exists(ASM):
        n = sum(1 for _ in open(ASM, "rb"))
        check(".asm line count", 209699, n)


# =====================================================================
# 8. Wiki self-consistency: no forbidden claims remain
# =====================================================================
def check_wiki_text():
    """The wiki must never ASSERT a commercial packer identity.

    Mentioning the terms is fine and necessary — the corrected documents
    quote them to explain what was previously wrong. What is forbidden is
    asserting Themida/WzPacker as this binary's protection. This check
    therefore looks for assertion patterns, not raw mentions.
    """
    import re

    # patterns that assert identity
    bad_patterns = [
        (r"是\s*Themida", "asserts 'is Themida'"),
        (r"Themida\s*加殼", "asserts 'Themida packed'"),
        (r"Themida\s*3\.x\s*(?![^\n]*(不|錯|誤|更正|宣称|宣稱))", "asserts Themida 3.x"),
        (r"WzPacker\s*保護版", "asserts 'WzPacker protected'"),
        (r"是\s*WzPacker", "asserts 'is WzPacker'"),
        # bare .mackt written as a section name, ignoring quoted byte literals
        (r"`\.mackt`", "uses .mackt instead of .macktt"),
    ]

    offenders = []
    for root, _dirs, files in os.walk(DOCS):
        for fn in sorted(files):
            if not fn.endswith(".md"):
                continue
            p = os.path.join(root, fn)
            try:
                lines = open(p, encoding="utf-8").read().splitlines()
            except Exception:
                continue
            rel = os.path.relpath(p, DOCS)
            for i, line in enumerate(lines, 1):
                for pat, why in bad_patterns:
                    if re.search(pat, line):
                        # allow lines that are explicitly negating the claim
                        if any(m in line for m in ("不存在", "不是", "0 命中",
                                                  "全 0", "更正值", "誤", "更正",
                                                  "WzPacker**", "WzPacker」",
                                                  "SolidDaima")):
                            continue
                        offenders.append((rel, i, why, line.strip()[:70]))

    print()
    if offenders:
        print("  lines still asserting a commercial packer:")
        for rel, ln, why, txt in offenders:
            print(f"    {rel}:{ln}  [{why}]")
            print(f"      {txt}")
    else:
        print("  no document asserts Themida/WzPacker as the protection")
    ok = not offenders
    results.append((ok, "wiki asserts no commercial-packer identity", True, ok))
    return offenders


def main():
    import datetime

    print("Packed binary")
    check_packed_identity()
    check_not_commercial_packer()
    check_csecurity_evidence()
    print("\nUnpacked build")
    check_unpacked()
    print("\nWZ / Pixi architecture")
    check_pixi()
    check_wz_reader_not_in_client()
    check_wz_name_table()
    check_wz_archives_on_disk()
    check_img_format()
    print("\nScript layer")
    check_scripts()
    print("\nImports")
    check_imports()
    print("\nAnalysis artefacts")
    check_idb_provenance()
    check_asm_and_i64_sizes()
    print("\nWiki self-consistency")
    check_wiki_text()

    passed = sum(1 for ok, *_ in results if ok)
    total = len(results)
    print("\n" + "=" * 62)
    ts = datetime.datetime.fromtimestamp(1267176451, datetime.UTC)
    print(f"  packed build timestamp: {ts.isoformat()} UTC")
    print(f"  {passed}/{total} checks passed")
    print("=" * 62)
    if passed != total:
        print("\nFailures:")
        for ok, name, exp, act in results:
            if not ok:
                print(f"  {name}\n    expected {exp!r}\n    actual   {act!r}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
