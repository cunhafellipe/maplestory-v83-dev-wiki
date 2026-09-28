# W3-2: MapleStory-Client (HeavenClient) 獨立深度拆解

> **分析時間**: 2026-09-27
> **本地位置**: `C:\Users\e7896\AppData\Local\hermes\cache\scratch\maple-story-client-isolated\msc-repo`
> **獨立工作區原則**:此 repo 完整複製到獨立資料夾,**沒污染任何原生路徑**
> **不評斷其他項目,僅純技術拆解**

---

## §0 倉庫基本資訊

| 屬性 | 值 |
|---|---|
| repo | `ryantpayton/MapleStory-Client` |
| 顯示名稱 | **HeavenClient** |
| 描述 | A custom client for HeavenMS |
| Stars / Forks | **243** / 96 |
| 創建 | 2015-10-13 |
| 最後 commit | 2026-02-25 |
| 預設 branch | master |
| 主語言 | C(API 為 C,實作為 C++) |
| License | AGPL-3.0 |
| Commit 總數(master) | 262 |
| Repo size | 28.8 MB |
| 大小(含 .git) | 55 MB(clone 後) |

---

## §1 4 個本地分支全部事實

| Branch | Commit 數 | 最早 commit | 最後 commit | 用途 |
|---|---:|---|---|---|
| **master** | **262** | 2015-10-13 | 2026-02-25 | **Windows PC 主線** |
| **linux** | 224 | 2015-10-13 | **2020-05-10** | Linux PC |
| **mac** | 131 | 2015-10-13 | **2019-11-04** | macOS |
| **v92-support** | 259 | 2015-10-13 | **2024-04-30** | **v92 server 相容**(不是 v83) |

**純事實**:
- 全部從同個 initial commit `b71da42 2015-10-13` 出發
- 4 個分支**初始 commit 都是 Daniel Allendorf 時代**
- master 是最活躍分支
- **v92-support** 比 master 少 3 commit,但**仍在 2024 活躍**(Audio fix)
- linux 在 2020-05 凍、mac 在 2019-11 凍、v92 在 2024-04 凍

### §1.1 commit 時間線

```
2015-10 ─┐ Initial commit (Daniel Allendorf 時代)
         │
2020-05 ─┤ Linux branch last activity
2019-11 ─┤ mac branch last activity
2023-04 ─┤ ryantpayton 重啟開發
2024-04 ─┤ master + v92 last activity
         │ (2 年低活動)
2026-02 ─┘ 突然 4 commit 復活 (README + NoLifeNx + NoLifeWzToNx 文件)
```

---

## §2 頂層結構事實

```
msc-repo/                                  (1,298 檔 / 55 MB)
├── Audio/                                 (2 個 .cpp/.h)
├── Character/                             (38 個檔 — 完整角色 + 庫存 + 外觀)
│   ├── Inventory/                         (12 個)
│   └── Look/                              (14 個)
├── Data/                                  (12 個)
├── Gameplay/                              (80 個)
│   ├── Combat/                            (24 個 — 戰鬥系統)
│   ├── MapleMap/                          (32 個 — 地圖/怪物/NPC/反應堆)
│   └── Physics/                           (4 個 — 物理 + 移動)
├── Graphics/                              (18 個)
├── IO/                                    (142 個 — UI + 元件 + UITypes)
│   ├── Components/                        (12 個 — 共用 UI 元件)
│   └── UITypes/                           (70+ 個 — 全部 UI 畫面)
├── Net/                                   (54 個 — 網路通訊)
│   ├── Packets/                           (12 個 .h 封包定義)
│   └── Handlers/                          (12 對 .cpp/.h + Helpers)
├── Template/                              (12 個 — Singleton/Point/TypeMap 等基底)
├── Util/                                  (12 個 — Misc/WzFiles/QuadTree 等)
├── fonts/Arial/                           (字體)
├── includes/                              (7 個 third-party)
│   ├── bass24/                            (BASS audio library)
│   ├── freetype/                          (字體渲染)
│   ├── glew-2.1.0/                        (OpenGL extension)
│   ├── glfw-3.3.2.bin.WIN32               (視窗管理 32-bit)
│   ├── glfw-3.3.2.bin.WIN64               (視窗管理 64-bit)
│   ├── NoLifeNx/                          (NX 格式解析)
│   └── stb/                               (圖片載入)
├── Configuration.{cpp,h}                  (全域設定)
├── Constants.h
├── Error.h
├── Icon.{ico,png}                         (圖示)
├── LICENSE                                (35 KB, AGPL-3.0)
├── MapleStory.cpp                         (主程式入口)
├── MapleStory.h
├── MapleStory.rc                          (Windows 資源)
├── MapleStory.sln                         (VS 方案檔)
├── MapleStory.vcxproj                     (VS 專案, 36 KB)
├── MapleStory.vcxproj.filters             (VS filter, 46 KB)
├── README.md                              (4 KB)
├── Timer.h
└── resource.h
```

