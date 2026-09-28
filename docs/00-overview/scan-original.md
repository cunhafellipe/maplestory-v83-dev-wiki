# 待分類資料夾 — 純技術掃描結果

> **掃描時間**: 2026-09-27
> **範圍**: `C:\MUWORK\GAME\MAPLESOTRY\待分類\` 全部 33 個檔案 + 22 個 RAR 解壓後內容
> **性質**: 純事實記錄,不下結論,不評論

---

## §0 總體規模

| 指標 | 值 |
|---|---|
| 根目錄檔案數 | 33 |
| 總大小 | 193 MB |
| 解壓後 RAR/7Z 內檔案總數 | 1,200+ |
| 子目錄 | `GMS083客戶端/`, `簽到表/` |

---

## §1 根目錄檔案分類(技術構成)

### 1.1 GMS v083 客戶端主程式

| 檔案 | 大小 | 識別 | 技術屬性 |
|---|---|---|---|
| `MapleStory 0.83.exe` | 4.28 MB | PE32 i386 GUI, 7 sections | **客戶端主執行檔** |
| ImageBase | 0x400000 | (PE header) | — |
| EntryPoint | 0xa8c000 | (PE header) | — |
| TimeDateStamp | 7,270,400 (≈2018) | (PE header) | **與 kaentake 目標版本一致** |

### 1.2 客戶端資源 + 補丁(壓縮格式)

| 檔案 | 大小 | 格式 | 解壓後內容 |
|---|---|---|---|
| `BeautySalonv83.zip` | 403 KB | ZIP(UNIX v2.0) | 42 個檔案:1 .cpp(46 KB)+ 7 reference headers + 4 .java + 2 SQL + 3 .wz(UI/String/Sound/Item)|
| `cashshop-window.7z` | 983 KB | 7-zip LZMA2:22 | 15 個檔案:1 .cpp(174 KB)+ 1 .h + 4 .java + 1 TSV(1843 商品)+ 2 .py + 1 .img + 1 .png + 2 README |
| `crit_and_range (1).7z` | 117 KB | 7-zip LZMA2:384k | 13 個檔案:5 .cpp + 2 .h + 1 .img(UIWindow)+ 1 .img(ToolTipHelp)+ 1 README |
| `v83.rar` | 20.2 MB | RAR5 | **1 個檔: `v83.idb`(125 MB,IDA 逆向工程資料庫,2014)|

### 1.3 GMS083客戶端子目錄(22 個 RAR 補丁包)

| RAR 檔名 | 大小 | 解壓後內容 |
|---|---|---|
| `083怪物掉落与反应堆数据.rar` | 506 KB | **1,138 個 .txt**(怪物圖鑑資料)|
| `Data 客户端可调分辨率.rar` | 9.4 MB | Data 目錄(客戶端 data) |
| `Etc.rar` | 182 KB | `Etc.wz`(1.2 MB 解壓)|
| `GMS083登录新界面.part1.rar` | 44 MB | 12 檔(含 5 個大 .img + 3 個 .png)|
| `GMS083登录新界面.part2.rar` | 42 MB | 7 檔(含 6 個 .img + 1 個 MapLogin.img)|
| `Quest.rar` | 182 KB | `Quest.wz`(5.5 MB 解壓)|
| `scripts脚本.rar` | 1.6 MB | **2,297 個 .js 腳本**(38 個目錄)|
| `String.rar` | 1.1 MB | `String.wz`(3.7 MB 解壓)|
| `UI.rar` | 30 MB | UI 資源 |
| `wz 客户端可调分辨率.rar` | 32 MB | wz 目錄(可調解析度版)|
| `主程序繁化 可调分辨率补丁.rar` | 3.6 MB | 8 檔:`MapleStory v83(已繁化).exe`(9.9 MB)+ `nmconew.dll` + `Gms.083.ini` + STREDIT .Net 工具 + CSV 繁化對照 |
| `多彩地图特效.rar` | 81 KB | `Data/Map/Tile/grassySoil.img` |
| `多彩地图特效2.rar` | 904 KB | `grassySoil.img.xml` + `颜色2.png` |
| `更正启动错误补丁 支持WZ，IMG端.rar` | 62 KB | 3 檔:`ijl15.dll` + `MapleFix.dll` + `MapleFix.ini` |
| `祝福混沌点卷掉落提示补丁.rar` | 919 KB | 3 個 .img(0204/0234/0403) |
| `原版商店 1024.rar` | 855 KB | `CashShop.img` + `CashShopPreview.img` |
| `原版商店 1280.rar` | 2.9 MB | 同上 |
| `新版商店1280-720.rar` | 1.4 MB | 同上 |
| `源码支持中文.rar` | 12 KB | **23 個 .txt**(Java 源碼修改片段):中文字符、組隊、公會、戰神動畫、新手出生地、拍賣按鍵、代碼顯示等 |

### 1.4 簽到表子目錄(獨立完整功能包)

| 子項 | 路徑 | 內容 |
|---|---|---|
| README.md | `簽到表/README.md` | 16.8 KB,完整 Daily Check-In 28 天安裝手冊 |
| 客戶端源碼 | `簽到表/client/src/dailycheckin.cpp` | 583 行 C++ |
| 服務端 handler | `簽到表/server/src/main/java/net/server/channel/handlers/DailyCheckinHandler.java` | 完整 Java handler |
| 服務端獎勵表 | `簽到表/server/src/main/java/server/DailyCheckinRewards.java` | Java 獎勵配置類 |
| GM 指令 | `簽到表/server/src/main/java/client/command/commands/gm0/CheckinCommand.java` | `@checkin` 指令 |
| SQL | `簽到表/server/sql/daily_checkin.sql` | 1.7 KB,加 3 欄位到 characters 表 |
| WZ | `簽到表/wz/UI.wz` | 25.4 KB,DailyCheckin 視窗資源 |

---

## §2 三個完整功能包技術構成(已逐個拆解原始碼)

### 2.1 Daily Check-In 簽到表(每日登入 28 天獎勵)

**檔案位置**: `簽到表/`

#### (a) 通訊協議

| 項目 | 值 |
|---|---|
| 客戶端→服務端 opcode | `0x11A`(RecvOpcode.DAILY_CHECKIN)|
| 服務端→客戶端 opcode | `0x17C`(SendOpcode.DAILY_CHECKIN)|
| 字串格式 | `writeShort(len) + bytes`(與 Cosmic `OutPacket.writeString` 一致)|

#### (b) 客戶端 C++ DLL(`dailycheckin.cpp` 583 行)

**硬碼記憶體位址**(image base 0x400000):

```cpp
kAddr_play_ui_sound           = 0x00989588
kAddr_ProcessBasicUIKey       = 0x00A07431
kAddr_CWvsContext_Instance    = 0x00BE7918
kAddr_ClientSocket_Instance   = 0x00BE7914
kAddr_ClientSocket_SendPacket = 0x0049637B
kAddr_ClientSocket_ProcessPkt = 0x004965F1
kAddr_CUtilDlg_Notice         = 0x009929DD
kAddr_get_basic_font          = 0x0098A707
kAddr_SetFont                 = 0x0046341A
```

**技術機制**:
- 派生自 `CWnd`(從 kaentake framework 的 `wvs/wnd.h`)
- 7×4 = 28 天格子 grid,繪圖基於 `UI/UIWindow.img/DailyCheckin/backgrnd`(513×346)
- 3 種狀態:locked(灰)/claimable(閃爍金邊)/claimed(綠+勾選)
- 從服務器推 snapshot,**客戶端從不決定 unlock/claim**
- 跨執行緒:`HandleSync` 在 receive thread 填資料 + mutex + flag,`Tick` 在 main thread 建 CWnd

#### (c) 服務端 Java

**3 個新檔**:
- `DailyCheckinHandler.java`(extends AbstractPacketHandler)
- `DailyCheckinRewards.java`(獎勵表,預設 mock = 每 1 meso + placeholder icon 2000000)
- `CheckinCommand.java`(gm0 等級指令)

**既有檔修改**(以 snippet 方式):
- `net/opcodes/RecvOpcode.java`:加 `DAILY_CHECKIN(0x11A)`
- `net/opcodes/SendOpcode.java`:加 `DAILY_CHECKIN(0x17C)`
- `net/PacketProcessor.java`:`registerHandler(...)`
- `tools/PacketCreator.java`:加 `dailyCheckinSnapshot(...)`
- `client/Character.java`:加 `checkinDay / checkinClaimed / checkinLastClaim` 3 欄位 + 6 個方法
- `net/server/channel/handlers/PlayerLoggedinHandler.java`:level gate ≥ MIN_LEVEL(預設 10)

#### (d) SQL

```sql
ALTER TABLE characters ADD COLUMN checkinDay int NOT NULL DEFAULT 0;
ALTER TABLE characters ADD COLUMN checkinClaimed int NOT NULL DEFAULT 0;
ALTER TABLE characters ADD COLUMN checkinLastClaim bigint NOT NULL DEFAULT 0;
```

(用 stored procedure 包 idempotent)

#### (e) 業務邏輯

- 24h epoch-millis gate:`CHECKIN_PERIOD_MS = 86_400_000L`
- 超過 48h 自動重置 streak
- Day 28 完成 → 開新 cycle
- Level gate:預設 MIN_LEVEL = 10

---

### 2.2 Beauty Salon 美容院(髮型/臉型/膚色儲存套用)

**檔案位置**: `BeautySalonv83/`

#### (a) 通訊協議

| 項目 | 值 |
|---|---|
| 雙向 opcode | `0x174`(RecvOpcode.BEAUTY_ACTION / SendOpcode.BEAUTY_RESULT)|
| 解鎖道具 | `5920000`(每個解 1 個 slot,0→6)|
| Tab | Hair / Face / Skin |
| Slot per tab | 6 |
| 動作類型 | REQUEST/SAVE/APPLY/DELETE/UNLOCK |

#### (b) 客戶端 C++(`beautyshop.cpp` 46 KB)

**技術構成**:
- 單一檔案 self-contained
- 自有 logger 寫 `beauty_debug.txt`(Windows handle,FILE_APPEND_DATA)
- VEH(Vectored Exception Handler)crash recovery
- 3 個 reference headers 來自 kaentake framework(`wvs/wnd.h` 等)

#### (c) 服務端 Java 結構

```
java/src/main/java/net/server/channel/handlers/BeautyHandler.java   5.2 KB
java/src/main/java/server/beauty/BeautyData.java                    226 B
java/src/main/java/server/beauty/BeautyPackets.java                 3.0 KB
java/src/main/java/server/beauty/BeautyStorage.java                 4.8 KB
java/src/main/resources/db/tables/025-beauty.sql                    968 B
java/src/main/resources/db/tables/026-beauty-unlock.sql             229 B
```

#### (d) 既有檔修改

- `net/opcodes/RecvOpcode.java`:加 `BEAUTY_ACTION(0x174)`
- `net/opcodes/SendOpcode.java`:加 `BEAUTY_RESULT(0x174)`
- `net/PacketProcessor.java`:import + `registerHandler(...)`
- `net/server/channel/handlers/GeneralChatHandler.java`:加 `@beauty` block
- `resources/db/changelog-tables.xml`:註冊 changeSets 25 + 26

#### (e) 業務邏輯

- Save:儲存當前 hair/face/skin 到 slot
- Apply:套用 slot
- Delete:確認後刪除
- Unlock:消耗道具 5920000 解新 slot
- 預覽:frozen avatar preview(隱藏帽子 + 臉部配件)

---

### 2.3 Cash Shop Window(場景切換式→視窗式現金商城)

**檔案位置**: `cashshop-window/`

#### (a) 設計動機(從原始碼註解)

**取代 vanilla cash shop 的兩個限制**:
1. **不切換 stage**(vanilla 是 stage,進入會拆 buffs、脫離地圖)
2. **無列數上限**(vanilla 用 `Etc/Commodity.img` serial 編碼 tab,單類別有上限)

**核心設計**:
- `CWnd` 派生,**疊在 field 上方**,buff/互動不中斷
- 商品目錄**完全 server-side**(讀 TSV)
- **每次只傳一個 category**,不一次傳全部(無上限)
- **即時 avatar preview**:走、跳、攻擊、表情、cash 效果,**可爬梯**(看披風背面)

#### (b) 通訊協議

| 項目 | 值 |
|---|---|
| 客戶端→服務端 opcode | `0x3730`(CP_DailyCheckin)|
| 服務端→客戶端 opcode | `0x3731`(LP_DailyCheckin)|
| 商品目錄來源 | **TSV 檔**(非 Commodity.img)|

#### (c) 客戶端 C++(`cashshopwnd.cpp` 174 KB,~3500 行)

**重要設計**:
- **無 Detours hook**(這包不 hook 任何東西)
- `0x004965F1` 在 dispatcher hook 中路由(不能在該位址加第二個 Detour)
- `HandleSync` 在 receive thread 填目錄(mutex + flag)
- `Tick` 在 main thread 建 CWnd(原因:server push 不能在 receive thread 建視窗)
- 硬碼位址(image base 0x400000)每個都引用別的 .cpp 已驗證

#### (d) 商品目錄

**`data/catalog.tsv`** = 1843 列(從 stock v83 Etc/Commodity.img 生成):

```
# 格式:itemId	price	count	tab	category	period	gender	name
1000000	3000	1	2	0	0	0	Blue Beanie
1000001	3500	1	2	0	0	2	Fine Black Hanbok Hat
...
```

**`tools/gen_cashshop_catalog_v83.py`**:從任何 v83 client 重新生成
**`tools/import_cashshop_bg.py`**:安裝 plate 進自家 CashShop.img
**`tools/make_cashshop_buttons.py`**:re-bake 按鈕

#### (e) 服務端 Java 結構

```
server/net/server/channel/handlers/CashShopWindowHandler.java  5.2 KB
server/server/cashshop/CashShopCatalog.java                     9.3 KB
server/server/cashshop/CashShopWindowPackets.java               7.0 KB
server/server/cashshop/CashShopWindowPurchase.java             13.1 KB
```

**重要設計**:
- 目錄載入位置:`cashshop-path` system property 或 `./cashshop/`
- **不在 classpath**(避免每次改都要 `mvn package`)
- 4 個 action:REQUEST_CATALOG / REQUEST_CATEGORY / BUY / BUY_CART
- BUY_CART 累積驗證:bound check → 空間檢查 → 預算檢查 → **一起交付**

#### (f) WZ 資源

- `wz/UI/CashShop.img`:已 baked 進 plate + 按鈕
- `art/backgrnd.png`:760×495 視窗底圖(原圖)

---

## §3 crit_and_range(暴擊率/暴擊傷害/魔攻範圍)

**檔案位置**: 解壓於 `C:/Users/e7896/AppData/Local/Temp/peek_crit/crit_and_range/`

### 結構

```
client/
  critmodel.h, critratedisplay.cpp, critrouting.cpp
  magicdmg.cpp, magicdmg.h, patch_statuirender.cpp, statdetaillayout.cpp
