# 10-client-analysis — 客戶端分析

> **目的**:從 v83 client 角度整理所有已知資訊

## 子章節

- [v83.idb IDA 結構](v83-idb/index.md) — 54,357 函數 / 1,262 strings / 6 核心 pseudocode
- [IDA Pro MCP](ida-pro-mcp/index.md) — AI 逆向工具
- [WZ 結構](wz-structures/index.md) — UI.wz / Map.wz / etc.
- [wf 分析](wf-analysis/W1-1-v83-idb-structure.md) — W1~W3 章節

## 重要事實速查

| 項目 | 值 |
|---|---|
| 原檔名 | `MapleAeon.exe` |
| Image Base | `0x00400000` |
| 架構 | 32-bit i386 |
| 總函數 | 54,357 |
| Strings ≥4B | 1,262 |
| WZ 路徑 | 38 條 UI/ 內 + 13 條其他 |

## 4 個核心 Packet Dispatcher

| 函數 | 地址 | opcode 範圍 |
|---|---|---|
| `CLogin::OnPacket` | `0x5F80FF` | 0~28 |
| `CField::OnPacket` | `0x531325` | 125~345 |
| `CWvsContext::OnPacket` | `0xA07A08` | 29~62 |
| `CStage::OnPacket` | `0x644446` | 128/129/130 |

詳見 [v83-idb/technical-report.md](v83-idb/technical-report.md)