---

## §3 自己寫的 C++ 統計(排除 includes/ 與 fonts/)

| 類型 | 數量 | 大小 |
|---|---:|---:|
| .cpp | **183** | 1,232 KB |
| .h | **239** | 646 KB |
| **合計** | **422** | **1,878 KB** (1.8 MB) |

### §3.1 15 個最大 .cpp

| 檔案 | 大小(bytes) | 模組 |
|---|---:|---|
| `IO/UITypes/UICommonCreation.cpp` | **44,583** | 角色創建 UI(共通) |
| `IO/UITypes/UIKeyConfig.cpp` | **39,120** | 鍵盤設定 |
| `IO/UITypes/UIChatBar.cpp` | 36,994 | 聊天列 |
| `IO/UITypes/UIStatusBar.cpp` | 33,160 | 狀態列 |
| `IO/UITypes/UIItemInventory.cpp` | 30,919 | 道具庫存 |
| `Graphics/GraphicsGL.cpp` | 29,000 | OpenGL 圖形後端 |
| `IO/UITypes/UICharSelect.cpp` | 28,071 | 角色選擇 |
| `IO/UITypes/UIMiniMap.cpp` | 26,439 | 小地圖 |
| `IO/Components/EquipTooltip.cpp` | 25,323 | 裝備提示 |
| `Net/PacketSwitch.cpp` | 24,400 | opcode dispatch |
| `IO/UITypes/UISkillBook.cpp` | 24,279 | 技能書 |
| `IO/UITypes/UIShop.cpp` | 21,405 | 商店 |
| `IO/UITypes/UIStatsInfo.cpp` | 20,640 | 屬性資訊 |
| `Character/Look/CharLook.cpp` | 19,119 | 角色外觀 |
| `IO/UITypes/UIWorldSelect.cpp` | 18,337 | 世界選擇 |

### §3.2 15 個最大 .h

| 檔案 | 大小(bytes) | 模組 |
|---|---:|---|
| `IO/UITypes/UIKeyConfig.h` | **15,159** | 鍵盤設定 |
| `Configuration.h` | **14,989** | 全域設定 |
| `Graphics/GraphicsGL.h` | 7,559 | OpenGL 圖形 |
| `IO/UITypes/UILoginNotice.h` | 7,338 | 登入提示 |
| `Util/QuadTree.h` | 6,802 | 四元樹(碰撞偵測) |
| `Character/Player.h` | 6,566 | 玩家 |
| `Util/WzFiles.h` | 6,537 | NX/WZ 檔案清單 |
| `Graphics/Color.h` | 6,526 | 顏色 |
| `Net/Packets/GameplayPackets.h` | 6,450 | 遊戲封包 |
| `Character/Char.h` | 6,160 | 角色基底 |
| `Graphics/DrawArgument.h` | 6,005 | 繪圖參數 |
| `Gameplay/MapleMap/Mob.h` | 5,616 | 怪物 |
| `Template/Point.h` | 5,458 | 座標 |
| `Character/Inventory/Inventory.h` | 5,427 | 庫存 |
| `IO/UITypes/UICommonCreation.h` | 5,422 | 角色創建 UI |

