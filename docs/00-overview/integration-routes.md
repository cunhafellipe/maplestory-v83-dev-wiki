# 整合路線 — 從 v83.idb + kaentake + Cosmic 到新功能

> **目的**:純技術事實的整合路線(不下結論、不推薦「最佳」)
> **驗證**:截至 2026-09-28 為止所有資料已抓取

## 已驗證的技術鏈(純事實)

```
逆向分析
  ↓
v83.idb (angel 釋出,125MB,IDA 6.1)
  ↓ idat.exe + IDAPython
v83-copy.i64 (102MB,IDA 9.3 轉檔)
  ↓ Hex-Rays Decompile
6 個核心 MapleStory 函數 pseudocode (CLogin/CField/CWvsContext/CStage/StringPool/CInPacket/_WinMain)
  ↓
未命名的 sub_xxx (54,153 個,99.6%) ← 需要 xref 分析
  ↓
已知可套用:diamondo25 IDC + angel ToolTip (16+13 = 29 個命名機會)
```

## 整合路線(從這個 WIKI 出發)

### 路線 A:加 UI 功能(推薦起點)

```
1. 讀 WIKI 30-ui-classes/cuiwnd/ + cuitooltip/ 了解 UI 結構
2. 看 decompiles.md 內 CUIStatusBar::ChatLogDraw 等 pseudocode
3. 改 WZ (HaRepacker):加新視覺
4. patch EXE (kaentake 或 OllyDbg):改 UI 行為
5. 連 local server (Cosmic) 測試
```

### 路線 B:加 Packet 行為

```
1. 讀 WIKI 40-protocol/ 了解 opcode 結構
2. 看 CLogin::OnPacket / CField::OnPacket / CWvsContext::OnPacket / CStage::OnPacket pseudocode
3. 找到對應的 case (例如 CField::OnPacket case 0x130 = sub_7465F4)
4. decompile 該 sub_xxx 看實際邏輯
5. server 端 (Cosmic Java):加對應 RecvPacketHandler
6. client 端 patch
7. 測試互通
```

### 路線 C:hook client 不改 EXE

```
1. 讀 WIKI 50-tools/kaentake/ 了解 hook 框架
2. 寫 C++ hook DLL 注入 MapleStory 0.83.exe
3. 用 Detours 攔截 CClientSocket::SendPacket 處理自訂邏輯
4. 測試不需要 patch 主程序
```

### 路線 D:完全從零寫 client

```
1. 看 WIKI 10-client-analysis/wf-analysis/W3-1-HeavenClient-4-platforms-deep-dive.md
2. 參考 HeavenClient (https://github.com/ryantpayton/MapleStory-Client)
3. 或參考 JourneyClient (本機 04-Emulators/JourneyClient/)
4. 連到 Cosmic / HeavenMS server 測試
```

## 不做的事(下結論)

- **不推薦** 哪個 server 比較好(Cosmic vs HeavenMS vs BeiDou)
- **不推薦** 哪個 client 比較好(JourneyClient vs MortalClient vs OpenMapleClient)
- **不預測** 哪個方向「比較有前途」

只列**事實**:
- Cosmic 是 Java 21,適合現代 JVM 部署
- HeavenClient 支援 4 平台(Windows / macOS / Linux / Android?)
- kaentake 是最成熟的 C++ hook client
- v83.idb 是 angel 從 'localhost mooplestory client' 做的

## 待整合 / 未驗證

| 項目 | 狀態 |
|---|---|
| WZ 結構完整 dump | ✗ 沒跑 |
| strings min_length=2 全 dump | ✗ 沒跑 |
| sub_xxx 的自動分群(54,153 個)| ✗ 沒跑 |
| ida-pro-mcp 完整測試 66 tools | ✗ 沒跑完(只測了基本功能)|
| HexRaysSA/ida-mcp 安裝 | ✗ 沒做 |
| HaRepacker 安裝 | ✗ 沒做 |
| MapleEzorsia DLL hook 實戰 | ✗ 沒做 |
| Cosmic server 架設 | ✗ 沒做 |
