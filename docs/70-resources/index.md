# 70-resources — 原始資料

> **目的**:把所有 raw data、歷史文檔、外部連結統一存放

## 子章節

- [Raw Data](raw-data/index.md) — JSON / log 原始資料
- [歷史文檔](historical/index.md) — RaGEZONE + IDC scripts
- [外部連結](external-links/index.md) — GitHub repos / tutorials

## 已驗證的原始資料夾

```
C:\MUWORK\GAME\MAPLESOTRY\
├── wf-output/
│   ├── ida-v83-direct/        ← v83.idb 完整 dump
│   │   ├── functions.json     54,357 函數
│   │   ├── strings.json       1,262 strings
│   │   ├── decompiles.json    6 pseudocode
│   │   ├── segments.json
│   │   ├── string_xrefs.json
│   │   ├── mapple_methods.json
│   │   ├── historical_renames.json  ← IDC + ToolTip
│   │   └── 00-TECHNICAL-REPORT.md   120KB 報告
│   ├── W1-1 ~ W1-7.md        ← wf 客戶端分析
│   ├── W2-1 ~ W2-4.md        ← wf server / client 比較
│   ├── W3-1 ~ W3-2.md        ← wf C++ client 深入
│   └── *.json / *.log        ← 中間分析
│
├── 04-Emulators/             ← 服務端源碼
├── 05-Documentation/         ← 官方 / 社群文檔
├── 02-Tools/                 ← 工具源碼
└── 待分類/                   ← 本次新增的 IDA 分析資料
```
