# W1-6 JS 腳本索引

> 來源:`<MAPLESOTRY>\待分類\GMS083客戶端\scripts脚本.rar`
> 解壓位置:`<USERPROFILE>\AppData\Local\Temp\peek_gms\scripts脚本\scripts\`
> 對照目標:Cosmic `<MAPLESOTRY>\04-Emulators\GMS-v083-Cosmic\scripts\`
> 本文件**僅做技術拆解與索引**,不評論內容品質。

---

## 1. 數量統計

| 項目 | 數值 |
|---|---|
| RAR 內 entries | 2,335 |
| `.js` 檔(已解壓) | **2,294** |
| 其他(`.txt` / 子目錄佔位 / nested `.rar`) | 41 |
| **總行數** | **108,689** |
| **總位元組** | **2,920,153** (≈2.79 MB) |

> 用戶口述為 2,297 — 實際差異來自 41 個非 `.js` 條目(子目錄佔位 17、`.txt` 1、嵌套 `.rar` 3 等)。`.js` 實數為 2,294。

### 編碼分佈

| 編碼 | 檔數 |
|---|---|
| GBK / CP936(繁體中文) | 1,441 |
| UTF-8(英文) | 853 |

GBK 比例 ≈ 63%,主要出現在 NPC(繁體中文 NPC 名)、副本/嘉年華/女神之塔/家族對抗等子資料夾。

---

## 2. 目錄分類與檔案分布

```
scripts/
├── NPC Base.js          1  (1,824 B,    58 行) — NPC 通用樣板
├── QUEST Base.js        1  (1,880 B,    71 行) — 任務通用樣板
├── REACT Base.js        1  (  961 B,    28 行) — 反應堆通用樣板
├── event/             108  (415,343 B, 17,147 行) — 活動/PQ/Boss
├── item/                2  (  3,714 B,   113 行) — 道具腳本
├── map/                72  ( 24,785 B,  1,134 行) — 地圖事件腳本
├── npc/             1,101  (1,821,961 B, 61,665 行) — NPC 對話
├── portal/            409  (161,507 B,  7,544 行) — 傳點腳本
├── quest/             330  (406,336 B, 16,730 行) — 任務腳本
└── reactor/           269  ( 81,842 B,  4,199 行) — 反應堆腳本
```

### 2.1 子結構(npc/ 內部分類)

```
npc/
├── 純數字 ID (.js 檔, 主體)    ≈ 920 檔
└── npc分类/                     424 檔(繁中分類)
    ├── 副本/                  341 檔
    │   ├── 女神之塔/         57
    │   ├── 绯红/             53
    │   ├── 家族对抗/         49
    │   ├── 婚礼村/           34
    │   ├── 毒物森林/         22
    │   ├── 罗密欧/           22
    │   ├── 玩具塔101/        21
    │   ├── 朱丽叶/           21
    │   ├── 海盗船/           19
    │   ├── 嘉年华/           18
    │   ├── 废弃/              9
    │   ├── 盖福克斯的宝藏/    7
    │   ├── 阿里安特竞技场/    5
    │   └── 月妙/              3
    ├── 美容美发/              54
    ├── 制造/                  22
    └── 探险队/                 7
```

### 2.2 子結構(quest/ 內部分類)

```
quest/
├── 純數字 ID .js (主體)       ≈ 219 檔
├── 职业任务/                  102
│   ├── 战神任务/             57
│   └── 骑士团/               45
└── 过期任务/                    9
```

### 2.3 子結構(map/、event/)

```
map/
├── onUserEnter/        70  (map.onUserEnter 觸發器)
└── onFirstUserEnter/    2  (首次進入觸發器)