### §3.3 各目錄 C++ 檔案分佈

```
IO/          142 (UI 最多 — 70+ 個 UI 畫面)
Gameplay/     80 (戰鬥/地圖/物理)
Character/    72 (角色/庫存/外觀)
Net/          54 (網路/封包/handlers)
./             8 (Configuration/Constants/Error/MapleStory 主程式)
Graphics/     18 (OpenGL 後端)
Data/         12 (從 NX 載入資料)
Util/         12 (工具)
Template/     12 (基底)
Audio/         2 (音效)
```

---

## §4 建置配置(MSBuild/Visual Studio)

### §4.1 編譯環境需求

| 項目 | 版本 |
|---|---|
| IDE | Visual Studio 2026 Community(v18.2.1) |
| Windows SDK | 8.1 |
| Platform Toolset | v140 |
| C++ 標準 | C++17 |
| Build 系統 | MSBuild(`MapleStory.sln` + `MapleStory.vcxproj`) |

### §4.2 預設 define

從 `MapleStory.h`:
```cpp
// #define USE_ASIO            // 預設關
#define USE_CRYPTO               // 預設開
#define USE_NX                   // 預設開(讀 NX 而非 WZ)
```

### §4.3 Log level

```cpp
#define LOG_ERROR    1
#define LOG_WARN     2
#define LOG_INFO     3
#define LOG_DEBUG    4
#define LOG_NETWORK  5
#define LOG_UI       6
#define LOG_TRACE    7

#ifdef _DEBUG
    #define LOG_LEVEL LOG_DEBUG
#else
    #define LOG_LEVEL LOG_WARN
#endif
```

### §4.4 第三方庫(全在 includes/)

| 函式庫 | 用途 |
|---|---|
| **bass24** | BASS audio library(商業音效引擎) |
| **freetype** | 字體渲染 |
| **glew-2.1.0** | OpenGL extension loader |
| **glfw-3.3.2.bin.WIN32/64** | 視窗管理 + 輸入 |
| **NoLifeNx** | NX 格式解析(內建 .lib / .obj) |
| **stb** | 圖片載入(單一 header) |

---

## §5 Net 通訊結構

### §5.1 NetConstants.h

```cpp
namespace ms
{
    const size_t HEADER_LENGTH = 4;
    const size_t OPCODE_LENGTH = 2;
    const size_t MIN_PACKET_LENGTH = 6;     // HEADER + OPCODE
    const size_t MAX_PACKET_LENGTH = 131072; // 128 KB
}
```

**純事實**:與 OpenMapleClient 完全相同的通訊參數。

### §5.2 PacketSwitch 結構

```cpp
class PacketSwitch : public Forwarder
{
public:
    static constexpr size_t NUM_HANDLERS = 500;
    std::unique_ptr<PacketHandler> handlers[NUM_HANDLERS];
    
    template<size_t O, typename T, typename... Args>
    void emplace(Args&&... args)
    {
        static_assert(O < NUM_HANDLERS,
                      "PacketSwitch::emplace - Opcode out of array bounds");
        // ...
    }
};
```

**純事實**:
- `NUM_HANDLERS = 500`(opcode 上限 499)
- 編譯期 `static_assert` 阻擋 ≥500 的 opcode
- 與 OpenMapleClient 結構相同(但 OpenMapleClient 用 `std::array`,這裡用 C-style 陣列)

### §5.3 已註冊 handler 數量

從 `PacketSwitch.cpp` 計算 `emplace` 呼叫:**56 個**

**純事實**:
- 500 上限中**只用 56 個**(11.2%)
- 大量 opcode 是「unhandled」(會印「Unhandled packet detected」警告)

### §5.4 已實作的 handler(56 個)

