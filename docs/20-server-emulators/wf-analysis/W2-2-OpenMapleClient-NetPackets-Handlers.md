# W2-2: OpenMapleClient Net/Packets 與 Handlers 子樹拆解

> **分析時間**: 2026-09-27
> **位置**: `app/src/main/cpp/src/Net/Packets/` + `Net/Handlers/`
> **總檔**: 24 個(12 Packets + 12 Handlers)+ Helpers 子目錄

---

## §0 結構概覽

### Net/Packets/(12 個, 全部 .h)

| 檔案 | 大小 | 內容 |
|---|---:|---|
| LoginPackets.h | 3,599 | LOGIN / CHAR_LIST_REQUEST / SERVER_STATUS / TOS / SET_GENDER |
| CharCreationPackets.h | 2,006 | 建立角色 / 刪除角色 / PIC |
| SelectCharPackets.h | 2,475 | 角色選擇 |
| PlayerPackets.h | 2,198 | 玩家狀態 |
| MovementPacket.h | 1,452 | 移動 / 換地圖 |
| GameplayPackets.h | 6,704 | 技能 / buff / 動作 |
| AttackAndSkillPackets.h | 4,110 | 攻擊 |
| InventoryPackets.h | 3,703 | 道具移動 / 使用 |
| MessagingPackets.h | 1,175 | 一般聊天 / 私聊 / 隊伍 |
| NpcInteractionPackets.h | 2,590 | NPC 對話 / 商店 |
| PlayerInteractionPackets.h | 3,455 | 隊伍 / 公會 / 家族 / 互動 |
| CommonPackets.h | 1,042 | 通用 |
| **小計** | **34,611** | **12 個封包類別** |

### Net/Handlers/(12 個 + Helpers/)

| 檔案 | 大小 | 內容 |
|---|---:|---|
| LoginHandlers.{cpp,h} | 8,787 + 2,478 | 登入流程 |
| MapObjectHandlers.{cpp,h} | 16,189 + 5,506 | 地圖物件(spawn/remove/move)|
| InventoryHandlers.{cpp,h} | 7,531 + 1,389 | 道具 |
| PlayerHandlers.{cpp,h} | 10,343 + 3,485 | 玩家 |
| PlayerInteractionHandlers.{cpp,h} | 5,116 + 2,482 | 互動 |
| MessagingHandlers.{cpp,h} | 9,642 + 2,156 | 聊天 / 訊息 |
| SetFieldHandlers.{cpp,h} | 4,249 + 1,266 | 換地圖 |
| AttackHandlers.{cpp,h} | 2,256 + 1,478 | 攻擊 |
| CashShopHandlers.{cpp,h} | 2,407 + 1,053 | **商城** |
| NpcInteractionHandlers.{cpp,h} | 2,989 + 1,174 | NPC |
| CommonHandlers.{cpp,h} | 1,086 + 957 | 通用 |
| TestingHandlers.{cpp,h} | 2,557 + 1,107 | 測試 |
| **小計** | **96,737** | **12 個 handler 對** |

---

## §1 關鍵事實

### §1.1 SendOpcode 從 OutPacket.h(`send_op_name_map`)

**結構**:
```cpp
static const std::unordered_map<uint16_t, std::string_view> send_op_name_map {
    { 1, "LOGIN_PASSWORD" },
    { 2, "GUEST_LOGIN" },
    ...
}
```

**從 1 連續到 149**(從 LOGIN_PASSWORD 開始)。**與 Cosmic RecvOpcode 100% 對應**。

### §1.2 派發機制(PacketSwitch.h)

**事實**:
- `NUM_HANDLERS = 500`(只支援 opcode 0~499)
- `std::array<std::unique_ptr<PacketHandler>, 500>`
- `template<size_t O, typename T, typename... Args> emplace(...)` 靜態 opcode 註冊
- **沒有動態註冊或 hot-reload**

