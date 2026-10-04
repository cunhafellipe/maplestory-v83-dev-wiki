# 40-protocol — MapleStory v83 Protocol

> **目的**:從 v83 client 角度整理已知 protocol(opcode / handler / packet 結構)

## 4 個核心 Packet Dispatcher

| Dispatcher | 地址 | opcode 範圍 | 用途 |
|---|---|---|---|
| `CLogin::OnPacket` | `0x5F80FF` | 0~28 | 登入、選角、連線 |
| `CField::OnPacket` | `0x531325` | 125~345 | 遊戲內(戰鬥、NPC、聊天)|
| `CWvsContext::OnPacket` | `0xA07A08` | 29~124 | 世界(道具、技能、好友)|
| `CStage::OnPacket` | `0x644446` | 128~130 | 階段切換(選角→世界、商城)|

!!! note "CWvsContext 的範圍更正"
    先前此處寫作 `29~62`。實際指令碼為 `add eax, -29` 後接
    `cmp eax, 0x5f` (95),再由 `jmp dword ptr [eax*4 + 0x00A07E8E]` 查表。
    該表自 opcode 29 起有 **96 個連續有效項**,故真實範圍是 **29~124**。
    `62` 只是文件中已列出 handler 的那一段,不是範圍上限。
    驗證腳本 `check_opcode_bounds()` 會重算此值。

完整 pseudocode 見 [10-client-analysis/v83-idb/decompiles.md](../10-client-analysis/v83-idb/decompiles.md)

## CLogin::OnPacket opcode 表

| Opcode | Handler | 推測用途 |
|---|---|---|
| 0 | `sub_5F83EE` | 帳號驗證結果(包含 ban message)|
| 1 | `sub_5F8F27` | 角色列表 |
| 2 | `sub_5F92DF` | 角色資訊 |
| 3 | `sub_5F92AE` | 角色選擇結果 |
| 4 | `sub_5FC731` | 伺服器列表 |
| 5 | `sub_5FC838` | 世界資訊 |
| 6 | `sub_5FC89D` | 頻道資訊 |
| 7 | `sub_5FCBC1` | IP 配置 |
| 8 | `sub_5FACCA` | 帳號建立 |
| 9 | `sub_5FB245` | 帳號刪除 |
| 10 | `sub_5F95B7` | 檢查 pincode |
| 11 | `sub_5F9891` | pincode 結果 |
| 12 | `sub_5FB541` | 性別變更 |
| 13 | `sub_5F9C72` | 推薦禮物 |
| 14 | `sub_5FA26C` | 道具訊息 |
| 15 | `sub_5F9D15` | 道具結果 |
| 22 | `sub_5FB83D` | 角色資料 |
| 23 | `sub_5FB950` | 選單 |
| 26 | `sub_5F82F4` | 錯誤 |
| 27 | `sub_5F8340` | 連線狀態 |
| 28 | `sub_5FBA49` | 結束 |
| 125~127 | `sub_775FE6` | 範圍 |
| 128~130 | `CStage::OnPacket` | 轉給 stage |

## CField::OnPacket opcode 表(部分)

| Opcode | Handler |
|---|---|
| 0x7D (125) | (range) |
| 0x80 (128) | → `CStage::OnPacket` |
| 0x82 (130) | → `CStage::OnPacket` |
| 0x97 (151) | (range 160-235) |
| 0xEC (236) | (range 236-256) |
| 0x101 (257) | (range 257-264) |
| 0x109 (265) | (range 265-267) |
| 0x12F (303) | `sub_53347C` |
| 0x130 (304) | `sub_7465F4` |
| 0x135 (309) | `sub_7C8A4C` |
| 0x138 (312) | `sub_73FFF1` |
| 0x139 (313) | `sub_8511FC` |
| 0x13A (314) | `sub_65DF4C` |
| 0x142 (322) | `sub_6F56EA` |

詳見 `wf-analysis/W1-2-opcode-collision.md`

## CWvsContext::OnPacket opcode 表

| Opcode | Handler |
|---|---|
| 0x1D (29) | `sub_A1EAD9` |
| 0x1E (30) | `sub_A1F881` |
| 0x1F (31) | `sub_A1FB52` |
| 0x20 (32) | `sub_A202BE` |
| 0x21 (33) | `sub_A2071F` |
| 0x22 (34) | `sub_A208FF` |
| 0x23 (35) | `sub_A2091C` |
| 0x24 (36) | `sub_A1E48C` |
| 0x25 (37) | `sub_A209B2` |
| 0x26 (38) | `sub_A223DC` |
| 0x27 (39) | `sub_A209D4` |
| 0x28 (40) | `sub_A20AC0` |
| 0x29 (41) | `sub_A2508B` |
| 0x2A (42) | `sub_A25268` |
| 0x2B (43) | `sub_A265C2` |
| 0x2D (45) | `sub_A27891` |
| 0x2E (46) | `sub_A27B38` |
| 0x2F (47) | `sub_A27B61` |
| 0x30 (48) | `sub_A29115` |
| 0x31 (49) | `sub_A26D44` |
| 0x32 (50) | `sub_A27D75` |
| 0x33 (51) | `sub_A1E5AF` |
| 0x34 (52) | `sub_A1E943` |
| 0x35 (53) | `sub_A1E96D` |
| 0x37 (55) | `sub_A29739` |
| 0x39 (57) | `sub_A23D92` |
| 0x3A (58) | `sub_A23D79` |
| 0x3B (59) | `sub_A1233F` |
| 0x3D (61) | `sub_A2370B` |
| 0x3E (62) | `sub_A3E31C` |

## 工具 / 已知結構

### CInPacket(客戶端接收)

- `CInPacket::Decode1` (0x4065F3) — 讀 1 byte
- `CInPacket::Decode2` (0x42470C) — 讀 2 bytes (short)
- `CInPacket::Decode4` (0x406629) — 讀 4 bytes (int)
- `CInPacket::DecodeBuffer` (0x432257) — 讀 buffer
- `CinPacket::DecodeStr` (0x46F30C) — 讀 string

### Encode side
- 沒找到 named Encode 方法,但通常在 CClientSocket::SendPacket 內呼叫 COutPacket methods

## 參考資料

- [10-client-analysis/v83-idb/decompiles.md](../10-client-analysis/v83-idb/decompiles.md) — 完整 pseudocode
- [wf-output/W1-2-opcode-collision.md](../10-client-analysis/wf-analysis/W1-2-opcode-collision.md) — opcode 衝突檢查
- [HeavenMS source](https://github.com/ronancpl/HeavenMS) — server 端實作對照