event/                  108 全部直接列在 event/ 下,不再分子資料夾
```

### 2.4 入口函式分布

| 目錄 | 主要入口 | 比例 |
|---|---|---|
| `event/` | `init` | 108/108 (100%) |
| `map/` | `start`(實作 onUserEnter 觸發) | 72/72 |
| `npc/` | `start` + `action` | 843 個含 `start`、621 個含 `action` |
| `quest/` | `start` | 254/330 |
| `portal/` | `enter` | 409/409(由 557 個 `enter` 計算) |
| `reactor/` | `act` | 339/269(部分具多個) |

`event/` 的 108 個腳本,**每個都實作**以下 17 個事件生命週期函式(共 108 × 17 = 1,836 命中):

```
init, setup, afterSetup, playerEntry, playerExit,
allMonstersDead, monsterKilled, monsterValue,
playerDisconnected, playerDead, playerRevive,
changedMap, changedLeader, leftParty, disbandParty,
clearPQ, scheduledTimeout, cancelSchedule, dispose
```

說明:`event/` 全為 PQ / Boss 戰 / 副本流程,**共享同一個 HeavenMS / OdinMS 模板**。

---

## 3. 檔名特徵統計

| 特徵 | 數量 |
|---|---|
| 純數字檔名(`1002000.js`、`2001000.js`) | 1,512(65.9%) |
| 含繁體中文檔名 | 76(3.3%) |
| 含半形空格(多為中文後綴) | 74(3.2%) |
| 含特殊符號(非中英數 `.` `-` `_` 空白) | 5 |
| 大小寫混合英文檔名(`gachapon.js`、`scroll_generator.js`) | 約 600 |

### 3.1 命名類型樣本

| 類型 | 範例 |
|---|---|
| NPC ID 直命名 | `1002000.js`、`2001000.js`、`9201100.js` |
| 同 ID 多版本 | `9010000.js`、`9010000_1.js`、`9010000_2.js`、`9010000_3.js`、`9010000_4.js`(美容) |
| 英文語意命名 | `gachapon.js`、`scroll_generator.js`、`waterOfLife.js`、`commands.js`、`mapleTV.js`、`credits.js`、`changeName.js`、`cpqchallenge.js`、`cpqchallenge2.js` |
| 繁中後綴 | `1022101兑换枫叶.js`、`9105004 雪人.js`、`9000011 马丁.js`、`9000012 G★椰子比赛.js`、`2032002 奥拉.js`、`1300013 東側城塔大門.js`、`1102003 骑士殿堂.js`、`9900000 GM.js`、`9900001 GM.js` |
| 標記註記型 | `BalrogBattle_Easy 暂时没有.js`、`AreaBossZeno 待定 3457.js`、`1092019 喬納森的房間.js`、`2022004 完成保護泰勒斯.js`、`9201033 Simon 没有整个NPC.js` |
| 標記型(Chinese + '删除/无/不需要') | `PupeteerPassword删除.js`、`MaybeItsGrendel_end 删除.js`、`2042009 没有.js`、`kpq4 无.js`、`party3_r4pt1 无.js` |
| 用途說明型 | `1052115 廢棄的地鐵月台.js`、`2103013 金字塔山丘.js`、`28004 保護雪人!.js`、`29400 精明的獵人.js`、`4647 訓練師的秘方.js`、`8185 寵物的進化2.js`、`8189 寵物的再進化.js`、`空间 gagga_success 太空佳佳.js` |
| `raid_*` 多語言版 | `raid_rest.js`、`raid_rest 第一個休息處.js`、`raid_stage.js`、`raid_stage 階段1&lt;紅寶王&gt;.js` |
| 多語言 URL-encode | `raid_stage 階段1&amp;lt;紅寶王&amp;gt;.js`(`&amp;lt;` = `&lt;` HTML 雙重轉義) |

---

## 4. 代表性腳本(10 個)內容分析

> 抽樣策略:最大檔 + 特殊命名 + 各目錄代表 + GM/活動/範本

### 4.1 `npc/npc分类/副本/嘉年华/2042000.js` (20,298 B / 505 行)

- **入口**: `function start(mode, type, selection)`
- **輔函式**: `action`、`getRefineFee`、`isRefineTarget`、`getRockRefineTarget`、`refineItems`、`refineRockItems`
- **標頭宣告**: 名字 `休彼德蔓`,地圖 `玩具城`,描述 `220000000`
- **用到地圖 ID**: `980000000`(CPQ 大廳)、`980030000`(嘉年華)
- **GM/管理**:含 `isGM` 檢查(允許 GM 跳過條件)
- **事件/活動邏輯**: 無
- **類型**:副本/嘉年華 NPC — 礦石升級精煉師(Heav enMS 加分風格,Ronan 加的副本輔助 NPC)

### 4.2 `npc/9977777.js` (19,889 B / 371 行)

- **入口**: `start`(輔以 `action`)
- **輔函式**: 18 個,包含 `addFeature`、`writeFeatureTab_PQs`、`writeFeatureTab_Skills`、`writeFeatureTab_Quests`、`writeFeatureTab_PlayerSocialNetwork`、`writeFeatureTab_CashItems`、`writeFeatureTab_MonstersMapsReactors`、`writeFeatureTab_PQpotentials`
- **授權**:HeavenMS Copyleft (C) RonanLana 2016-2019,**GNU AGPL v3**
- **GM/管理**:含 `GM` 關鍵字
- **類型**:HeavenMS 內建「功能型 NPC」— 提供遊戲內查詢面板(任務、技能、PQ、社交、商城等分頁);**非原版 GMS 內容**,為伺服端擴充。

### 4.3 `npc/scroll_generator.js` (14,475 B / 439 行)

- **入口**: `start` + `action`
- **輔函式**: 21 個 — `getJobTierScrolls`、`getScrollTypePool`、`getScrollTier`、`getScrollSuccessTier`、`getAvailableScrollsPool`、`getLevelTier`
- **授權**:HeavenMS Copyleft RonanLana 2016-2019,**GNU AGPL v3**
- **類型**:職業卷軸製造 NPC(為天堂私服自製)

### 4.4 `npc/1022101兑换枫叶.js` (14,172 B / 227 行)

- **入口**: `start` + `action`
- **輔函式**: 無
- **授權**:OdinMS(C) Patrick Huy / Matthias Butz / Jan Christian Meyer,**GNU AGPL v3**
- **用到地圖 ID**: `209000000`
- **GM/管理**: 無
- **類型**:兌換楓葉 NPC — 對應 **GMS v83** 原版的 1022101(繁中本地化後綴)

### 4.5 `event/MagatiaPQ_A.js` (12,673 B / 427 行)

- **入口**: `init`(無 `start`/`action` — event 腳本標準入口)
- **輔函式**: 33 個,包含 `setLobbyRange`、`setEventRequirements`、`setEventExclusives`、`setEventRewards`、`getEligibleParty`、`setup`、`shuffle`、`afterSetup` 等完整 PQ 生命週期
- **標頭**: 名字 `茱麗葉`,地圖 `卡帕萊特祕密之室`,描述 `261000021`
- **用到地圖 ID**:`926110000`(進入)、`926110600`(區間)、`926110700`(結束);recruit `261000021`
- **GM/管理**: 無
- **事件/活動邏輯**: 完整 PQ — `setProperty` 世界狀態、`setLobbyRange` 同時 1 廳、`getEligibleParty` 隊伍資格(2-4 人、L71-85)
- **類型**:馬加提亞副本 **A 線**

### 4.6 `event/ZakumBattle.js` (4,897 B / 203 行)

- **入口**: `init`
- **輔函式**: 28 個(含 `setup`、`afterSetup`、`playerEntry`)
- **標頭**: 名字 `阿杜比斯`,地圖 `殘暴炎魔祭壇入口`,描述 `211042400`
- **用到地圖 ID**:`280030000`(祭壇入口/戰鬥)、`211042400`(退場/招募)
- **GM/管理**: 無
- **事件/活動邏輯**: Boss 戰 — `setProperty` 控制進度、`setEventRewards` 掉落表、`setEventExclusives`(1-30 人)
- **類型**:扎昆 Boss 戰入口腳本(對應 `npc\2032002.js` 入口 NPC)

### 4.7 `npc/commands.js` (2,347 B / 73 行)

- **入口**: `start` + `action`
- **輔函式**: `writeHeavenMSCommands`(命令表輸出)
- **標頭**: Name `Steward`,Map `Foyer`,Script `commands.js`(作者 Ronan + Vcoc)
- **GM/管理**:**是** — 列出 `Common / Donator / JrGM / GM / SuperGM / Developer / Admin` 7 級權限、`@` 玩家指令與 `!` 員工指令前綴
- **類型**:HeavenMS **命令清單 NPC**(門房對話視窗顯示)

### 4.8 `event/0_EXAMPLE.js` (5,184 B / 168 行)

- **入口**: `init`
- **輔函式**: 35 個 — 完整 PQ 樣板的所有 callback,作為活動腳本開發範本
- **類型**:**空白範本**(`// Event-instantiation variables` 註解,所有變數 `undefined`),由活動作者複製後填入

