# 歷史文檔 — RaGEZONE + IDC scripts + 重要 Threads

> **目的**:把過去 10+ 年 MapleStory v83 逆向社群的智慧保存下來

## 已驗證可用的資源

### 1. diamondo25 IDC script
- **URL**: https://gist.github.com/diamondo25/be95345a2875ab4342cd
- **作者**:diamondo25 (2015-07-30)
- **內容**:IDC script 用 string→xref 自動 rename MapleStory 函數
- **條目**:24 個 FindStringAndRenameFirstXrefFromData
- **對應本 IDB**:16 個 string 命中

### 2. angel v83 IDB 釋出
- **URL**: https://forum.ragezone.com/threads/v83-idb-client-edit-dump.1193418/
- **作者**:Angxl (2020-12-24)
- **內容**:v83 IDB (IDA 7.0) + ToolTip addresses
- **條目**:13 個 CUIToolTip::* addresses
- **本機對應**:已驗證 13 個 ToolTip address

### 3. RaGEZONE Common Strings for Disassemblers
- **URL**: https://forum.ragezone.com/threads/for-disassemblers-maplestory-common-strings.975001
- **作者**:diamondo25
- **內容**:MapleStory 公開 strings 對照 function

### 4. RaGEZONE - IDAQ.EXE 教學
- **URL**: https://forum.ragezone.com/threads/help-understanding-the-idaq-exe-file-and-how-to-find-methods-in-it.991744/
- **作者**:sunnyboy (2014-03-13)
- **內容**:教你用 STREDIT + xref 找 CField::OnPacket 等入口
- **對應本 IDB**:完全對應(CField::OnPacket = 0x531325)

### 5. RaGEZONE - CField/CWvsContext addresses
- **URL**: https://forum.ragezone.com/threads/v83-idb-client-edit-dump.1193418/
- **內容**:kevintjuh93 + sunnyboy 釋出的 v83 函數地址
- **對應**:
  - 00531325 - CField::OnPacket ✓
  - 005F80FF - CLogin::OnPacket ✓
  - 00A07A08 - CWvsContext::OnPacket ✓

### 6. RaGEZONE - v83 Client Resolution Changes
- **URL**: https://forum.ragezone.com/threads/v83-client-resolution-changes.1179964/
- **作者**:Daniel (2024)
- **內容**:解析度修正的具體位址
- **重點**:
  - `CUIStatusBar::ToggleQuickslot`
  - `CUIStatusBar::OnCreate`
  - `CField::ShowScreenEffect`
  - `sub_8D850B` (gray HP/MP/EXP bar)

### 7. RaGEZONE - UI Position Storage
- **URL**: https://forum.ragezone.com/threads/where-does-maplestory-record-the-ui-position.1165487/
- **作者**:RaGEZONE community
- **內容**:CConfig::m_nUIWnd_X/Y[43] 結構
- **重點**:UI 位置持久化機制

### 8. alohakuhanaba - v83 Client Setup and Development Guide
- **URL**: https://github.com/alohakuhanaba/v83-Client-Setup-and-Development-Guide
- **內容**:完整 v83 開發指南,含 IDA/IDB 教學 + tutorials
- **對應**:本 wiki 結構參考

### 9. bilibili - MapleStory v083 客戶端分析
- **URL**: https://www.bilibili.com/video/BV1m2421F7de/
- **作者**:昨日小睡大佬
- **內容**:基於天堂服務端的二開發,完整分析

## 重要的 GitHub Repos

| Repo | 用途 | 連結 |
|---|---|---|
| P0nk/Cosmic | Java 21 server | https://github.com/P0nk/Cosmic |
| HeavenMS | Java server | https://github.com/ronancpl/HeavenMS |
| MadaraGameDev/SoloMapling | AI bot framework | https://github.com/MadaraGameDev/SoloMapling |
| MadaraGameDev/SoloMapling-wisteria | WZ Mod Tool | https://github.com/MadaraGameDev/SoloMapling-wisteria-Wz-Mod-Tool-Suite |
| BeiDouMS/BeiDou-Server | Java + Spring/Netty | https://github.com/BeiDouMS/BeiDou-Server |
| OpenMapleClient | C# from scratch | https://github.com/speedyHKjournalist/OpenMapleClient |
| ryantpayton/MapleStory-Client | 4-platform HeavenClient | https://github.com/ryantpayton/MapleStory-Client |
| mrexodia/ida-pro-mcp | AI 逆向 MCP | https://github.com/mrexodia/ida-pro-mcp |
| xiaoye1103613624 | 開發規範 | https://github.com/xiaoye1103613624 |
| iw2d/kaentake | C++ Detours hook | https://github.com/iw2d/kaentake |

## 重要的已讀的 wiki 文章

| 文章 | 內容 |
|---|---|
| [v83 addresses from kevintjuh93](https://forum.ragezone.com/) | 完整 v83 client 函數地址 |
| [MapleEzorsia V2 Client Guide](https://github.com/phantomeis/MapleEzorsia-v2/wiki/v83%E2%80%90Client%E2%80%90Setup%E2%80%90and%E2%80%90Development%E2%80%90Guide) | 完整 DLL hook 開發指南 |
| [MapleEzorsia V2](https://github.com/RoeeLior/MapleEzorsia-v2) | C++ DLL hook |
| [How to use IDA in v83](https://forum.ragezone.com/threads/how-to-use-ida-in-v83.1107216/) | IDA 教學 |
| [Removing a check in v83](https://forum.ragezone.com/threads/removing-a-check-in-the-maplestory-client-v83.1147791/) | patch 教學 |
| [Importing v100 item to v83](https://forum.ragezone.com/threads/importing-new-type-of-item-from-v100-to-v83.1223253/) | 新物品類型 |

## 已下載但尚未深入研究

| 資源 | 路徑 |
|---|---|
| BeiDou Server Notes | `05-Documentation/BeiDou-Server-Notes/` |
| xiaoye-MapleStory-dev | `05-Documentation/xiaoye-MapleStory-dev/` |
| awesome-maplestory | `05-Documentation/awesome-maplestory/` |
| awesome-game-security | `05-Documentation/awesome-game-security/` |
