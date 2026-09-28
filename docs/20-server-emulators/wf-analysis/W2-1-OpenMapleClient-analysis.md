# OpenMapleClient — 純技術拆解

> **分析時間**: 2026-09-27
> **repo**: https://github.com/speedyHKjournalist/OpenMapleClient
> **作者**: speedyHKjournalist(港籍開發者)
> **官方測試相容**: `P0nk/Cosmic`(用戶已在用)、`speedyHKjournalist/MapleServerAndroid`

---

## §0 元資料

| 屬性 | 值 |
|---|---|
| 創建 | 2023-12-26 |
| 最後 commit | 2024-05-03(`dev` 分支,「Add Drag UI」)|
| 最後 issue | 2026-03-05(PIN 碼後黑屏)|
| Stars / Forks | 101 / 26 |
| 語言(主)| C++ + Kotlin |
| License | **AGPL-3.0**(整個 repo + 包含 nlnx)|
| 預設 branch | main |
| 額外 branch | dev(僅多 1 commit)|
| Clone URL | https://github.com/speedyHKjournalist/OpenMapleClient.git |
| Repo size | 110 MB(git tracked 49 MB)|
| 頂層結構 | Android Studio 標準 Gradle:`app/` + `gradle/` + `build.gradle` |

---

## §1 結構事實

```
app/src/main/
├── AndroidManifest.xml           1.5 KB
├── assets/
│   ├── Roboto-Bold.ttf           170 KB
│   └── Roboto-Regular.ttf        171 KB
├── cpp/                          ← 主要 C++ 程式
│   ├── CMakeLists.txt            9.4 KB(C++17)
│   ├── gl.cpp/h
│   ├── src/                      (18 大類,190+ .cpp)
│   └── thirdparty/
│       ├── nlnx/                 ← NoLifeNX(NX 格式解析)
│       ├── asio/                 ← 非同步網路
│       ├── bass/                 ← 音效
│       ├── freetype/             ← 字體渲染
│       ├── glfm/                 ← OpenGL ES for mobile
│       ├── glfw/                 ← PC 版 OpenGL
│       ├── lz4/                  ← 壓縮(nlnx 內)
│       └── stb/                  ← 圖片載入
├── java/openMapleClient/
│   ├── MainActivity.kt           1.6 KB(輸入 HOST IP)
│   └── MapleActivity.kt          261 B(extends NativeActivity)
└── res/
```

---

## §2 上游血統

**事實鏈**:
1. **`Copyright (C) 2015-2019 Daniel Allendorf, Ryan Payton`** 在每個 .cpp/.h 開頭
2. **`namespace ms`** — Daniel Allendorf 的 **JourneyClient** 上游 namespace
3. **MortalClient** 是同一上游的另一個 fork(`namespace jrc`)
4. 因此 OpenMapleClient = **JourneyClient 直接 fork 改 namespace + 加 Android wrapper**

**與 MortalClient 同源檔案**:
- `Net/Cryptography.h`(完全相同結構)
- `Net/NetConstants.h`(完全相同 HEADER_LENGTH=4 / MAX_PACKET_LENGTH=131072)
- `Net/Session.h`(同 USE_ASIO / SocketWinsock 條件編譯)
- `Graphics/GraphicsGL.{cpp,h}`(同 OpenGL 後端)
- `IO/Keyboard.cpp` / `Window.cpp`(同 UI 系統)
- 整個 `Gameplay/Combat/` `MapleMap/` `Data/`

**差異點**(fork 改的):
- `Session` 多了 `Forwarder`(packet 轉發到 Java UI)
- `MainActivity.kt` AlertDialog 輸入 HOST IP
- Android NativeActivity 整合 glfm

---

## §3 通訊協議事實

| 屬性 | 值 |
|---|---|
| HEADER_LENGTH | 4 |
| OPCODE_LENGTH | 2 |
| MIN_PACKET_LENGTH | 6 |
| MAX_PACKET_LENGTH | 131,072 |
| 加密 | Maple custom encryption(roll-left/right) + AES OFB(`#ifdef USE_CRYPTO`)|
| 傳輸層 | asio(預設)/ Winsock(PC fallback)|
| Handshake | 從 16-byte handshake 取 initialization vector |

**與 Cosmic 對應**:
- Header 4 byte + opcode 2 byte = **與 GMS v83 標準一致**
- AES + Maple custom encrypt = **與 Cosmic 服務端加密演算法一致**
- 因此**可與 Cosmic 通訊**(作者 README 明說)

---

## §4 資源格式事實

