# 專案地圖 — 本地資源

> **目的**:把所有已下載到本機的 MapleStory v83 相關項目列出,**不做評價**,僅標出位置與用途

## 客戶端

| 項目 | 路徑 | 用途 |
|---|---|---|
| MapleStory 0.83.exe | `待分類/` | WzPacker 加殼原檔 (4.3 MB) |
| MapleStory 0.83.exe.i64 | `待分類/` | IDA 自動分析的 IDB (17 MB) |
| v83.rar | `待分類/` | 完整 v83 client 包 (20 MB) |
| GMS083客戶端/ | `待分類/` | GMS v083 客戶端資料夾 |
| 簽到表/wz/UI.wz | `待分類/` | 部分 UI WZ (25 KB) |

## IDA 分析產物

| 項目 | 路徑 | 內容 |
|---|---|---|
| 00-TECHNICAL-REPORT.md | `wf-output/ida-v83-direct/` | 120 KB 完整技術報告 |
| functions.json | `wf-output/ida-v83-direct/` | 54,357 函數 |
| strings.json | `wf-output/ida-v83-direct/` | 1,262 strings |
| decompiles.json | `wf-output/ida-v83-direct/` | 6 核心 pseudocode |
| historical_renames.json | `wf-output/ida-v83-direct/` | IDC + ToolTip addresses |

## 服務端模擬器

| 項目 | 路徑 | 語言 |
|---|---|---|
| Cosmic | `04-Emulators/GMS-v083-Cosmic/` | Java 21 |
| HeavenMS | `04-Emulators/GMS-v083-HeavenMS/` | Java |
| SoloMapling | `04-Emulators/SoloMapling-wisteria-Wz-Mod-Tool-Suite/` | Java + AI |
| BeiDou Server | `04-Emulators/BeiDou-Server/` | Java + Spring/Netty |
| MapleEzorsia v83 | `04-Emulators/MapleEzorsia-v83/` | C++ DLL hook |
| JourneyClient | `04-Emulators/JourneyClient/` | C++ 從零寫 |
| MortalClient | `04-Emulators/MortalClient/` | C++ 從零寫 |
| OpenMapleClient | `04-Emulators/OpenMapleClient/` | C# 從零寫 |

## 工具

| 項目 | 路徑 | 用途 |
|---|---|---|
| kaentake | `02-Tools/kaentake/` | C++ Detours hook client |
| WZ Mod Tool Suite | `02-Tools/WZ-Mod-Tool/` | C# WZ 編輯 |
| ida-pro-mcp | `C:/Users/.../hermes/cache/scratch/` | AI 逆向 MCP |

## 文檔

| 項目 | 路徑 |
|---|---|
| BeiDou Server Notes | `05-Documentation/BeiDou-Server-Notes/` |
| xiaoye Maplestory dev | `05-Documentation/xiaoye-MapleStory-dev/` |
| awesome-maplestory | `05-Documentation/awesome-maplestory/` |
| awesome-game-security | `05-Documentation/awesome-game-security/` |

## 之前的 wiki 整合文檔

| 檔案 | 大小 | 內容 |
|---|---|---|
| `INTEGRATION-WIKI.md` | 22 KB | Cosmic + 5 衍生項目整合點 |
| `ROUTES-OVERVIEW.md` | 37 KB | 3 版本 + kaentake 路線 |
| `TECHNIQUE-EXTRACTION.md` | 38 KB | 7 項目技術精粹 |
| `WF-INTEGRATED-WIKI.md` | 10 KB | 待分類深度拆解 |
| `待分類-SCAN.md` | 19 KB | 待分類 33 檔案分類 |

## 之前 wf 子代理分析章節

| 章節 | 大小 | 主題 |
|---|---|---|
| W1-1 ~ W1-7 | 5~31 KB | 客戶端結構 |
| W2-1 ~ W2-4 | 5~7 KB | 開放源 client 比較 |
| W3-1 ~ W3-2 | 15~22 KB | C++ client 深入 |
