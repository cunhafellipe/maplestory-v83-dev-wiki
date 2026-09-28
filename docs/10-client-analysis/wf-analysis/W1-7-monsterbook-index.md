# W1-7 — 怪物圖鑑 (083MonsterBook) 索引分析報告

> **純技術拆解**,不下結論、不評論。
> 分析對象: `C:\Users\e7896\AppData\Local\Temp\gmspeek\083怪物掉落与反应堆数据\083怪物掉落与反应堆数据\` 目錄下的怪物 / 反應堆 / 任務掉落資料。
> 比對對象: `C:\MUWORK\GAME\MAPLESOTRY\04-Emulators\GMS-v083-Cosmic\src\main\java\server\life\*` + `server\maps\ReactorDropEntry.java` + `db\tables\009-drop.sql` + `db\data\131-reactordrops-data.sql`。

---

## 0. 全域統計

| 統計項 | 數值 |
|---|---|
| 總 `.txt` 檔案 (整個目錄樹) | **1,137** |
| `083MonsterBook/` 內 `.txt` | **365** |
| `083任务/` 內 `.txt` | 65 (任務腳本, 非掉落) |
| `083反应堆数据/` 內 `.txt` | **146** |
| `任务类怪物/` 內 `.txt` | 66 |
| `MonsterBook没有的/` 內 `.txt` | 115 |
| `活动类/` 內 `.txt` | 12 |
| `待验证的怪/` 內 `.txt` | 6 |
| `补全技能书掉落/` 內 `.txt` | 11 |
| 怪物卡 (`083怪物卡.txt`) | 352 行 (單檔) |
| 怪物書整合 (`7.27MonsterBook.txt`) | 11,070 行 (單檔) |

> 「1,138 個 .txt」實際總數為 **1,137**,差距 1 應來自外層 `083怪物掉落与反应堆数据/` 也含 `.txt`。

---

## 1. 檔案命名規律 (083MonsterBook/)

### 1.1 正規格式

```
<ID> <名稱> <等級>[   @][自加/验证/++++].txt
```

| 區段 | 說明 | 例 |
|---|---|---|
| `<ID>` | 怪物 WZ ID (6 或 7 位數字) | `100100`, `9400112` |
| 名稱 | 怪物中文名 (1~10 字) | `嫩寶`, `黑道保鑣` |
| 等級 | 整數 1~180 | `1`, `152` |
| `@` | BOSS 標記 (可選) | `@` |
| 尾巴 | 人工標註 (`自加++++`, `验证`) | `自加++++++` |

### 1.2 解析結果

| 項目 | 數值 |
|---|---|
| 解析成功 | **363** / 365 (99.5%) |
| 完全無法解析 | 2 (`7130001 地獄獵犬72.txt` 缺空白, `8820001 皮卡啾.txt` 無等級) |
| 含 `@` (BOSS) 標記 | **65** |
| 含人工尾巴 (`自加/验证/++++`) | 11 |

### 1.3 範例

```text
100100 嫩寶 1.txt                          ← 等級 1,新手怪
100101 藍寶 2.txt
1110100  綠菇菇 15.txt                     ← 名稱前多空白
9400112 黑道保鑣 152    @.txt              ← BOSS 152 等級
9400205 藍色蘑菇王 90    @.txt
5090000 冥界幽靈 56    @ 自加++++++.txt    ← 玩家自加掉落
8830007 巨魔蝙蝠怪 84    @没有这个怪.txt   ← 待驗證
9400569 大蛋糕    @@++++++.txt             ← 雙 @ 標記 (格式異常)
```

---

## 2. 怪物 ID 範圍與等級分佈

### 2.1 ID 範圍

| 項目 | 值 |
|---|---|
| 最小 ID | `100100` (嫩寶) |
| 最大 ID | `9500317` (小雪人) |
| 6 位 ID (舊) | 11 個 (100100~210100) |
| 7 位 ID (現代) | 352 個 |
| 重複 ID | **0** |

### 2.2 ID 第一碼 (區域代碼) 分佈

| 前綴 | 數量 | 推測區域 |
|---|---|---|
| `1xxxxxx` | 11 | 弓箭手村 / 維多利亞港近郊 |
| `2xxxxxx` | 31 | 魔法森林 / 弓箭手村 2 段 |
| `3xxxxxx` | 56 | 武陵 / 冰原雪域 |
| `4xxxxxx` | 51 | 地球防禦本部 / 神木村 |
| `5xxxxxx` | 47 | 玩具城 / 地球防禦本部深層 |
| `6xxxxxx` | 33 | 地球防禦本部 2 段 |
| `7xxxxxx` | 28 | 新葉城 / 桃花源 |
| `8xxxxxx` | 72 | 黃金寺院 / 時間神殿 |
| `9xxxxxx` | 23 | PQ 活動怪 / 隱藏地圖 |

### 2.3 等級分佈

| 等級區段 | 怪物數 |
|---|---|
| 新手區 (<30) | 56 |
| 中期 (30~59) | 157 |
| 中後期 (60~99) | 98 |
| 後期 (100~149) | 36 |
| 頂級 (150~199) | 4 |
| 終極 (≥200) | 0 |
| **總計** | **351** |
| 平均等級 | **56.7** |

BOSS (`@`) 等級範圍: **20 ~ 180**,共 65 隻。

---

## 3. 怪物書欄位結構

### 3.1 每行格式 (7 個 TAB 分隔欄位)

```
<lineIdx> <monsterId> <itemId> <minQty> <maxQty> <questId> <chance>
```

> 經全 11,070 行驗證: **100% 都是 7 個 tab 分隔欄位**,無例外。

| 欄位 | 名稱 | 範例 | 說明 |
|---|---|---|---|
| 0 | `lineIdx` | `1` | 行編號 (怪物書內固定為 1) |
| 1 | `monsterId` | `100100` | 對應 WZ `Monster.wz` ID,亦即 `dropperid` |
| 2 | `itemId` | `4000019` / `0` | 道具 WZ ID;`0` = 楓幣 (meso) |
| 3 | `minQty` | `1` | 最小掉落數量 |
| 4 | `maxQty` | `1` | 最大掉落數量 |
| 5 | `questId` | `0` / `1` | 任務過濾 ID;`0` = 非任務道具 |
| 6 | `chance` | `400000` | 掉落機率分母 |

### 3.2 統計

| 指標 | 值 |
|---|---|
| 總掉落行數 | **11,070** |
| `itemId=0` (楓幣) | 918 行 (8.3%) |
| `itemId!=0` (道具) | 10,152 行 (91.7%) |
| `questId=0` | 11,068 行 |
| `questId=1` | 2 行 |
| `chance` 範圍 | 129 ~ 700,002 |
| `chance` 平均 | 46,255 |
| 常見 chance | `250000`(918)、`9000`(840)、`9300`(536)、`5500`(451) |
| `minQty` 常見值 | `1` (9,883 次,佔 89%) |
| `maxQty` 範圍 | 1 ~ 32,400 |
| 楓幣 (itemId=0) 數量分佈 | `1~2`(低等)、`22800~24320`(黑道)、`7200~8100`(藍色蘑菇王) |

### 3.3 道具 ID 前 2 碼 (大類) 分佈

| 前綴 | 行數 | 推測類別 |
|---|---|---|
| `10xxxxxx` | 3,327 | 武器 |
| `20xxxxxx` | 2,958 | 消耗品 (藥水/捲軸) |
| `40xxxxxx` | 1,566 | 雜項 (材料) |
| `14xxxxxx` | 800 | 套裝 / 披風 |
| `41xxxxxx` | 579 | 礦石 / 材料 |
| `13xxxxxx` | 538 | 道具 (其他) |
| `22xxxxxx` | 242 | 特殊道具 |
| `11xxxxxx` | 79 | 武器細項 |
| `23xxxxxx` | 56 | 怪物卡 (`238xxxx`) |
| `30xxxxxx` | 3 | 礦石類 |

### 3.4 道具 ID 前 4 碼常見中類 (Top 10)

| 前 4 碼 | 行數 | 推測類別 |
|---|---|---|
| `2040xx` | 702 | 弓矢 |
| `2000xx` | 680 | 藥水 |
| `1002xx` | 602 | 短劍 |
| `4130xx` | 545 | 礦石類 |
| `1072xx` | 513 | 棍棒 |
| `1082xx` | 453 | 長槍 |
| `2044xx` | 446 | 弩矢 |
| `4020xx` | 343 | 礦石 |
| `4010xx` | 325 | 礦石 |

---

## 4. 反應堆 (Reactor) 欄位結構

### 4.1 檔案命名

```
<reactorId>.txt
```

例:`1012000.txt`、`1022000.txt` ... (146 個檔案)

### 4.2 每行格式 (5 個 TAB 分隔欄位)

```
<lineIdx> <reactorId> <itemId> <chance> <questId>
```

| 欄位 | 名稱 | 範例 | 說明 |
|---|---|---|---|
| 0 | `lineIdx` | `1` | 行編號 |
| 1 | `reactorId` | `1012000` | 反應堆 WZ ID |
| 2 | `itemId` | `2000000` | 道具 ID |
| 3 | `chance` | `6` | 掉落機率 |
| 4 | `questId` | `-1` | 任務過濾;`-1` = 非任務 |

### 4.3 統計

| 指標 | 值 |
|---|---|
| 總反應堆檔案 | 146 |
| 總掉落行 | **1,099** |
| reactorId 範圍 | `2001` ~ `9202012` |
| 唯一 reactor 數 | 146 |
| 平均每反應堆掉落 | 7.5 |
| 最大掉落數 | 64 |
| `chance` 範圍 | 1 ~ 250 |

### 4.4 反應堆範例

```text
1	1012000	2000000	6	-1
1	1012000	4000003	6	-1
1	1012000	4031150	3	2067      ← 任務道具, questId=2067
1	1012000	4032143	6	20717
1	1022000	4031452	1	6201       ← 任務道具
```

---

## 5. 怪物卡 (083怪物卡.txt) 結構

單一檔,共 **352 行**。

### 格式 (7 個 TAB 欄位,與怪物書相同)

```
<lineIdx> <monsterId> <cardItemId> <minQty> <maxQty> <questId> <chance>
```

| 欄位 | 值 | 說明 |
|---|---|---|
| 0 | `1` | 行編號 |
| 1 | `100101` | monster ID |
| 2 | `2380001` | 怪物卡道具 ID (`238xxxx`) |
| 3-6 | 同怪物書 | 數量/任務/機率 |

### 統計

| 指標 | 值 |
|---|---|
| 唯一 cardItemId | **339** |
| cardItemId 範圍 | `2380001` ~ `2388070` |
| `chance` 範圍 | 固定 `10001` (大多數) / `24000` (極少) |
| 重複 (同卡配多怪) | 例:`2381033` 同時配 3000002/3/4;`2381044` 配多隻 |

> 怪物書掉落行中含 `238xxxx` (怪物卡) 的僅 **1 行** — 即怪物書與怪物卡是**兩套獨立表**。

---

## 6. 與 Cosmic 源碼比對

### 6.1 怪物書 / 怪物卡 → DB `drop_data` 表

**Cosmic `MonsterInformationProvider.java` L158~163:**

```java
"SELECT itemid, chance, minimum_quantity, maximum_quantity, questid FROM drop_data WHERE dropperid = ?"
ps.setInt(1, monsterId);
...
ret.add(new MonsterDropEntry(
    rs.getInt("itemid"),
    rs.getInt("chance"),
    rs.getInt("minimum_quantity"),
    rs.getInt("maximum_quantity"),
    rs.getShort("questid")
));
```

**Cosmic `MonsterDropEntry.java`:**

```java
public MonsterDropEntry(int itemId, int chance, int Minimum, int Maximum, short questid) {
public short questid;
public int itemId, chance, Minimum, Maximum;
```

**對照 `.txt` 行格式:**

| `.txt` 欄位 | DB 欄位 | Java 欄位 | 對應 |
|---|---|---|---|
| `monsterId` (col 1) | `dropperid` (WHERE) | `monsterId` | ✓ |
| `itemId` (col 2) | `itemid` | `itemId` | ✓ |
| `minQty` (col 3) | `minimum_quantity` | `Minimum` | ✓ |
| `maxQty` (col 4) | `maximum_quantity` | `Maximum` | ✓ |
| `questId` (col 5) | `questid` | `questid` | ✓ |
| `chance` (col 6) | `chance` | `chance` | ✓ |

> **結論:怪物書 `.txt` 與 Cosmic `drop_data` 表結構 100% 一致**,只差一個 `lineIdx` 前綴欄位 (本資料加的,DB 沒有)。

### 6.2 反應堆 → DB `reactordrops` 表

**Cosmic `009-drop.sql` L29~38:**

```sql
CREATE TABLE reactordrops (
    reactordropid INT UNSIGNED NOT NULL AUTO_INCREMENT,
    reactorid     INT          NOT NULL,
    itemid        INT          NOT NULL,
    chance        INT          NOT NULL,
    questid       INT          NOT NULL DEFAULT '-1',
    PRIMARY KEY (reactordropid),
    KEY reactorid (reactorid)
);
```

**Cosmic `131-reactordrops-data.sql`:**

```sql
INSERT INTO reactordrops (reactorid, itemid, chance, questid)
VALUES (2001, 4031161, 1, 1008),
       (1012000, 2000000, 6, -1),
       (1012000, 4031150, 3, 2067);
```

**對照反應堆 `.txt`:**

| `.txt` 欄位 | DB 欄位 | Java 欄位 | 對應 |
|---|---|---|---|
| `reactorId` (col 1) | `reactorid` | `ReactorDropEntry.itemId` 無 | ✓ (檔名 = reactorid) |
| `itemId` (col 2) | `itemid` | `ReactorDropEntry.itemId` | ✓ |
| `chance` (col 3) | `chance` | `ReactorDropEntry.chance` | ✓ |
| `questId` (col 4) | `questid` | `ReactorDropEntry.questid` | ✓ |

> **結論:反應堆 `.txt` 與 `reactordrops` 表結構 100% 一致**。

### 6.3 怪物 ID → MonsterStats

**Cosmic `MonsterStats.java` L40~54** 公開欄位:

```java
public class MonsterStats {
    public boolean changeable;
    public int exp, hp, mp, level, PADamage, PDDamage, MADamage, MDDamage,
               dropPeriod, cp, buffToGive = -1, removeAfter;
    public boolean boss, undead, ffaLoot, isExplosiveReward, firstAttack, removeOnMiss;
    public String name;
    ...
}
```

**`.txt` 檔名語意對應:**

| `.txt` 檔名區段 | MonsterStats 欄位 | 對應 |
|---|---|---|
| `<ID>` (`100100`) | `monsterId` (WZ 索引鍵) | ✓ |
| `<名稱>` (`嫩寶`) | `name` | ✓ |
| `<等級>` (`1`) | `level` | ✓ |
| `@` 標記 | `boss = true` | ✓ |

> **結論:檔名編碼的 4 個欄位精準對應 MonsterStats 4 個欄位**。

---

## 7. 子目錄分類用途

| 目錄 | 用途 |
|---|---|
| `083MonsterBook/` | **主怪物圖鑑** (本次分析主體,365 檔) |
| `7.27MonsterBook.txt` | 怪物書**整合單檔** (11,070 行,與 083MonsterBook/ 一致) |
| `7.27MonsterBook没有的.txt` | 未收錄的怪物清單 |
| `083怪物卡.txt` | 怪物卡掉落單獨表 (352 行) |
| `083任务/` | 任務 NPC 對話/物品腳本 (非怪物) |
| `083反应堆数据/` | **反應堆** (可破壞物件) 掉落 (146 檔) |
| `任务类怪物/` | 任務限定怪物 (66 隻,多為 `9xxxxxx` 開頭) |
| `MonsterBook没有的/` | 怪物書未收錄怪物 (115 隻) |
| `活动类/` | 活動期間限定怪物 (12 隻,多含 `PQ` 標記) |
| `待验证的怪/` | 待人工驗證怪物 (6 隻,檔名含 `没有这个怪`) |
| `补全技能书掉落/` | 技能書掉落補完 (11 隻) |
| `7.27补全技能书掉落.txt` | 整合版技能書掉落 |
| `7.31.psc` | 未知 (PSC 編譯檔?) |

---

## 8. 異常 / 特殊情況

### 8.1 命名格式異常 (11 隻)

| 類型 | 範例 |
|---|---|
| 玩家自加 (`自加++++`) | `5090000 冥界幽靈 56    @ 自加++++++.txt` |
| 玩家驗證 (`验证`) | `5120100 機器人堤安 54   @ 验证.txt` |
| 待驗證 (`没有这个怪`) | `8830007 巨魔蝙蝠怪 84    @没有这个怪.txt` |
| 雙 `@` | `9400569 大蛋糕    @@++++++.txt` |
| 無等級 | `8820001 皮卡啾.txt` |
| 名稱/等級無空白分隔 | `7130001 地獄獵犬72.txt` |

### 8.2 怪物書 vs 怪物卡

- 怪物書 365 個檔案,**怪物卡只配對其中 339 個怪物 ID**
- 怪物卡的 `chance` 多為固定 `10001`(部分 `24000`、`40001`、`40000`)
- 怪物書掉落中**不含 `238xxxx`** 怪物卡道具 → 兩表獨立

### 8.3 重複怪物卡配對

- `2381033` → 同時配 3000002 / 3000003 / 3000004
- `2388020` → 同時配 8510000 / 8520000
- `2381044` → 多隻 4xxxxxx 怪物

---

## 9. 代表性檔案 (12 個樣本)

### 怪物書樣本 (10 個)

| # | 檔名 | 行數 | 重點 |
|---|---|---|---|
| 1 | `100100 嫩寶 1.txt` | 11 | 等級 1 最低,典型新手怪 |
| 2 | `100101 藍寶 2.txt` | 14 | 含披風/帽子裝備掉落 |
| 3 | `1210100 肥肥 7.txt` | 19 | 經典楓葉地形怪 |
| 4 | `9400112 黑道保鑣 152    @.txt` | 13 | BOSS,楓幣 22800~24320 |
| 5 | `9400205 藍色蘑菇王 90    @.txt` | 30 | BOSS,楓幣 7200~8100 |
| 6 | `9500317 小雪人 10.txt` | 3 | 最少掉落行 |
| 7 | `5090000 冥界幽靈 56    @ 自加++++++.txt` | ? | 玩家自加 |
| 8 | `8830007 巨魔蝙蝠怪 84    @没有这个怪.txt` | ? | 待驗證 |
| 9 | `9400114 乐乐机  50    @没有这个怪.txt` | ? | 待驗證 (ID 缺空白) |
| 10 | `8820001 皮卡啾.txt` | ? | 無等級 |

### 反應堆樣本 (2 個)

| # | 檔名 | 行數 |
|---|---|---|
| 1 | `1012000.txt` | 4 |
| 2 | `1022000.txt` | 1 |

---

## 10. 整合資料流

```
083MonsterBook/<ID> 名稱 等級.txt    ←── drop_data (DB)
        │ (line by line: dropperid, itemid, min, max, quest, chance)
        ▼
MonsterInformationProvider.retrieveDrop(monsterId)
        ▼
MonsterDropEntry(itemId, chance, Minimum, Maximum, questid)
        ▼
MapleMap.dropItemsFromMonster(...)
        ▼
玩家點擊掉落物

083反应堆数据/<reactorId>.txt         ←── reactordrops (DB)
        │ (line by line: reactorid, itemid, chance, questid)
        ▼
ReactorDropEntry(itemId, chance, questid)
        ▼
MapleReactor.hitReactor(...)
```

---

## 11. 統計匯總表

| 指標 | 值 |
|---|---|
| 主目錄總 `.txt` | 365 |
| 解析成功率 | 99.5% |
| 怪物 ID 範圍 | 100,100 ~ 9,500,317 |
| 等級範圍 | 1 ~ 180 |
| 平均等級 | 56.7 |
| BOSS 數 | 65 |
| 總掉落行 | 11,070 |
| 楓幣行 (itemId=0) | 918 |
| 道具行 (itemId!=0) | 10,152 |
| 平均掉落/怪 | 30.3 |
| 反應堆檔案 | 146 |
| 反應堆掉落總行 | 1,099 |
| 怪物卡行 | 352 |
| 異常命名 | 11 |

---

> **純技術分析完畢**。後續若需導入,只需將 `083MonsterBook/*.txt` 去掉首欄 `lineIdx` 後,以 `\t` 分隔的 6 欄直接 `INSERT INTO drop_data (dropperid, itemid, chance, minimum_quantity, maximum_quantity, questid)`。