從 PacketSwitch.cpp 完整抽出:
```
PING, LOGIN_RESULT, SERVERSTATUS, SELECT_CHARACTER_BY_VAC, SERVERLIST, CHARLIST,
SERVER_IP, CHARNAME_RESPONSE, ADD_NEWCHAR_ENTRY, DELCHAR_RESPONSE, SET_FIELD,
SPAWN_CHAR, CHAR_MOVED, UPDATE_CHARLOOK, SHOW_FOREIGN_EFFECT, REMOVE_CHAR,
SPAWN_PET, SPAWN_NPC, SPAWN_NPC_C, SPAWN_MOB, SPAWN_MOB_C, MOB_MOVED,
SHOW_MOB_HP, KILL_MOB, DROP_LOOT, REMOVE_LOOT, HIT_REACTOR, SPAWN_REACTOR,
REMOVE_REACTOR, ATTACKED_CLOSE, ATTACKED_RANGED, ATTACKED_MAGIC, CHANGE_CHANNEL,
KEYMAP, SKILL_MACROS, CHANGE_STATS, GIVE_BUFF, CANCEL_BUFF, RECALCULATE_STATS,
UPDATE_SKILL, ADD_COOLDOWN, SHOW_STATUS_INFO, CHAT_RECEIVED, SCROLL_RESULT,
SERVER_MESSAGE, WEEK_EVENT_MESSAGE, SHOW_ITEM_GAIN_INCHAT, MODIFY_INVENTORY,
GATHER_RESULT, SORT_RESULT, ...(共 56 個)
```

### §5.5 Net/Packets/ 與 Net/Handlers/

**12 個 Packets(全部 .h)**:
- AttackAndSkillPackets / CharCreationPackets / CommonPackets
- GameplayPackets / InventoryPackets / LoginPackets
- MessagingPackets / MovementPacket / NpcInteractionPackets
- PlayerInteractionPackets / PlayerPackets / SelectCharPackets

**12 對 Handlers**:
- Attack / CashShop / Common / Inventory / Login
- MapObject / Messaging / NpcInteraction / Player / PlayerInteraction
- SetField / Testing

**事實**:有 `CashShopHandlers.{cpp,h}` — 對應 v83 商城功能。

---

## §6 遊戲檔(28 個 .wz)

從 `Util/WzFiles.h` 抽出(僅 `#ifndef USE_NX`):

```cpp
constexpr uint8_t NUM_FILES = 28;
constexpr std::array<const char*, NUM_FILES> filenames =
{
    "Base.wz",
    "Character.wz",
    "Effect.wz",
    "Etc.wz",
    "Item.wz",
    "Map.wz",
    "Map001.wz", "Map002.wz", "Map2.wz",       // Map 系列 4 個
    "Mob.wz",
    "Mob001.wz", "Mob002.wz", "Mob2.wz",       // Mob 系列 4 個
    "Morph.wz",
    "Npc.wz",
    "Quest.wz",
    "Reactor.wz",
    "Skill.wz",
    "Skill001.wz", "Skill002.wz", "Skill003.wz", // Skill 系列 4 個
    "Sound.wz",
    "Sound001.wz", "Sound002.wz", "Sound2.wz",   // Sound 系列 4 個
    "String.wz",
    "TamingMob.wz",
    "UI.wz"
};
```

**純事實**:
- **28 個 .wz 檔**(= 韓版地圖/怪物/技能/音效分檔)
- **4 個系列各有 4 個**:Map / Mob / Skill / Sound(基本 .wz + 001 + 002 + 2)
- 對應韓版客戶端結構(因為 JourneyClient 是韓版起源)
- **Data.wz 不在清單**(NoLifeWzToNx 也警告 Data.wz 不是標準 WZ)

**對應你的 GMS v83**:
- GMS v83 通常沒有 `Map001/002/2.wz`(只有 Map.wz)
- **GMS v83 客戶端不能直接用 HeavenClient 預期清單** — 必須用 `itayzrihan/MapleStory-Client-Cosmic` 那種 fork

---

## §7 Configuration.h 主要設定介面

從 `Configuration.h` API:

```cpp
class Configuration : public Singleton<Configuration>
{
public:
    bool get_show_fps() const;
    bool get_show_packets() const;        // 顯示封包內容(debug 用)
    bool get_auto_login() const;
    uint8_t get_auto_world();
    uint8_t get_auto_channel();
    std::string get_auto_acc();
    std::string get_auto_pass();
    std::string get_auto_pic();
    int32_t get_auto_cid();
    std::string get_title() const;
    std::string get_version() const;
    std::string get_login_music() const;
    std::string get_login_music_sea() const;
    std::string get_login_music_newtro() const;
    std::string get_joinlink() const;
    std::string get_website() const;
    std::string get_findid() const;
    std::string get_findpass() const;
    std::string get_resetpic() const;
    std::string get_chargenx() const;
    void set_macs(char* macs);
    void set_hwid(char* hwid, char* volumeSerialNumber);
    void set_max_width(int16_t);
    void set_max_height(int16_t);
    std::string get_macs();
    std::string get_hwid();
    std::string get_vol_serial_num();
    int16_t get_max_width();
    int16_t get_max_height();
    bool get_rightclicksell();
    void set_rightclicksell(bool);
    bool get_show_weekly();
    void set_show_weekly(bool);
    bool get_start_shown();
    void set_start_shown(bool);
    uint8_t get_worldid();
    void set_worldid(uint8_t);
    uint8_t get_channelid();
    void set_channelid(uint8_t);
    bool get_admin();
    // ...
};
```

**純事實**:
- 自動登入(AUTO_LOGIN/AUTO_WORLD/AUTO_CHANNEL/AUTO_ACC/AUTO_PASS/AUTO_PIC/AUTO_CID)
- MACS + HWID + Volume Serial(對應 GMS 反外掛 HWID 機制)
- RightClickSell(商店右鍵賣)
- WeekEventMessage(楓之谷週年訊息)

---

## §8 與 OpenMapleClient 的程式碼層差異

兩者都是 JourneyClient 同源(由 commit `b71da42 2015-10-13` 出發),**結構幾乎一致**,但有差異:

| 差異點 | HeavenClient (master) | OpenMapleClient |
|---|---|---|
| 平台 | **Windows PC(主)+ Linux/mac 分支** | **Android(主)+ PC** |
| 建置 | **MSBuild / .sln / .vcxproj** | **Gradle / CMake** |
| 第三方依賴 | **直接放在 includes/(bass24, glew, glfw)** | thirdparty/ 子目錄(submodule) |
| 預設視窗尺寸 | `Configuration::set_max_width/height`(從 Settings 讀) | 1366 × 768 寫死 |
| Settings 檔案 | 自動生成,持久化 | 沒有 |
| 配置 UI | 完整 `UIKeyConfig`(39 KB)+ `UIOptionMenu` | 沒實作 |
| FX Pipeline | OpenGL 純 C++ | OpenGL ES via glfm(Android) |
| 維護狀態 | 2026-02 仍活躍 | 2024-05 停 |
| 對應 server | v83 + v229.2(預設 v229.2) | v83 + MapleServerAndroid |

### §8.1 Configuration.h 預設值差異(從原始碼)

從兩個 repo 的 `Configuration.cpp` 對比(都用 `Configuration.cpp/h`,但內容有差異):

| 設定 | HeavenClient | OpenMapleClient |
|---|---|---|
| TITLE | "MapleStory"(從 .h) | "MapleStory" |
| VERSION | "229.2" | "083" |
| WEBSITE | "https://www.nexon.com" | "https://www.nexon.com" |
| FINDID | "https://www.nexon.com/account/..." | ? |
| FINDPASS | "https://www.nexon.com/account/..." | ? |
| JOINLINK | (對應 server IP) | (對應 server IP) |
| MAXWIDTH/MAXHEIGHT | 1366 / 768 | 1366 / 768 |

**純事實**:**VERSION 不同**(229.2 vs 083)— 這是兩個 fork 最大差別。

---

## §9 4 個分支差異詳細

### §9.1 master vs linux

