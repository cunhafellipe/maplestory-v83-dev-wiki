# 開源 Client 拆解 (wf-analysis)

> 2026-09-27 對四個同源開源客戶端的技術拆解。作者皆為
> `speedyHKjournalist`(港籍開發者)與 `ryantpayton`。

## 上游血統

```
ryantpayton/MapleStory-Client  (HeavenClient, C++)
        │
        ├── JourneyClient
        ├── MortalClient      (配對伺服器: HypatiaOfAlexandria/MortalMS)
        └── OpenMapleClient   (C# 改寫, 官方測試相容: P0nk/Cosmic)
                    │
                    └── MapleServerAndroid  (Cosmic v83 + Android 包裝)
```

| 文件 | 內容 |
|---|---|
| [W2-4 血統對比](W2-4-Journey-vs-Mortal-vs-OpenMaple-compare.md) | 三個 fork 的差異矩陣,說明各自改了什麼 |
| [W2-1 OpenMapleClient](W2-1-OpenMapleClient-analysis.md) | 專案結構、渲染後端、與 Cosmic 的相容性 |
| [W2-2 Net/Packets 與 Handlers](W2-2-OpenMapleClient-NetPackets-Handlers.md) | 24 個封包類別與 handler 的子樹拆解 |
| [W2-3 MapleServerAndroid](W2-3-MapleServerAndroid-analysis.md) | Android 封裝層做了什麼、沒做什麼 |

!!! warning "這四個 repo 都不是原始碼級的乾淨參考"
    它們是 fork 出去的成品,含大量個人修改與未整理的程式碼。適合看
    **「一個完整客戶端需要哪些模組」**,不適合直接 copy 程式碼。
    乾淨的參考是 [v83.idb 分析](../../10-client-analysis/v83-idb/index.md) 與
    [kaentake 工具](../../50-tools/kaentake/index.md)。
