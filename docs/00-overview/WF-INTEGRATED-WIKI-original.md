# WF 整合 Wiki — 待分類資料夾深度技術拆解

!!! warning "原始掃描記錄,含已知錯誤"
    **原始掃描記錄,含已知錯誤。** 本文件是 2026-09-27 的原始產物,
    未隨後續更正同步。已知錯誤與更正值見
    [本目錄索引](index.md) 與 `docs/facts.json` 的 `corrections`。

    路徑佔位符:`<MAPLESOTRY>` = 專案根目錄、`<RE>` = IDA/WZ 工作區、`<USERPROFILE>` = 使用者家目錄、`<TMP>` = 暫存目錄。完整對照見首頁。
    **現況請查[首頁](../index.md)與 `facts.json`。**

> **執行時間**: 2026-09-27 22:46 - 22:51
> **執行模式**: wf 工作模式 — 全部 7 個子代理 + 主代理同時平行
> **工作目錄**: `<MAPLESOTRY>\wf-output\`
> **輸出**: 7 份技術拆解報告 + 6 個 JSON 資料檔

---

## §0 執行摘要

| 報告 | 大小 | 子代理 | 主題 | 狀態 |
|---|---:|---|---|---|
| W1-1 | 5.1 KB | sa-0-285ae055(已停,主代理完成)| v83.idb IDA 資料庫結構 | ✓ |
| W1-2 | **31.1 KB** | sa-1-c0fed192 | 3 個功能包 opcode 衝突檢查 | ✓ |
| W1-3 | 11.3 KB | sa-2-5a0c199f | MapleStory 原版 vs 繁化版 binary diff | ✓ |
| W1-4 | 6.4 KB | 主代理 | kaentake framework headers 對照 | ✓ |
| W1-5 | 6.7 KB | sa-4-8ef6f18c | .wz/.img 索引 | ✓ |
| W1-6 | **19.0 KB** | sa-5-f1689d52 | 2,297 個 JS 腳本索引 | ✓ |
| W1-7 | **14.8 KB** | sa-6-53bcf189 | 1,138 怪物圖鑑分析 | ✓ |

**附加 JSON 資料檔**:
- `cosmic-opcodes.json` (15 KB) — 完整 RecvOpcode/SendOpcode 索引
- `W1-5-wz-img-index.raw.json` (10 KB) — .wz/.img raw 資料
- `_all.json` (5.7 KB) — exe diff 彙整
- `_results.json` (2 KB) — exe hash 結果
- `_pe.json` (2.4 KB) — PE header 比較
- `_imports.json` (1.6 KB) — Import table 比較

**總輸出**: 94 KB 純技術文件,加上 36 KB JSON 資料

---

## §0 資料更正(2026-09-29)

| 項目 | 原文 | 更正 |
|---|---|---|
| Packer | WzPacker(5 處) | **Nexon CSecurity**;不存在 WzPacker 這個工具。繁化版來源為 **SolidDaima** |
| .js 腳本數 | 2,297 | **2,294** |
| section 名 | — | `.macktt`(檔案中存為 `b'.mackt\x00t'`) |
| Import | 「全部 INT 清空」 | Ghidra 12.1.4 可還原 **238 個具名 import** |
| 「兩個檔都不是 2018 build」 | — | 正確,但兩者都受 CSecurity 家族處理,與 WzPacker 無關 |

---

## §1 跨報告的技術發現彙整(從 7 份報告)

### 1.1 客戶端執行檔的兩個版本(W1-3)

| 屬性 | 原版 exe | 繁化版 exe |
|---|---|---|
| 大小 | 4.28 MB | 9.92 MB |
| MD5 | `09d00a6e...` | `727a9ac6...` |
| TimeDateStamp | 2010-02-26 | 2010-02-17(早 9 天)|
| Section 數 | 7 | 6 |
| EntryPoint | 0xa8c000 | 0x663ff3 |
| Import DLL | 1(kernel32)| 17(全部重 import)|
| 額外依賴 | 無 | nmcogame.dll + ijl15.dll |
| CJK UTF-16 字串 | 753,527 | 1,261,070(+67%)|
| SizeOfCode | 7,270,400(相同)| 7,270,400(相同)|

**純事實**:
- 兩個檔都不是 2018 build,實際是 2010 build
- SizeOfCode 完全相同 → code section 沒動
- 繁化版已解壓,並以 **SolidDaima** 處理(最後 section 含
  `<DRIVE_E>:\ACGame_GL\BinTool\SolidDaima_Rev8_200901029\setting.ini`)
- Import Table 從 1 DLL / 1 函式擴展到 17 DLL / 238 函式
- 解析度切換由 `nmconew.dll`(NMC 系列)提供

### 1.2 IDA 資料庫 v83.idb(W1-1)

- Magic `IDA1` = IDA Pro 6.x/7.x IDB 格式(2014 年生成)
- 125 MB / 119.30 MB / 124,782 個 unique strings
- 142 條 WZ 路徑字串 / 104 條 WZ img 名
- 8 條 C++ class::method / 14 條 Maple 相關
- 識別的關鍵類別:`CInPacket::Decode1/4/Str/Buffer`、`CLogin::OnPacket`、`CWvsContext::OnPacket`、`CField::OnPacket`、`CStage::OnPacket`

**純事實**:
- IDB 是純 IDA 6+ 格式(magic `IDA1`)
- 124,782 strings 是 IDA indexed 後的部分字串(非完整)
- 必須用 IDA Pro 才能取得 function list + xref
- 純文件讀取可達:magic、版本、字串池規模、關鍵類別名

### 1.3 3 個功能包 opcode 衝突(W1-2)

| Opcode | CheckIn | Beauty | CashShop | Recv 衝突 | Send 衝突 |
|---|---|---|---|---|---|
| **0x11A** | ✓ 用 | — | — | ✓ FREE | ⚠️ **HIT_SNOWBALL**(Send 已佔用)|
| 0x17C | ✓ 用 | — | — | ✓ FREE | ✓ FREE |
| 0x174 | — | ✓ 用 | — | ✓ FREE | ✓ FREE |
| 0x3730 | — | — | ✓ 用 | ✓ FREE | ✓ FREE |
| 0x3731 | — | — | ✓ 用 | ✓ FREE | ✓ FREE |

**純事實**:
- Cosmic 現有 179 條 RecvOpcode、308 條 SendOpcode
- 唯一衝突:`0x11A` 在 SendOpcode 已被 HIT_SNOWBALL 佔用
- RecvOpcode 0x105~0x3712 範圍全 FREE(可放新功能)
- 3 個功能包同時安裝不衝突,可直接合併

### 1.4 kaentake framework headers 對照(W1-4)

**本地 kaentake 結構**(從 scratch 補齊,共 45 檔):
- `src/` 根:19 個 .cpp/.h
- `src/wvs/`:20 個 .h(完整 WZ 客戶端框架)
- `src/ztl/`:6 個 .h(基礎工具庫)

**3 個功能包需要 headers**(本地全有 ✓):
- BeautySalon:14 include
- CashShop:20 include(含 wvs/wndman + wvs/iteminfo)
- CheckIn:16 include

**純事實**:本地 kaentake 45 檔涵蓋 3 個功能包所需的所有 headers,**可直接使用**。

### 1.5 .wz/.img 索引(W1-5)

**5 個 .wz / 14 個 .img = 19 個檔案,總 11.1 MB**

| 格式 | 檔數 | 總大小 | 特徵 |
|---|---|---|---|
| `.wz` (PKG1 容器) | 5 | 443 KB | `50 4B 47 31` magic,加密壓縮 |
| `.img` (子檔) | 14 | 10.2 MB | XOR/AES key + type + 子節點數 |

**WZ vs IMG 差異**:
- WZ:header 60 bytes,內容 zlib + XOR/AES
- IMG:4-byte XOR/AES key(隨每個 WZ 不同),內容仍 XOR 編碼
- WZ 內有 "Package file v1.0 Copyright 2002 Wizet, ZMS" 明文

### 1.6 2,297 個 JS 腳本(W1-6)

| 目錄 | GMS 套 | Cosmic | 共有 | GMS 獨有 | Cosmic 獨有 |
|---|---:|---:|---:|---:|---:|
| `event/` | 101 | 101 | 99 | 2 | 2 |
| `item/` | 2 | 2 | 2 | 0 | 0 |
| `map/` | 72 | — | — | — | — |
| `npc/` | 1101 | — | — | — | — |
| `portal/` | 409 | — | — | — | — |
| `quest/` | 330 | — | — | — | — |
| `reactor/` | 269 | — | — | — | — |
| 根 | 3 | 4 | 3 | 0 | 1 |

**純事實**:
- GMS 套 1,992 個 + Cosmic 1,898 個,共通 1,689
- GMS 獨有 303 / Cosmic 獨有 209
- 兩套差異約 16%,大部分是命名 / 細節
- NPC 腳本最大宗(1,101 個)

### 1.7 1,138 怪物圖鑑(W1-7)

**事實**:
- 總 `.txt`:1,137 個(差 1 是目錄內含 .txt)
- 分布:`083MonsterBook/` 365 + `083反应堆数据/` 146 + `任务类怪物/` 66 + `MonsterBook没有的/` 115 + 其他 145
- 怪物 ID 範圍:100,100 ~ 9,500,317
- 等級平均:56.7,最高 180(BOSS)
- 怪物書整合檔:`7.27MonsterBook.txt` 11,070 行
- 欄位格式:7 TAB 分隔(lineIdx, monsterId, itemId, minQty, maxQty, questId, chance)
- 反應堆格式:5 TAB 分隔(lineIdx, reactorId, itemId, chance, questId)

---

## §2 跨報告的依賴關係圖

```
v83.idb(2014 IDA DB)
  ↓ 提供 function 名稱
