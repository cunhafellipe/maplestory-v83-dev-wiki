# 深度分析 (wf-analysis)

> 2026-09-27 對 v83 客戶端與其衍生專案做的技術拆解。**這些是原始掃描記錄**,
> 記載當時觀察到的事實;若與本 WIKI 其他章節衝突,以 `facts.json` 與
> `verify_wiki_claims.py` 為準。

## 客戶端二進位

| 文件 | 內容 |
|---|---|
| [W1-1 IDB 結構](W1-1-v83-idb-structure.md) | `v83.idb` 的 B-tree 結構、node 佈局、字串池位置 |
| [W1-2 Opcode 衝突](W1-2-opcode-collision.md) | 官方 opcode 與 Cosmic 的 `RecvOpcode`/`SendOpcode` 對撞分析 |
| [W1-3 原版 vs 繁化版](W1-3-exe-diff.md) | `MapleStory 0.83.exe` 與繁中版的二進位差異(hash、段、匯入表) |
| [W1-5 WZ/IMG 索引](W1-5-wz-img-index.md) | 5 個工作區內所有 `.wz` / `.img` 的清單與雜湊 |
| [W1-6 JS 腳本索引](W1-6-js-script-index.md) | 2,294 個腳本的分類統計、GB18030 編碼、與 Cosmic 的差異 |
| [W1-7 怪物圖鑑索引](W1-7-monsterbook-index.md) | 怪物掉落 / 反應堆掉落與 Cosmic `server/life/*` 的對照 |

## 開源客戶端

| 文件 | 內容 |
|---|---|
| [W3-1 HeavenClient 4 端](W3-1-HeavenClient-4-platforms-deep-dive.md) | `ryantpayton/MapleStory-Client` 及其 4 個平台 fork 的路線拆解 |
| [W3-2 MapleStory-Client 拆解](W3-2-MapleStory-Client-isolated-analysis.md) | 該 repo 的獨立深度分析(渲染、輸入、封包層) |
| [W1-4 kaentake headers 對照](W1-4-framework-headers-compare.md) | kaentake 的 45 個 source 檔與功能包介面的對應 |

!!! tip "這些文件怎麼用"
    原始掃描的用途是**回答當時的特定問題**,不是通讀。查東西時:
    - 要 opcode 數值 → [40-protocol](../../40-protocol/index.md) 或 `facts.json`
    - 要 client 改法 → [60-secondary-dev](../../60-secondary-dev/index.md)
    - 要看別人怎麼做 → 本目錄的 W3-1 / W3-2
    - 要 WZ 素材清單 → [W1-5](W1-5-wz-img-index.md)
