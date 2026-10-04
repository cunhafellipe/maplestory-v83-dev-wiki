# v83.idb 客戶端逆向分析

> **目的**:從 IDA Pro 9.3 對 `v83.idb` (125 MB) 的完整分析中,提取**可被源碼驗證**的技術事實,給二次開發者使用

## 子章節

- [技術報告](technical-report.md) — 120 KB 完整技術報告(functions/strings/decompiles 全列)
- [Decompiled 函數](decompiles.md) — 6 個核心 MapleStory 函數的 pseudocode
- [Strings 清單](strings.md) — 1,262 strings 分類與用途
- [已知 Class Methods](class-methods.md) — 已命名的 10 個 MapleStory methods
- [歷史 Renames](historical-renames.md) — diamondo25 IDC + angel ToolTip addresses

## 重點事實速查

| 項目 | 值 |
|---|---|
| 原檔名 | `MapleAeon.exe` |
| Image Base | `0x00400000` |
| 架構 | 32-bit i386 |
| 總函數 | 54,357 |
| Named 函數 | 204 |
| Strings ≥4B | 1,262 |
| Segments | 7 |

## 4 個核心 OnPacket Dispatcher

| 函數 | 地址 | 大小 | 行數 | opcode 範圍 |
|---|---|---|---|---|
| `CLogin::OnPacket` | `0x5F80FF` | 385B | 86 | 0 ~ 28 |
| `CField::OnPacket` | `0x531325` | 1,201B | 246 | 125 ~ 345 |
| `CWvsContext::OnPacket` | `0xA07A08` | 1,158B | 284 | 29 ~ 124 |
| `CStage::OnPacket` | `0x644446` | 60B | 14 | 128/129/130 |

## 5 個關鍵 String 與 Xref

| String | 地址 | Xref From |
|---|---|---|
| `You have been blocked for typing in an invalid password...` | `0xAF6B48` | `0x5F8598` (in CLogin) |
| `This user has been blocked.` | `0xB3C178` | `0x90B3E0` |
| `CashShop` | `0xAF46D4` | `0x532C77` |
| `siFieldID` | `0xAF2760` | 4 refs |
| `You must have at least one character over level 30...` | `0xAF1F2C` | `0x46DEB7` |

## 已驗證的歷史文檔對應

| 文檔 | 內容 | 對應本 IDB |
|---|---|---|
| sunnyboy on RaGEZONE | CLogin::OnPacket = 0x5F80FF | ✓ 完全對應 |
| angel RaGEZONE IDB | CField::OnPacket = 0x531325 | ✓ 完全對應 |
| diamondo25 IDC script | 24 個 string→function | 16/24 命中 |
| angel ToolTip addresses | 13 個 CUIToolTip::* | 已記錄 |

## 工具鏈

| 工具 | 版本 | 用途 |
|---|---|---|
| IDA Pro 9.3 (cracked) | 9.3.0.251224 | 反組譯 |
| idat.exe headless | 9.3 | 跑 IDAPython 腳本 |
| Hex-Rays Decompiler | 9.3 | pseudocode |
| goMBA ML | 9.3 內建 | pseudocode 增強 |
| ida-pro-mcp v2.0 | 2026 | AI 逆向 MCP (HEADLESS mode) |

## IDB 來源

| 項目 | 值 |
|---|---|
| IDB 原檔 | `v83.idb` (125 MB, IDA 6.1) |
| 來源 | [RaGEZONE thread 1193418](https://forum.ragezone.com/threads/v83-idb-client-edit-dump.1193418/) |
| 原作者 | Angxl (2014-2021) |
| 原 client | 'localhost mooplestory client' (leaked GMS v83) |
| 我們的 64-bit 轉檔 | `v83-copy.i64` (102 MB) |

## 已驗證的限制

- IDB 內的 `sub_xxx` 函數佔 99.6% (54,153 / 54,357) — 都不是 named
- 需要手動 xref + string scan 才能判斷用途
- strings 只有 1,262 條 (≥4B)。原檔受 CSecurity 保護,字串在執行期才解密
