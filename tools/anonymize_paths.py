#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把文件中的本機絕對路徑換成佔位符,讓公開的 GitHub Pages 版本不洩漏
本機目錄結構,也不對其他人的機器產生誤導。

轉換規則(由長到短,避免先吃掉前綴):
    C:\\MUWORK\\GAME\\MAPLESOTRY   -> <MAPLESOTRY>
    C:\\RE\\msv83                    -> <RE>
    C:\\MUWORK\\app\\scoop           -> <SCOOP>
    C:\\Users\\<任意用戶>\\...        -> <USERPROFILE>/...
    C:\\path\\... / C:\\Nexon\\...    -> 相對路徑或移除

原始掃描檔(00-overview/*-original.md)本來就是「當時在這台機器上做的紀錄」,
路徑是證據的一部分,因此只加註說明、不改寫內容。

Run:  python tools/anonymize_paths.py [--check]
"""
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(REPO, "docs")

# 依序套用;每條是 (regex, replacement)
RULES = [
    # 本專案根目錄
    (r"C:\\+MUWORK\\+GAME\\+MAPLESOTRY", "<MAPLESOTRY>"),
    (r"C:/+MUWORK/GAME/MAPLESOTRY", "<MAPLESOTRY>"),
    # IDA / WZ 工作區
    (r"C:\\+RE\\+msv83", "<RE>"),
    (r"C:/+RE/msv83", "<RE>"),
    # 工具鏈安裝位置
    (r"C:\\+MUWORK\\+app\\+scoop", "<SCOOP>"),
    (r"C:\\+Program Files\\+", "<PROGRAMFILES>/"),
    # 使用者目錄(含 e7896 這類具體帳號)
    (r"C:\\+Users\\+[^\\/\s\"'`]+", "<USERPROFILE>"),
    (r"C:/+Users/+[^/\s\"'`]+", "<USERPROFILE>"),
    # 暫存目錄
    (r"C:\\+Users\\+<USERPROFILE>\\+AppData\\+Local\\+Temp", "<TMP>"),
    (r"[A-Z]:\\\\[^\s\"'`]*?\\\\Temp\\\\", "<TMP>"),
    # 佔位路徑
    (r"C:\\+path\\+to\\+", "<PATH>/to/"),
    (r"C:/+path/to/+", "<PATH>/to/"),
    (r"C:\\+path\\+", "<PATH>/"),
    (r"C:\\+Nexon\\+MapleStory", "<NEXON>/MapleStory"),
    # 工具鏈(IDA / Ghidra / Nexon 內部工具鏈)
    (r"C:\\+MUWORK\\+apps\\+", "<TOOLS>/"),
    (r"C:/+MUWORK/apps/+", "<TOOLS>/"),
    (r"[Ee]:\\\\ACGame_GL\\\\BinTool\\\\[A-Za-z0-9_\\\\.]+", "<BINTOOL>"),
    (r"[Ee]:/ACGame_GL/BinTool/[A-Za-z0-9_./]+", "<BINTOOL>"),
    (r"[Ee]:\\\\Work\\\\[^\s\"'`)\]]+", "<WORKDIR>"),
    (r"[Ee]:/Work/[^\s\"'`)\]]+", "<WORKDIR>"),
    (r"[Ee]:\\\\[^\s\"'`)\]]+", "<DRIVE_E>"),
    (r"[Ee]:/[^\s\"'`)\]]+", "<DRIVE_E>"),
    (r"C:\\\\", ""),
    # 大小寫混雜的 Program Files(strings.md 內的雙重跳脫殘留)
    (r"[Cc]:\\\\+[Pp]rogram\s?[Ff]iles\\\\+", "<PROGRAMFILES>/"),
    (r"[Cc]:/+[Pp]rogram\s?[Ff]iles/+", "<PROGRAMFILES>/"),
    # 任何其他磁碟代號(教學素材常出現於 D:/E:/F: 等個人機器)。
    # 只遮掉磁碟代號,保留其下的目錄結構 —— 那結構本身是教學內容的一部分。
    # markdown 內的反斜線常被轉義成 \\ ,故兩種形式都要匹配。
    # 用 lambda 回傳,避免替換字串裡的反斜線被當成跳脫序列。
    (re.compile(r"(?<![A-Za-z0-9])[DEFGde]:\\{1,2}"), (lambda m: "<DRIVE>" + chr(92))),
    (re.compile(r"(?<![A-Za-z0-9])[DEFGde]:/"), "<DRIVE>/"),
]

# 這些檔案的路徑是「當時在哪台機器上做的」的一部分,屬於原始紀錄
HISTORICAL = re.compile(r"00-overview[/\\][^/\\]*-original\.md$|00-overview[/\\]scan-original\.md$")


def convert(text):
    n = 0
    for pat, rep in RULES:
        text, k = re.subn(pat, rep, text)
        n += k
    return text, n


def main():
    check = "--check" in sys.argv
    total_files = 0
    total_hits = 0
    leftovers = []

    for root, _dirs, files in os.walk(DOCS):
        for fn in sorted(files):
            if not fn.endswith(".md"):
                continue
            p = os.path.join(root, fn)
            rel = os.path.relpath(p, DOCS).replace(os.sep, "/")
            body = open(p, encoding="utf-8").read()

            if HISTORICAL.search(rel):
                # 原始掃描的路徑是「當時在哪台機器上做的」的一部分,但這是
                # 公開網站,不能洩漏本機目錄結構 — 一樣轉成佔位符,並在
                # 開頭說明當時使用的是本機環境。
                new, hits = convert(body)
                note = ('!!! note "原始掃描記錄"\n'
                        "    本文件為原始掃描。內含當時的**本機**工作目錄,"
                        "為避免洩漏無關使用者的路徑已轉為佔位符:\n"
                        "    `<MAPLESOTRY>` = 專案根目錄、`<RE>` = IDA/WZ 工作區、"
                        "`<USERPROFILE>` = 使用者家目錄、`<TMP>` = 暫存目錄。\n"
                        "    現況請查首頁與 `docs/facts.json`。\n\n")
                lines = new.split("\n")
                for i, l in enumerate(lines):
                    if l.startswith("# "):
                        new = ("\n".join(lines[:i + 1]) + "\n\n" + note
                               + "\n".join(lines[i + 1:]))
                        break
                if hits:
                    total_files += 1
                    total_hits += hits
                    if not check:
                        # the stale-data warning is already there; append the
                        # placeholder legend to it rather than adding a second
                        # admonition
                        legend = ("\n    路徑佔位符:"
                                  "`<MAPLESOTRY>` = 專案根目錄、`<RE>` = IDA/WZ 工作區、"
                                  "`<USERPROFILE>` = 使用者家目錄、`<TMP>` = 暫存目錄。"
                                  "完整對照見首頁。\n")
                        new = new.replace(
                            "  在 `v83.idb` 上跑 `idat.exe` 即可完整重現。\n",
                            "  在 `v83.idb` 上跑 `idat.exe` 即可完整重現。\n", 1)
                        if "!!! warning" in new:
                            lines = new.split("\n")
                            for i, l in enumerate(lines):
                                if l.strip().startswith('!!! warning'):
                                    j = i + 1
                                    while j < len(lines) and lines[j].startswith("    "):
                                        j += 1
                                    lines.insert(j - 1, legend.rstrip("\n"))
                                    new = "\n".join(lines)
                                    break
                        else:
                            lines = new.split("\n")
                            for i, l in enumerate(lines):
                                if l.startswith("# "):
                                    new = ("\n".join(lines[:i + 1]) + "\n\n"
                                           + note + "\n".join(lines[i + 1:]))
                                    break
                        open(p, "w", encoding="utf-8").write(new)
                    else:
                        print("  [HIST] %s — %d 處" % (rel, hits))
                continue

            new, hits = convert(body)
            if hits:
                total_files += 1
                total_hits += hits
                if check:
                    print("  [PATH] %s — %d 處" % (rel, hits))
                else:
                    open(p, "w", encoding="utf-8").write(new)

            # 檢查是否還有殘留(排除 https:// 這類 URL 的誤判)
            rest = [m for m in re.findall(r"(?<![A-Za-z])[A-Za-z]:[\\/][^\s\"'`)\]]{4,80}", new)]
            if rest:
                leftovers.extend((rel, r) for r in rest)

    print()
    if check:
        print("需要處理的檔案: %d (%d 處路徑)" % (total_files, total_hits))
    else:
        print("已改寫 %d 個檔案,共 %d 處路徑" % (total_files, total_hits))

    if leftovers:
        print("\n仍殘留的絕對路徑 (%d 處):" % len(leftovers))
        for rel, r in leftovers[:20]:
            print("  %s: %s" % (rel, r))
        return 1
    print("無殘留絕對路徑。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
