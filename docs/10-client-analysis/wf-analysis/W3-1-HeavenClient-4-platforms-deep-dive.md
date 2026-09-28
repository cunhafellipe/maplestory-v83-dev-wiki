# W3-1: MapleStory-Client / HeavenClient 4 端路線深度拆解

> **分析時間**: 2026-09-27
> **路線核心**: ryantpayton/MapleStory-Client + 4 個 platform fork

---

## §0 為什麼「居然 4 端通用」是真的

**事實**:**同一份 C++ core source code**,透過 4 個 platform fork 編譯到 4 個作業系統/裝置:

| 端 | Repository | 平台 |
|---|---|---|
| **PC (Windows)** | `ryantpayton/MapleStory-Client` master | Windows |
| **PC (Linux)** | `ryantpayton/MapleStory-Client` @ branch `linux` | Linux |
| **PC (macOS)** | `ryantpayton/MapleStory-Client` @ branch `mac` | macOS |
| **Switch** | `lain3d/HeavenClientNX` | Nintendo Switch(自製韌體)|
| **Web (WASM)** | `nmnsnv/maplestory-wasm` | 任何瀏覽器 |
| **Android** | `Joseph1010805/HeavenClient-Android` = **LocalStory** | Android(包括掌機)|

**為什麼能這麼做**(純技術事實):

1. **C++17**(所有平台都用)
2. **PLATFORM_UNIX + PLATFORM_SWITCH + PLATFORM_ANDROID 條件編譯**(`#ifdef`)
3. **同一份 Net/ Gameplay/ IO/ Graphics 模組** — 只換 platform abstraction
4. **同一份 NX 資源檔** — 跨平台通用(只讀檔,不需要轉檔)
5. **同一份 OpCode** — 不需對應任何特殊 server,只看 server 送什麼

---

## §1 PC (master 分支) — 主線

### §1.1 repo metadata

| 屬性 | 值 |
|---|---|
| 完整名稱 | ryantpayton/MapleStory-Client |
| 描述 | A custom client for HeavenMS |
| Stars / Forks | **243** / 96 |
| 最後 commit | 2026-02-25 |
| 預設 branch | master |
| 主語言 | C(API 用 C 但實作是 C++)|
| License | AGPL-3.0 |
| Repo size | 28.8 MB |

### §1.2 頂層結構

```
MapleStory-Client/
├── Audio/         (BASS 音效後端)
├── Character/     (角色資料 + 庫存 + Look)
├── Data/          (從 NX 載入道具/技能/怪物資料)
├── Gameplay/      (Combat/ + MapleMap/ + Physics/)
├── Graphics/      (OpenGL 後端 + Animation + Texture)
├── IO/            (UI + Keyboard + Cursor + UIState)
├── Net/           (Cryptography + Session + Packets/ + Handlers/)
├── Util/          (工具函式)
├── Template/      (Singleton / Point / TypeMap 等基底)
├── fonts/         (字體檔)
├── includes/      (外部 header)
├── Configuration.{cpp,h}
├── Constants.h
├── Error.h
├── MapleStory.{cpp,h,rc,sln,vcxproj,filters}   ← VS 專案
├── Timer.h
└── LICENSE(34.5 KB, AGPL-3.0)
```

### §1.3 建置需求

| 項目 | 版本 |
|---|---|
| IDE | **Visual Studio 2026 Community v18.2.1**(新)|
| Windows SDK | 8.1 |
| Platform Toolset | v140 |
| 預設 define | `USE_CRYPTO` ✓ / `USE_NX` ✓ / `USE_ASIO` ✗ |

### §1.4 自有分支

| branch | 最後 commit | 內容 |
|---|---|---|
| `master` | 2026-02-25 | 主線(Windows PC)|
| `linux` | 2020-05-09 | Linux 編譯改善 |
| `mac` | 2019-11-05 | macOS port(實驗性)|
| `v92-support` | ? | **v92 server 相容**(不是 v83!)|

**純事實**:
- 4 個分支:**master 是活躍開發、linux/mac 很久沒動、v92-support 是另條相容線**
- 目前 master 對應 v229.2 + HeavenMS,**不是 GMS v83 + Cosmic**(雖然 README 有提 v83 相容)

---

## §2 Switch port — `lain3d/HeavenClientNX`

### §2.1 repo metadata

| 屬性 | 值 |
|---|---|
| Stars / Forks | 40 / 16 |
| 最後 commit | 2020-05-14 |
| License | AGPL-3.0 |
| 開發者 | lain3d |

### §2.2 編譯需求