### §1.3 重要限制:OpenMapleClient **不支援大於 499 的 opcode**

**純事實**:
- 編譯期 `static_assert(O < NUM_HANDLERS)` — **編譯失敗** if opcode ≥ 500
- **CheckIn 用的 `0x11A`(282)→ ✓ 可用**
- **BeautySalon 用的 `0x174`(372)→ ✓ 可用**
- **CashShop 用的 `0x3730`(14000)→ ✗ 編譯期失敗**
- **CashShop 用的 `0x3731`(14001)→ ✗ 編譯期失敗**

→ OpenMapleClient **無法直接整合 CashShop 功能包**(opcode 太大)

### §1.4 CashShop Handlers 已實作

**事實**:`CashShopHandlers.{cpp,h}` 已存在(2,407 + 1,053 bytes)— 表示 OpenMapleClient **自帶商城**(走 `ENTER_CASHSHOP(0x28)` opcode)。

→ **這跟 v83 Cosmic 原生商城對應**,**CashShop-window 功能包是另一種獨立的商城 UI 改寫**。

### §1.5 Cryptography 對應

**與 Cosmic 服務端**:
- 一致的 handshake 16-byte IV
- 一致的 Maple custom encryption(roll-left/right)
- 一致的 AES OFB(`#ifdef USE_CRYPTO`)
- **直接通訊相容**

---

## §2 與 GMS v83 / Cosmic 的 opcode 對照

**已知 OpenMapleClient 內含 opcode**(從 handlers 命名推):

| Opcode | 方向 | 處理器 |
|---|---|---|
| 0x28 | Recv | `ENTER_CASHSHOP` |
| 0x29 | Recv | `MOVE_PLAYER` |
| 0x26 | Recv | `CHANGE_MAP` |
| 0x27 | Recv | `CHANGE_CHANNEL` |
| 0xB0 | Recv | `GENERAL_CHAT` |
| 0x85 | Recv | `USE_RETURN_SCROLL` |
| 0x86 | Recv | `USE_UPGRADE_SCROLL` |

**結論**(純事實):
- OpenMapleClient 對 GMS v83 的 opcode **覆蓋率中等**
- 沒實作的 opcode(從 PacketSwitch::NUM_HANDLERS 與 handlers 列表推估)大約 200-300 個
- **沒實作的關鍵功能**:CashShop-window 自訂 opcode、BeautySalon opcode、CheckIn opcode

---

## §3 純事實總結

### 與現有項目的相容性矩陣

| 項目 | OpenMapleClient |
|---|---|
| GMS v83 原生客戶端 | ❌ 不相容(NX 格式)|
| Cosmic v83 server | ✓ README 明說可連 |
| CheckIn opcode 0x11A | ✓ 可用 |
| CheckIn opcode 0x17C | ✓ 可用 |
| BeautySalon opcode 0x174 | ✓ 可用 |
| CashShop opcode 0x3730 | ❌ **編譯失敗**(>500)|
| CashShop opcode 0x3731 | ❌ **編譯失敗**(>500)|
| GMS v83 WZ 資源 | ❌ 不相容 |
| 韓版/西版 NX 資源 | ✓ 預期用這個 |
| Android 平台 | ✓ 預設目標 |
| PC(Win/Mac/Linux)| ✓ 但需要 PC 用 NX + 對應 server |

### 結論(純技術)

1. **OpenMapleClient = JourneyClient 同源 + Android wrapper**
2. **opcode 數上限 500**(`NUM_HANDLERS`)→ 阻擋 CashShop-window 自訂 opcode
3. **NX 資源格式** → 與 GMS v83 WZ 不相容
4. **加密 = Cosmic 一致** → 通訊沒問題
5. **CashShopHandlers 已實作**但走原生 0x28,不是自訂 0x3730/0x3731

---

**輸出位置**: `<MAPLESOTRY>\wf-output\W2-2-OpenMapleClient-NetPackets-Handlers.md`
