# MapleStory v83 二次開發 WIKI

> **本地知識庫** — 整合所有 v83 客戶端 / 服務端 / 工具 / 逆向工程資料

## 📚 WIKI 文庫

位置:`C:\MUWORK\GAME\MAPLESOTRY\wiki\`

### 啟動本地 server(MkDocs)

```bash
cd C:\MUWORK\GAME\MAPLESOTRY\wiki
pip install mkdocs-material
mkdocs serve
# 開啟 http://localhost:8000
```

### 或直接看 markdown

所有檔案都是 .md 格式,可以用任何 markdown 編輯器看。

## 🗂️ 結構

```
wiki/
├── mkdocs.yml                 ← MkDocs 設定
├── README.md                  ← 本檔
└── docs/
    ├── index.md               ← 主索引
    ├── 00-overview/           ← 總覽 + 專案地圖 + 整合路線
    ├── 10-client-analysis/    ← 客戶端分析
    │   ├── v83-idb/           ← v83.idb IDA 完整 dump
    │   ├── ida-pro-mcp/       ← AI 逆向工具
    │   ├── wz-structures/     ← WZ 結構
    │   └── wf-analysis/       ← W1~W3 章節
    ├── 20-server-emulators/   ← 服務端模擬器
    ├── 30-ui-classes/         ← UI Class 結構(CUIWnd/CUIToolTip/Equip)
    ├── 40-protocol/           ← Packet Opcode Dispatchers
    ├── 50-tools/              ← 工具鏈
    ├── 60-secondary-dev/      ← 二次開發指南
    └── 70-resources/          ← 原始資料 + 歷史文檔 + 外部連結
```

## 🚀 快速開始

| 你是 | 從哪裡開始 |
|---|---|
| 改 UI | [30-ui-classes/](docs/30-ui-classes/index.md) |
| 加 packet 行為 | [40-protocol/](docs/40-protocol/index.md) |
| 做 client patch | [60-secondary-dev/patches/](docs/60-secondary-dev/patches/index.md) |
| 架 server | [20-server-emulators/](docs/20-server-emulators/index.md) |
| 逆向 client | [10-client-analysis/v83-idb/](docs/10-client-analysis/v83-idb/index.md) |
| hook client | [50-tools/kaentake/](docs/50-tools/kaentake/index.md) |

## 🎯 已驗證的核心事實

| 項目 | 值 |
|---|---|
| 原檔名 | `MapleAeon.exe` |
| Image Base | `0x00400000` |
| 架構 | 32-bit i386 |
| 總函數 | 54,357 |
| Strings ≥4B | 1,262 |
| 4 個核心 OnPacket dispatcher | 完整 pseudocode |
| 13 個 CUIToolTip addresses | 已驗證 |

## 📦 工具狀態

| 工具 | 狀態 |
|---|---|
| IDA Pro 9.3 (cracked) | ✓ 已安裝 |
| ida-pro-mcp v2.0 | ✓ 已安裝 + Hermes 整合(disabled)|
| v83.idb | ✓ 完整 dump |
| Cosmic / HeavenMS | ✓ 已 clone |
| kaentake | ✓ 已 clone |
| WZ Mod Tool | ✓ 已 clone |
| HaRepacker | ✗ 未安裝 |

## 🔑 關鍵地址速查

| 用途 | 地址 |
|---|---|
| `CLogin::OnPacket` | `0x5F80FF` |
| `CField::OnPacket` | `0x531325` |
| `CWvsContext::OnPacket` | `0xA07A08` |
| `CStage::OnPacket` | `0x644446` |
| `StringPool::GetString` | `0x406455` |
| `CInPacket::Decode1/2/4/Buffer` | `0x4065F3 / 0x42470C / 0x406629 / 0x432257` |
| Ban message string | `0xAF6B48` |
| Ban xref | `0x5F8598` (in CLogin) |