| 統計 | 值 |
|---|---|
| 變動檔數 | **1090** |
| 新增行數 | +35,010 |
| 刪除行數 | -75,620 |

主要改動:
- `includes/NoLifeNx/nlnx/` 改為 `includes/nlnx/`(簡化路徑)
- 升級 NoLifeNx 為新版本(對應 Linux .so 編譯)
- 加入 `stb_vorbis.c`(for audio)

### §9.2 master vs mac

| 統計 | 值 |
|---|---|
| 變動檔數 | **1310** |
| 新增行數 | +19,416 |
| 刪除行數 | -185,545 |

主要改動:
- `stb/` 全部替換(從 master 早期版本升級)
- 移除大量 Visual Studio 專案檔(因為 mac 用 Xcode)
- 大量 visual studio obj 移除

### §9.3 master vs v92-support

| 統計 | 值 |
|---|---|
| 變動檔數 | 47 |
| 新增行數 | +89 |
| 刪除行數 | -166 |

主要改動:
- 移除 NoLifeNx 編譯產物(因為 v92 編譯時動態生成)
- 微調 Audio handler

**結論(純技術)**:
- **linux/mac 分支差異主要在 third-party 函式庫版本與編譯產物**,code 本身差異不大
- **v92-support 差異極小** — 主要針對 audio

---

## §10 LICENSE 條款事實

`LICENSE`(35,182 bytes = AGPL-3.0 全文):

```
GNU AFFERO GENERAL PUBLIC LICENSE
Version 3, 19 November 2007

Copyright (C) 2007 Free Software Foundation, Inc.
```

**LICENSE 警告**:
- **AGPL-3.0** 是**最嚴格開源許可證**
- 若 fork 出來**提供網路服務**,必須**也開源**整個衍生作品
- 包含 NoLifeNx(AGPL-3.0)、NoLifeWzToNx(AGPL-3.0)
- BASS audio library **是商業授權**(bass24)
- stb 是 public domain / MIT

---

## §11 主線時序(2015-2026)

### §11.1 2015-10 ~ 2019(Daniel Allendorf 時期)

- 2015-10-13:`b71da42` Initial commit(Daniel Allendorf 原始)
- 2015-10 ~ 2019:Revision 1 ~ 6(快速迭代)
- 2019-11-04:mac port 由 ryantpayton 加入
- 2019:Daniel Allendorf 停止維護

### §11.2 2019 ~ 2020(ryantpayton 接手)

- 2020-05-10:linux 最後 commit(a359863 「Linux improvements」)
- 2020:COVID 開始,開發節奏放慢

### §11.3 2020 ~ 2023(低活動)

- 2-3 年低活動
- 沒有顯著 commit

### §11.4 2023-04(ryantpayton 重啟)

- 2023-04-21 ~ 2023-04-24:**3 週密集 commit**(約 5-10 commit)
  - Fixed general map issues
  - Added equipment rule for Magician and Warrior
  - Handled player.message() from server
  - Added better logging for Opcodes
  - Fixed issue where character is nude when no equips
  - General UI positioning fixes

### §11.5 2024(穩定)

- 2024-03-18:Fixed typo + Updated links
- 2024-04-21:Bug fixes
- 2024-04-30:v92-support branch last commit(Fixes for audio)

### §11.6 2024-04 ~ 2026-02(沉默 2 年)

- 沒有顯著 commit

### §11.7 2026-02(突然復活)

- 2026-02-09 11:03:43:**Fixed wrong name for NoLifeWzToNx file**(56812b6)
- 2026-02-09 11:04:05:Merge branch 'master' of HeavenClient(5b1eb4c)
- 2026-02-09 17:35:45:Update NoLifeNx libs(同 NoLifeWzToNx 新版本)
- 2026-02-09 17:43:42:**Update README: VS 2026, v229.2**(9dfa3dc)
- 2026-02-25 17:28:44:**Add Web compatibility information to README**(cbb0fe2)

