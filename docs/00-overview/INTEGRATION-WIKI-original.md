# MAPLESOTRY 整合 Wiki — Cosmic 為核心 + 5 大衍生項目

!!! warning "原始掃描記錄,含已知錯誤"
    **原始掃描記錄,含已知錯誤。** 本文件是 2026-09-27 的原始產物,
    未隨後續更正同步。已知錯誤與更正值見
    [本目錄索引](index.md) 與 `docs/facts.json` 的 `corrections`。

    路徑佔位符:`<MAPLESOTRY>` = 專案根目錄、`<RE>` = IDA/WZ 工作區、`<USERPROFILE>` = 使用者家目錄、`<TMP>` = 暫存目錄。完整對照見首頁。
    **現況請查[首頁](../index.md)與 `facts.json`。**

> **更新時間**: 2026-09-27
> **本機根目錄**: `<MAPLESOTRY>\`
> **核心**: P0nk/Cosmic v1.1.3 (GMS v083 server emulator)
> **本 wiki 目的**: 把所有已下載/已 clone 的衍生項目,標出**整合點 + 依賴鏈 + 工作流**,給功能整合任務用

---

## §0 整合全貌圖

```
                          ┌─────────────────────────────────────────────┐
                          │  Cosmic (P0nk/Cosmic v1.1.3)                │
                          │  本機: 04-Emulators/GMS-v083-Cosmic/        │
                          │  GMS v083 server emulator                  │
                          │  - Login port 8484 / Channel 7575+         │
                          │  - 177 Recv + 307 Send opcodes              │
                          │  - 173 GM commands + 1915 JS scripts        │
                          │  - 16 WZ files                             │
                          └──────────┬──────────────────────────────────┘
                                     │ derived / extends
        ┌───────────────────┬───────┼─────────┬─────────────────┐
        │                   │       │         │                 │
        ▼                   ▼       ▼         ▼                 ▼
┌──────────────┐   ┌──────────────┐ ┌─────────────┐ ┌──────────────┐
│ BeiDou-      │   │ SoloMapling  │ │   HeavenMS  │ │ Client forks │
│ Server v1.11 │   │ (Madara)     │ │ (ronancpl)  │ │              │
│ ★663 fork386 │   │ ★183 fork54  │ │ 已封存      │ │ ─ kaentake ★ │
│ Spring Boot  │   │ Bot 框架    │ │              │ │   (iw2d)     │
│ + Vue Web UI │   │ + 31.5k 行  │ │              │ │ ─ Mortal     │
│ + ijl15 插件 │   │             │ │              │ │ ─ Journey    │
└──────┬───────┘   └──────┬───────┘ └─────────────┘ └──────────────┘
       │                  │
       │ 提供             │ 提供
       ▼                  ▼
┌──────────────┐   ┌──────────────────────────────┐
│ BeiDou-i15   │   │ WZ Mod Tool Suite            │
│ ijl15 插件  │   │ (SoloMapling × wisteria)     │
│ 解析/上傳    │   │ - Builder (瀏覽 v269 資源)  │
│              │   │ - Manager (套用 v83 端)     │
└──────────────┘   │ - wzmods CLI                 │
                   │ - 適用: Cosmic XML WZ 服務   │
                   └──────────────────────────────┘

