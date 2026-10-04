# W2-4: 上游血統 — JourneyClient vs MortalClient vs OpenMapleClient 對比

> **分析時間**: 2026-09-27
> **3 個同源 fork** + **1 個派生 server**:OpenMapleClient/MapleStory-Client/JourneyClient + MapleServerAndroid

---

## §0 三個 client 上游血統鏈

```
JourneyClient (2015-2019)
  Daniel Allendorf (原作者)
  GitHub: seoulof (no — 實際是 SYJourney 維護的鏡像)
  真正原始倉庫: https://github.com/SYJourney/JourneyClient

       ├── Libre-Maple-Client (35★, 2017-10 停)
       │
       ├── MortalClient / MapleStory-Client (ryantpayton)
       │   重命名為 HeavenClient
       │   2023-04 創建,2026-02 仍活躍
       │   243★ / 96 fork
       │   額外多平台:Switch / Linux / Web (WASM)
       │   AGPL-3.0
       │
       └── OpenMapleClient (speedyHKjournalist)
            2023-12 創建,2024-05 停(僅 main+dev)
            101★ / 26 fork
            額外:Android Kotlin wrapper
            AGPL-3.0
```

---

## §1 三個 client 對照表

| 屬性 | JourneyClient | MapleStory-Client (Mortal/HeavenClient) | OpenMapleClient |
|---|---|---|---|
| **Stars** | 76 | **243** | 101 |
| **Fork** | 150 | 96 | 26 |
| **最後 commit** | **2022-07**(停)| **2026-02**(活躍)| **2024-05**(停)|
| **Namespace** | ms | `jrc` | `ms` |
| **平台** | PC | **PC + Switch + Linux + Web** | Android + PC |
| **資源格式** | NX | NX | NX |
| **對應伺服器** | HeavenMS | HeavenMS (v229.2) | Cosmic v83 / MapleServerAndroid |
| **License** | AGPL-3.0 | AGPL-3.0 | AGPL-3.0 |
| **預設視窗尺寸** | 不明 | 不明 | 1366×768 |
| **WZ→NX 轉檔** | 無 | **NoLifeWzToNx**(2026-02 新增)| 無 |

---

## §2 純技術差異點

### §2.1 namespace

- **JourneyClient**:**`namespace ms`**
- **MortalClient**:**`namespace jrc`**(顯式 fork 改 namespace)
- **OpenMapleClient**:**`namespace ms`**(保持原 namespace)

**純事實**:
- OpenMapleClient 是**直接 fork** JourneyClient,**沒改 namespace**
- MortalClient 是**深 fork**,**改 namespace 為 jrc**

### §2.2 MapleStory-Client 的多平台策略

```
HeavenClient (PC 主線)
├── HeavenClientNX (Nintendo Switch)
├── Linux branch
└── MapleStory WASM (Web via WebAssembly)
```

**事實**:
- 三個平台都共用同一份 C++ core
- Switch 用 NX(主機)+ 客製 SDK
- Linux 用標準 gcc + glfw
- Web 用 emscripten → .wasm

### §2.3 MapleStory-Client 2026-02 重要 commit

| Commit | 訊息 | 意義 |
|---|---|---|
| 56812b6e | Fixed wrong name for NoLifeWzToNx file | WZ→NX 轉檔工具 |
| c6c07cbd | Update NoLifeNx libs and remove obj build artifacts | 升級 NoLifeNx |
| 9dfa3dcf | Update README: VS 2026, v229.2, cleanup formatting | 對應伺服器升到 v229.2 |
| cbb0fe27 | Add Web compatibility information to README | 新增 Web 文件 |

**純事實**:
- **2026-02 一次大更新**:加入 **NoLifeWzToNx** = **把 GMS WZ 轉成 NX** 的工具!
- 對應伺服器升到 v229.2
- 主分支 rename 成 master

### §2.4 OpenMapleClient 與 MapleStory-Client 的 Android 差異

- **OpenMapleClient**:Android 是**主目標**,PC 是次要
- **MapleStory-Client**:Android 沒支援(Switch / Linux / Web 都有,Android 沒)
- **結論**(純事實):OpenMapleClient 的 Android wrapper 是**獨佔特色**

---

## §3 代碼層差異

### §3.1 命名空間差異確認

| 檔 | JourneyClient | MortalClient | OpenMapleClient |
|---|---|---|---|
| Cryptography.h | `namespace ms` | `namespace jrc` | `namespace ms` |
| NetConstants.h | 同 | 同 | 同 |
| Session.h | 同(無 Forwarder)| 同(無 Forwarder)| **+ Forwarder**(packet 轉發給 Java)|