**純事實**:
- 2026-02-09 一個小時內 4 個 commit
- 配合 `ryantpayton/NoLifeWzToNx` repo 2026-02 同步上線
- README 升級:**VS 2026**(從舊版升到 2026 社區版)、**v229.2**(對應 server 升級)

---

## §12 純事實總結(不下結論)

### §12.1 結構規模

- **422 個 C++ 檔(1.8 MB 自己寫的)**
- **包含 7 個 third-party 函式庫**(全部 in-tree)
- **56 個 opcode 已處理(500 上限中佔 11.2%)**
- **28 個遊戲檔需求(.wz 模式)/ 15 個(.nx 模式)**
- **VS 2026 Community v18.2.1 + Windows SDK 8.1 + Platform Toolset v140**

### §12.2 4 個分支時序

- master 2026-02(活躍)/ linux 2020-05(凍)/ mac 2019-11(凍)/ v92-support 2024-04(凍)
- 全部從 2015-10-13 initial commit 出發
- v92-support 與 master 高度相似(只差 3 commit)

### §12.3 與 OpenMapleClient 的關係

- **同源 JourneyClient**(Daniel Allendorf 2015-2019)
- **HeavenClient 為 Windows PC 主線**(ryantpayton 維護)
- **OpenMapleClient 為 Android wrapper**(speedyHKjournalist 維護)
- **兩個 fork 的 Configuration.cpp 不一樣**(VERSION 不同)
- **兩個 fork 的 Net/ 結構完全相同**(同一份 Cryptography / PacketSwitch / Session)

### §12.4 對 GMS v83 + Cosmic 的事實

- **預設不直接給 GMS v83 + Cosmic**:
  - VERSION = "229.2"
  - 28 個 .wz 是韓版
- **需要使用 `itayzrihan/MapleStory-Client-Cosmic` fork**(專門給 v83 + Cosmic)
- **NoLifeWzToNx 工具可把 GMS v83 WZ 轉 NX**(但只支援 v83,不是韓版 28 個清單)
- **Configuration::VERSION 改成 "083" + 28 個 .wz 換成 GMS v83 16 個** = 改造成 GMS v83 client

### §12.5 不做的事(刻意)

- ❌ 不評論 HeavenClient 與其他 client 哪個好
- ❌ 不評論整合方案
- ❌ 不評論法律風險
- ❌ 不評論 AGPL-3.0 對實際部署的限制
- ❌ 不評論 BASS 商業授權問題

---

## §13 本地獨立位置

**此分析對應的本地 repo**:
```
C:\Users\e7896\AppData\Local\hermes\cache\scratch\maple-story-client-isolated\
├── msc-repo/                    (完整 git repo, 4 個分支)
│   ├── .git/
│   ├── Audio/
│   ├── Character/
│   ├── Data/
│   ├── Gameplay/
│   ├── Graphics/
│   ├── IO/
│   ├── Net/
│   ├── Template/
│   ├── Util/
│   ├── fonts/
│   ├── includes/
│   ├── Configuration.cpp/.h
│   ├── Constants.h
│   ├── Error.h
│   ├── Icon.{ico,png}
│   ├── LICENSE
│   ├── MapleStory.{cpp,h,rc,sln,vcxproj,filters}
│   ├── README.md
│   ├── Timer.h
│   └── resource.h
├── repo.json                    (GitHub API metadata)
└── W3-2-MapleStory-Client-isolated-analysis.md  (本報告本地副本)
```

**獨立原則**:
- 此資料夾**沒有污染** `12-OffShelf-Client-Fork/`(本地其它項目位置)
- 也不在 `MUWORK\GAME\MAPLESOTRY\`(工作區)
- 完全在 **scratch** 隔離區

---

**輸出位置**:
- 主索引: `C:\MUWORK\GAME\MAPLESOTRY\wf-output\W3-2-MapleStory-Client-isolated-analysis.md`
- 本地副本: `C:\Users\e7896\AppData\Local\hermes\cache\scratch\maple-story-client-isolated\W3-2-MapleStory-Client-isolated-analysis.md`
