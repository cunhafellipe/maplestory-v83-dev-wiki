# Raw Data — 原始資料檔案

## v83.idb IDA Dump

位置:`wf-output/ida-v83-direct/`

| 檔案 | 大小 | 內容 |
|---|---|---|
| `functions.json` | 7.3 MB | 54,357 函數清單 |
| `strings.json` | 133 KB | 1,262 strings |
| `decompiles.json` | 20 KB | 6 核心 MapleStory 函數 pseudocode |
| `segments.json` | 1 KB | 7 PE segments |
| `string_xrefs.json` | 644 B | 5 重點 strings 的 xrefs |
| `mapple_methods.json` | 1 KB | 6 MapleStory class / 10 methods |
| `historical_renames.json` | 3 KB | diamondo25 IDC + angel ToolTip |
| `00-TECHNICAL-REPORT.md` | 121 KB | 完整技術報告 |

## wf-output 其他 JSON

| 檔案 | 大小 | 內容 |
|---|---|---|
| `W1-5-wz-img-index.raw.json` | 10 KB | WZ img 索引 |
| `_all.json` | 5.7 KB | wf 全部結果 |
| `_imports.json` | 1.6 KB | import 分析 |
| `_pe.json` | 2.4 KB | PE 結構 |
| `_results.json` | 2 KB | wf results |
| `cosmic-opcodes.json` | 15 KB | Cosmic opcodes |
| `auto-funcs-first200.json` | 364 B | 自動函數列表 |
| `auto-globals-first200.json` | 1.5 KB | 自動 globals |
| `auto-imports-first200.json` | 166 B | 自動 imports |
| `auto-strings-maple.json` | 881 B | 自動 strings |
| `auto-survey-minimal.json` | 2.2 KB | 自動 survey |

## wf-output 自動分析腳本

| 檔案 | 用途 |
|---|---|
| `dump_v83_idb.py` | IDAPython 自動 dump 腳本(已跑過) |
| `auto_ida_analysis.py` | idalib-mcp 自動分析 MapleStory 0.83.exe |
| `auto_idb_analysis.py` | idalib-mcp 自動分析 v83.idb |