optional/gear-crit-tooltips/gear_crit_tooltip.cpp
server/wz/Server/wz/String.wz/ToolTipHelp.img.xml
wz/String/ToolTipHelp.img
wz/UIWindow.img
```

### 技術構成

- **暴擊率/暴擊傷害**:detail-stats 視窗擴展(5 個屬性:Crit Rate, Crit Damage, Weapon Attack, Magic Attack, 魔攻範圍)
- **魔攻範圍**:從 `Map.wz/Physics.img` 讀魔導師真實範圍
- **WZ 改動**:合併 `UIWindow.img`(detail-stats sprite)+ `String/ToolTipHelp.img`(tooltip 文字)
- **可選**:gear tooltip 加 crit rate / crit damage 顯示

### 整合入口

```cpp
AttachMagicDamageMod();     // 魔攻 + 範圍
AttachCritRoutingMod();     // crit 路由
AttachStatDetailLayoutMod(); // detail-stats 視窗
PatchStatUIRender();        // 在 PatchUncapStats() 之後
```

---

## §4 主程式繁化 + 解析度補丁(主執行檔補丁)

**檔案位置**: `GMS083客戶端/主程序繁化 可调分辨率补丁/`

### 結構

```
MapleStory v83(已繁化).exe         9.9 MB  PE32 i386 (繁化版本)
STREDIT.exe                       .Net    Mono/.Net assembly
主程序导出来的繁化内容.exe.csv     (繁化字串對照)
可调分辨率补丁/
  Gms.083.ini                     (ini 配置)
  nmconew.dll                     (解析度切換 DLL)
  nmconew2.dll                    (備用)
  可調補丁必須配合UI.txt
