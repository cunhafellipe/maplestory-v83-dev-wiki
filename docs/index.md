# MapleStory v83 二次開發 WIKI

> GMS v83 客戶端的逆向、協議與二次開發知識庫。
> 所有技術主張都有 `verify_wiki_claims.py` 的自動斷言支撐,
> 每一條都經過突變測試證明會在錯誤時轉紅。
> 執行 `python verify_wiki_claims.py` 查看目前通過率。

<div class="grid cards" markdown>

-   :material-rocket-launch:{ .lg .middle } **改 UI**

    ---

    視窗系統、tooltip、狀態列

    [:octicons-arrow-right-24: 30-ui-classes](30-ui-classes/index.md)

-   :material-lan-connect:{ .lg .middle } **加封包行為**

    ---

    4 個 dispatcher、opcode 範圍

    [:octicons-arrow-right-24: 40-protocol](40-protocol/index.md)

-   :material-source-branch:{ .lg .middle } **改客戶端**

    ---

    DLL、code cave、Detours

    [:octicons-arrow-right-24: 60-secondary-dev](60-secondary-dev/index.md)

-   :material-book-open-variant:{ .lg .middle } **找社群專案**

    ---

    **215 個 GitHub 專案**,已按用途分類、可篩選版本與維護狀態

    [:octicons-arrow-right-24: 70-resources/github-bookmarks](70-resources/github-bookmarks/index.md)

-   :material-server-network:{ .lg .middle } **架伺服器**

    ---

    Cosmic / HeavenMS / BeiDou

    [:octicons-arrow-right-24: 20-server-emulators](20-server-emulators/index.md)

-   :material-magnify-scan:{ .lg .middle } **逆向客戶端**

    ---

    v83.idb、pseudocode、位址

    [:octicons-arrow-right-24: 10-client-analysis](10-client-analysis/index.md)

</div>

!!! tip "書籤頁怎麼用"
    [GitHub 專案書籤](70-resources/github-bookmarks/index.md)收錄 **215 個**
    已實測可用的 v83 二次開發專案,分 13 類:

    | 優先看 | 內容 |
    |---|---|
    | **渲染層** | gr2dpatcher、kaentake — 讓 v83 脫離 1024×768 |
    | **Hook / DLL** | Detours、code cave、ijl15 proxy 注入 |
    | **WZ 編輯** | HaRepacker、WzComparerR2、六種語言的 WzLib |
    | **封包** | MaplePE、PacketPuller、sniffer |

    頁面上方可依 **版本 / 語言 / 維護狀態** 篩選;「活躍」欄位可直接看出
    哪些專案還在更新。下方另有完整靜態清單可供站內搜尋。

## 🔑 關鍵地址速查

Image base `0x00400000`。地址已對解包後的 `msv83_trad.exe` 逐一驗證。

| 用途 | VA | 驗證 |
|---|---|---|
| `CLogin::OnPacket` | `0x5F80FF` | opcode 0~28 |
| `CField::OnPacket` | `0x531325` | opcode 125~345 |
| `CWvsContext::OnPacket` | `0xA07A08` | opcode 29~124 |
| `CStage::OnPacket` | `0x644446` | opcode 128~130 |
| `StringPool::GetString` | `0x406455` | — |
| `StringPool::GetInstance` | `0x79E805` | — |
| `CInPacket::Decode1` | `0x4065F3` | 讀 1 byte |
| `CInPacket::Decode2` | `0x42470C` | 讀 2 bytes |
| `CInPacket::Decode4` | `0x406629` | 讀 4 bytes |
| `CInPacket::DecodeBuffer` | `0x432257` | 讀 buffer |
| `CinPacket::DecodeStr` | `0x46F30C` | stub 形式 |
| `_WinMain@16` | `0x9F19F2` | 程式進入點 |
| Ban handler | `0x5F83EE` | 從 `CLogin` case 0 進入 |

**30 個 `CWvsContext` handler** 的完整 opcode 對照表在
[40-protocol/index.md](40-protocol/index.md) 與 `facts.json` 的
`cwvs_context_handlers`。

## 🤖 給 AI agent

!!! tip "先讀 `facts.json`,再讀 `AGENTS.md`"
    - **`docs/facts.json`**(8 KB)— machine-readable 事實索引:位址、opcode
      範圍、handler 對照、腳本統計、**已知錯誤清單**。查資料時讀它,
      不要在 683 KB 的散文中 grep。
    - **`AGENTS.md`** — agent 操作說明:查資料順序、不可引用的文件、
      檔案位置速查、已知的坑。

    兩者都放在 `wiki/` 根目錄,與 `mkdocs serve` 的網站內容平行。

## ✅ 已驗證的技術事實

