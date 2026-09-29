# 引用來源 / References

> 本 Wiki 引用大量第三方資源,所有引用都標明來源

## 主要來源分級

### Tier 1:核心分析來源(本 Wiki 主要事實根據)

#### IDA Pro 9.3 分析結果(本機)

- **資料源**:`v83-copy.i64` (102 MB, 由 `v83.idb` 轉檔)
- **來源**:angel 於 RaGEZONE 釋出(2020)
- **URL**: https://forum.ragezone.com/threads/v83-idb-client-edit-dump.1193418/
- **作者**:Angxl (RaGEZONE 用戶名)
- **授權**:公開釋出(RaGEZONE)
- **使用方式**:用 IDA Pro 9.3 + idat.exe 載入 IDB,跑 IDAPython 腳本 dump

#### MapleStory v83 Client

- **資料源**:MapleStory 0.83.exe (4.3 MB)
- **產權**:屬 Nexon / Wizet(韓國遊戲公司)
- **使用方式**:本機分析用途,不上傳到公開 repo
- **參考**:MapleStory Wiki - https://en.wikipedia.org/wiki/MapleStory

### Tier 2:工具與逆向社群資源

#### ida-pro-mcp

- **URL**: https://github.com/mrexodia/ida-pro-mcp
- **作者**:mrexodia (Markus Gaßner)
- **授權**:MIT License
- **引用章節**:10-client-analysis/ida-pro-mcp/, 50-tools/ida-pro-mcp-setup/
- **Stars**:12.3k

#### IDA Pro 9.3 (Hex-Rays)

- **URL**: https://hex-rays.com/IDA-pro/
- **產權**:Hex-Rays(IDA Pro 商業授權)
- **使用方式**:本機使用,需合法授權
- **本機狀態**:Cracked(`idapro.hexlic`)

#### HaRepacker(WZ 編輯器)

- **URL**: https://github.com/lastbattle/Harepacker
- **作者**:lastbattle
- **授權**:GPL-3.0
- **引用章節**:50-tools/wz-mod-tool/

### Tier 3:RaGEZONE 社群教學

#### sunnyboy 教學 - Understanding IDAQ.EXE

- **URL**: https://forum.ragezone.com/threads/help-understanding-the-idaq-exe-file-and-how-to-find-methods-in-it.991744/
- **作者**:sunnyboy (RaGEZONE)
- **日期**:2014-03-13
- **引用內容**:CField::OnPacket / CLogin::OnPacket / CWvsContext::OnPacket 地址對應
- **驗證**:全部地址與本機 IDA 分析吻合

#### angel - v83 IDB + Client Edit Dump

- **URL**: https://forum.ragezone.com/threads/v83-idb-client-edit-dump.1193418/
- **作者**:Angxl (RaGEZONE)
- **日期**:2020-12-24
- **引用內容**:13 個 CUIToolTip::SetToolTip_* addresses + tooltip color patch

#### diamondo25 - Common Strings for Disassemblers

- **URL**: https://forum.ragezone.com/threads/for-disassemblers-maplestory-common-strings.975001
- **作者**:diamondo25
- **引用章節**:10-client-analysis/v83-idb/historical-renames.md

#### diamondo25 - IDC script

- **URL**: https://gist.github.com/diamondo25/be95345a2875ab4342cd
- **作者**:diamondo25
- **日期**:2015-07-30
- **授權**:公開 gist(無明確授權)
- **引用章節**:10-client-analysis/v83-idb/historical-renames.md
- **使用方式**:在 IDA Pro 內套用 FindStringAndRenameFirstXrefFromData

#### Daniel - v83 Client Resolution Changes

- **URL**: https://forum.ragezone.com/threads/v83-client-resolution-changes.1179964/
- **作者**:Daniel (RaGEZONE)
- **日期**:2024
- **引用內容**:CUIStatusBar::ToggleQuickslot 等解析度相關位址

#### RaGEZONE - UI Position Storage

- **URL**: https://forum.ragezone.com/threads/where-does-maplestory-record-the-ui-position.1165487/
- **作者**:RaGEZONE 社群
- **引用內容**:CConfig::m_nUIWnd_X/Y[43] 結構

