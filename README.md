# MapleStory v83 二次開發 WIKI

> GMS v83 客戶端的逆向、協議與二次開發知識庫。
> 每一條技術主張都有對應的自動驗證腳本,數字直接從二進位重算,不是抄來的。

**線上版**: https://e78-png.github.io/maplestory-v83-dev-wiki/

## 快速開始

```bash
git clone https://github.com/e78-png/maplestory-v83-dev-wiki
cd maplestory-v83-dev-wiki

pip install mkdocs-material
mkdocs serve          # http://localhost:8000
```

直接看 markdown 也行 — 所有內容都是 `.md`。

## 這個 wiki 收錄什麼

| 章節 | 內容 |
|---|---|
| `10-client-analysis/` | **核心** — v83.idb 逆向、pseudocode、位址、WZ 結構 |
| `20-server-emulators/` | Cosmic / HeavenMS / SoloMapling / BeiDou + 開源 client 拆解 |
| `30-ui-classes/` | CUIWnd 視窗系統、CUIToolTip、裝備道具欄位 |
| `40-protocol/` | 4 個 opcode dispatcher、handler 對照表 |
| `50-tools/` | kaentake、WZ Mod Tool、IDA Pro MCP |
| `60-secondary-dev/` | Client patches、新功能創建指南 |
| `70-resources/` | GitHub 專案書籤(215 個)、外部連結、歷史文檔 |

## 給 AI agent

- **`docs/facts.json`** — machine-readable 事實索引(8 KB):位址、opcode 範圍、
  handler 對照、腳本統計、**已知錯誤清單**。查資料讀它,不要在散文中 grep。
- **`AGENTS.md`** — 查資料順序、不可引用的文件、檔案位置速查、已知的坑。

## 驗證

```bash
python verify_wiki_claims.py
```

腳本從二進位重算每一個數字。**二進位本身不收錄於本 repo**,需自行取得後
指向正確路徑(見 `verify_wiki_claims.py` 開頭的路徑常數)。

## 授權與致謝

- 內容:[CC BY 4.0](docs/LICENSE.md)
- 程式碼:MIT
- 引用來源:[REFERENCES](docs/REFERENCES.md)
- 致謝:[CREDITS](docs/CREDITS.md)

MapleStory 是 Wizet / Nexon 的註冊商標。本 wiki 僅供教育與研究用途,
不含破解或盜版工具的連結。

## 🔑 關鍵位址

Image base `0x00400000`。地址已對解包後的二進位逐一驗證。

| 用途 | VA |
|---|---|
| `CLogin::OnPacket` | `0x5F80FF` |
| `CField::OnPacket` | `0x531325` |
| `CWvsContext::OnPacket` | `0xA07A08` |
| `CStage::OnPacket` | `0x644446` |
| `StringPool::GetString` | `0x406455` |
| `CInPacket::Decode1/2/4/Buffer` | `0x4065F3 / 0x42470C / 0x406629 / 0x432257` |

30 個 `CWvsContext` handler 的完整 opcode 對照表見
[40-protocol](docs/40-protocol/index.md) 與 `docs/facts.json`。

## ❗ 已知錯誤與更正

| 舊的說法 | 更正 | 依據 |
|---|---|---|
| 保護層是 Themida / WzPacker | **Nexon CSecurity**(第一方) | RTTI 證據;五種商業殼簽章全 0 命中 |
| `7,270,400` 是 2018 年的時間戳 | 那是 **SizeOfCode** | PE 標頭直讀 |
| `CWvsContext` opcode 29~62 | **29~124** | `add eax,-29` + `cmp eax,0x5f` + 96 項 jump table |
| 腳本 2,297 個 | **2,294** | 差異為 41 個非 `.js` 條目 |

完整清單見 `docs/facts.json` 的 `corrections` 欄位。
原始掃描記錄(含上述錯誤)保留在
[00-overview](docs/00-overview/index.md),每份都有警告標頭。