外部規範/工具鏈:
- xiaoye-MapleStory-dev (開發 SKILL + toolchain + checklist + 模板)
- orange-wz MCP (WZ/IMG 編輯 + MCP 服務)
- ida-pro-mcp (IDA 逆向 MCP)
- NapMysqlTool (MySQL 圖形化管理)
- HaRepacker-resurrected / WzComparerR2-KENNYSOFT (本機 01-WZ-Tools/)
```

---

## §1 各項目整合矩陣

| 項目 | 與 Cosmic 關係 | 本機路徑 | 大小 | 整合難度 | 適用場景 |
|---|---|---|---|---|---|
| **Cosmic** (基線) | 本體 | `04-Emulators/GMS-v083-Cosmic/` | ~25k 檔 | — | 所有研究/修改基礎 |
| **HeavenMS** | 上游 (Cosmic fork 之父) | `04-Emulators/GMS-v083-HeavenMS/` | 22 entries | 比對歷史 | 學習演進、找被移除功能 |
| **SoloMapling** | 上層框架(31.5k 行,只動 33 檔 Cosmic) | `04-Emulators/SoloMapling-Documents/` | 9 文件 114KB | **中** | NPC 機器人、Free Market、自動玩家模擬 |
| **BeiDou-Server** | 漢化增強 + Spring Boot | `05-Documentation/BeiDou-Server-Notes/` | 4 文件 18KB | **高** | 商用運營、Web 後台、JWT API、雙語 |
| **WZ Mod Tool Suite** | 工具(讀 Cosmic XML WZ 輸出) | `07-Tools-General/SoloMapling-wisteria-Wz-Mod-Tool-Suite/` | 13 檔 + docs/ | **低** | v268+ 外觀/物品移植到 v83 |
| **kaentake** | 客戶端 hook (binary) | `12-OffShelf-Client-Fork/kaentake/` | 3 檔 190KB | **極低** | 客戶端 IP/port 重定向,解析度選擇 |
| **xiaoye-MapleStory-dev** | AI 開發 SKILL 包 | `05-Documentation/xiaoye-MapleStory-dev/` | 5 檔 55KB | — | AI Agent 開發規範 |

---

## §2 SoloMapling 整合 — Bot 框架整合到 Cosmic

### 2.1 它做什麼

**給 Cosmic 加上數百個自動玩家**:逛城鎮、開店、聊天、開小遊戲、跑 OPQ、招待新玩家等。
- **31,500 行 framework code** + **1,104 行** 對 Cosmic 的最小修改(33 檔案)
- 15 種 Bot 類型 + 7 個 command packs
- 440 條預錄路徑 + 26 地圖
- 全 YAML 驅動(對話、物品池、價格、路徑)

### 2.2 對 Cosmic 的改動面(極小)

> 「The bulk of the additions to Cosmic's own packages are 11 self-contained GM command classes (`!bot`, `!move`, `!env`, `!opq`, …, ~2,850 lines) under `client/command/commands/gm4/`」

**Cosmic 改動統計**(從 README):
- 33 個檔案被改
- +1,104 / -146 行(淨增不到 1k 行)
- 11 個新 GM 指令 → `gm4/` 資料夾

**因此整合策略**:整個 `soloMapling/` 套件可直接移植(因為獨立 package),只需:
1. 把 11 個 `gm4/` 指令複製到 Cosmic 的 `client/command/commands/gm4/`
2. 把 `soloMapling/` 整個 package 複製到 `src/main/java/`
3. 註冊到 `CommandsExecutor.registerLv4Commands()`(複製 SoloMapling 的那段 register 邏輯)

### 2.3 依賴新增

SoloMapling 引入:
- **JGraphT**(圖論/路徑搜尋) — 加到 `pom.xml`
- YAML 解析(估計 SnakeYAML)— 確認版本
- 預錄路徑資料(26 地圖 × ~440 paths) — 不在 repo,需另外生成

### 2.4 不 clone 整包的原因

- 31,500 行程式碼與本地 Cosmic clone 重複
- 主要價值在**文檔**(`Documents/`)與**設計模式**
- 程式碼部分已從 `Artificial Player Framework Architecture.md` + `Claude Summary.txt` 摘要,可照架構重寫

**已下載的 9 份文檔**(`04-Emulators/SoloMapling-Documents/`):

| 文件 | 大小 | 內容 |
|---|---|---|
| `Claude Summary.txt` | 28KB | 完整架構總覽 — 每個子系統、設計模式、並發模型 |
| `Artificial Player Framework Architecture.md` | 18KB | Bot 框架深度解析 — 身份、生命週期、狀態機 |
| `Dev Commands Cheat Sheet.md` | 28KB | 11 個 `!` 開頭 dev 指令完整參考 |
| `FreeMarket and ItemPool Architecture.txt` | 21KB | 商店生成管線、tier/version 系統、經濟引擎 |
| `Environment and World Startup.md` | 6KB | 7 波世界初始化 |
| `Movement-Recording.md` | 3KB | 預錄移動 + 路徑圖 |
| `Logging and Observability.md` | 4KB | BotLog + MMC operator console |
| `SHOWCASE.md` | 6KB | 圖片展示導引 |
| `DEV-DIARY.md` | 1KB | 開發日誌 |

### 2.5 整合工作流

```
1. 讀 Claude Summary.txt → 理解整體架構
2. 讀 Artificial Player Framework Architecture.md → BotSM 抽象狀態機設計
4. 複製 soloMapling/ package 到 Cosmic src/main/java/
5. 複製 gm4/ 11 個指令到 Cosmic gm4/
6. 在 CommandsExecutor.registerLv4Commands() 註冊
7. 加 JGraphT 依賴到 pom.xml
8. 編譯 + 啟動
9. 在遊戲中用 !bot 驗證
```

---

## §3 BeiDou-Server 整合 — 商用增強

### 3.1 與 Cosmic 的差異

> 本項目基於 Cosmic 來做漢化和優化

**主要新增**:
- **Spring Boot 3** 框架:商業 API 端點
- **Vue 3 + Arco Design Pro** Web 後台(`gms-ui/`)
- **MyBatis-Flex** ORM(替代 Cosmic 原生 JDBC)
- **JWT 認證**(API 端口 8686)
- **Swagger**(開發用)
- **雙語資源覆蓋機制**(wz + wz-zh-CN / scripts + scripts-zh-CN)
- **MyBatis-Flex CodeGen** 工具(自動生成實體)
- 內建 `ijl15` 插件整合

### 3.2 雙引擎架構(關鍵設計)

> 一個 JVM 裡跑兩個引擎,靠 `ServerManager` 橋接

```
SpringApplication.run()
   ↓