```bash
DevkitPro setup → source $DEVKITPRO/switchvars.sh
./build-deps.sh
./build-switch.sh
```

### §2.3 Switch 平台條件編譯(`CMakeLists.txt`)

```cpp
add_definitions(-D__SWITCH__=1)
add_definitions(-DSTATIC_LIBVORBIS=1)
add_definitions(-DPLATFORM_UNIX=1)
add_definitions(-DPLATFORM_SWITCH=1)
add_compile_options(-march=armv8-a -mtune=cortex-a57 -mtp=soft -fPIE)
add_compile_options(-mcpu=cortex-a57+crc+fp+simd)
```

**事實**:
- 目標 CPU:**NVIDIA Tegra X1 的 ARM Cortex-A57**(Switch 處理器)
- 共用 Switch 與 Linux 的 POSIX 環境(PLATFORM_UNIX)
- 使用 devkitpro/libnx(Switch homebrew SDK)
- 走 Atmosphere CFW 載入 `.nro`

### §2.4 特殊技術

- **同一份 .nx 檔直接從 PC 版用過來**(不用轉檔)
- **特殊按鍵映射** — keyboard keys 對應 Switch 按鈕(用 glfw3 codes)
- 透過 **nxlink** 可以用 stdout 看到 debug print

### §2.5 對應 server

> "The client is currently compatible with **version 83 servers**. The client has only been tested with HeavenMS."

→ Switch port 對應 **v83**,**不是 v229**!

**結論(純事實)**:**Switch port 仍是 v83 相容**,對應 HeavenMS(v83 系列)。

---

## §3 Web (WASM) — `nmnsnv/maplestory-wasm`

### §3.1 repo metadata

| 屬性 | 值 |
|---|---|
| Stars / Forks | 89 / 51 |
| 最後 commit | 2026-02 |
| License | AGPL-3.0 |
| 創建時間 | 2025-12-27(快 1 年了)|
| Homepage | https://wuzekang.github.io/maple-rs/(誤,實際是 https://discord.gg/bfnmA9sVZ4)|

### §3.2 架構圖(README 原文)

```
┌───────────────────────────┐       ┌──────────────────────────────────────┐
│     Web Server (Python)   │       │            Browser (Client)          │
│     web/server.py         │──────▶│   MapleStory WASM Client Runtime     │
│     http://localhost:8000 │ HTTP  │       (JS + WASM in browser)         │
└───────────────────────────┘       └───────────────┬──────────────┬───────┘
                                                    │              │
                                                    │ WebSocket    │ WebSocket
                                                    │ (Game        │ (Asset
                                                    │ Packets)     │ Requests)
                                                    ▼              ▼
                                          ┌────────────────┐  ┌───────────────────────────┐
                                          │ WS Proxy       │  │   Assets Server (Python)  │
                                          │ web/ws_proxy.py│  │   ws://localhost:8765     │
                                          │ :8080          │  └───────────────────────────┘
                                          └───────┬────────┘
                                                  │ TCP
                                                  ▼
                                          ┌───────────────────────────┐
                                          │    Cosmic Server (TCP)    │
                                          └───────────────────────────┘
```

### §3.3 純技術事實

1. **WASM 編譯**:Emscripten 把 C++ 編譯成 WASM + JS 綁定
2. **瀏覽器不能直連 TCP** → Python `ws_proxy.py` 當 **WebSocket ↔ TCP 橋接**
3. **Web Server** (Python, port 8000) 服務 WASM 與 JS bundle
4. **Assets Server** (Python, port 8765) 透過 WebSocket 提供 NX 檔
5. **WS Proxy** (Python, port 8080) 透過 WebSocket 提供 game packets
6. **目標 server**:README 明說 **「The client is designed to run with Cosmic server」**

**結論**:Web 版是 **唯一一個在 browser 跑 v83 + Cosmic** 的方案!

### §3.4 缺點

- WASM 效能受限(不是 native)
- 額外要架設 2 個 Python server
- LazyFS(動態檔案系統)額外複雜

---

## §4 Android — `Joseph1010805/HeavenClient-Android`(LocalStory)

### §4.1 repo metadata

| 屬性 | 值 |
|---|---|
| 名稱(顯示)| **LocalStory** |
| Stars / Forks | 1 / 1 |
| 最後 commit | 2026-09-27(**今天!**)|
| 創建時間 | 2026-08-20(一個月多)|
| License | AGPL-3.0 |

**驚人事實**:
- **ryantpayton 是 contributor #2(101 commits)!** → HeavenClient 原作者也參與 Android port 開發
- lain3d(40 ★ Switch port 作者)也是 contributor(34 commits)

