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

### 打包原檔 `MapleStory 0.83.exe`

| 項目 | 值 |
|---|---|
| 大小 / MD5 | 4,281,928 bytes / `09d00a6ebd70aaf0026d6feb764a1f21` |
| 架構 | PE32, i386, Windows GUI |
| Image Base | `0x00400000` |
| EntryPoint | `0x00A8C000`(位於 4 KB section `tfqhbstk`) |
| TimeDateStamp | `0x4B879403` = **2010-02-26 09:27:31 UTC** |
| Section 數 | 7(首段 entropy **7.98**) |
| Import | **1 個** — `kernel32.dll!FileTimeToLocalFileTime` |
| Export | 3 個 — `ZtlTaskMemAllocImp` / `ZtlTaskMemFreeImp` / `ZtlTaskMemReallocImp` |
| **保護層** | **Nexon CSecurity**(第一方,非商業加殼器) |

> 簽章掃描確認 Themida / WinLicense / VMProtect / ASProtect / Enigma / UPX **全部 0 命中**。
> 識別依據是解包版字串池中的 RTTI:`CSecurityException`、`CSecurityInitFailed`、
> `CSecurityUpdateFailed`、`CSecurityThreatDetected`、`CSecurityClearFailed`。
>
> `TimeDateStamp` 曾被誤記為 `7,270,400 (≈2018)` — `7,270,400` 是 **SizeOfCode**。

### 解包版 `msv83_trad.exe`(Ghidra 全量分析)

| 項目 | 值 |
|---|---|
| 大小 | 9,920,523 bytes |
| 入口 | `0x00663FF3` |
| **函式** | **52,083** |
| **符號** | **254,338** |
| **Import** | **238**,分佈於 17 個 DLL |
| 工具鏈來源 | `SolidDaima_Rev8_200901029`(`E:\ACGame_GL\BinTool\`) |

### `v83.idb`(IDA 6 資料庫,2014-03-25)

| 項目 | 值 |
|---|---|
| 大小 | 125,092,284 bytes |
| 原檔名 | `MapleAeon.exe` |
| 原路徑 | `…\MapleStory IDBs\GMS\v83\MapleAeon.exe` |
| 總函數 | 54,357(其中 204 個 named) |
| Strings ≥4B | 1,262 |
| 4 個核心 OnPacket dispatcher | `CLogin` / `CField` / `CWvsContext` / `CStage` |
| 關鍵匯出證據 | 映像 import `nmcogame.dll`,含 `NMCO_*` 8 個 API |

> `MapleAeon.exe` 是原持有者的重新命名,路徑中的 `GMS\v83\` 明確標示為 GMS v83。

### 資源與腳本

| 項目 | 值 |
|---|---|
| WZ 載入清單 | **15 個**:Character, Mob, Skill, Reactor, Npc, UI, Quest, Item, Effect, String, Etc, Morph, TamingMob, Sound, Map |
| WZ 綁定機制 | **Pixi**(`GetProcAddress(h, "PcCreateObject")`),非 Windows COM |
| 容器解析器 | **不在 client image 內**(`PKG1` / 公開 v83 key / `Wizet` 字串皆 0 命中) |
| WZ 封存檔 | `PKG1` header + `Package file v1.0 Copyright 2002 Wizet, ZMS` |
| 散落 `.img` | 無 header,開頭 `73 f8 6c 77`,entropy 7.84 |
| JS 腳本 | **2,294** 個,GB18030 編碼 |

---

## ✅ 驗證

```bash
python verify_wiki_claims.py
```

**129 / 129 檢查通過。** 每條主張都有對應的自動檢查,預期值為原始碼中的字面值 ——
修改任一預期值即可觀察檢查轉紅,以確認該檢查確實有效。

腳本同時掃描 `docs/` 全部 markdown,確保沒有任何文件仍**斷言**本檔案使用商業加殼器。

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

## 📜 授權與致謝

- 內容:CC BY 4.0(見 [LICENSE](docs/LICENSE.md))
- 程式碼:MIT(見 [LICENSE](docs/LICENSE.md))
- 完整引用清單:見 [REFERENCES](docs/REFERENCES.md)
- **作者與致謝**:見 [CREDITS](docs/CREDITS.md) ← **列出所有引用作者 + 感謝詞句**

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