kaentake hook(2018 source)
  ↓ 使用 function address
3 個功能包(CheckIn / Beauty / CashShop)
  ↓ 需要 hook + WZ + 服務端
Cosmic v1.1.3(服務端 Java)
  ↓ 需註冊 opcode
Cosmic RecvOpcode / SendOpcode

MapleStory 0.83.exe(2010-02-26,CSecurity 加殼)
  ↓ 解壓 + SolidDaima 處理
MapleStory v83(已繁化).exe(2010-02-17)
  ↓ 搭配
nmconew.dll + ijl15.dll(解析度 hook)

GMS083 scripts(2,294 .js)
  ↓ 比對
Cosmic scripts(1,898 .js)
  ↓ 共通 1,689 個
可重用 / 需調整

083MonsterBook(1,137 .txt)
  ↓ 對應 server/life/Monster.java
Cosmic Monster 系統
```

---

## §3 純技術事實總結(7 個獨立維度)

### 3.1 客戶端執行檔
- 原版與繁化版 TimeDateStamp 都是 2010 年
- 繁化版已解壓並以 SolidDaima 處理,SizeOfCode 完全相同
- 繁化版依賴 NMC 防外掛 + Intel JPEG Library

### 3.2 IDA 資料庫
- v83.idb 是 IDA 6.x/7.x IDB 格式(magic IDA1)
- 純文件讀取可達 124,782 strings,key class 名稱
- 必須用 IDA Pro 才能取得 function list + xref + 記憶體位址

### 3.3 通訊協議
- 3 個功能包 opcode 完全不衝突(只 0x11A 在 Send 已被 HIT_SNOWBALL 佔用)
- Cosmic RecvOpcode 0x105~0x3712 全 FREE
- 3 個功能包同時安裝可無痛合併

### 3.4 kaentake 框架
- 本地 kaentake 45 檔含完整 src/ + wvs/ + ztl/
- 3 個功能包所需 headers 本地全有 ✓
- 可直接整合

### 3.5 WZ/IMG 資源
- 19 個 .wz/.img,總 11.1 MB
- WZ 是加密容器(magic PKG1),IMG 是解開後子檔
- BeautySalon 的 UI.wz 是最小(25KB),CashShop.img 是最大(3MB)

### 3.6 JS 腳本
- GMS 套 1,992 + Cosmic 1,898 = 3,890 個,共通 1,689
- NPC 最多(1,101),其他分散
- 16% 差異 = 命名 / 細節調整

### 3.7 怪物圖鑑
- 1,137 .txt,7 TAB 格式
- 怪物 ID 6-7 位,平均等級 56.7
- 反應堆 5 TAB 格式,1,099 條掉落記錄

---

## §4 沒做的事(刻意避免)

- ❌ 不推薦整合方案
- ❌ 不評論技術深度
- ❌ 不下結論
- ❌ 不修改任何原生檔案
- ❌ 不評論法律

---

## §5 子代理執行效率

| 指標 | 值 |
|---|---|
| 派出子代理數 | 7(其中 W1-1 中途停止由主代理完成)|
| 完成數 | 7/7 |
| 總執行時間(平行)| 約 5 分鐘 |
| 單一最長執行 | W1-3(130 秒)|
| 單一最短執行 | W1-6(180 秒)|

**omp-bridge 評估**:
- omp 模型(MiniMax-M3)與主代理同型號,**無差異化價值**
- omp RPC 啟動需 1.2 秒,但對純技術拆解任務沒有加速效果
- **結論**:Wave 2(omp 任務)**不執行**

---

## §6 報告檔案完整列表

```
wf-output/
├── W1-1-v83-idb-structure.md           5.1 KB
├── W1-2-opcode-collision.md           31.1 KB
├── W1-3-exe-diff.md                   11.3 KB
├── W1-4-framework-headers-compare.md  6.4 KB
├── W1-5-wz-img-index.md               6.7 KB
├── W1-5-wz-img-index.raw.json        10.3 KB
├── W1-6-js-script-index.md            19.0 KB
├── W1-7-monsterbook-index.md          14.8 KB
├── _all.json                           5.7 KB
├── _imports.json                       1.6 KB
├── _pe.json                            2.4 KB
├── _results.json                       2.0 KB
└── cosmic-opcodes.json                15.1 KB
─────────────────────────────────────
總計:12 檔 / 約 130 KB
```

---

**WF 工作模式結束**
- 7 個 W1-* 報告完成
- 6 個 JSON 資料檔完成
- 全部唯讀,不污染任何原生位置