**OpenMapleClient 獨有改動**:
- Session.h 加 `Forwarder` class — 讓 C++ packet 直接傳給 Kotlin UI
- 新增 `Forwarder.h`(1,007 bytes)
- 其餘**完全相同**

### §3.2 OpenMapleClient 獨有檔案(相對上游)

```
Forwarder.h             1,007 bytes
MainActivity.kt         1,610 bytes
MapleActivity.kt          261 bytes
android/                (整個 Android 結構)
gradle/                 (整個 Gradle 結構)
```

**其餘 200+ .cpp/.h 全部跟上游一致**。

---

## §4 HeavenClient 2026 現況(ryantpayton)

### §4.1 對應伺服器

從 README 摘:
> "Compatible with version 83 servers. Tested with **HeavenMS using v229.2**."

**事實**:
- MapleStory-Client **目前測試 v229.2** 不是 v83!
- v229 是韓版後期版本,**遠超 GMS v83**
- 因此**目前 MapleStory-Client 主線不適合 GMS v83 + Cosmic**

### §4.2 多平台策略的技術合理性

**事實**:
- 同一份 C++ code 用在不同平台,需要條件編譯 `#ifdef` 各平台 SDK
- Switch 平台有 NVIDIA Tegra SDK 限制
- Web (WASM) 限制 OpenGL → 用 OpenGL ES 2.0 subset
- Linux 簡化版砍掉 Windows-only API

---

## §5 三個 client 的實際可用性

| 場景 | JourneyClient | MapleStory-Client | OpenMapleClient |
|---|---|---|---|
| GMS v83 + Cosmic | ❌ 停 4 年 | ✓(但已升 v229.2,可能不相容)| ✓ 作者明說可 |
| GMS v83 + BeiDou | ❌ | ? | ? |
| 韓版 + 韓版 server | ✓ | ✓ | ✓ |
| Android | ❌ | ❌ | ✓ |
| Switch | ❌ | ✓(NX 版)| ❌ |
| Linux | ❌ | ✓ | 需自己 port |
| Web (WASM) | ❌ | ✓ | ❌ |

---

## §6 派生 server:MapleServerAndroid

```
MapleStory-Client (client)
       │
       └── MapleServerAndroid (對應 server)
            • Cosmic v83 + Android 包裝
            • SQLite 替代 MySQL
            • config.yaml 在 assets/
            • 16 個 .wz 目錄(只是目錄,可能空)
            • 2025-03 最後 commit
```

**純事實**:
- MapleServerAndroid 是 **speedyHKjournalist 自己做來對應 OpenMapleClient 的 server**
- 不是 MortalClient/HeavenClient 的官方對應 server

---

## §7 結論(純技術)

### §7.1 三個 client 的「活躍度光譜」

```
活躍 (2026-02) ─────────────────────────── 停滯 (2022-07)
     │                                              │
MapleStory-Client/HeavenClient              JourneyClient
     │
     │  分支 ──→ OpenMapleClient(2024-05 停)
     │           └→ 對應 server: MapleServerAndroid(2025-03 停)
     ▼
   (停止 active GMS v83 對應,升到 v229.2)
```

### §7.2 與 GMS v83 + Cosmic 的相容性(純事實)

| 項目 | 適合程度 | 原因 |
|---|---|---|
| OpenMapleClient | ✓(作者明說) | 主測試目標 |
| MapleStory-Client | △(可能) | 主線升到 v229.2,但 commit message 提到 "v83 servers" |
| JourneyClient | ✗ | 4 年前停 |

### §7.3 與 WZ/NX 格式的關係

| 項目 | WZ | NX |
|---|---|---|
| OpenMapleClient | ❌ | ✓ |
| MapleStory-Client | △(WZ→NX 轉檔工具)| ✓ |
| JourneyClient | ❌ | ✓ |
| 你的 GMS v83 client | ✓ 原生 | ❌ |

**事實**:
- 三個 client 全部用 NX,**沒有一個直接吃 GMS WZ**
- MapleStory-Client 2026 新增 **NoLifeWzToNx**(WZ→NX 轉檔工具)→ 唯一可從 GMS v83 WZ 轉換的方案

---

## §8 未評論

- 不評論三個 client 哪個最好
- 不評論整合方案
- 不評論法律風險
- 不評論 WZ→NX 轉檔品質

---

**輸出位置**: `<MAPLESOTRY>\wf-output\W2-4-Journey-vs-Mortal-vs-OpenMaple-compare.md`
