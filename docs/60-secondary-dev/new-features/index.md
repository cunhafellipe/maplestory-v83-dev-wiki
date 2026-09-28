# 新功能 — 如何加新功能到 v83 Client

> **目的**:從「無到有」加新功能到 MapleStory v83 client 的完整流程
>
> **重要**:v83 是 14 年前的 client,新功能要符合 v83 protocol + v83 server 端支援,不能直接搬 v200+ 的功能

## 加新功能的三層架構

```
新功能 = Client UI + Client Logic + Server Logic + WZ 資料

需要改的層:
1. WZ 檔 (UI.wz, Map.wz, etc.)     ← 新視覺
2. Client EXE (C++ via IDB)         ← UI 行為
3. Server (Java via Cosmic)         ← packet 處理
4. Database (MySQL via Cosmic)      ← 持久化
```

## 範例:加一個「自訂裝備欄位」(假設情境)

### 步驟

#### 1. 規劃
- 欄位名稱:Shoulder(肩膀,從 v100 學來)
- 視覺位置:披風右邊
- 道具類型 ID:0115xxxx(戒指 4 是 0114)

#### 2. Server 端(Cosmic)

在 `MapleInventoryType.java` 加新 type:
```java
public enum MapleInventoryType {
    UNDEFINED(0), EQUIP(1), USE(2), SETUP(3), ETC(4), CASH(5),
    SHOULDER(100, 96);  // 新增
    // ...
}
```

在 `Item.java` 加判斷:
```java
public static boolean isShoulder(int itemId) {
    return itemId / 10000 == 115;
}
```

#### 3. WZ 端(UI.wz)

在 `UI/UIWindow.img/Equip/backgrnd` 加新 slot
- 用 HaRepacker 編輯 UI.wz
- 加新背景圖層
- 設定新 slot 的坐標

#### 4. Client 端(IDB / Patch)

- Patch `CUIEquip::OnCreate` 加新 slot 的 render 邏輯
- Patch `CItemInfo::RegisterEquipItemInfo` 加 isShoulder 判斷
- 改 `CUIToolTip::SetToolTip_Equip` 加 Shoulder 道具描述

### 步驟總結

```
1. 規劃(欄位名 / 類型 / 位置)
2. Server 端加 enum + 邏輯
3. WZ 加新視覺
4. Client 端 patch UI render + tooltip
5. 測試 client + server 互通
6. 文件化
```

## 範例:加一個「自訂 Packet」

假設要加一個 client→server packet `OP_NEW_FUNCTION`(opcode 0x9999):

### 1. Server 端

在 `RecvOpcode.java`:
```java
public static final RecvOpcode NEW_FUNCTION = new RecvOpcode(0x9999);
```

在 `PacketHandler.java`:
```java
handlers[0x9999] = new HandleNewFunction();
```

### 2. Client 端

在 client 加 send packet 邏輯:
```c
COutPacket packet(0x9999);
// ... 填資料
CClientSocket::SendPacket(packet);
```

要 patch 的位置:
- `CClientSocket::SendPacket` 或類似
- 新 UI 按鈕的 onClick handler

### 3. 測試

- 連 local server (Cosmic)
- 點新 UI 按鈕
- 觀察 server log 是否收到 opcode 0x9999
- 驗證 server 邏輯跑通

## 工具建議

| 工具 | 用途 |
|---|---|
| **kaentake** | DLL hook,加新功能不需 patch EXE |
| **IDA Pro + idat.exe** | 找 hook point + decompile |
| **ida-pro-mcp** | AI 自動分析(這次裝好的工具)|
| **Cosmic source** | Server 端參考實作 |
| **WZ Mod Tool Suite** | 改 WZ |

## 注意事項

- v83 protocol opcode 空間有限(0x0000 ~ 0xFFFF),新功能 opcode 不要衝突
- client 改太多會被 GM detect(若連官方)
- server + client 一定要同步改,不然會 disconnect
- 加新功能要對應 OPCode + RecvPacketEncoder + PacketHandler

## 參考資料

- [W1-2-opcode-collision.md](../../10-client-analysis/wf-analysis/W1-2-opcode-collision.md) — v83 opcode 衝突檢查
- [Cosmic source](**Cosmic** (本機 clone 在 `04-Emulators/GMS-v083-Cosmic/`)) — Server 端實作參考
- [W3-1-HeavenClient-4-platforms-deep-dive.md](../../10-client-analysis/wf-analysis/W3-1-HeavenClient-4-platforms-deep-dive.md) — C++ client 開發指南