```

### `Gms.083.ini` 內容

```ini
[client]
resolutiontype= 1 ; (0)800:600, (1)1024:768, (2)1280:720, (3) 1440:900,
                ; (4) 1680:1050, (5) 1920x1080
```

**技術構成**:
- `MapleStory v83(已繁化).exe` = **修改過的 MapleStory.exe**(繁體中文字串替換)
- `nmconew.dll` = **類似 kaentake 的記憶體 hook DLL**(改視窗解析度)
- `Gms.083.ini` = nmconew.dll 讀取的配置
- `STREDIT.exe` = .Net 工具,用於匯出/匯入字串(可見 CSV 內容是 nexon.net URL + 字串 ID)

### CSV 前 19 列(觀察)

```
0;"http://passport.nexon.net/?PART=/Registration/AgeCheck"
1;"http://passport.nexon.net/WZ.ASPX?PART=/Accounts/ForgotId"
...
8;"Tahoma"
9;"Arial Narrow"
10;"裝備"
11;"Setup"
12;"初心者"
13;"劍士"
14;"弓箭手"
...
```

---

## §5 v83.rar → `v83.idb`(IDA 逆向工程資料庫)

| 屬性 | 值 |
|---|---|
| 檔名 | `v83.idb` |
| 大小 | 125 MB |
| 識別 | `IDA (Interactive Disassembler) database` |
| 日期 | 2014-03-25 |
| 內容 | IDA Pro 對 v83 客戶端的完整逆向工程資料庫 |

**意義**:
- 完整的 function 名稱、xref、結構、字串標記
- 可直接用 IDA Pro / IDA Free 開啟
- 對 hook 開發有**極大價值**(直接查 function 而非手動 pattern scan)

---

## §6 GMS083客戶端其他 .wz/.img 內容概覽

### 6.1 scripts 腳本(2,297 個 .js)

子目錄:event / item / map / npc / portal / quest / reactor + scripts/ 根

| 目錄 | 範例 |
|---|---|
| `scripts/event/` | 0_EXAMPLE.js, 2xEvent.js, 3rdJob_*.js, 4j*.js, AirPlane.js, AmoriaPQ.js, AreaBoss*.js |
| `scripts/npc/` | NPC 對話 |
| `scripts/portal/` | 傳送點 |
| `scripts/quest/` | 任務 |
| `scripts/reactor/` | 反應器 |

### 6.2 怪物圖鑑(1,138 個 .txt)

`083MonsterBook/<id> <name> <level>.txt` 命名格式

### 6.3 主登入介面(part1 + part2)

`GMS083登录新界面/`:
- 3 張 PNG 截圖(1图/2图/3图)
- 9 個 .img(地圖物件:14thEvent, gran_helisium, Lacheln, login, worldTour2015, xenonLab, zero)
- `Bgm27.img`(背景音樂)
- `MapLogin.img`(主登入畫面)

### 6.4 商店 .img(3 套不同解析度)

| 套 | 解析度 | 大小 |
|---|---|---|
| `原版商店 1024` | 1024×768 | 997 KB |
| `原版商店 1280` | 1280×? | 3.1 MB |
| `新版商店1280-720` | 1280×720 | 3.0 MB |

每套含:`Data/UI/CashShop.img` + `Data/UI/CashShopPreview.img`

### 6.5 多彩地圖特效

| 套 | 內容 |
|---|---|
| `多彩地图特效` | `Data/Map/Tile/grassySoil.img`(單檔)|
| `多彩地图特效2` | `grassySoil.img.xml` + `颜色2.png` |

### 6.6 啟動錯誤修正補丁

`更正启动错误补丁 支持WZ，IMG端/`:
- `ijl15.dll`(JPG/JPEG 解碼函式庫,常見於遊戲)
- `MapleFix.dll`(修正補丁)
- `MapleFix.ini`(配置)

### 6.7 祝福/混沌/點卷掉落提示

`祝福混沌点卷掉落提示补丁/`:
- `Data/Item/Consume/0204.img`(消耗品)
- `Data/Item/Consume/0234.img`
- `Data/Item/Etc/0403.img`

### 6.8 源碼支援中文(23 個 .txt)

Java 修改片段:
- `中文名字/`(6 檔):CharsetConstants, GenericLittleEndianAccessor, GenericLittleEndianWriter, MapleCharacter, StringUtil
- `中文名字/公会支持中文.txt`
- `中文名字/组队支持中文.txt`
- `修复战神2转动画.txt`
- `修改冒险家新手出生地.txt`
- `修正坐船动画.txt`
- `拍卖按键.txt`
- `添加掉率查询物品显示.txt`
- `20=经验，金币，掉落.txt`(exp/meso/drop 設定)
- `2EXP任务倍率.txt`
- `个人爆率与世界爆率提示.txt`
- `游戏代码显示/`(8 檔):任務/傳送/怪物/反應器/攻擊/背包/過地圖/錯誤地圖代碼顯示

---

## §7 全部資源的「整合點」技術摘要

### 7.1 共同依賴:kaentake-style DLL 框架

三個功能包(BeautySalon / CashShop / CheckIn)都使用**同一個 client framework**:

```
pch.h / hook.h / debug.h
wvs/packet.h       COutPacket / CInPacket
wvs/wnd.h          CWnd 基底
wvs/util.h         get_rm() / WZ 資源
wvs/wvsapp.h       app/update timing
wvs/iteminfo.h     item icons
wvs/wndman.h       window manager
ztl/ztl.h          ZXString, COM
```

### 7.2 共同硬碼(image base 0x400000)

| 位址 | 用途 | 用在 |
|---|---|---|
| `0x00989588` | play_ui_sound | CheckIn |
| `0x00BE7918` | CWvsContext | CheckIn |
| `0x00BE7914` | ClientSocket | CheckIn |
| `0x0049637B` | ClientSocket::SendPacket | CheckIn |
| `0x004965F1` | ClientSocket::ProcessPacket | CheckIn, CashShop |

**`0x004965F1` 是常見的 packet dispatch hook 點**(兩處都提到,警告不要重複 hook)

### 7.3 服務端共通點:opcode enum 修改

所有功能包都需要:
1. `RecvOpcode.java` 加 enum
2. `SendOpcode.java` 加 enum
3. `PacketProcessor.java` 註冊 handler

### 7.4 WZ 結構共通點

| 功能 | WZ 路徑 |
|---|---|
| CheckIn | `UI/UIWindow.img/DailyCheckin/backgrnd` |
| BeautySalon | `UI.wz/v83.img/beautyRoom/` |
| CashShop | `UI/CashShop.img/Base/WndBg` + `BtBuy/` + `BtCart/` |
| crit_and_range | `UIWindow.img`(完整替換)+ `String/ToolTipHelp.img`(完整替換)|

---

## §8 純技術總結(不含評估)

**這個資料夾包含**:

1. **完整的 v83 GMS 客戶端主程式**(4.28 MB PE,2018 build)
2. **完整的 v83 客戶端 WZ/IMG 資源**(2,300 個 .js 腳本 + 1,138 個怪物圖鑑 + 商店 .img + 登入介面)
3. **3 個獨立的完整功能包**(CheckIn / BeautySalon / CashShop),每個都是 client C++ + server Java + SQL + WZ 完整配套
4. **1 個暴擊/魔攻 mod 補丁**(client C++ + WZ 修改)
5. **1 個主程式繁化 + 解析度切換 DLL**(`nmconew.dll` 類似 kaentake)
6. **1 個 v83 IDA 逆向工程資料庫**(125 MB,2014,完整 function/xref)
7. **1 套 Java 源碼中文支援片段**(23 個 .txt 修改片段)

**所有客戶端 C++ 都設計給同一個 build**:image base `0x400000` 的標準 v83 MapleStory.exe。

---

**檔案狀態**:
- 本檔:剛寫入
- `C:/Users/e7896/AppData/Local/Temp/gmspeek/`:10 個 RAR 解壓
- `C:/Users/e7896/AppData/Local/Temp/peek_cash/`:cashshop-window 解壓
- `C:/Users/e7896/AppData/Local/Temp/peek_crit/`:crit_and_range 解壓
- `C:/Users/e7896/AppData/Local/Temp/peek1/BeautySalonv83/`:BeautySalonv83 解壓
- `C:/Users/e7896/AppData/Local/Temp/v83peek/v83.idb`:v83.idb 取出
- `C:/Users/e7896/AppData/Local/Temp/gmslogin1b/` + `gmslogin2/`:登入介面解壓

`待分類/` 本體**完全沒動**。
