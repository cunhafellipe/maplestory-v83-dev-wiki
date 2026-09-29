# MapleStory v83 二次開發 WIKI

> **本地知識庫** — 整合所有 v83 客戶端 / 服務端 / 工具 / 逆向工程資料,便利二次開發與新功能創建
>
> **最後更新**: 2026-09-28
> **根目錄**: `C:\MUWORK\GAME\MAPLESOTRY\`
> **本機 WIKI**: `C:\MUWORK\GAME\MAPLESOTRY\wiki\`

## 🚀 快速開始

| 你是 | 從哪裡開始 |
|---|---|
| **想改 UI** | [30-ui-classes/index.md](30-ui-classes/index.md) → CUIToolTip / CUIWnd / 裝備道具 |
| **想加 packet 行為** | [40-protocol/index.md](40-protocol/index.md) → Opcodes |
| **想做 client patch** | [60-secondary-dev/patches/index.md](60-secondary-dev/patches/index.md) |
| **想架 server** | [20-server-emulators/index.md](20-server-emulators/index.md) → Cosmic |
| **想逆向 client** | [10-client-analysis/v83-idb/index.md](10-client-analysis/v83-idb/index.md) |
| **想 hook client** | [50-tools/kaentake/index.md](50-tools/kaentake/index.md) |

## 📦 本地資源總覽

```
C:\MUWORK\GAME\MAPLESOTRY\
├── wiki/                           ← 本知識庫
├── 04-Emulators/                   ← 服務端模擬器源碼
│   ├── GMS-v083-Cosmic/           ← Java 21 服務端(主推薦)
│   ├── GMS-v083-HeavenMS/
│   ├── SoloMapling-wisteria-Wz-Mod-Tool-Suite/
│   ├── BeiDou-Server/
│   ├── JourneyClient/             ← C++ 從零寫 client
│   ├── MortalClient/              ← C++ 從零寫 client
│   ├── OpenMapleClient/           ← C# 從零寫 client
│   └── MapleEzorsia-v83/          ← C++ DLL hook client
├── 05-Documentation/               ← 官方 + 社群文檔
├── 待分類/                         ← IDA 已分析的 client 資料
│   ├── MapleStory 0.83.exe       ← Nexon CSecurity 加殼
│   ├── MapleStory 0.83.exe.i64   ← IDA auto-analyzed IDB
│   ├── v83.rar                    ← 完整 v83 client 包
│   ├── BeautySalonv83.zip
│   ├── cashshop-window.7z
│   ├── crit_and_range (1).7z
│   ├── GMS083客戶端/
│   └── 簽到表/wz/UI.wz           ← 25KB UI.wz 部分
└── wf-output/                      ← 自動分析產物
    ├── W1-1 ~ W1-7.md            ← 客戶端結構分析
    ├── W2-1 ~ W2-4.md            ← 開放源 client 比較
    ├── W3-1 ~ W3-2.md            ← C++ client 深入
    ├── ida-v83-direct/            ← IDA Pro v83.idb 完整 dump
    │   ├── 00-TECHNICAL-REPORT.md ← 120KB 完整報告
    │   ├── functions.json         ← 54,357 函數
    │   ├── strings.json           ← 1,262 strings
    │   ├── decompiles.json        ← 6 核心 pseudocode
    │   ├── string_xrefs.json
    │   ├── mapple_methods.json
    │   ├── segments.json
    │   └── historical_renames.json ← diamondo25 IDC + angel ToolTip
    └── *.json / *.log             ← 中間資料
```

## 📚 章節索引

### [00-overview/index.md](00-overview/index.md)
- 專案地圖
- 整合路線

### [10-client-analysis/index.md](10-client-analysis/index.md)
- **v83.idb IDA 結構分析** ← 客戶端逆向核心
- IDA Pro MCP 工具設定
- WZ 結構解析

### [20-server-emulators/index.md](20-server-emulators/index.md)
- Cosmic (Java 21,主推薦)
- HeavenMS / SoloMapling / BeiDou / MapleEzorsia

### [30-ui-classes/index.md](30-ui-classes/index.md)
- CUIWnd 視窗系統
- CUIToolTip 13 個 Tooltip 方法
- 裝備/道具欄位結構

### [40-protocol/index.md](40-protocol/index.md)
- Opcode dispatchers
- CLogin::OnPacket / CField::OnPacket / CWvsContext::OnPacket / CStage::OnPacket

### [50-tools/index.md](50-tools/index.md)
- kaentake (C++ Detours hook)
- WZ Mod Tool Suite
- IDA Pro MCP 設定

### [60-secondary-dev/index.md](60-secondary-dev/index.md)
- Client Patches (ToolTip, Cash Shop, Bypass)
- 新功能創建 (UI 視窗, packet handler)

### [70-resources/index.md](70-resources/index.md)
- Raw Data
- 歷史文檔 (RaGEZONE, IDC scripts)
- 外部連結

## 🎯 已驗證的純技術事實

| 項目 | 值 | 來源 |
|---|---|---|
| 原檔名 | `MapleAeon.exe` | `wf-output/ida-v83-direct/` |
| Image Base | `0x00400000` | IDA metadata |
| 架構 | 32-bit i386 | IDA metadata |
| 總函數 | 54,357 | `functions.json` |
| Named 函數 | 204 | (sunnyboy + angel + ida-mcp 自帶) |
| Strings ≥4B | 1,262 | `strings.json` |
| Segments | 7 | `segments.json` |
| 6 核心函數 pseudocode | 完整 | `decompiles.json` |

## 🔑 關鍵地址速查

| 用途 | 地址 |
|---|---|
| `CLogin::OnPacket` | `0x5F80FF` |
| `CField::OnPacket` | `0x531325` |
| `CWvsContext::OnPacket` | `0xA07A08` |
| `CStage::OnPacket` | `0x644446` |
| `StringPool::GetString` | `0x406455` |
| `StringPool::GetInstance` | `0x79E805` |
| `CInPacket::Decode1/2/4/Buffer` | `0x4065F3 / 0x42470C / 0x406629 / 0x432257` |
| `_WinMain@16` | `0x9F19F2` |
| Ban message | `0xAF6B48` (xref: `0x5F8598` in CLogin) |

## 📖 對應 RaGEZONE 教學

完整驗證 CLogin::OnPacket / CField::OnPacket / CWvsContext::OnPacket / CStage::OnPacket 與 2014 sunnyboy 教學地址**完全一致**。

## 🛠️ 已驗證工具鏈

| 工具 | 版本 | 用途 |
|---|---|---|
| IDA Pro 9.3 (cracked) | 9.3.0.251224 | 反組譯 |
| idat.exe headless | 9.3 | 跑 IDAPython |
| ida-pro-mcp v2.0 | 2026 | AI 逆向 |
| Hex-Rays Decompiler | 9.3 | pseudocode |
| goMBA ML | 9.3 內建 | pseudocode 增強 |

## 📜 授權與致謝

- 內容:CC BY 4.0(見 [LICENSE](LICENSE.md))
- 程式碼:MIT(見 [LICENSE](LICENSE.md))
- 完整引用清單:見 [REFERENCES](REFERENCES.md)
- **作者與致謝**:見 [CREDITS](CREDITS.md) ← **列出所有引用作者 + 感謝詞句**