### §4.2 編譯(Android 平台條件編譯)

```cpp
if(ANDROID)
    add_definitions(-DPLATFORM_UNIX=1)
    add_definitions(-DPLATFORM_ANDROID=1)
    add_definitions(-DUSE_ASIO=1)
    add_definitions(-DASIO_STANDALONE=1)
```

**事實**:
- POSIX 共用 Switch(Linux/BSD socket stack)
- **SDL2 取代 GLFW**(Android 視窗管理)
- **GLES2 取代 desktop GL**
- **USE_ASIO** 開啟(Android 用標準 POSIX socket,不用 mbedtls)
- 遊戲資料放 external storage,**沒有 romfs**

### §4.3 完整產品定位(作者原文)

> "MapleStory on your phone or handheld. ... it plays against a v83 private server like Cosmic or HeavenMS. I built it to play with my sons over our home WiFi on an AYN Thor."

> "**The app can run the server itself, so a handheld can host a game with no PC, no router and no internet at all** — one device becomes the network and the others join it by name."

**重點事實**:
- **目標硬體**:AYN Thor(Android 掌機,Steam Deck 類)
- **可選 hosting**:手機本身當 server,**不用 PC、不用網路**
- 透過 **Termux**(Android 上的 Linux 環境)跑 **Java + MariaDB + Cosmic**
- 帳號:任意 username/password,**自動建立**(沒 sign-up)

### §4.4 遊戲檔需求

| 版本 | 用途 |
|---|---|
| **v83** client | 全部遊戲檔(Base/Character/Effect/Etc/Item/Map/Mob/Morph/Npc/Quest/Reactor/Skill/Sound/String/TamingMob)|
| **v178** client | **只取 UI.wz**(一個檔案)— 因為 v83 UI 太舊 client 啟動不了 |

**事實**:
- 安裝器自動跑 **NoLifeWzToNx** 把 v83 的 WZ 全部轉成 NX
- v178 的 UI.wz 轉成 UI.nx
- 保留原 WZ 不動

### §4.5 安裝流程(作者原文)

1. 下載 `LocalStory-installer-*.zip`(120 KB)
2. 裝兩個 MapleStory client(v83 + v178)
3. 開 USB debugging
4. 插線跑 `INSTALL.bat`(10 分鐘首次)
5. 開 app → CREATE A GAME → 選 PUBLIC/PRIVATE → 玩

---

## §5 「Cosmic v83 專用」 fork — `itayzrihan/MapleStory-Client-Cosmic`

### §5.1 repo metadata

| 屬性 | 值 |
|---|---|
| 名稱(顯示)| MapleStory-Client-Cosmic |
| Stars / Forks | 0 / 2 |
| 最後 commit | 2025-11-11 |
| License | AGPL-3.0 |

### §5.2 純事實

- 這是一個**特殊 fork**,README 標題:**「HeavenClient for Cosmic v83 MapleStory server — Cosmic NX file compatibility modifications」**
- 目標:**確保 NX 檔案格式與 Cosmic server 完全相容**
- 對應 v83 server(不是 v229.2)
- 規模小(0 ★)但**仍在活躍**(2025-11 commit)

**事實結論**:ryantpayton 的 master 主推 v229.2,而 fork 出來支援 v83 + Cosmic — 因為 **v229.2 + v83 客戶端不能直接互通**。

---

## §6 WZ ↔ NX 轉換:NoLifeWzToNx

### §6.1 repo metadata

| 屬性 | 值 |
|---|---|
| 名稱 | ryantpayton/NoLifeWzToNx |
| 類型 | CLI 工具 |
| 最後 commit | 2026-02-09(同步 master)|
| 維護者 | ryantpayton + Peter Atashian |

### §6.2 支援的 WZ 格式

| 格式 | 版本範圍 | 狀態 |
|---|---|---|
| Legacy + version hash | Pre-v170(**含 v83**、v112)| ✓ 支援(自動爆破 version hash)|
| New 64-bit (無 version hash) | v170+ / v200+(含 v229.2)| ✓ 支援 |

**重要**:**v83 完全支援**(GMS v83 用 legacy format)!**這就是 GMS v83 WZ 能轉成 NX 的唯一已知工具**。

### §6.3 用法

```bash
# 把 .wz 放在 files/ 目錄
NoLifeWzToNx files -c      # client 模式(含 image/sound)
NoLifeWzToNx files -s      # server 模式(跳過 image/sound)
NoLifeWzToNx files -h      # 用 LZ4 HC 高壓縮
NoLifeWzToNx files -i      # 只顯示 WZ 資訊
```

### §6.4 包含依賴(全在 includes/)

