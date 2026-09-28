# 60-secondary-dev — 二次開發指南

> **目的**:給「想改 MapleStory v83 client」的人一份快速入門指南

## 兩種改 client 的方式

### 方式 A:Patch EXE (改主程序)

適用場景:
- 改 UI 行為(開啟/關閉視窗的條件)
- 改 ToolTip 顯示邏輯
- 改 Packet handler(新增 opcode)
- Bypass 限制(等級、技能點、寵物等級)

工具:
- **kaentake** (C++ Detours hook client)— 不需改 EXE,DLL 注入
- **OllyDbg / IDA Pro 直接 patch** — 需要 decompile + understand logic
- **WZ Mod Tool Suite** — 改 WZ 檔(視覺層)

### 方式 B:Hook / DLL 注入(不改主程序)

適用場景:
- 加外掛功能
- Hook socket 攔截 packet
- 動態注入 UI 修改

工具:
- **kaentake** (推薦)— 現成的 C++ 框架
- **MapleEzorsia v83** — DLL 注入 + HD resolution patch

## 子章節

- [Patches](patches/index.md) — 常見的 client patch 範例
- [新功能](new-features/index.md) — 如何加新功能(packet handler / UI 視窗)

## 完整的改 client 工作流程

```
1. 確認要改什麼
   ├─ 改 UI 視覺 → 改 UI.wz (HaRepacker)
   ├─ 改 UI 行為 → patch EXE (kaentake 或 IDA 直接改)
   ├─ 改 packet → packet opcode dispatch (CLogin/CField/CWvsContext OnPacket)
   └─ 加新功能 → 全部都要改(server + client + WZ)

2. 取得工具
   ├─ 逆向用:IDA Pro 9.3 + idat.exe + ida-pro-mcp
   ├─ WZ 編輯:HaRepacker 4.2.4 + WZ Mod Tool Suite
   ├─ patch 用:kaentake + OllyDbg
   └─ Hook:kaentake + DLL injection

3. 測試流程
   ├─ 載 IDB 看 pseudocode
   ├─ 寫 patch 程式碼
   ├─ 載入 v83 client 測試
   ├─ 連到 local server (Cosmic / HeavenMS)
   └─ 驗證效果
```

## 對應的 v83.idb 知識

| 想做的事 | 用什麼 IDB 資料 |
|---|---|
| 找某 UI 視窗的 handler | [10-client-analysis/v83-idb/strings.md](../10-client-analysis/v83-idb/strings.md) |
| 找某 opcode 的處理器 | [10-client-analysis/v83-idb/decompiles.md](../10-client-analysis/v83-idb/decompiles.md) — 4 個 OnPacket dispatcher |
| 找某 string 的 xref | [10-client-analysis/v83-idb/historical-renames.md](../10-client-analysis/v83-idb/historical-renames.md) — 5 個重點 strings |
| 找某 class method | [10-client-analysis/v83-idb/class-methods.md](../10-client-analysis/v83-idb/class-methods.md) — 10 個已知 methods |

## 對應的 Wiki 章節

- [UI Classes](../30-ui-classes/index.md) — 改 UI 用
- [Tools](../50-tools/index.md) — kaentake + WZ Mod Tool
- [Protocol](../40-protocol/index.md) — 改 packet 用
- [Server Emulators](../20-server-emulators/index.md) — 改 server 配合