| 資源 | 格式 | 庫 | 對應 |
|---|---|---|---|
| 客戶端資料 | **NX**(韓版/西版)| **nlnx** (NoLifeNX)| `character/`, `string/`, `item/`, `mob/` |
| 字體 | TTF | freetype + Roboto | 內建 |
| 圖片 | IMG | stb | 載入後轉 OpenGL texture |
| 音效 | BASS | bass | 背景音 + 音效 |

**重要事實**:
- **GMS v83 用 WZ,OpenMapleClient 走 NX 格式**
- 因此直接替換 GMS v83 客戶端資料**不相容**
- 作者 README 明說測試用 server 是 `MapleServerAndroid`(自己的 server,韓版/西版基礎)
- Cosmic 用戶需要**單獨提供韓版/西版 NX 檔**才能用這個 client 連 Cosmic

---

## §5 Android wrapper 事實(Kotlin)

### `MainActivity.kt`(1,610 bytes)
```kotlin
class MainActivity : AppCompatActivity() {
    onCreate() → showTextBoxDialog()
    dialog: AlertDialog "Specify HOST IP Address"
    → 寫到 ExternalFilesDir/hostip.txt
    → 啟動 MapleActivity
}
```

### `MapleActivity.kt`(261 bytes)
```kotlin
class MapleActivity : NativeActivity() {
    // 完全標準 Android NDK 介面
}
```

**純事實**:
- Android wrapper **極簡** — 只有 2 個 Activity
- 沒有任何 UI 邏輯,只是把 C++ Game 啟動起來
- HOST IP 用 `hostip.txt` 檔案傳給 native 層

---

## §6 已知 Bug / Issues

| Issue | 日期 | 內容 |
|---|---|---|
| #5 | 2025-01 | 職業限定裝備無法裝備(只能戰士/法師)|
| #7 | 2026-03 | 人物輸入 PIN 碼後黑屏卡死 |
| (closed) | 2024-03 | 「where can i get the nx files?」(資源檔哪裡拿)|
| (closed) | 2024-03 | Build is failing(gradle 設定問題)|

**作者自陳問題**(README):
- Map rendering
- Quest system
- 完整圖形系統

---

## §7 與現有項目的純技術對照

| 對比項 | OpenMapleClient | MortalClient | kaentake |
|---|---|---|---|
| 語言 | C++ + Kotlin | C++ | C++ |
| 平台 | Android(主要)+ PC | PC | PC |
| Namespace | `ms` | `jrc` | (Win32 DLL)|
| 上游 | JourneyClient(Daniel A.)| JourneyClient(Daniel A.)| 無上游(獨立 hook)|
| 客戶端資源 | NX(韓/西版)| NX(韓/西版)| **WZ(GMS v83 原生)**|
| 加密 | Maple AES OFB | Maple AES OFB | hook 原生 client 跳過 |
| License | AGPL-3.0 | AGPL-3.0 | 不明 |
| 維護 | 2024-05 最後 commit | 不明 | 不明 |
| 對應伺服器 | MapleServerAndroid | MapleStory-io | Cosmic v83 / BeiDou |

**純事實總結**:
- OpenMapleClient 與 MortalClient **幾乎結構相同**(僅 namespace)
- **與 kaentake 是完全不同的路線**:
  - kaentake = hook 原生 MapleStory.exe,UI 用 WZ 原生
  - OpenMapleClient = 自己寫引擎,UI 用自己寫的 OpenGL,資源用 NX(轉換版)
- 要用在 GMS v83 + Cosmic,**需提供韓/西版 NX 檔**(即額外資源)
- 要在 Android 跑,**目標平台一致**;kaentake 只能 PC

---

## §8 純技術限制(作者自陳)

**README 原文**:
- "currently do not have full functionality of the game"
- 未實作:地圖渲染、任務系統、完整圖形
- 測試過的伺服器:`P0nk/Cosmic` + `speedyHKjournalist/MapleServerAndroid`

**最後 commit 訊息**(2024-05-03):
- 「Add Drag UI」(dev 分支最後一個)
- main 分支最後 commit = 2024-04-05

---

## §9 純事實 — 不評論

- 結構 = JourneyClient fork
- 平台 = Android(主要)
- 資源 = NX(韓/西版)
- 通訊 = 與 GMS v83 標準相容(handshake + AES OFB + Maple 自訂加密)
- License = AGPL-3.0(整 repo + 含 nlnx)
- 維護 = 2024-05 後停止 commit(但有 issue 持續回報)
- 與 kaentake 是**不同技術路線**(自寫引擎 vs hook 原生)

---

**輸出位置**: `C:\MUWORK\GAME\MAPLESOTRY\wf-output\W2-1-OpenMapleClient-analysis.md`