| 函式庫 | 用途 |
|---|---|
| **libsquish** | DXT texture decompression |
| **LZ4** | 快速無損壓縮 |
| **zlib** | 一般用途壓縮 |

### §6.5 不相容

- **`Data.wz`** — 不是標準 WZ 檔,會造成錯誤(README 警告)

---

## §7 完整的「HeavenClient 跨平台宇宙」對照

```
JourneyClient (Daniel Allendorf 2015-2019)
  └── MapleStory-Client (ryantpayton 2023-04)
        │
        ├── master branch (Windows PC, v229.2)
        ├── linux branch (Linux PC, 2020-05 停)
        ├── mac branch (macOS, 2019-11 停)
        ├── v92-support branch (v92 server)
        │
        ├── MapleStory-Client-Cosmic (itayzrihan 2025-11)
        │     → 為 Cosmic v83 NX 相容性修改
        │
        ├── NoLifeWzToNx (ryantpayton 2026-02)
        │     → WZ → NX 轉檔工具(含 v83)
        │
        └── 4 個 Platform fork:
              │
              ├─ lain3d/HeavenClientNX (Switch, 2020-05 停)
              │    → DevkitPro + libnx + Atmosphere
              │    → 對應 v83
              │
              ├─ nmnsnv/maplestory-wasm (Web, 2025-12, 活躍)
              │    → Emscripten + Python WS Proxy + Cosmic server
              │    → 對應 v83
              │
              └─ Joseph1010805/HeavenClient-Android (Android, 2026-09)
                   → LocalStory(掌機 + 手機)
                   → SDL2 + GLES2 + Termux(可 host Cosmic)
                   → 對應 v83
                   → ryantpayton 是 contributor #2
```

---

## §8 對 GMS v83 + Cosmic 的「兼容性」光譜

| 平台 | Repository | 對應 v83? | 對應 v229.2? | 對應 Cosmic? | 活躍? |
|---|---|---|---|---|---|
| PC Windows master | ryantpayton/MapleStory-Client | △(可但預設 v229.2)| ✓ | ✗(預設)| ✓ |
| PC Linux | 同上 @ linux branch | △ | ? | ? | ✗(2020-05)|
| PC macOS | 同上 @ mac branch | ? | ? | ? | ✗(2019-11)|
| Switch | lain3d/HeavenClientNX | ✓ | ✗ | △ | ✗(2020-05)|
| Web | nmnsnv/maplestory-wasm | **✓** | ✗ | **✓** | ✓(2025-12~)|
| Android | LocalStory | **✓** | ✗ | **✓** | **✓(2026-09)**|
| Cosmic 專用 fork | itayzrihan/MapleStory-Client-Cosmic | **✓** | ✗ | **✓** | ✓(2025-11)|

---

## §9 純技術事實結論(不下結論)

### 4 端通用怎麼做到

1. **C++17** + 嚴格 `#ifdef` 平台抽象
2. **POSIX 共用層**(Switch、Android、Linux、macOS)
3. **網路抽象**(`SocketAsio` 取代 `SocketWinsock`)
4. **圖形抽象**(GLFW3 / GLES2 / SDL2 各平台挑選)
5. **資源格式 NX**(跨平台檔案,所有平台讀同一份)
6. **數據資料**(`USE_NX` 預設開啟,WZ 是 fallback)

### 對你 GMS v83 + Cosmic 路線的技術事實

1. **MapleStory-Client master 不直接給 v83 + Cosmic**(預設 v229.2)
2. **但是 Cosmic 專用 fork exists**:`itayzrihan/MapleStory-Client-Cosmic`(2025-11 活躍)
3. **NoLifeWzToNx 完全支援 v83 WZ → NX** — 你的 GMS v83 WZ 可直接轉
4. **Web 版 nmnsnv/maplestory-wasm 明確說設計給 Cosmic**
5. **LocalStory (Android) 明確說對應 v83 + Cosmic**(而且是 ryantpayton 參與)
6. **OpenMapleClient 與 MapleStory-Client 都是 Daniel Allendorf 同源** — 都是 JourneyClient fork

### 沒做的事(刻意)

- ❌ 不評論技術深度
- ❌ 不推薦整合方案
- ❌ 不評論法律風險
- ❌ 不評論 WZ→NX 轉檔品質
- ❌ 不評論 AYN Thor 掌機可用性
- ❌ 不評論 Termux 跑 Cosmic server 的可行性

---

**輸出位置**: `C:\MUWORK\GAME\MAPLESOTRY\wf-output\W3-1-HeavenClient-4-platforms-deep-dive.md`