### 4.9 `npc/9900000 GM.js` (4,813 B / 98 行)

- **入口**: `start` + `action`
- **輔函式**: `pushIfItemExists`(髮型/臉型 menu 過濾)
- **標頭**: 名字 `KIN`,地圖 `工作场所`,描述 `180000000`(shotbow town 工作场所)
- **GM/管理**:無顯式 `isGM`,但檔名直接標 `GM` + NPC ID `9900000` 為 **GMS 自訂 GM 區塊**專用
- **類型**:韓版 GMS v83 自製 **GM 美容 NPC**(髮型/髮色/臉型選單,改 ID `9900000/9900001` 作為預留 GM NPC 區)

### 4.10 `npc/gachapon.js` (3,176 B / 73 行)

- **入口**: `start` + `action`
- **輔函式**: 無
- **授權**:OdinMS AGPL v3
- **GM/管理**: 無
- **事件/活動邏輯**: 無
- **類型**:標準轉蛋機 NPC(通用介面,所有轉蛋地點共用此檔)

---

## 5. GM / 管理指令統計

| 檔案 | 是否含 GM | 形式 |
|---|---|---|
| `npc/commands.js` | **是** | 顯式 `@` / `!` 指令前綴對話視窗 |
| `npc/9900000 GM.js` | 是 | GM 區 NPC 編號(9900000/9900001),檔名直接標 GM |
| `npc/9900001 GM.js` | 是 | 同上 |
| `npc/9977777.js` | 部分 | 含 `GM` 字串(HeavenMS 內建查詢面板) |
| `npc/2042000.js`(嘉年華) | 是 | `isGM` 條件檢查(允許 GM 跳過副本條件) |
| `npc/2081004.js` 等 | 部分 | 各 NPC 中有零星 `isGM` 判斷 |

