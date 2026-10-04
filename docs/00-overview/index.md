# 00-overview — 總覽

本目錄收錄專案地圖、整合路線與全局性文檔。

## 文件

- [專案地圖](project-map.md) — 所有已下載/已 clone 的專案總覽
- [整合路線](integration-routes.md) — 從 v83.idb + kaentake + Cosmic 整合的可行路線

## 原始掃描記錄

2026-09-27 ~ 09-29 第一輪掃描的產物。**全部是當時的原始記錄**,
保留是為了留下依據與推翻過程,不作為現況查詢的來源。

!!! danger "這些文件含已知的錯誤"
    掃描當時把 `SizeOfCode`(7,270,400)誤認為時間戳、誤判保護層為
    商業加殼器(Themida / WzPacker)、腳本數量統計有偏差(2,297)。
    這些都已更正,更正值見 `facts.json` 的 `corrections` 欄位。
    **引用本文前請先對照更正表。**

| 文件 | 原始內容 | 主要已知錯誤 |
|---|---|---|
| [待分類資料夾掃描](scan-original.md) | `待分類/` 33 個檔案的完整清單、大小、雜湊 | TimeDateStamp 誤植、腳本數 2,297 |
| [技法萃取](TECHNIQUE-EXTRACTION-original.md) | 從二進位萃取的技法清單(反作弊、封包、渲染) | 保護層誤判為 Themida |
| [路線總覽](ROUTES-OVERVIEW-original.md) | 各種二次開發路線的可行性評估 | 引用了未驗證的版本關聯 |
| [整合 WIKI](INTEGRATION-WIKI-original.md) | 首版整合架構草稿 | 結構已被現行章節取代 |
| [WF 整合 WIKI](WF-INTEGRATED-WIKI-original.md) | 第二版整合草稿 | 同上 |
| [環境建置計畫](ENVIRONMENT-PLAN.md) | IDA Pro、WZ 工具鏈的安裝與設定步驟 | — |

!!! tip "為什麼保留這些"
    它們記錄了**錯誤是怎麼被發現的**。`scan-original.md` 的
    「§0 資料更正」段落是整套驗證機制的起點 — 它列出了哪些數字錯了,
    後來才有 `verify_wiki_claims.py` 把它們變成可自動重跑的斷言。
