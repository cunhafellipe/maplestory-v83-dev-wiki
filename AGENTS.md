# AGENTS.md — 如何使用這份 WIKI

給 AI agent 的操作說明。**先讀這裡,再讀 `docs/facts.json`,最後才進散文章節。**

## 為什麼要這樣

這份 WIKI 有 683 KB 散文。直接 grep 找一個位址會很慢,而且會命中
`00-overview/*-original.md` 裡**已被推翻的舊數字**。`docs/facts.json`
是同一批事實的結構化版本,由二進位直接算出,不含過時內容。

## 查資料的順序

### 1. 先開 `docs/facts.json`(8 KB)

```jsonc
{
  "addresses":    { "CField::OnPacket": { "va": 5435173, "hex": "0x531325", "in_code": true } },
  "dispatchers":  { "CWvsContext::OnPacket": { "opcode_range": [29, 124], "bias": 29 } },
  "cwvs_context_handlers": { "62": { "hex": "0xA3E31C" } },
  "corrections":  [ { "claim": "...", "corrected": "...", "why": "..." } ],
  "entry_points": { "want_to_change_ui": "docs/30-ui-classes/index.md" }
}
```

- `entry_points` — 依你的目的直接跳到對應章節
- `corrections` — **引用任何數字前先看這裡**,避免複用已推翻的說法
- `in_code: false` — 該地址不在程式碼段,寫在文件裡就是錯的

### 2. 再依 `entry_points` 進具體章節

| 我要做 | 讀 |
|---|---|
| 改 UI | `docs/30-ui-classes/index.md` |
| 加封包行為 | `docs/40-protocol/index.md` |
| 改客戶端(hook/patch) | `docs/60-secondary-dev/index.md` |
| 架伺服器 | `docs/20-server-emulators/index.md` |
| 逆向客戶端 | `docs/10-client-analysis/v83-idb/index.md` |
| 找社群專案 | `docs/70-resources/github-bookmarks/index.md` |

### 3. 必要時才讀深度分析

`*/wf-analysis/` 是原始掃描記錄,回答的是「當時的特定問題」而非
通讀材料。**它們的數字可能已過時** — 以 `facts.json` 為準。

## 絕對不要引用這些

- `docs/00-overview/*-original.md` — 原始掃描,含已知錯誤
  (TimeDateStamp 誤植、保護層誤判、腳本數偏差)。每份都有警告標頭。
- 任何與 `facts.json` 的 `corrections` 相衝突的敘述

## 怎麼自己驗證

```bash
cd C:\MUWORK\GAME\MAPLESOTRY\wiki
python verify_wiki_claims.py
```

腳本從磁碟上的二進位重算每一個數字。它是這份 WIKI 的可信度來源 ——
若你發現文件與腳本衝突,**以腳本為準**,並回報差異。

三種輸出:

| 級別 | 意義 |
|---|---|
| `PASS` / `FAIL` | 真正的斷言,參與通過率 |
| `INFO` | 量測值,不參與通過率 |
| `SKIP` | 輸入檔不存在,無法執行 |

`soft()` 若收到字面值會直接拋錯中止 — 這是刻意的,防止「假檢查」
重新出現在腳本裡。

## 改動這個 WIKI 的規則

1. **不要手改 `docs/facts.json`** — 它由 `python gen_facts_index.py` 產生
2. 改了 `mkdocs.yml` 的 nav,確認新檔案不該漏掉 — 2026-09 前有 21 個
   文件沒被 nav 引用,其中 11 篇有實質內容
3. 改動任何技術數字,同步更新對應章節 **並** 確認 `verify_wiki_claims.py`
   仍全綠。若無法新增斷言,至少在該章節註明數字未經驗證

## 檔案位置速查

| 用途 | 路徑 |
|---|---|
| 加殼原檔 | `C:\MUWORK\GAME\MAPLESOTRY\待分類\MapleStory 0.83.exe` |
| 解包後二進位 | `C:\RE\msv83\bin\msv83_trad.exe` |
| IDA IDB | `C:\RE\msv83\ida\v83.idb` |
| WZ 檔案 | `C:\RE\msv83\wz\`(僅 4 個)、`C:\RE\msv83\gate\`(完整 16 個) |
| GM Script | `C:\RE\msv83\wz\scripts\`(2,294 個 `.js`) |
| 主推伺服器 | `C:\MUWORK\GAME\MAPLESOTRY\04-Emulators\GMS-v083-Cosmic\` |
| 專案書籤 | `wiki\tools\bookmarks\楓之谷專案書籤.html` |

## 已知的坑

- **IDB 與本機二進位是不同檔案。** IDB 是 2014 年的
  `MapleAeon.exe`,磁碟上的是 2010 build。地址吻合,但要清楚差在哪。
- **`v83.idb` 只有 16 個 `Class::method` 符號**,其餘 54,357 個函式
  都是 `sub_XXXXX`。網路上流傳的「命名」多半是後來套的。
- **WZ 檔案兩處內容不同。** `C:\RE\msv83\wz\` 有 4 個(部分被改過),
  `C:\RE\msv83\gate\` 有完整 16 個(原始)。比對時要選對來源。
- **客戶端 WZ 裡沒有容器解析器。** `PKG1`、公開 v83 key、`Wizet` 字串
  在 client image 裡都是 0 命中 — 解析器在 `ijl15.dll` 或外部工具。
- **客戶端用 Pixi 而非 COM。** `GetProcAddress(h, "PcCreateObject")`。