> **`event/` 目錄中沒有顯式 GM 指令腳本**;`commands.js` 是集中式指令視窗。

---

## 6. 事件 / 活動邏輯統計

- `event/` 共 **108 個腳本**,**100% 使用 `init` 入口**,並實作 17 個共同生命週期 callback。
- 分類(由檔名識別):
  - **PQ / 副本**: `KerningPQ.js`、`LudiPQ.js`、`OrbisPQ.js`、`LudiMazePQ.js`、`MagatiaPQ_A/Z.js`、`PiratePQ.js`、`ElnathPQ.js`、`HenesysPQ.js`、`EllinPQ.js`、`CafePQ_1..6.js`、`HolidayPQ_1..3.js`、`BossRushPQ.js`、`CWKPQ.js`、`TreasurePQ.js`、`Hak.js`(?)
  - **Boss 戰**: `ZakumBattle.js`、`HorntailBattle.js`、`HorntailPQ.js`、`PapulatusBattle.js`、`PinkBeanBattle.js`、`Pianus.js`(portal)、`BalrogBattle.js`、`BalrogQuest.js`、`ScargaBattle.js`、`ShowaBattle.js`、`MahaBattle.js`、`LatanicaBattle.js`、`DelliBattle.js`、`ElementalBattle.js`、`GuardianNex.js`、`Cygnus_Magic_Library.js`、`DollHouse.js`、`NineSpirit.js`、`Puppeteer.js`、`RockSpirit.js`、`RockSpiritVIP.js`、`RescueGaga.js`、`KingPepeAndYetis.js`、`TD_Battle1..5.js`、`s4World.js`、`MK_PrimeMinister/2.js`
  - **小活動**: `2xEvent.js`、`3rdJob_bowman/magician/mount/pirate/thief/warrior.js`(三轉教材)、`4jaerial.js`、`4jship.js`、`4jsuper.js`、`AirPlane.js`(飛機)、`Boats.js`、`Trains.js`、`Subway.js`、`Cabin.js`、`Elevator.js`、`Genie.js`(精靈)、`AmoriaPQ.js`、`Hak.js`、`AreaBoss*`(18 隻區域王+計時器+城門)
  - **樣板 / 未實作**: `0_EXAMPLE.js`、`BalrogBattle_Easy 暂时没有.js`(空殼)、`AreaBossZeno 待定 3457.js`