ServerManager (Spring ApplicationRunner) 啟動 Netty
   ↓
Server.getInstance().init()  (Netty game server)
   ├─ LoginServer :8484
   └─ ChannelServer :7575+
   ↓
REST 控制: /server/v1/startServer, /stopServer, /restartServer, /online
```

### 3.3 整合成本

**高**。Spring Boot + MyBatis-Flex + JWT 全是 BeiDou 新增,整合到 vanilla Cosmic 需要:
1. 引入 Spring Boot starter(改 pom.xml 結構)
2. 把 Netty 啟動包進 `ApplicationRunner`
3. 加入 MyBatis-Flex + 自動生成 DAO
4. 加 JWT 過濾鏈
5. 加 Controller 層 + ResultBody/SubmitBody 信封

**不建議**:把 BeiDou 直接套到你的 Cosmic(本地 v1.1.3)。原因:
- Cosmic v1.1.3 是 2026-02 最新,但 BeiDou master 是基於舊版 Cosmic fork(他們用的是 BEI_DOU_VERSION = "1.11" 內部版號)
- 合併衝突會很多

**建議**:採用 BeiDou 的**設計思想**而非代碼:
- 借 `GameConfig` 熱重載模式
- 借 i18n 雙語覆蓋機制
- 借 `ServerController` REST 控制

### 3.4 已下載的 4 份文檔(`05-Documentation/BeiDou-Server-Notes/`)

| 文件 | 大小 | 內容 |
|---|---|---|
| `CLAUDE.md` | 12KB | **完整的開發者指南**(架構、命令、規範、坑) |
| `README.md` | 5KB | 用戶向導(客戶端下載、MySQL、docker) |
| `AGENTS.md` | 1KB | Agent 入口(指向 CLAUDE.md) |
| `gms-server-README.md` | <1KB | gms-server 子目錄說明 |

> **強烈推薦**讀 `CLAUDE.md` — 揭示了 8 個非顯而易見的坑(如 `saveCharToDB` 兩個版本哪個真生效、刪號 NPE 風險等)

---

## §4 WZ Mod Tool Suite 整合 — v268+ 內容移植到 v83

### 4.1 它做什麼

把**現代 MapleStory (v268+) 的外觀內容**(椅子、翅膀、武器、戒指、寵物、髮型) **移植到 v83**:
- **WZ Mod Builder**:視覺化瀏覽現代客戶端 → 選物品 → 匯出成 YAML pack
- **WZ Mod Manager**:套用/取消 pack(每次 Apply 從 pristine baseline 重來)
- **wzmods CLI**:無頭版管理指令
- **WzPackTool** (C# 引擎):實際 WZ 轉換/注入

### 4.2 為什麼對 Cosmic 整合很重要

Cosmic 是 **XML WZ** 服務器(`wz/*.xml` 結構),這套工具**專門為此設計**:
> "Only v83 Cosmic-style servers that store WZ data as XML are supported."

### 4.3 套件結構

```
07-Tools-General/SoloMapling-wisteria-Wz-Mod-Tool-Suite/
├── README.md                                       (主說明, 25KB)
├── BUILDING.md                                     (從源碼建置)
├── NOTICE.md                                       (第三方元件聲明)
├── LICENSE                                         (GPLv3)
├── WZ Mod Builder - Quickstart.md                  (製作 mod pack)
├── WZ Mod Builder.bat                              (啟動 Builder GUI)
├── WZ Mod Manager - Quickstart.md                  (套用 mod pack)
├── WZ Mod Manager.bat                              (啟動 Manager GUI)
├── WZ Mod System - Public Guide.md                 (手寫 pack YAML 格式)
├── WZ Mods - Standalone vs SoloMapling.md          (Standalone vs SoloMapling 模式)
├── wzmods.bat                                      (CLI: status/compile/revert/doctor)
├── docs/images/                                    (10 張展示圖)
└── (預期有 builder/, manager/, packtool/ 子專案原始碼)
```

### 4.4 整合工作流

```
1. 安裝 Java 21 (可能已內建在 release zip)
2. 安裝 .NET 8 SDK (若要從源碼 build; 預編譯 release 不需要)
3. 安裝一個現代 MapleStory (GMS v269 測試) 的客戶端
4. 啟動 WZ Mod Builder → 指向現代客戶端的 Data/ 資料夾
5. 瀏覽物品 → 加到 basket → Export .yaml
6. 關閉 server 和 game client
7. 啟動 WZ Mod Manager → 指向 Cosmic 的 wz/ + 客戶端 .wz/
9. Tick pack → Apply
10. 重啟 server + client
```

### 4.5 已知限制

- Modern-only 武器類型(katara/dual bowgun/shining rod)**不存在於 v83**,會被 reject
- 某些椅子/標籤戒指**渲染不完整**(Nexon 端問題)
- Standalone 模式不會清理資料庫已有物品 → 玩家持有的失效物品會 crash 客戶端
- **必須在乾淨的 v83 wz 環境首次 Apply**(快照建立 baseline)

### 4.6 與你既有工具的搭配

```
WzComparerR2-KENNYSOFT  ←→  WZ Mod Tool Suite
(讀取 .wz / .img 對比)        (讀 v269 .wz / 寫 v83 .wz)
                                ↓
                         配合 Cosmic XML WZ
                                ↓
                         HaRepacker-resurrected (單獨編輯)
```

---

## §5 kaentake 整合 — 客戶端 IP/port 注入

### 5.1 它做什麼

**已編譯的客戶端啟動器**,把 GMS v083 客戶端導向**自架伺服器**:
- `Kaentake.exe` (32KB):主程式,管理員權限執行
- `Kaentake.dll` (113KB):DLL 注入到 MapleStory.exe
- `Custom.wz` (45KB):客製 WZ(新增解析度選擇 combobox 到 system option)

### 5.2 使用方式(三選一)

**A. 命令列**(優先級最高):
```
Kaentake.exe 127.0.0.1 8484
```

**B. config.ini**:
```ini
[config]
host=127.0.0.1
port=8484
```

**C. 預設**:127.0.0.1

### 5.3 對應到 Cosmic 預設值

| 項目 | Cosmic | kaentake | 相容 |
|---|---|---|---|
| Login port | 8484 | 8484 | ✓ |
| Channel port | 7575 | (由 Login 告知) | ✓ |
| VERSION | 83 | (鎖 v83) | ✓ |

**已抓的 3 個 binary**(190 KB 總計) 在 `12-OffShelf-Client-Fork/kaentake/`:

| 檔案 | 大小 | 類型 |
|---|---|---|
| `Kaentake.exe` | 31,744 B | PE MZ executable |
| `Kaentake.dll` | 113,664 B | PE MZ DLL(注入用) |
| `Custom.wz` | 45,859 B | WZ v1 加密(標頭 `PKG1`) |

### 5.4 整合工作流

```
1. 客戶端先安裝原始 MapleStory 到 <NEXON>/MapleStory
2. 刪除 HShield/、ASPLnchr.exe、MapleStory.exe、Patcher.exe
3. 把這 3 個檔案複製到客戶端目錄
4. 創建 config.ini (或用命令列參數)
5. 雙擊 Kaentake.exe (管理員)
6. Kaentake.dll 注入 → 連到你的 Cosmic :8484
7. 遊戲中可選解析度(Custom.wz 提供)
```

---

## §6 xiaoye-MapleStory-dev 整合 — AI Agent 開發規範

### 6.1 它做什麼

**Agent Skill 包**,把 MapleStory 全棧開發規範固化成 AI 可讀的指引。

### 6.2 5 份文檔(`05-Documentation/xiaoye-MapleStory-dev/`)

| 檔案 | 大小 | 內容 |
|---|---|---|
| `README.md` | 11KB | 倉庫介紹 + 四平台整合方法 |
| `SKILL.md` | 23KB | **核心規範**:15 條強制門禁、思考→抉擇→計劃流程 |
| `toolchain.md` | 17KB | BeiDou 全套工具鏈集成指南(MySQL/MCP/IDA/插件) |
| `checklist.md` | 2KB | 交付前逐項檢查清單 |
| `feature-doc-template.md` | 2KB | 功能最終實現文檔模板 |

### 6.3 15 條強制門禁(從 SKILL.md 摘錄)

> 違反即停

1. **先抉擇、再計劃、後實現** — 禁止立刻寫代碼
2. **規範優先** — 符合既有約定
3. **驗證門禁** — 單測 + 構建必須
5. **禁止想象修改** — 插件/二進制/協議改動必須 IDA MCP 校準
6. **資源同步意識** — 跨端/多語言目錄同步
7. **編碼防亂碼** — 禁止 UTF-8 中文直塞 GBK 封包
8. **WZ/IMG/XML 走 MCP** — 用 orange-wz MCP,禁止手改二進制
11. **交付文檔** — 寫清「最終實現邏輯文檔」
13. **同会话任務續作** — 防遺忘
14. **插件改完同步客戶端** — 自動覆蓋

### 6.4 怎麼安裝(給 Agent 平台用)

```bash
# 完整複製整個目錄到目標 skills 目錄
# 例如 ~/.agents/skills/ (Cursor/CodeBuddy/Claude Code)
cp -r xiaoye-MapleStory-dev/ ~/.agents/skills/

# 自動觸發:在對話提到「冒險島/MapleStory/WZ/IMG/道具/小冊子」等
# 手動觸發:/xiaoye-MapleStory-dev
```

### 6.5 與你整合任務的關聯

這個 SKILL **不是工具**,而是**方法論**。在你做「功能整合」時:
- 寫整合前先讀 `SKILL.md` 取得 15 條門禁
- 寫整合後用 `checklist.md` 自檢
- 寫整合文檔用 `feature-doc-template.md` 模板
- 工具鏈整合照 `toolchain.md`(但你的工具鏈跟 BeiDou 的不完全相同)

---

## §7 整合任務優先級建議

依「投入/收益」排序,給你做決策用:

### 🟢 **極易 + 高收益**(建議立刻做)

| 任務 | 來源 | 動作 |
|---|---|---|
| 1. **用 kaentake 連本機 Cosmic** | kaentake binary | 把客戶端導向 `127.0.0.1:8484` |
| 2. **讀 WZ Mod Tool Suite README** | docs 已在 | 確認能不能用本地 `04-Emulators/GMS-v083-Cosmic/wz/` XML 結構 |
| 3. **用 xiaoye SKILL 作為開發流程** | 5 文件已在 | 把 `SKILL.md` 當後續所有任務的 checklist |

### 🟡 **中等難度**(選做)

| 任務 | 來源 | 動作 |
|---|---|---|
| 4. **移植 SoloMapling 的 11 個 GM 指令** | gm4/ SoloMapling 指令 | 複製 `client/command/commands/gm4/` 11 個檔到 Cosmic |
| 5. **整合 WZ Mod Manager** | WZ Mod Tool Suite | 跑一次 status/doctor 驗證 Cosmic wz 結構相容 |
| 6. **用 BeiDou 的 GameConfig 設計思想** | CLAUDE.md 概念 | 設計 Cosmic 配置熱重載 |

### 🔴 **高難度**(長期)

| 任務 | 來源 | 動作 |
|---|---|---|
| 7. **完整移植 SoloMapling bot 框架** | 31.5k 程式碼 | 整包 `soloMapling/` 進 Cosmic(需重新編譯,加 JGraphT 依賴) |
| 8. **BeiDou 商業層引入** | Spring Boot + JWT | 需要大改 Cosmic 啟動架構 |
| 9. **整合 orange-wz MCP** | 外部工具 | 單獨專案,與服務器整合需要 MCP server 串接 |

---

## §8 整合路徑依賴鏈

```
Cosmic (本機 v1.1.3)
│
├── 可直接用(零修改)
│   ├── kaentake (binary → 客戶端)
│   ├── WZ Mod Tool Suite (讀 wz/*.xml)
│   └── xiaoye SKILL (規範文檔)
│
├── 需小修改(< 100 行)
│   ├── SoloMapling GM 指令 (11 檔, ~2850 行,但僅 gm4 範圍)
│   ├── SoloMapling 框架 copy (1 個 package, 33 檔改 cosmic base)
│   └── BeiDou i18n 雙語機制(wz-zh-CN 覆蓋 wz)
│
└── 需大改(架構)
    ├── Spring Boot 整合(BeiDou 風格)
    ├── JWT API 層
    └── MyBatis-Flex ORM 替換
```

---

## §9 相依工具鏈(你的本機已有)

| 工具 | 路徑 | 用途 |
|---|---|---|
| WzComparerR2-KENNYSOFT | `01-WZ-Tools/` | WZ 比較/編輯 |
| HaRepacker-resurrected | `07-Tools-General/` (待 clone) | WZ 編輯 |
| wz-node (toyobayashi) | `01-WZ-Tools/` | Node.js WZ 解析 |
| MapleStory-GM-Client | `07-Tools-General/` | 離線客戶端模擬器 |
| WZFiles enum | Cosmic 源碼 | 列出所有依賴的 .wz |

---

## §10 給你的整合任務啟動腳本

如果你要開始一個具體整合工作,先問自己:

```markdown
□ 任務名稱:______
□ 目標專案: P0nk/Cosmic (本機 v1.1.3) ← 不可改主版本
□ 修改範圍: [ ] client/  [ ] net/  [ ] server/  [ ] scripting/  [ ] scripts/  [ ] wz/
□ 新增依賴: 是 / 否 → 哪些?
□ 預估行數: < 100 / 100-1000 / 1000+
□ 單元測試: 有 / 無 / N/A
□ 文檔: 是否寫「最終實現邏輯文檔」(用 feature-doc-template.md)
□ 驗證: 客戶端連得到 + 操作正確 = 通過
□ 風險: 是否會動到其他功能?若會,先列清單
```

---

## §11 來源驗證清單

| 事實 | 驗證命令 | 結果 |
|---|---|---|
| kaentake Custom.wz 是加密 WZ | `head -c 32 Custom.wz \| xxd` | `PKG1 v1.` |
| kaentake 二進制是真 PE | `head -c 2 Kaentake.exe` | `MZ` |
| Cosmic port 8484 | `grep 8484 Server.java` | 行 936,938 |
| Cosmic Channel 7575 | `grep BASE_PORT Channel.java` | 行 78,131 |
| SoloMapling 是 Cosmic fork | SoloMapling README | ✓ |
| BeiDou 是 Cosmic 漢化 | BeiDou README | ✓ |
| WZ Mod 工具只支援 XML WZ | Tool Suite README | ✓ "Only v83 Cosmic-style servers" |
| xiaoye skill 4 文件結構 | xiaoye README | ✓ |

---

## §12 下次該 clone/抓取的清單(若需要)

| 項目 | URL | 為什麼需要 |
|---|---|---|
| Cosmic-client | https://github.com/P0nk/Cosmic-client | 客戶端檔案(已驗證,可用) |
| BeiDou-ijl15 | https://github.com/BeiDouMS/BeiDou-ijl15 | ijl15 插件源碼 |
| BeiDou-docker | https://github.com/BeiDouMS/BeiDou-docker | docker 部署 |
| orange-wz | https://github.com/gujichu/orange-wz | WZ/IMG MCP 工具 |
| ida-pro-mcp | https://github.com/mrexodia/ida-pro-mcp | IDA MCP |
| NapMysqlTool | https://github.com/SleepNap/NapMysqlTool | MySQL 圖形化工具 |
| Maplestory-HaRepacker | https://github.com/lastbattle/Harepacker-resurrected | WZ 編輯器 |

> 這些都與你「個人學習/單機版」目標一致,且不違反法律風險。

---

## §13 完成動作摘要

本次執行的所有下載/抓取動作:

| 動作 | 大小 | 耗時 | 目標位置 |
|---|---|---|---|
| 抓 xiaoye-MapleStory-dev 5 文件(raw) | 55 KB | < 5 秒 | `05-Documentation/xiaoye-MapleStory-dev/` |
| 抓 WZ Mod Tool Suite(gh-proxy 加速) | 5.9 MB | **1.3 秒** | `07-Tools-General/SoloMapling-wisteria-Wz-Mod-Tool-Suite/` |
| 抓 SoloMapling 9 份架構文檔(raw) | 114 KB | < 10 秒 | `04-Emulators/SoloMapling-Documents/` |
| 抓 kaentake v3.4.1 release(3 binaries) | 190 KB | < 2 秒 | `12-OffShelf-Client-Fork/kaentake/` |
| 抓 BeiDou 4 份核心文檔(raw) | 18 KB | < 5 秒 | `05-Documentation/BeiDou-Server-Notes/` |

**未執行的(刻意)**:
- ❌ SoloMapling 整包 clone(太大,與 Cosmic 重複;用文檔已足)
- ❌ BeiDou-Server 整包 clone(太大,商業性質強;用 CLAUDE.md 已足)
- ❌ xiaoye-MapleStory-dev git clone(timeout 300 秒還沒好;改用 raw 5 秒搞定)
- ❌ kaentake 整包 clone(只有 3 個 binary,直接從 Release 抓更快)
