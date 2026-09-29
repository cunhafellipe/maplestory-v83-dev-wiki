# Authors & Credits — 作者與致謝

> 本 Wiki 是**眾多開源社群成員**的集體智慧結晶。所有貢獻者、工具作者、教學作者都列在此處。
>
> **本 Wiki 內容**:`CC BY 4.0`(見 LICENSE.md)
>
> **最後更新**: 2026-09-28

---

## 👥 本 Wiki 編輯者

| 角色 | 帳號 | 貢獻 |
|---|---|---|
| **Wiki 編輯 / 維護者** | [`@e78-png`](https://github.com/e78-png) | IDA Pro 分析腳本、WIKI 整合、GitHub Pages 部署 |

如果你要貢獻,請透過 [GitHub Issues](https://github.com/e78-png/maplestory-v83-dev-wiki/issues) 或 Pull Request。

---

## 🛠️ 核心工具作者(沒有他們就沒有本 Wiki)

### IDA Pro 9.3 + Hex-Rays Decompiler

| 項目 | 作者 / 公司 | 開源連結 | 授權 |
|---|---|---|---|
| **IDA Pro 9.3** | Hex-Rays(比利時公司)| https://hex-rays.com/IDA-pro/ | 商業授權(本機用 cracked `idapro.hexlic`)|
| **Hex-Rays Decompiler** | Hex-Rays | https://hex-rays.com/products/decompiler/ | 商業授權(bundled with IDA Pro)|

### ida-pro-mcp(AI 逆向)

| 項目 | 作者 | 開源連結 | 授權 | 引用 |
|---|---|---|---|---|
| **ida-pro-mcp** | [Markus Gaßner](https://github.com/mrexodia) | https://github.com/mrexodia/ida-pro-mcp | MIT | 引用於 [10-client-analysis/ida-pro-mcp/index.md](10-client-analysis/ida-pro-mcp/index.md) + [50-tools/ida-pro-mcp-setup/](50-tools/ida-pro-mcp-setup/index.md) |

> 🙏 感謝 mrexodia 開源了這個強大的 AI-assisted 逆向工具

---

## 🌍 MapleStory v83 逆向社群(本 Wiki 主要內容來源)

### Tier 1:IDB 與主要資料釋出者

#### Angxl(RaGEZONE)

- **貢獻**:釋出 `v83.idb`(125 MB, IDA 6.1, 2014~2021)+ 13 個 `CUIToolTip::SetToolTip_*` 直接 addresses
- **出處**: [RaGEZONE thread 1193418 - v83 IDB + Client Edit Dump](https://forum.ragezone.com/threads/v83-idb-client-edit-dump.1193418/)
- **RaGEZONE 用戶名**: Angxl
- **使用於**: 本 Wiki 所有 v83.idb 分析
- **影響**: 沒有這個 IDB,本 Wiki 不可能存在

> 🙏 感謝 Angxl 整理 IDB 並釋出,讓 2014 的 v83 客戶端結構得以保存到今天

#### sunnyboy(RaGEZONE)

- **貢獻**:CLogin::OnPacket / CField::OnPacket / CWvsContext::OnPacket / CStage::OnPacket 地址教學 + STREDIT + xref 方法論
- **出處**: [RaGEZONE thread 991744 - Understanding the IDAQ.EXE](https://forum.ragezone.com/threads/help-understanding-the-idaq-exe-file-and-how-to-find-methods-in-it.991744/)
- **RaGEZONE 用戶名**: sunnyboy
- **日期**: 2014-03-13
- **使用於**: [40-protocol/index.md](40-protocol/index.md) + [10-client-analysis/v83-idb/technical-report.md](10-client-analysis/v83-idb/technical-report.md) §9
- **影響**: 教學被本 Wiki 完整驗證(地址完全對應)

> 🙏 感謝 sunnyboy 詳細的 IDAQ.EXE 教學,本 Wiki 4 個 OnPacket 地址完全沿用他的教學

### Tier 2:工具腳本作者

#### diamondo25(RaGEZONE)

- **貢獻 1**: 24 個 `FindStringAndRenameFirstXrefFromData` IDC script
  - **出處**: [Gist be95345a2875ab4342cd](https://gist.github.com/diamondo25/be95345a2875ab4342cd)
  - **日期**: 2015-07-30
- **貢獻 2**: MapleStory Common Strings for Disassemblers
  - **出處**: [RaGEZONE thread 975001](https://forum.ragezone.com/threads/for-disassemblers-maplestory-common-strings.975001)
- **使用於**: [10-client-analysis/v83-idb/historical-renames.md](10-client-analysis/v83-idb/historical-renames.md)
- **本 Wiki 驗證**: 16/24 string 在 v83.idb 中命中

> 🙏 感謝 diamondo25 提供 IDC script,讓 IDA 自動 rename MapleStory 函數變得可行

#### Daniel(RaGEZONE)

- **貢獻**: v83 Client Resolution Changes 教學(CUIStatusBar / CField::ShowScreenEffect 等地址)
- **出處**: [RaGEZONE thread 1179964](https://forum.ragezone.com/threads/v83-client-resolution-changes.1179964/)
- **使用於**: [30-ui-classes/cuiwnd/index.md](30-ui-classes/cuiwnd/index.md) + [60-secondary-dev/patches/index.md](60-secondary-dev/patches/index.md)

> 🙏 感謝 Daniel 的解析度修正教學,給改 v83 HD 視窗的人鋪好路

#### kevintjuh93(RaGEZONE)

- **貢獻**: 完整的 v83 client 函數地址列表(CCashShop::OnPacket, CDropPool::OnPacket 等)
- **出處**: RaGEZONE 上 kevintjuh93 thread
- **影響**: 本 Wiki 未能完整採用 kevintjuh93 的列表,僅引用部分

### Tier 3:UI / WZ / Client 開發者

#### Crat / Vajamas / RonYNWA(RaGEZONE)

- **貢獻**: 感謝 angel IDB 釋出的 follow-up 討論(2020)
- **出處**: [RaGEZONE thread 1193418 - 後續留言](https://forum.ragezone.com/threads/v83-idb-client-edit-dump.1193418/)

---

## 🛠️ 開源項目作者(本 Wiki 引用)

### 服務端模擬器

| 項目 | 作者 | 開源連結 | 授權 | 引用 |
|---|---|---|---|---|
| **Cosmic (P0nk/Cosmic)** | P0nk | https://github.com/P0nk/Cosmic | AGPL-3.0 | [20-server-emulators/cosmic/index.md](20-server-emulators/cosmic/index.md) |
| **HeavenMS (ronancpl)** | Ronan | https://github.com/ronancpl/HeavenMS | AGPL-3.0 | [20-server-emulators/heavenms/index.md](20-server-emulators/heavenms/index.md) |
| **BeiDou Server (BeiDouMS)** | BeiDouMS | https://github.com/BeiDouMS/BeiDou-Server | (見原 repo) | [20-server-emulators/beidou/index.md](20-server-emulators/beidou/index.md) |
| **SoloMapling (MadaraGameDev)** | MadaraGameDev | https://github.com/MadaraGameDev/SoloMapling | (見原 repo) | [20-server-emulators/solomapling/index.md](20-server-emulators/solomapling/index.md) |

### 客戶端 / Hook

| 項目 | 作者 | 開源連結 | 授權 | 引用 |
|---|---|---|---|---|
| **kaentake** | iw2d | https://github.com/iw2d/kaentake | (見原 repo) | [50-tools/kaentake/index.md](50-tools/kaentake/index.md) |
| **OpenMapleClient** | speedyHKjournalist | https://github.com/speedyHKjournalist/OpenMapleClient | AGPL-3.0 | [wf-analysis/W2-1](20-server-emulators/wf-analysis/W2-1-OpenMapleClient-analysis.md) |
| **HeavenClient (ryantpayton)** | ryantpayton | https://github.com/ryantpayton/MapleStory-Client | AGPL-3.0 | [wf-analysis/W3-1](10-client-analysis/wf-analysis/W3-1-HeavenClient-4-platforms-deep-dive.md) |
| **MapleEzorsia V2** | phantomeis / RoeeLior | https://github.com/phantomeis/MapleEzorsia-v2 | AGPL-3.0 | [30-ui-classes/cuiwnd/index.md](30-ui-classes/cuiwnd/index.md) |
| **SoloMapling-wisteria (WZ Mod Tool)** | MadaraGameDev | https://github.com/MadaraGameDev/SoloMapling-wisteria-Wz-Mod-Tool-Suite | (見原 repo) | [50-tools/wz-mod-tool/index.md](50-tools/wz-mod-tool/index.md) |

### 開發指南

| 項目 | 作者 | 開源連結 | 授權 | 引用 |
|---|---|---|---|---|
| **v83 Client Setup and Development Guide** | alohakuhanaba | https://github.com/alohakuhanaba/v83-Client-Setup-and-Development-Guide | MIT | [70-resources/historical/index.md](70-resources/historical/index.md) |
| **xiaoye-MapleStory-dev** | xiaoye1103613624 | https://github.com/xiaoye1103613624/xiaoye-MapleStory-dev | (見原 repo) | [00-overview/project-map.md](00-overview/project-map.md) |
| **MapleStory-Inventory** | cksuwjr | https://github.com/cksuwjr/MapleStory-Inventory | (見原 repo) | [30-ui-classes/item-equip/index.md](30-ui-classes/item-equip/index.md) |

### 服務端衍生

| 項目 | 作者 | 開源連結 | 授權 |
|---|---|---|---|
| **daiy29/MSv83** | daiy29 | https://github.com/daiy29/MSv83 | (見原 repo) |
| **v3921358/HuiMS079** | v3921358 | https://github.com/v3921358/HuiMS079 | (見原 repo) |
| **jonnylin13/Maple83** | jonnylin13 | https://github.com/jonnylin13/Maple83 | (見原 repo) |
| **Tancen/MapleStory-Client-Package** | Tancen | https://github.com/Tancen/MapleStory-Client-Package | (見原 repo) |

---

## 📹 教學影片作者

### 昨日小睡大佬(bilibili)

- **貢獻**: 中文 MapleStory v083 客戶端分析教學
- **出處**: https://www.bilibili.com/video/BV1m2421F7de/
- **語言**: 中文
- **使用於**: [00-overview/project-map.md](00-overview/project-map.md) + [70-resources/historical/index.md](70-resources/historical/index.md)

> 🙏 感謝昨日小睡大佬的詳細中文教學

---

## 📚 教學文件 / Wiki 作者

### MapleStory 官方

- **Nexon 官方論壇**: https://forums.maplestory.nexon.net/(論壇, 不是技術教學)
- **Orange Mushroom(KMS 公告)**: https://orangemushroom.net/

### 第三方 Wiki

- **Strategy Wiki**: https://strategywiki.org/
- **MapleStory Wiki(Fandom)**: https://maplestory.fandom.com/

---

## 🔧 工具/輔助作者

### HaRepacker(在本 Wiki 中提及)

- **作者**: lastbattle
- **開源連結**: https://github.com/lastbattle/Harepacker
- **授權**: GPL-3.0

### MkDocs / Material 主題

| 項目 | 作者 | 開源連結 | 授權 |
|---|---|---|---|
| **MkDocs** | Tom Christie | https://github.com/mkdocs/mkdocs | BSD-2-Clause |
| **mkdocs-material** | squidfunk | https://github.com/squidfunk/mkdocs-material | MIT |

---

## 🙏 致謝(中文)

本 Wiki 之所以能完成,要特別感謝以下社群成員與開源貢獻者:

- 🌟 **angxl**: 釋出 v83 IDB 是本 Wiki 的基礎,沒有這個 IDB 一切都無法開始
- 🌟 **sunnyboy**: 教學內容在 2014 年保存了 v83 client 結構的關鍵知識
- 🌟 **diamondo25**: IDC script 讓 IDA Pro 自動化分析 MapleStory 成為可能
- 🌟 **Daniel**: 解析度修正教學給 HD 顯示鋪路
- 🌟 **mrexodia**: ida-pro-mcp 是 AI 逆向 MapleStory 的革命性工具
- 🌟 **P0nk**: Cosmic 服務端是現代 v83 開發的核心
- 🌟 **ronancpl**: HeavenMS 是整個 v83 私服社群的基石
- 🌟 **alohakuhanaba**: v83 Client Setup Guide 整合了所有開發資源
- 🌟 **iw2d**: kaentake hook 框架讓無需 patch EXE 就能加功能
- 🌟 **phantomeis / RoeeLior**: MapleEzorsia V2 是最完整的 DLL hook client
- 🌟 **昨日小睡大佬**: 中文教學讓中文圈開發者也能學習
- 🌟 **RaGEZONE 社群**: 10+ 年的 v83 開發討論累積的寶藏
- 🌟 **所有 commit / issue 貢獻者**: 開源社群的力量

---

## 📝 引用原則

本 Wiki 引用所有第三方資源時遵守以下原則:

1. **標明出處**: 每個引用都附上原始 URL、作者、日期
2. **標明授權**: 對每個被引用的內容說明原授權
3. **不做為自己成果**: 明確標示哪些是 IDA 自動分析、哪些是人工分析、哪些來自社群教學
4. **教育用途**: 本 Wiki 純為教育用途,不包含任何破解工具下載
5. **第三方 binary 不上傳**: MapleStory EXE / WZ 屬於 Nexon,本機分析但不對外發布

---

## 🙏 如果你想被加到致謝

如果你對本 Wiki 有任何貢獻(PR / Issue / 文件修正 / 提供資料),請告訴我。我會把你的名字加到本檔案中。