### Tier 4:GitHub 開源項目

#### 服務端模擬器

| 項目 | URL | 授權 |
|---|---|---|
| P0nk/Cosmic | https://github.com/P0nk/Cosmic | AGPL-3.0 |
| ronancpl/HeavenMS | https://github.com/ronancpl/HeavenMS | AGPL-3.0 |
| MadaraGameDev/SoloMapling-wisteria | https://github.com/MadaraGameDev/SoloMapling-wisteria-Wz-Mod-Tool-Suite | (見原 repo) |
| BeiDouMS/BeiDou-Server | https://github.com/BeiDouMS/BeiDou-Server | (見原 repo) |

#### 客戶端

| 項目 | URL | 授權 |
|---|---|---|
| iw2d/kaentake | https://github.com/iw2d/kaentake | (見原 repo) |
| speedyHKjournalist/OpenMapleClient | https://github.com/speedyHKjournalist/OpenMapleClient | AGPL-3.0 |
| ryantpayton/MapleStory-Client | https://github.com/ryantpayton/MapleStory-Client | AGPL-3.0 |

#### 工具與開發指南

| 項目 | URL | 授權 |
|---|---|---|
| mrexodia/ida-pro-mcp | https://github.com/mrexodia/ida-pro-mcp | MIT |
| alohakuhanaba/v83-Client-Setup-and-Development-Guide | https://github.com/alohakuhanaba/v83-Client-Setup-and-Development-Guide | MIT |
| phantomeis/MapleEzorsia-v2 | https://github.com/phantomeis/MapleEzorsia-v2 | AGPL-3.0 |
| xiaoye1103613624/xiaoye-MapleStory-dev | https://github.com/xiaoye1103613624/xiaoye-MapleStory-dev | (見原 repo) |
| jonnylin13/Maple83 | https://github.com/jonnylin13/Maple83 | (見原 repo) |

### Tier 5:其他教學資源

#### bilibili - MapleStory v083 客戶端分析

- **URL**: https://www.bilibili.com/video/BV1m2421F7de/
- **作者**:昨日小睡大佬
- **語言**:中文
- **引用內容**:天堂服務端的二開發與 IDA 分析方法

#### Orange Mushroom(KMS patch notes)

- **URL**: https://orangemushroom.net/
- **引用內容**:KMST ver 1.2.187 等更新資訊

## 引用格式

所有 Wiki 文件中的引用都遵循以下格式:

```
### 函數名 @ 地址

> **來源**:RaGEZONE Thread ID / GitHub Repo / IDC script
> **原始作者**:sunnyboy / angel / diamondo25 等
> **驗證**:對應本機 IDA 分析,完全吻合
```

例如:

```
### CField::OnPacket @ 0x531325

> **來源**:sunnyboy 教學 (RaGEZONE 2014)
> **原始地址**:0x531325
> **驗證**:本機 IDA Pro 9.3 decompile 完全吻合(1201B / 246 行 pseudocode)
```

## 鳴謝

特別感謝以下社群成員的貢獻:

- **sunnyboy** (RaGEZONE) — 4 個 OnPacket dispatcher 地址教學
- **Angxl** (RaGEZONE) — v83 IDB 釋出 + ToolTip patch
- **diamondo25** (RaGEZONE) — IDC script + Common Strings
- **Daniel** (RaGEZONE) — v83 解析度修正教學
- **kevintjuh93** (RaGEZONE) — v83 client 函數地址
- **mrexodia** — ida-pro-mcp 工具
- **P0nk** — Cosmic server
- **ronancpl** — HeavenMS server
- **alohakuhanaba** — v83 開發指南
- **phantomeis** — MapleEzorsia V2

## 免責聲明

本 Wiki 僅供教育與研究用途。MapleStory 是 Wizet / Nexon 的註冊商標,所有相關商標與版權屬原公司所有。

本 Wiki 不包含任何破解、逆向、盜版工具的下載連結。所有 binary 檔案保留在本機,不上傳到公開 repo。

若您是版權持有人並希望移除特定內容,請透過 GitHub Issues 聯絡。