- `map/` 共 72 個,**全為 `onUserEnter` 觸發器**(首次進入時執行劇情/動畫/任務推進),位於 `map/onUserEnter/` 與 `map/onFirstUserEnter/`。
- `portal/` 共 409 個,**全為 `enter` 觸發器**(子埠跳轉),但數個特殊 `rankDeveloperRoom.js` / `rankRoom.js` 帶有 GM 房功能。

---

## 7. Cosmic 對比(本地既有 scripts/)

### 7.1 對照表

| 目錄 | GMSpeek 檔數 | Cosmic 檔數 | 共同(以 `(目錄, 數字ID)` 比對) | GMS 獨有 | Cosmic 獨有 |
|---|---|---|---|---|---|
| `.` (root) | 3 | 4 | 3 | 0 | 1(`devtest.js`) |
| `event/` | 101 | 101 | 99 | 2 | 2 |
| `item/` | 2 | 2 | 2 | 0 | 0 |
| `map/` | 72 | 90 | 72 | 0 | **18** |
| `npc/` | 910 | 699 | 644 | **266** | 55 |
| `portal/` | 409 | 458 | 389 | 20 | **69** |
| `quest/` | 227 | 252 | 216 | 11 | **36** |
| `reactor/` | 268 | 292 | 264 | 4 | **28** |
| **小計** | **1,992** | **1,898** | **1,689** | **303** | **209** |

### 7.2 GMS 獨有的關鍵 NPC(304 個) — 大檔與類型

| 檔名 | 大小 | 性質 |
|---|---|---|
| `npc/scroll_generator.js` | 14,475 B | **HeavenMS 自製**職業卷軸製造 NPC |
| `event/BalrogBattle_Easy 暂时没有.js` | 7,810 B | Easy 難度未實作(空殼) |
| `npc/音乐播放.js` | 3,050 B | 音樂播放 NPC |
| `npc/2081004.js` | 2,634 B | 補上 Cosmic 缺的 NPC |
| `quest/29400 精明的獵人.js` | 2,234 B | 任務 29400 |
| `quest/29002 人氣王！.js` | 2,063 B | 任務 29002 |
| `quest/29503 捐獻王.js` | 1,667 B | 任務 29503 |
| `quest/29508 優秀社會人士.js` | 較小 | 任務 29508 |
| `quest/29900~29909,29924~29928.js` | ~14 個 | 連續任務 299xx 系列 |
| `quest/8222.js` | 1,537 B | 寵物再進化相關 |
| `event/AreaBossZeno 待定 3457.js` | 1,502 B | Zeno 王(待定) |
| `npc/道具回收.js` | 1,406 B | 自訂道具回收 |
| `npc/9010000_4.js` | 1,387 B | 美容 NPC 第 4 變體 |
| `npc/9977777.js` | 19,889 B | HeavenMS 自製多功能 NPC(Cosmic 沒有 9977777) |
| `npc/9900000/9900001 GM.js` | ~4.8 KB | GM 自訂 NPC(本地伺服管理用) |

### 7.3 GMS 獨有的中文後綴 NPC(典型樣本)

```
npc/1002103.js                          npc/1052012 馬龍.js
npc/1022101兑换枫叶.js                  npc/1052115 廢棄的地鐵月台.js
npc/1063011.js / 1063015.js             npc/1092019 喬納森的房間.js
npc/1102003 骑士殿堂.js                 npc/1202010 达人殿堂.js
npc/1204005/1204030/1204032.js          npc/1300010/1300011.js
npc/1300013 東側城塔大門.js             npc/2022004 完成保護泰勒斯.js
npc/2032002 奥拉.js                     npc/2081004.js
npc/2100002商店.js / 2100003商店.js     npc/2103013 金字塔山丘.js
```

### 7.4 GMS 獨有的 `npc/npc分类/副本/` 子樹(424 個 NPC)

完整子樹 — **Cosmic 完全沒有**這個分類層級。這 424 個檔案全為繁體中文分類版本,包含:

- `副本/嘉年华/` 18 檔(礦石精煉、CPQ 入口、月妙相關)
- `副本/女神之塔/` 57 檔(`party3_*` 副本流程 NPC)
- `副本/家族对抗/` 49 檔(含子資料夾 `反应堆/`)
- `副本/婚礼村/` 34 檔(`male00 婚礼村.js`、`Spacegaga_*`)
- `副本/毒物森林/` 22 檔
- `副本/罗密欧/` 22 檔
- `副本/朱丽叶/` 21 檔
- `副本/玩具塔101/` 21 檔
- `副本/海盗船/` 19 檔(含 `davy_next*` 系列)
- `副本/绯红/` 53 檔
- `副本/盖福克斯的宝藏/` 7 檔
- `副本/月妙/` 3 檔
- `副本/阿里安特竞技场/` 5 檔
- `副本/废弃/` 9 檔(標 `kpq4 无.js` 等)
- `美容美发/` 54 檔(髮型/臉型變體)
- `制造/` 22 檔(捲軸/道具製造)
- `探险队/` 7 檔

### 7.5 Cosmic 獨有的檔(典型樣本)

```
npc/1002008/1002009.js           npc/1012118.js
npc/1013001/1013002.js           npc/1013104.js
npc/1013200.js                   npc/1021002.js
npc/1022101_old.js               npc/1022104.js
npc/1029000.js                   npc/1032113.js
npc/1052113.js                   npc/10940.js
npc/1094000.js                   npc/1095001.js
npc/1096001~1096010.js           npc/11000.js
npc/1103005.js                   npc/200.js ~ 200003.js (低編號)
portal/08_xmas_out.js            portal/market18..22.js (新版)
quest/2001/2034/2124/2126.js 等  reactor/2408005.js 等
```

> Cosmic 比 GMS 多出 209 個獨立檔案,但 GMS 比 Cosmic 多 303 個。雙方**不對稱**,互補性高。

---

## 8. 摘要

| 指標 | 數值 |
|---|---|
| 總 `.js` | **2,294** |
| NPC | 1,101(其中 424 個有繁中子分類) |
| event | 108(100% PQ/Boss 模板) |
| portal | 409 |
| quest | 330(含 102 個職業任務子分類) |
| reactor | 269 |
| map | 72 |
| 含 `isGM` / GM 字串的腳本 | 約 8 個(`commands.js`、`9900000/9900001 GM.js`、`9977777.js`、`2042000.js`、各子分類零星) |
| 與 Cosmic 重複(以 `(top, numeric_id)` 比對) | **1,689** |
| **GMS 獨有** | **303** |
| **Cosmic 獨有** | **209** |
| 編碼 | GBK 1,441 + UTF-8 853 |

---

## 9. 重要觀察(僅列事實、不評論)

1. **RAR 內含 41 個非 `.js` 條目**(包括 nested `.rar`、`薑餅人.txt` 1 個、`.txt` 樣板檔等);實際 `.js` 為 **2,294**,非用戶口述的 2,297。
2. `event/` 目錄 108 個腳本**全部共享同一個 PQ 模板**(同 17 個 callback)。
3. `npc分类/` 子資料夾(424 檔)為本包**獨有**,Cosmic 無對應層級。
4. **HeavenMS 自製腳本**集中在:
   - `npc/scroll_generator.js`(14.4 KB)
   - `npc/9977777.js`(19.9 KB,功能面板)
   - `npc/commands.js`(2.3 KB,命令清單)
   - 授權:`(C) RonanLana 2016-2019, GNU AGPL v3`
5. **OdinMS 遺產腳本**(2008 Patrick Huy / Matthias Butz / vimes)是主體授權,內容多為 GMS v83 客戶端還原的 NPC/任務/反應堆。
6. 編碼 63% 為 GBK(繁中 NPC 對話與備註),37% 為 UTF-8(英文版與 HeavenMS 新增)。
7. `npc/9900000 GM.js` 與 `npc/9900001 GM.js` 為 **GMS 自訂 GM NPC**(檔名直接標 `GM`)。
8. 中文檔名後綴常見模式:`<ID> <中文名>.js`(76 個)或 `<ID><無空格中文>.js`,部分帶狀態註記(`删除`、`待定`、`无`、`不需要`)。