| 項目 | 值 |
|---|---|
| 原檔 MD5 | `09d00a6ebd70aaf0026d6feb764a1f21`(4,281,928 bytes) |
| Image base | `0x00400000`,PE32 / i386,7 個 section |
| Entry point | `0x00A8C000` |
| 建置時間 | `2010-02-26 09:27:31 UTC` |
| 保護層 | **Nexon CSecurity**(第一方,非商業加殼器) |
| WZ 綁定 | **Pixi**(`GetProcAddress "PcCreateObject"`),非 COM |
| WZ 數量 | 15 個封存檔,`PKG1` + Wizet 聲明 |
| 散落 `.img` | 無檔頭,magic `73f86c77`,entropy ~7.84 |
| JS 腳本 | 2,294 個,GB18030 編碼 |
| IDB 原始檔 | `…\GMS\v83\MapleAeon.exe`(2014 的 IDB,地址與本機二進位吻合) |

## ❗ 已知錯誤與更正

| 舊的說法 | 更正 | 依據 |
|---|---|---|
| 保護層是 Themida / WzPacker | **Nexon CSecurity** | RTTI 證據;Themida/VMProtect/ASProtect/Enigma/UPX 簽章全 0 命中 |
| `7,270,400` 是 2018 年的時間戳 | 那是 **SizeOfCode**;時間戳是 `1,267,176,451` | PE 標頭直讀 |
| `CWvsContext` opcode 29~62 | **29~124** | `add eax,-29` + `cmp eax,0x5f` + 96 項 jump table |
| 腳本 2,297 / 2,300 個 | **2,294** | 差異為 41 個非 `.js` 條目 |

原始掃描記錄(含上述錯誤)保留在 [00-overview](00-overview/index.md),
每份都有警告標頭。

## 📚 章節索引

| 章節 | 內容 |
|---|---|
| [00-overview](00-overview/index.md) | 專案地圖、整合路線、原始掃描記錄 |
| [10-client-analysis](10-client-analysis/index.md) | **客戶端逆向核心** — v83.idb、pseudocode、WZ 結構、深度分析 |
| [20-server-emulators](20-server-emulators/index.md) | Cosmic / HeavenMS / SoloMapling / BeiDou + 開源 client 拆解 |
| [30-ui-classes](30-ui-classes/index.md) | CUIWnd 視窗系統、CUIToolTip、裝備道具欄位 |
| [40-protocol](40-protocol/index.md) | 4 個 opcode dispatcher、handler 對照表 |
| [50-tools](50-tools/index.md) | kaentake、WZ Mod Tool、IDA Pro MCP |
| [60-secondary-dev](60-secondary-dev/index.md) | Client patches、新功能創建指南 |
| [70-resources](70-resources/index.md) | GitHub 專案書籤(215 個)、外部連結、歷史文檔 |

## 📁 專案結構

本 wiki 為**純文件專案**,不含遊戲二進位。所有技術數字都由
`verify_wiki_claims.py` 從二進位重算驗證,二進位本身需自行取得。

```
wiki\                          ← 本知識庫(公開 GitHub repo)
├── docs\                       網站內容
│   ├── facts.json                 機器可讀事實索引
│   └── assets\stylesheets\        主題樣式
├── tools\
│   ├── bookmarks\                 GitHub 專案書籤資料 + 產生器
│   ├── anonymize_paths.py         將本機路徑轉為佔位符
│   └── gen_*.py                   各產生器
├── gen_facts_index.py          產生 facts.json
├── gen_github_bookmarks.py     產生網站嵌入版
└── verify_wiki_claims.py       驗證全部技術主張
```

文中佔位符對照:

| 佔位符 | 意義 |
|---|---|
| `<MAPLESOTRY>` | 專案工作根目錄 |
| `<RE>` | IDA 資料庫 / WZ 素材工作區 |
| `<TOOLS>` | 外部工具鏈安裝位置(IDA、Ghidra 等) |
| `<USERPROFILE>` | 使用者家目錄 |
| `<BINTOOL>` | Nexon 內部工具鏈路徑(見 §1 保護層分析) |
| `<DRIVE_E>` | 客戶端建置機的路徑前綴 |

### 需要的外部資源

| 類別 | 內容 | 取得方式 |
|---|---|---|
| 客戶端二進位 | `MapleStory 0.83.exe`(加殼)、解包版 | 自行取得;本 wiki 不提供 |
| IDA 資料庫 | `v83.idb`(2014,IDA 6) | [RaGEZONE 公開釋出](https://forum.ragezone.com/threads/v83-idb-client-edit-dump.1193418/) |
| WZ 素材 | 15 個 `.wz` 封存檔 | 客戶端內;本 wiki 僅記錄結構 |
| GM Script | 2,294 個 `.js`(GB18030) | 客戶端內;與 Cosmic 對照見 W1-6 |
| 服務端原始碼 | Cosmic / HeavenMS / BeiDou | 見下方章節索引 |

## 🛠️ 工具鏈

| 工具 | 用途 |
|---|---|
| IDA Pro 9.3 + idat headless | 反組譯、跑 IDAPython |
| ida-pro-mcp v2.0 | AI 輔助逆向 |
| Microsoft Detours | DLL 掛鉤(code cave) |
| HaRepacker / WzComparerR2 | WZ 編輯 |
| Python 3.14 | 腳本層(GM Script 是 Nashorn JS) |

## 📜 授權

- 內容:[CC BY 4.0](LICENSE.md)
- 程式碼:MIT
- 引用來源:[REFERENCES](REFERENCES.md)
- 致謝:[CREDITS](CREDITS.md)
