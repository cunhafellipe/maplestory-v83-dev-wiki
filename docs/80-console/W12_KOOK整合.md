# W12　KOOK 整合

> 本頁為主題式重組，內容全部來自原始的 42 份逐片教學筆記，未引入外部資訊。
> 每條可獨立引用；條目 ID 穩定，請勿隨意改號。

> ⚠️ **本頁兩課素材的識別字狀態**：
> 第 27 課的畫面理解層把 **KOOK** 誤讀成 `Room`／`Boss`／`Kuo`／`Kuk` 等多組名字，
> 第 26 課的畫面層則橫跨多套專案版本。**本頁的程式碼逐字保留筆記中的畫面原文（連同誤讀的識別字）**，
> 推定正解只在條目文字中標示，不改寫程式碼本身。衝突一律並列，見「本頁的坑總表」。

## 覆蓋來源

| 課次 | 筆記檔 | 本頁取用範圍 |
|---|---|---|
| 第26課 | `L26_第二十六课_教學筆記.md` | 全課（KOOK 管理頁、綁定訊息表、機器人上下線實測） |
| 第27課 | `L27_第二十七课_教學筆記.md` | 全課（KOOK 配置表、反射讀寫、介面校驗、系列收尾） |

## 速查

| ID | 一句話 |
|---|---|
| W12-001 | KOOK 管理頁照 `MenuCommand` 複製，覆寫 `show()` 再到枚舉註冊 |
| W12-002 | 綁定訊息表欄位重定義為 accountId 20%／receive／reply 40%／bindCode |
| W12-003 | 綁定狀態靠 `selectedIndex` 對應 `account_id is null` / `is not null` |
| W12-004 | `kook_message` 建表腳本與逐欄語意（`account_id` 為 null＝未綁定） |
| W12-005 | 綁定碼 6 位、已存在就取既有碼不重建 |
| W12-006 | `bindKeywords` 與綁定頻道名都可改，改了只在自己指定頻道內生效 |
| W12-007 | 綁定頻道不存在會自動建立；頻道 ID 與名稱二選一 |
| W12-008 | 上線／下線按鈕三要件：`setDisable` 防連點、UI 更新切 FX 執行緒、`isOnline()` 事後驗證 |
| W12-009 | ASR 音譯 → 正確詞彙對照表（`cookie`／`库克` → KOOK 等） |
| W12-010 | `kook_config` 建表與初始 INSERT：六筆還是七筆、`guildId` 還是 `qqId` |
| W12-011 | `readKookProp()` 用 `getDeclaredField` 把資料庫字串塞進 `KookProp` |
| W12-012 | `updateKookProp()` 用 `getDeclaredFields()` 產生通用 UPDATE |
| W12-013 | 🔴 建表叫 `config_data`、程式用 `config_value` → 值全讀不到 |
| W12-014 | 上線前四道校驗，以及校驗失敗 `return` 忘記解鎖按鈕 |
| W12-015 | 🔴 輸入框只在值變動時回填，沿用預設值會把其他欄位清空 |
| W12-016 | 配置頁完整串接：`Pair` 造欄位 → `getInputs` → `isNull` → 回填 → `update` |
| W12-017 | ⚠ 開源專案不要把 Token 與伺服器／頻道 ID 寫死或留預設值 |
| W12-018 | 401 診斷：Token 錯則 gateway 建連被拒；`guild_id`／`target_id` 從 Console JSON 反查 |
| W12-019 | ⚠ KOOK 概念在畫面層被讀成至少 4 套名字 |
| W12-020 | 系列收尾自陳的未完成項與不列入本教學的部分 |

## 條目

### W12-001　照 `MenuCommand` 複製一個 KOOK 管理頁再註冊進選單

- **關鍵字**：`MenuAbstract` `MenuEnum` `MenuKook` `MenuCook` `show()` `ui/menu`
- **來源**：第26課 00:00–03:00｜`L26_第二十六课_教學筆記.md`
- **要點**：新增一個管理頁有三步：①在 `src/main/java/ui/menu` 底下 `New` → `Java Class`
  建立頁面類別並 `extends MenuAbstract`；②實作 `show()`，把 `MenuCommand.show()` 裡
  建構 UI 的程式碼（`HBox`、`TextField`、`Button` 等）貼進來再慢慢改；③到枚舉類
  `src/main/java/ui/menu/MenuEnum.java` 加一行註冊把類別塞進選單。
  口述命名為 `MenuCook`（語音多處寫成 `Cook`／`cookie`／`庫客`），畫面 v007 讀到
  `src/main/java/gui/MenuKook.java`，推定正解為 `MenuKook`。
- **程式碼**：

  ```java
  // src/main/java/ui/menu/MenuEnum.java
  PUSH("推送控制", MenuPush.class),
  ```

  ```java
  package ui.menu;

  public class MenuPush extends MenuAbstract {
      @Override
      protected void show() {
          // 初始測試
          // System.out.println("show");
      }
  }
  ```

- **坑**：⚠ **畫面與口述衝突**：口述說本課做的是 KOOK 管理頁（`MenuCook`），
  畫面 v000 卻是 `MenuPush`「推送控制」頁；兩者套件也不同。
  ⚠ 從 `MenuCommand` 複製過來會出現大量紅字（如 `list-doCommand`、`originalCommands`），
  因這些變數屬於指令管理頁、尚未在 `MenuPush` 宣告，講者說是開發過程正常現象。
- **相關**：見 W04（選單系統與視圖切換）

### W12-002　綁定訊息表只留四個欄位並綁定欄寬比例

- **關鍵字**：`accountId` `receive` `reply` `bindCode` `TableColumn` `prefWidthProperty` `0.2` `0.4`
- **來源**：第26課 06:00–09:00、21:00–24:00｜`L26_第二十六课_教學筆記.md`
- **要點**：KOOK 綁定訊息頁不保留原本指令管理頁的欄位。決定只展示
  `accountId`（帳號 ID，佔 20%）、`receiveColumn`（原始綁定訊息）、
  `replyColumn`（原始回覆訊息，佔 40%）、`codeColumn`（綁定碼 `bindCode`），
  欄寬用 `prefWidthProperty().bind(tableView.widthProperty().multiply(0.2))` 綁定。
  `receive` 與 `reply` 都是 `String`，綁定碼也明講是 `String`。
  另外把 `pageSize` 調成 1，要求一頁顯示完、不要拉捲軸。
- **程式碼**：

  ```java
  // src/main/java/ui/view/MenuCommand.java — createTableView()
  TableColumn<KooMessage, String> channelIdColumn = new TableColumn<>("频道ID");
  channelIdColumn.prefWidthProperty().bind(tableView.widthProperty().multiply(0.1));
  channelIdColumn.setCellValueFactory(new PropertyValueFactory<>("channelId"));

  TableColumn<KooMessage, String> accountIdColumn = new TableColumn<>("账号ID");
  accountIdColumn.prefWidthProperty().bind(tableView.widthProperty().multiply(0.1));
  accountIdColumn.setCellValueFactory(new PropertyValueFactory<>("accountId"));

  TableColumn<KooMessage, String> receiveCharacterColumn = new TableColumn<>("角色名字");
  receiveCharacterColumn.prefWidthProperty().bind(tableView.widthProperty().multiply(0.1));
  receiveCharacterColumn.setCellValueFactory(new PropertyValueFactory<>("receiveCharacter"));
  ```

  ```java
  // src/main/java/ui/model/KooMessage.java
  private String channelId;
  private String accountId;
  private String receiveCharacter;
  private Integer accountIc; // 畫面上有短暫出現拼字錯誤，後續未明顯修正
  ```

- **坑**：⚠ 口述列的欄位（`accountId`／`receive`／`reply`／`bindCode`）與畫面這段程式碼的欄位
  （`channelId`／`accountId`／`receiveCharacter`）並不相同，兩說並列。
  ⚠ `accountIc` 疑似 `accountId` 的拼字錯誤，畫面未見修正。
  ⚠ `pageSize` 調成 1 是口述值；畫面對應段落顯示的是 `macro_message` 的純分頁查詢
  （`if (selectedIndex == 1)` 才加條件），與本條的 0/1 兩分支寫法不同。
- **相關**：見 W08（配置管理與熱重載）

### W12-003　綁定狀態過濾靠 `selectedIndex` 對應 `account_id` 是否為 null

- **關鍵字**：`selectedIndex` `account_id is null` `selectCountByCondition` `statusComboBox` `Pagination`
- **來源**：第26課 06:00–12:00｜`L26_第二十六课_教學筆記.md`
- **要點**：KOOK 綁定頁不用搜尋輸入框（表裡都是 ID，沒有人會手打來查），
  改成「綁定狀態」下拉做過濾器：未綁定／已綁定，默認全查。
  判斷依據是**有沒有 `account_id`**：`selectedIndex == 0` → `where account_id is null`（未綁定）、
  `selectedIndex == 1` → `where account_id is not null`（已綁定）、其他值不加 `where`。
  `levelComboBox` 改名叫 `statusComboBox`，UI 層 `onSearch` 精簡成
  `private void onSearch(Pagination center, ComboBox<Integer> levelComboBox, Integer selectedIndex)`。
- **程式碼**：

  ```java
  // 口述為 KookMessageDao / kook_message 表；畫面 v002 為 RoomMessageDao / room_message 表
  public static int selectCountByCondition(int selectedIndex) {
      String sql = "select count(1) as count from room_message";
      if (selectedIndex != -1) {
          if (selectedIndex == 0) {
              sql += " where account_id is null";
          }
          if (selectedIndex == 1) {
              sql += " where account_id is not null";
          }
      }
      return SqliteConnection.selectOneInt(sql);
  }
  ```

- **坑**：⚠ **索引對調衝突**：口述（a002）為 `0 = 未綁定 is null`、`1 = 已綁定 is not null`；
  畫面 v005 卻寫 `if (selectedIndex == 1) { sql += " where account_id is null"; }`。
  同一專案內兩種語義，必有一處是錯的，兩說並列。
  ⚠ 條件全部以字串拼接（`sql += " where ..."`），有注入風險；畫面 v005 更顯示作者把
  `PreparedStatement`／`ResultSet` 版本**刪掉**改回拼接版，方向相反。
  ⚠ 目標類別與表名衝突：口述是 `KookMessageDao`／`kook_message`，畫面 v002 是
  `RoomMessageDao`／`room_message`。
- **相關**：見 W08（配置管理與熱重載）

### W12-004　`kook_message` 建表腳本與逐欄語意

- **關鍵字**：`kook_message` `account_id` `reply_content` `receive_content` `channel_id` `Q.sql` `InnoDB`
- **來源**：第26課 15:00–21:00、27:00–30:00｜`L26_第二十六课_教學筆記.md`
- **要點**：`kook_message` 記錄 KOOK 頻道裡的綁定對話，主鍵是訊息 ID（`id`）。
  講者口述逐欄解釋：`channel_id` 是綁定頻道 ID、`author_id` 是誰發的、
  `receive_*` 是收到的訊息與時間、`reply_*` 是回復的訊息與時間，
  **`account_id` 必須在遊戲裡真的完成綁定後才會賦值，否則就是未綁定狀態**。
  語意上「原始綁定訊息」＝我發的綁定訊息、「原始回覆訊息」＝我的綁定碼。
- **程式碼**：

  ```sql
  drop table if exists kook_message;
  create table if not exists kook_message(
      `id` varchar(255) not null comment '消息ID',
      `channel_id` varchar(255) default null comment '频道ID',
      `author_id` varchar(255) default null comment '发送者ID',
      `author_username` varchar(255) default null comment '发送者昵称',
      `receive_content` varchar(255) default null comment '接收的消息',
      `receive_timestamp` bigint(20) default null comment '接收时间戳',
      `reply_message_id` varchar(255) default null comment '回复的消息ID',
      `reply_content` varchar(255) default null comment '回复的消息内容',
      `reply_timestamp` bigint(20) default null comment '回复的时间戳',
      `account_id` int(11) default null comment '绑定的账号ID',
      PRIMARY KEY (`id`) USING BTREE,
      INDEX `channel_id`(`channel_id`) USING BTREE
  ) ENGINE = InnoDB AUTO_INCREMENT = 1 comment = '频道聊天记录';
  ```

- **坑**：⚠ **表名不一致**：口述與畫面 v004 用 `kook_message`，畫面 v008 除錯時查的是
  `kook_message_log`（`select * from kook_message_log t;`）；畫面 v007 開頭看到的欄位是
  `id, channel_id, is_receive_message, receive_message_id`，與建表腳本的欄位集不一致
  （`is_receive_message` 不在建表腳本中）。
  ⚠ `account_id` 型別是 `int(11)`，其餘 ID 欄位是 `varchar(255)`，型別不一致。
  ⚠ 第 26 課踩到「把 MySQL 當成 SQLite 初始化」：`no such table: kook_message`、`missing database`；
  另一個錯誤是 `java.lang.ClassCastException: class java.lang.Long cannot be cast to class java.lang.Integer`
  （`at vl.JDBC.RoomMessageDao.selectCountByCondition(RoomMessageDao.java:264)`）——
  MySQL 的 `count` 是 `Long`、SQLite 才是 `int`。

### W12-005　綁定碼只有 6 位，且已存在就取既有碼不重建

- **關鍵字**：`bindCode` `綁定碼` `6 位` `唯一性` `bindKeywords`
- **來源**：第26課 21:00–24:00、27:00–30:00、33:00–36:00｜`L26_第二十六课_教學筆記.md`
- **要點**：綁定碼長度固定 **6 位**，所以介面欄位不需要特別寬，但**綁定訊息本身可能比較長**。
  唯一性靠資料庫：**已生成並記錄在資料庫的，直接取既有值回給使用者，不重新生成**；
  沒生成過才新建。重複發送關鍵字不會產生新碼，講者實測時先刪掉資料庫記錄才拿到新碼。
- **坑**：⚠ 若資料庫被清空或記錄遺失，舊使用者會拿到新碼，產生孤兒資料。
  ⚠ 第 26 課的**摘要列**欄位命名（`receive`／`reply`／`bindCode`）與**逐段記錄**的
  `TableColumn` 物件名（`receiveColumn`／`replyColumn`／`codeColumn`）、
  以及 `KooMessage` 的 Java 欄位（`receiveCharacter`／`accountIc`）
  是三套不同寫法，對應關係需自行對回實際程式碼。
  （`accountIc` 本身疑為 `accountId` 的拼字誤讀，畫面上有出現但後續未明顯修正。）

### W12-006　`bindKeywords` 與綁定頻道名都可隨時改，只在指定頻道內生效

- **關鍵字**：`bindKeywords` `綁定` `Hello World` `綁定頻道` `kook_config`
- **來源**：第26課 33:00–36:00；第27課 33:00–36:00｜`L26_第二十六课_教學筆記.md`；`L27_第二十七课_教學筆記.md`
- **要點**：`bindKeywords` 是**機器人在頻道裡實際監聽時用來比對的關鍵字**——
  玩家輸入什麼才會觸發綁定，預設是「綁定」。第 26 課實測把它改成 `Hello World`：
  輸入「綁定」機器人就不理會，輸入 `Hello World` 才回綁定碼。
  綁定頻道名稱同樣可改，改完要重啟；改了之後舊頻道失效，
  **只有在指定的那個頻道裡輸入關鍵字才會回綁定碼**。
- **坑**：⚠ 改名稱後舊頻道直接失效，容易誤以為改名沒生效（其實生效了，是換了頻道）。
  ⚠ 預設值文字兩說並列：口述說叫「綁定頻道」、關鍵字「綁定」；
  畫面 v000 建表腳本寫的是 `'默认频道'` 與 `'绑定 '`（**含尾隨空白**）。
  ⚠ 尾隨空白會影響關鍵字比對，`'绑定 '` 帶一個空格。
- **相關**：見 W15（伺服器遊戲機制）

### W12-007　綁定頻道不存在會自動建立；頻道 ID 與名稱二選一

- **關鍵字**：`channelId` `channelName` `綁定頻道` `setChannelName` `setGuildId` `二選一`
- **來源**：第26課 30:00–33:00；第27課 33:00–36:00｜`L26_第二十六课_教學筆記.md`；`L27_第二十七课_教學筆記.md`
- **要點**：上線時會檢查綁定頻道，**不存在就直接建立一個**（預設名稱「綁定頻道」）——
  第 26 課實測把頻道刪掉再上線，機器人又建了一個新的。
  ID 與名稱是刻意的冗餘設計、**二選一**：知道 ID 就填 ID，不知道 ID 就填名稱讓程式依名稱自動匹配。
  同一套規則也套在伺服器（`guildId`／`guildName`）上。
- **程式碼**：

  ```java
  // src/main/java/com/mxd/kboot/event/BotEventB.java — onlin()
  kookProp.setGuildId("2859016140504144");
  kookProp.setChannelName("753681");
  kookProp.setSort(1);
  ```

- **坑**：⚠ **「自動建立」是隱式副作用**：設定一個打錯的頻道名，會在 KOOK 上真的開出新頻道。
  ⚠ **方法名與傳入語義不一致（畫面自身的不一致）**：v006 用 `setChannelId(...)`，
  v007／v008 卻是 `setChannelName("852818")` 這類純數字——方法名是 Name 卻傳 ID。
  ⚠ 第 26 課的 `setChannelName` 從 `"7831818"` 改成 `"852818"`、再改成 `"753681"`／`"8818"`／`"358487"`，
  搭配 `setGuildId` 換過三組值仍抓不到正確頻道，最後靠資料庫
  `select * from kook_message_log t;` 查 `guild_id`／`target_id` 才修正。
  ⚠ `setChannelName`／`setGuildId` 的語意需回頭確認 API 定義。

### W12-008　上線／下線按鈕的三個要件：防連點、切 FX 執行緒、事後驗證

- **關鍵字**：`setDisable` `Platform.runLater` `updateNodeColor` `Not on FX application thread` `isOnline` `KookManager`
- **來源**：第26課 21:00–27:00、27:00–30:00｜`L26_第二十六课_教學筆記.md`
- **要點**：上線／下線機器人按鈕要做到三件事。
  ①**防連點**：進來就先 `onlineButton.setDisable(true)`，操作完再 `setDisable(false)`，
  否則會「瘋狂點，不給我點壞了」。
  ②**UI 更新必須切回 JavaFX 主執行緒**：在非 FX 執行緒直接 `setText()`／`setStyle()` 會拋
  `IllegalStateException: Not on FX application thread; currentThread = Thread-4`；
  解法是封裝一個 `updateNodeColor` 用 `Platform.runLater()` 換色。
  ③**按下去成功不等於真的成功**：執行完必須用 `KookManager.getInstance().isOnline()` 再驗一次，
  因為可能資料庫沒起或某步報錯。查詢可以不等服務在線，但**上線機器人需要服務啟動**。
- **程式碼**：

  ```java
  // src/main/java/client/ui/ButtonTypes.java
  public static void updateNodeColor(Node node, String color) {
      Platform.runLater(() -> {
          node.setStyle("-fx-background-color: " + color + ";");
      });
  }
  ```

  ```java
  // src/main/java/client/ui/ServerApp.java
  if (KookManager.getInstance().isOnline()) {
      onLineButton.setText("下线");
      ButtonTypes.updateNodeColor(onLineButton, "red"); // 狀態改為紅色
  } else {
      onLineButton.setText("上线");
      ButtonTypes.updateNodeColor(onLineButton, "green"); // 狀態改為綠色
  }
  ```

  ```java
  // 畫面 v005：自訂封裝
  PlatformImpl.runOnBack(() -> {
      PlatformImpl.runOnFx(() -> onlineButton.setDisable(true));
      // ... 開關機邏輯 ...
      PlatformImpl.runOnFx(() -> onlineButton.setDisable(false));
  });
  ```

- **坑**：⚠ **下線狀態有延遲，UI 不可盡信**：講者實測「上線倒是上得挺快的，下線好像並沒有很快」，
  實際上 WebSocket 已關閉但按鈕仍顯示在線。準確反映狀態要輪詢 `isOnline()` 或由連線事件觸發 UI 更新。
  ⚠ 背景執行緒切 UI 執行緒有兩套封裝並存：`PlatformImpl.runOnFx`／`runOnBack`（自訂）
  與 `Platform.runLater`／`runAndWait`（JDK 原生），做法相同但別混用。
  ⚠ 口述提到的樣式封裝類 `viewStyle`／`onlineStyle` **在畫面中完全未出現**。
- **相關**：見 W05（服務起停與日誌輸出）

### W12-009　ASR 音譯 → 正確詞彙對照表

- **關鍵字**：`ASR` `語音辨識` `cooker` `cookie` `cuckoo` `库克` `库客` `KookProp` `kook_config` `botToken` `guildId` `bindKeywords` `channelUrl`
- **來源**：第27課 全課（第三節說明、第六節 (b) 18）；第26課 00:00–03:00｜`L27_第二十七课_教學筆記.md`；`L26_第二十六课_教學筆記.md`
- **要點**：第 27 課的語音轉錄把 KOOK 相關詞彙大量誤聽，以下是本課可用的對照。
  讀逐字稿時把右欄代回程式碼即可，不要照左欄的識別字去搜尋。
- **對照**：

  | ASR 聽到的 | 正確詞彙 |
  |---|---|
  | `cooker`／`cookie`／`cuckoo`／`cuky`／`库克`／`库客`／`库客服務器` | **KOOK** |
  | `cookie property`／`Cook` | **`KookProp`** |
  | `cook config`／`cuckoo_config` | **`kook_config`** |
  | `btn token`／`boxToken` | **`botToken`** |
  | `grid ID`／`grid name` | **`guildId`／`guildName`** |
  | `band keywords` | **`bindKeywords`** |
  | `ws URL` | **`channelUrl`** |
  | `卓爾小睡`／`左手小碎` | **昨日小睡**（UP 主自稱） |
  | `circle` | **`SQL`／`where`**（條件） |
  | `建權失敗` | **建連（gateway）失敗** |
  | `讀條` | 載入進度條（講者用語） |
  | `菜單`／`頁面` | **頁籤** |
  | `異步執行異常` | 非同步執行異常 |

- **坑**：⚠ **對照只適用於語音層**。第 26 課的**畫面層**誤讀方向不同（`KookProp` 被讀成
  `RoomProp`／`BossProp`／`ReadDrop`／`KooMapProp`，`KookManager` 被讀成 `KuoManager`、
  `BossManager`、`KooManager`），兩層的對照表不共用。
  ⚠ ASR 誤聽也可能造成數值錯誤：口述的 `varchar 改大點，改成 20` 與畫面最終的 `VARCHAR(255)` 不符
  （推定為「255」的語音誤識）。

### W12-010　`kook_config` 建表與初始 INSERT：六筆還是七筆、`guildId` 還是 `qqId`

- **關鍵字**：`kook_config` `config_name` `config_data` `BEGIN TRANSACTION` `DROP TABLE IF EXISTS` `6 rows affected`
- **來源**：第27課 03:00–06:00｜`L27_第二十七课_教學筆記.md`
- **要點**：把寫死的 KOOK 設定搬進 SQLite。在 `resources` 的 DB 腳本裡
  `BEGIN TRANSACTION` → `CREATE TABLE`（兩列 `config_name`／`config_data`）→ 逐筆 `INSERT` 預設值 → `COMMIT`，
  因為表已存在，重跑前先 `DROP TABLE IF EXISTS`。六個設定項為
  `botToken`／`guildId`／`guildName`／`channelId`／`channelName`／`bindKeywords`。
- **程式碼**：

  ```sql
  BEGIN TRANSACTION;
  CREATE TABLE room_config
  (
      config_name     VARCHAR(255),
      config_data     VARCHAR(255)
  );

  INSERT INTO room_config VALUES('botToken', null);
  INSERT INTO room_config VALUES('guildName', null);
  INSERT INTO room_config VALUES('channelId', '默认频道');
  INSERT INTO room_config VALUES('channelName', '默认频道');
  INSERT INTO room_config VALUES('qqId', null);
  INSERT INTO room_config VALUES('bindKeywords', '绑定 ');

  COMMIT;
  ```

- **坑**：⚠ **筆數衝突（兩說並列，未擇一）**：
  - 畫面 v000 為 **6 rows**（Services 面板原文 `[2024-03-24 18:50:52] 6 rows affected in 3 ms`），
    內容為 `botToken`／`guildName`／`channelId`／`channelName`／**`qqId`**／`bindKeywords`——
    **有 `qqId` 也沒有 `guildId`**。
  - 口述 a000 說「會找到**七行**」，多的第六項是 **`ws URL`（＝`channelUrl`）**，
    且口述說「**有 `guildId` 也沒有 `qqId`**」——**與畫面相反**。
  - 但 v008 的 setter 簽章含 `guildId` 與 `channelUrl`，故口述版本較可信，
    畫面 `qqId` 一列疑為誤讀或舊版殘留（`代表人物QQ` 欄呼應同一個 `qqId`）。
  ⚠ **第二欄名衝突（本課最大 bug 源頭）**：建表用 `config_data`，讀寫全部用 `config_value`，
  見 W12-013。
  ⚠ **欄寬衝突**：口述說「改成 20」，畫面最終為 `VARCHAR(255)`。
  ⚠ **預設值文字衝突**：口述說「綁定頻道」／「綁定」，畫面是 `'默认频道'`／`'绑定 '`。
  ⚠ 識別字 `room_config` 為畫面層誤讀，推定正解為 `kook_config`。
  ⚠ v000 的 `resources/sql/Server-db/Server.sql`、`boss_config.sql`、`kook.config.sql`
  三個路徑並存，**哪一個才是本課實際執行的腳本無法由素材判定**。

### W12-011　`readKookProp()` 用 `getDeclaredField` 把資料庫字串塞進 `KookProp`

- **關鍵字**：`readKookProp` `getDeclaredField` `setAccessible` `SqliteConnection.select` `MapCommonUtils`
- **來源**：第27課 06:00–09:00｜`L27_第二十七课_教學筆記.md`
- **要點**：DAO 開頭先確保 SQLite 連線就緒（`static` 區塊判 `isInitialized()`），
  再 `select * from kook_config` 拿到 `List<Map<String, Object>>`。
  查無資料就直接回空的 `KookProp`（`MapCommonUtils.isEmpty`）。
  逐列以 `config_name` 的值當欄位名 `getDeclaredField` → `setAccessible(true)` → `field.set(...)`。
  講者強調**例外要吞掉但日誌要記**：「不能因為這個失敗了影響我們讀其他的值」。
- **程式碼**：

  ```java
  static {
      if (!SqliteConnection.isInitialized()) {
          SqliteConnection.init();
      }
  }
  ```

  ```java
  public static BossProp readBossProp() {
      BossProp bossProp = new BossProp();
      List<Map<String, Object>> selectList = SqliteConnection.select("select * from boss_config");

      for (Map<String, Object> map : selectList) {
          try {
              Field field = bossProp.getClass().getDeclaredField(map.get("config_name").toString());
              field.setAccessible(true);
              field.set(bossProp, map.get("config_value"));
          } catch (Exception e) {
              Log.error("獲取boss屬性異常: " + e);
          }
      }

      return bossProp;
  }
  ```

- **坑**：🔴 **取值 API 兩說並列**：口述是 `MapCommonUtils.getString(map, "configName")`，
  畫面是 `map.get("config_name").toString()`。**若 `config_value` 為 `null`，
  `.toString()` 直接 `NullPointerException`**——這正對應課堂上「怎麼讀到的值都為空」的現場。
  🔴 **駝峰／蛇形耦合（畫面層未察覺的隱藏坑）**：口述用 `configName`、畫面用 `config_name`
  當反射欄位名，但 `KookProp` 的欄位是 `botToken`／`guildId` 這類駝峰名。
  若真拿 `config_name` 去 `getDeclaredField`，**每一筆都會拋 `NoSuchFieldException` 並被 catch 吞掉**
  ——症狀同樣是「讀到的值都為空」。
  ⚠ `readKookProp` 放在哪個類別兩說並列：口述說 `KookConfigDao`，畫面 v001 讀成
  `BossConfigDao`（路徑 `Server-App/src/main/java/v1/jdbc/`）。
- **相關**：見 W08（配置管理與熱重載）

### W12-012　`updateKookProp()` 用 `getDeclaredFields()` 產生通用 UPDATE

- **關鍵字**：`updateKookProp` `getDeclaredFields` `update kook_config set config_value = ? where config_name = ?` `SqliteConnection.update`
- **來源**：第27課 09:00–12:00｜`L27_第二十七课_教學筆記.md`
- **要點**：寫入端與讀取端對稱。用 `kookProp.getClass().getDeclaredFields()` 取得**全部**欄位，
  逐欄位 `setAccessible(true)` → `field.get(kookProp)` 取值、`field.getName()` 當 `where` 條件，
  交給 `SqliteConnection.update` 的佔位符式更新。
  講者點出的價值：**新增設定項不必再回頭改 DAO 程式碼**。
  因為都是 `String` 欄位、資料庫都是 `varchar`，理論上不會有型別轉換錯誤，但仍 `try` 起來吞例外。
- **程式碼**：

  ```java
  public static void updateKookProp(KookProp kookProp) {
      for (Field field : kookProp.getClass().getDeclaredFields()) {
          try {
              field.setAccessible(true);
              SqliteConnection.update(
                "update kook_config set config_value = ? where config_name = ?",
                field.get(kookProp),
                field.getName());
          } catch (Exception e) {
              log.error("更新kook配置失败：{}", e);
          }
      }
  }
  ```

- **坑**：🔴 **代價是失去編譯期檢查**：欄位改名不會編譯錯誤，只會在執行時靜默失敗。
  🔴 **`where` 條件欄位名不一致**：畫面用 `config_name = ?` ＋ `field.getName()`（駝峰）比對蛇形欄位值，
  口述則說 `where configName`。駝峰／蛇形不一致會導致 **UPDATE 影響 0 列**，
  而 SQLite 不報錯。講者實測後續確實有寫入成功，**推定實際程式已做轉換或兩層皆有誤讀**。
  ⚠ **放在哪個類別互斥**：口述說寫在 `KookConfigDao`，畫面 v002 說寫在
  `Messages.java`（`src/main/java/config/Messages.java`）——同一方法不可能在兩處，必有一錯。
  ⚠ IDE 曾跳出灰色 AI 程式碼建議（含 `delete from boss_config` 與遍歷 `insert`），
  操作者按退格刪除，改為手寫 `update`。

### W12-013　🔴 建表叫 `config_data`、程式用 `config_value` → 值全讀不到

- **關鍵字**：`config_data` `config_value` `讀到的值都為空` `getDeclaredField` `map.get`
- **來源**：第27課 24:00–27:00｜`L27_第二十七课_教學筆記.md`
- **要點**：本課第一個實戰 bug 的因果鏈：①建表時第二欄命名為 `config_data`；
  ②但讀寫程式碼用 `config_value`；③結果 `map.get("config_value")` 回 `null`，
  若用 `.toString()` 還會 NPE；④講者在 debug 時從 SQL 反光框看到才恍然大悟；
  ⑤修正後重啟，綁定頻道／綁定頻道名稱／綁定關鍵字三列就正常顯示。
  **關鍵在於 `readKookProp` 用 `catch (Exception)` 把例外吞掉，所以表面完全沒有錯誤**。
- **程式碼**：

  ```java
  Field field = bossProp.getClass().getDeclaredField(map.get("config_name").toString());
  field.setAccessible(true);
  field.set(bossProp, map.get("config_value").toString());
  ```

- **坑**：⚠ **畫面的錯誤訊息與口述的症狀不同**：畫面 v007 拋的是
  `java.sql.SQLException: sql injection violation, syntax error: ERROR. pos 41, line 1, column 35, token EOF : update boss_config set config_data = ? where config_name = ?`
  （**SQL 語法層錯誤**，來自 `SqlSessionManager` 防注入層），口述是「讀到的值都為空」
  （**查詢結果層問題**）。兩者可能是兩個不同 bug，**無法由素材判定**。
  ⚠ `catch (Exception)` 吞例外是「單一欄位壞掉時繼續讀其他欄位」的合理設計，
  但**必須搭配足夠明確的日誌**，否則本課這種問題完全查不出來。
  ⚠ **預防**：欄位名不要在 SQL 與 Java 兩處各寫各的，改用常數或對映表。

### W12-014　上線前四道校驗，以及校驗失敗 `return` 忘記解鎖按鈕

- **關鍵字**：`notPassCheck` `testPassBossProp` `setDisable(false)` `机器人 token 未配置` `不能同时为空`
- **來源**：第27課 12:00–15:00、27:00–30:00｜`L27_第二十七课_教學筆記.md`
- **要點**：上線機器人前讀一次 `KookProp` 做四道校驗，全是 `String` 判空：
  ①`botToken` 不可為空；②`guildId` 與 `guildName` 不可同時為空；
  ③`channelId` 與 `channelName` 不可同時為空；④`bindKeywords` 不可為空。
  全部通過才 `KookManager.getInstance().setProp(kookProp)`。
  **校驗邏輯要抽成獨立方法**，且**每個提前 `return` 的分支都必須補 `setDisable(false)`**——
  漏掉就會讓上線按鈕永久卡死。
- **校驗清單（提示文案為原文）**：

  | # | 對象 | 條件 | 提示文案 | 需補 `setDisable(false)` |
  |---|---|---|---|---|
  | 1 | `botToken` | 空 | `机器人 token 未配置` | **是（踩坑處）** |
  | 2 | `guildId` + `guildName` | 同時空 | `服务器 ID 和服务器名称不能同时为空` | 是 |
  | 3 | `channelId` + `channelName` | 同時空 | `绑定频道 ID 和绑定频道名称不能同时为空` | 是 |
  | 4 | `bindKeywords` | 空 | `绑定关键字不能为空` | 是 |

- **程式碼**：

  ```java
  private boolean notPassCheck() {
      onLineButton.setDisable(true);                 // 進入前先鎖

      KookProp kookProp = KookConfigDao.readKookProp();

      if (kookProp.getBotToken() == null || kookProp.getBotToken().isEmpty()) {
          Message.showError(primaryStage, "机器人 token 未配置");
          onLineButton.setDisable(false);            // ★ 漏掉這行，按鈕就永久卡死
          return true;                               // true = 沒通過檢查
      }

      if (isEmpty(kookProp.getGuildId()) && isEmpty(kookProp.getGuildName())) {
          Message.showError(primaryStage, "服务器 ID 和服务器名称不能同时为空");
          onLineButton.setDisable(false);
          return true;
      }

      if (isEmpty(kookProp.getChannelId()) && isEmpty(kookProp.getChannelName())) {
          Message.showError(primaryStage, "绑定频道 ID 和绑定频道名称不能同时为空");
          onLineButton.setDisable(false);
          return true;
      }

      if (isEmpty(kookProp.getBindKeywords())) {
          Message.showError(primaryStage, "绑定关键字不能为空");
          onLineButton.setDisable(false);
          return true;
      }

      KookManager.getInstance().setProp(kookProp);   // 全部通過 → 設定機器人
      return false;                                  // false = 通過檢查
  }

  // 呼叫端
  onlineButton.setOnAction(event -> {
      if (notPassCheck()) {
          return;
      }
      // ... 真正的上線流程 ...
  });
  ```

- **坑**：🔴 **口述的布林語義自相矛盾**：「如果都通過的話就 `return true`……誒不對，
  `not pass check`，我們就 `return true`，啊，沒有通過檢查。如果全部通過了我們就 `return false`」
  ——**口述中自我修正了兩次**。以畫面 v007 的 `testPassBossProp()`（通過回 `true`、
  不通過回 `false`，呼叫端 `if (!testPassBossProp()) return;`）為準。
  ⚠ 第 4 項校驗的文案兩說並列：整理表寫 `绑定关键字`，口述說「綁定關鍵字不能為空」；
  講者還特別自我更正「**綁定碼是綁定碼，綁定關鍵字就是綁定關鍵字**」。
  ⚠ 校驗抽取法的語意在兩層相反（`notPassCheck` 與 `testPassBossProp`），
  跨人維護時務必確認是哪一個。
- **相關**：見 W05（服務起停與日誌輸出）

### W12-015　🔴 輸入框只在值變動時回填，沿用預設值會把其他欄位清空

- **關鍵字**：`getInputs` `textProperty` `addListener` `defaults` `inputs[i] = value` `showAndWait`
- **來源**：第27課 30:00–33:00｜`L27_第二十七课_教學筆記.md`
- **要點**：`TextField.textProperty().addListener(...)` **只有值真的改變才觸發**。
  使用者若沿用預設值直接按確定，該格的 `inputs[i]` 永遠是 `null`，
  回填時就會把資料清空。講者現場看到「它怎麼把其他的都給我刷沒了呀」才發現。
  **正解：建立 `TextField` 時若 `defaults` 有對應值，同時 `textInput.setText(value)`
  並手動 `inputs[i] = value`**，讓 listener 與預設值兩條路都會寫入。
  另外 Lambda 內要引用迴圈變數必須先 `final int index = i;`，
  確認後用 `stage.showAndWait()` 讓主執行緒等使用者操作完再 `return inputs;`。
- **程式碼**：

  ```java
  public static String[] getInputs(Stage primaryStage, List<String> texts, List<String> defaults) {
      String[] inputs = new String[texts.size()];

      for (int i = 0; i < texts.size(); i++) {
          TextField textInput = new TextField();

          // ★ 關鍵：使用者若沿用預設值，listener 不會觸發，inputs[i] 會永遠是 null
          if (defaults != null && defaults.size() > i) {
              String value = defaults.get(i);
              textInput.setText(value);
              inputs[i] = value;                 // ← 補這行
          }

          final int index = i;                   // Lambda 中必須 final
          textInput.textProperty().addListener(
              (observable, oldValue, newValue) -> inputs[index] = newValue);

          // ... 把 label + textInput 放進對話框 ...
      }

      // 確認按鈕：showAndWait 讓主執行緒等使用者操作完
      stage.showAndWait();
      return inputs;
  }
  ```

- **坑**：⚠ 講者自嘲「總是在不停地解決 bug，然後創建新的 bug」——補上這行後**又發現之前寫的一個問題**，
  需把值提出來命名成 `value` 再賦值。
  ⚠ 畫面 v008 的對話框只有**四欄**（`代表人物QQ`／`頻道号`／`频道邀请链接`／`机器人Token`），
  與口述的**六欄**不符；`代表人物QQ` 對應 v000 建表腳本的 `qqId`，
  **判定為「綁定碼」時代的舊版 UI**。以口述六欄為準。
  ⚠ 修正前的實測反證：第一次直接點「确定」（未輸入）視窗關閉、列表無變化；
  第二次點「取消」同樣沒有新增資料——攔截邏輯生效。

### W12-016　配置頁完整串接：`Pair` 造欄位 → `getInputs` → `isNull` → 回填 → `update`

- **關鍵字**：`configButton` `Pair` `buildKookProp` `buildKookProperty` `isNull` `showInputDialog` `updateKookProp`
- **來源**：第27課 00:00–03:00、15:00–21:00｜`L27_第二十七课_教學筆記.md`
- **要點**：KOOK 配置頁的流程是**讀 → 回填輸入框 → 使用者改 → 存回資料庫**。
  入口是在「上下線機器人」按鈕**前面**加一顆 `configButton`，點擊後
  `KookConfigDao.readKookProp()` 讀出（**這裡不做校驗，可以隨便改**），
  把欄位組成「標籤 List ＋ 預設值 List」的 `Pair` 傳給輸入對話框，
  回傳 `String[]` 後逐格回填 `KookProp`，最後 `updateKookProp()` 寫回資料庫。
- **程式碼**：

  ```java
  // 綠色按鈕（口述：用 ButtonUtil 產生綠色按鈕，名為「庫克配置」）
  Button configButton = ButtonUtils.createShadowButton("配置", "配置");

  configButton.setOnAction(actionEvent -> {
      if (!Server.getInstance().isOnline()) {   // ⚠ 口述實作是先讀 KookProp 並校驗，非此 Server 判斷
          ConfigIndex.main(null);
      } else {
          MessageUtils.info("提示", "请在服务器关闭时配置");
      }
  });

  top.getChildren().addAll(createRoomButton, searchRoomBox, resetSearchButton, configButton, onlineButton);
  ```

  ```java
  private Pair<List<String>, List<String>> buildKookProp(KookProp kookProp) {
      List<String> texts = new ArrayList<>();
      List<String> defaults = new ArrayList<>();

      texts.add("机器人Token");   defaults.add(kookProp.getBotToken());
      texts.add("服务器ID");       defaults.add(kookProp.getGuildId());
      texts.add("服务器名称");     defaults.add(kookProp.getGuildName());
      texts.add("频道ID");         defaults.add(kookProp.getChannelId());
      texts.add("频道名称");       defaults.add(kookProp.getChannelName());
      texts.add("绑定关键字");     defaults.add(kookProp.getBindKeywords());

      return new Pair<>(texts, defaults);      // getLeft() = texts, getRight() = defaults
  }
  ```

  ```java
  // ① 判斷使用者是否「直接按取消」
  public static boolean isNull(String[] inputs) {
      boolean isNull = true;                       // 默認為「已取消」
      for (String input : inputs) {
          if (input != null) {                     // 只要有一格有值 → 不是取消
              isNull = false;
              break;
          }
      }
      return isNull;
  }

  // ② 把輸入值寫回實體
  private void buildKookProperty(KookProp kookProp, String[] inputs) {
      kookProp.setBotToken(inputs[0]);
      kookProp.setGuildId(inputs[1]);
      kookProp.setGuildName(inputs[2]);
      kookProp.setChannelId(inputs[3]);
      kookProp.setChannelName(inputs[4]);
      kookProp.setBindKeywords(inputs[5]);
  }

  // ③ 按鈕事件完整串接
  configButton.setOnAction(event -> {
      KookProp kookProp = KookConfigDao.readKookProp();       // 先讀
      // 這裡不做校驗：配置頁可以隨便改

      Pair<List<String>, List<String>> pair = buildKookProp(kookProp);
      String[] inputs = InputBox.getInputs(primaryStage, pair.getLeft(), pair.getRight());

      if (isNull(inputs)) {                                    // 點取消 → 直接返回
          return;
      }

      buildKookProperty(kookProp, inputs);                    // 回填
      KookConfigDao.updateKookProp(kookProp);                 // 寫回資料庫
  });
  ```

- **坑**：🔴 **布林語義相反（兩層並存）**：口述 `isNull` = **true 代表已取消**；
  畫面 `isCtrl` = **true 代表有有效輸入**。引用時務必確認是哪一個。
  ⚠ **按鈕顏色與工廠衝突**：口述說是**綠色**按鈕「庫克配置」，畫面 v000 是
  `ButtonUtils.createShadowButton("配置", "配置")`（無顏色參數）。
  ⚠ **畫面 v004 的欄位是 BOSS 語境**（編號／名字／血量／藍量／等級／經驗／頻道／刷新時間，
  類別讀成 `MenuBook.java` 的 `buildBossProp`），與口述六欄完全不同。
  設計模式（`Pair<List<String>, List<String>>` → 輸入框）可確認相同，**欄位語意判定為跨版本素材**。
  ⚠ **非字串欄位要 `String.valueOf`**：v004 現場因 `List<String> defaults` 收 `Integer` 而紅線。
  ⚠ `Pair` 的來源函式庫（Apache Commons Lang3 或專案自訂）**未在畫面中出現，無法確認**。
  ⚠ v005 畫面的執行結果是「掉宝/刷怪 讀取配置」（經驗倍率／掉寶倍率／金幣倍率），
  與 KOOK 配置無關，僅 `isCtrl` 與「确定／取消實測」兩點與口述吻合、予以採信。

### W12-017　⚠ 開源專案不要把 Token 與伺服器／頻道 ID 寫死或留預設值

- **關鍵字**：`setBotToken` `寫死` `開源` `資訊洩露` `client_id` `OAuth` `setProp`
- **來源**：第26課 24:00–27:00；第27課 09:00–12:00、12:00–15:00｜`L26_第二十六课_教學筆記.md`；`L27_第二十七课_教學筆記.md`
- **要點**：第 26 課把機器人 Token、`guildId`、`channelId` **寫死在 `setOnLine()` 內**，
  是嚴重的安全反模式；第 27 課改成資料表 + 介面可改，並把 `setProp` 重構成參數寫入。
  但**預設值仍留在建表腳本裡**，開源後仍會外洩——講者本課主動提出：
  「**建議大家最好就不要用這個默認的配置，因為這個默認的配置可能會導致你的頻道信息洩露**。
  就是因為我這個是開源的」「**包括這個伺服器的那個 ID 或者是頻道的 ID 話，大家最好配自己的**」。
- **程式碼**（第 26 課，⚠ **憑證已遮蔽，切勿照抄**）：

  ```java
  // src/main/java/client/KookManager.java
  public void setOnLine() {
      try {
          KookProp kookProp = new KookProp();
          kookProp.setBotToken("1/MTE5MDUw/5GdbC0TiQa2erzaS3gqI+g=="); // 機器人 Token
          kookProp.setGuildId("8337922650774620"); // 伺服器 ID
          kookProp.setChannelId("2236111195"); // 頻道 ID
          onLine(kookProp);
      } catch (Exception e) {
          // ...
      }
  }
  ```

  ```java
  public void setProp(String botToken, String guildId, String channelId,
                      String channelUrl, String asr1, String bindKeywords) {
      KookProp kookProp = ...;
      kookProp.setBotToken(botToken);
      kookProp.setGuildId(guildId);
      kookProp.setChannelId(channelId);
      kookProp.setChannelUrl(channelUrl);
      kookProp.setAsr1(asr1);
      // kookProp.setBindKeywords(bindKeywords);
      // ...
  }
  ```

- **KOOK OAuth 授權網址**（v002 畫面原文）：

  ```
  https://www.kookapp.cn/app/oauth2/authorize?id=284976&permission=0&client_id=4796912918193269&redirect_uri=kookApp://bot
  ```

  > ⚠ **`id=284976` 與 `client_id=4796912918193269` 是片中本來就公開的 app 識別碼，不是 token、不是機密**，
  > 引用僅供辨識用途。**絕不可當作憑證使用；本頁不記錄任何 bot token 字面值。**
- **坑**：⚠ **`setProp` 簽章含 `asr1` 參數**（v008），但口述六欄與 v000 建表腳本皆無對應項目，
  **語意不明，無法由素材判定**。
  ⚠ **第 27 課註銷了 `setBindKeywords` 的賦值**（程式碼中該行是註解狀態），
  但 `bindKeywords` 又是必填校驗項——兩者不一致。
  ⚠ v002 的瀏覽器授權流程（機器人「明日小瞳 冒险岛服管」、伺服器「你好 world」）
  在 08:00–12:00 的**語音中沒有任何對應描述**，**無法確認是否真的出現在畫面上**。

### W12-018　401 診斷：Token 錯則 gateway 建連被拒；`guild_id`／`target_id` 從 Console JSON 反查

- **關鍵字**：`401` `kookapp.cn/api/v3/gateway/index` `guild_id` `target_id` `channel_type` `GROUP`
- **來源**：第27課 30:00–33:00；第26課 30:00–33:00、27:00–30:00｜`L27_第二十七课_教學筆記.md`；`L26_第二十六课_教學筆記.md`
- **要點**：填錯 Token 時校驗會過、但上線失敗，Console 出現 HTTP 401——
  `Server returned HTTP response code: 401 For URL: https://www.kookapp.cn/api/v3/gateway/index`，
  即 KOOK gateway 建連被拒。排查順序：**先換一個已知正確的 Token 排除設定問題，再懷疑平台**。
  另外 `guildId`／`channelId` 不必去官網翻：機器人收到的訊息會在 Console 印出 JSON，
  **裡面就有 `guild_id` 與 `target_id`**，反白複製即可。
- **程式碼**：

  ```json
  {"type":0,"channel_type":"GROUP","target_id":"2195034379","author_id":"1296547763",
   "content":"1","msg_id":"...","msg_timestamp":...,"guild_id":"8327011681276023"...}
  ```

  | JSON 欄位 | 對應設定欄位 | 本片取值 |
  |---|---|---|
  | `guild_id` | `guildId`（伺服器 ID） | `8327011681276023` |
  | `target_id` | `channelId`（頻道 ID） | `2195034379` |
  | `author_id` | （訊息作者 ID） | `1296547763` |
  | `content` | 玩家輸入的訊息內容（`bindKeywords` 比對對象） | `1` |

- **坑**：⚠ 講者先說「這還不是我們的問題」又馬上改口「啊是我們的問題，是因為我們配置的機器人是錯的」——
  診斷順序要自己收斂。⚠ 第 26 課的 `target_id` 值全片不一致
  （v006 `2236111195`、v007 `"852818"`、v008 `67623545648754`／`358487`），
  且 v008 伺服器名為「hello world」、v006 為「你行你雞躍」、v007 為「歡迎來到伺服器」，
  **推測分屬多個不同測試伺服器／拍攝批次**。
  ⚠ 第 26 課還有連線成功與下線的日誌原文可對照：
  `=== 正在连接KOOK服务器...` → `=== KOOK服务器连接成功...` → `=== 正在同步KOOK频道信息...`；
  心跳／事件封包 `"type":9`。
- **相關**：見 W05（服務起停與日誌輸出）

### W12-019　⚠ KOOK 概念在畫面層被讀成至少 4 套名字

- **關鍵字**：`BossConfigDao` `KookConfigDao` `BossProp` `KookProp` `RoomProp` `KookManager` `KuoManager` `cn.koo.heavenms.nap`
- **來源**：第27課 全課（第六節 (b) 1）；第26課 全課（第六節 (b) 1）｜`L27_第二十七课_教學筆記.md`；`L26_第二十六课_教學筆記.md`
- **要點**：兩課的畫面理解層都把同一個 KOOK 概念讀成多套名字，**推定正解是
  `KookConfigDao`／`KookProp`／`KookManager`／`kook_config`**。
  程式碼結構、SQL、反射邏輯可用，**識別字必須自行對回實際程式碼**。
  第 26 課另有 v009 讀到 `cn.koo.heavenms.nap` 套件，**疑為另一個專案版本**。
- **第 27 課識別字對照（畫面層讀到的 → 推定正解）**：

  | 片段 | 畫面層讀到的識別字 | 推定正解 |
  |---|---|---|
  | v000 | `RoomMain.java`、`RoomProp.java`、`room_config`、`ConfigIndex.main(null)` | `ServerApp.java`／`KookManager.java`、`KookProp.java`、`kook_config` |
  | v001–v002 | `BossConfigDao`、`BossProp`、`boss_config` **與** `KookProp`、`kook_config` 並存 | `KookConfigDao`、`KookProp`、`kook_config` |
  | v004 | `MenuBook.java`、`buildBossProp`、`BossProp`、`ViewUtil.showInputDialog` | `MenuKook.java`、`buildKookProp`、`KookProp`、`InputBox.getInputs` |
  | v005 | `KuoManager.java`、`ReadDrop`、`KuoConfigRead`、`buildReadDrop` | `KookManager.java`、`KookProp`、`KookConfigDao`、`buildKookProperty` |
  | v006 | `BossConfigDev.java`、`BossManager.java`、`BossProp` | `ServerApp.java`／`MenuKook.java`、`KookManager.java`、`KookProp` |
  | v007 | `BossAck.java`、`BossConfigExes`、`SqlSessionManager`、`Field.getJson` | `ServerApp.java`、`KookConfigDao`、`SqliteConnection`、無此 API |
  | v008 | ✅ `KookInputDialog.java`、`KookManager.java`、`KookProp`（乾淨） | 同左 |
  | v009 | `KooMap.java`、`KooMapProp`、`cn.koo.heavenms.nap` | 同系列但**另一個專案版本** |

- **第 26 課畫面層橫跨的套件**：`ui.menu.*`、`ui.view.*`、`ui.model.*`、`ms.app.db.*`、
  `ms.app.model.*`、`vl.database.*`、`vl.JDBC.*`、`client.ui.*`、`gui.*`、`kook.*`、
  `com.mxd.kboot.event.*`、`com.mxd.kboot.model.*`、`org.example.mxd.manager.*`。
  v009 為 **Swing `JFrame`** 的 `HeavenMXD top 控制台`，與全片 JavaFX 主線完全不同。
- **坑**：⚠ **視窗標題隨片段改變，單一教學不可能同時是這些**：
  第 26 課 `HeavenMS 控制台 (15911)`／`HeavenMS-Mng [已登录]`／`HeavenMS-top [启动]`／
  `HeavenMS-Top [EBS]`／`HeavenMS-Top (150)`／`HeavenMS-Top [5]01`／`HeavenMS-Top [235]1`／
  `HeavenMXD top 控制台`；第 27 課 `HeavenMS 113b 控制台`／`HeavenMS tool [T05]`／
  `HeavenMS Vep 控制台`／`HeavenMS Top (GUI)`／`HeavenMS Top (QQ1)`／
  `HeavenMS-Nap 控制台`／`HeavenMS-Nap v002 控制台`。**重現環境前請先確認分支。**
  ⚠ 第 27 課 v003（`HomePane.java`／`cn.xiaowen.ui.pane`，副本／活動地圖禁止切頻道）
  與 v009 幾乎與本課主軸無關，判定為跨版本素材。
  ⚠ v007 出現 Spring Boot 痕跡（`Starting ConsoleGuiApplication using Java...`、
  `Tomcat initialized with port(s):...`），但本專案主線是 JavaFX 桌面應用。
  ⚠ 第 26 課 v002–v005 是 `RoomMessageDao`／`RoomMessage`／`MacroView`／`macro_message`，
  v003–v005 的頁面與口述的 KOOK 綁定頁無關。
  ⚠ 兩課素材中**完全沒有任何命令列指令**，全部操作都在 IntelliJ IDEA GUI 內完成
  （第 27 課的 `Console 1` 是 Database Console，非 shell）。

### W12-020　系列收尾自陳的未完成項與不列入本教學的部分

- **關鍵字**：`2.x` 分支 `Readme` `WZ 配置` `商城管理` `介面美化` `快捷鍵`
- **來源**：第27課 36:00–40:00；第26課 33:00–36:00｜`L27_第二十七课_教學筆記.md`；`L26_第二十六课_教學筆記.md`
- **要點**：講者在第 27 課結尾明確收尾：**KOOK 管理完成**；隨後明確交代
  ①**商城管理與 WZ 配置不在這個教學裡面做**；
  ②本分支結束後**遷到 `2.x` 分支**；
  ③要做**重構前後的 UI 對比圖**貼到 `Readme`；
  ④系列**大概到第 28 課結束**，可能再有一期「展示更新」。
  同時自陳**這些細節沒整出來**：讀條、提示、輸入框、敲回車快捷鍵、整個介面美化。
- **坑**：⚠ **「遷 2.x」與「Readme 對比圖」在片尾尚未實際完成**——
  畫面 v009 只當場建立了分支 **`simple`**、只開啟了 Gitee 的 README，屬於**計畫而非既成事實**。
  ⚠ **分支名衝突**：畫面當場建立 `simple`、口述說課後遷 `2.x`；
  第 26 課畫面 v008 選的是 **`v.0.4-course`** 分支。兩者並非同一動作。
  ⚠ **GitHub vs Gitee**：口述說「放到我們的 `GitHub` 上」「貼到我們的 `Readme`」，
  畫面開啟的是 Gitee 儲存庫 `昨日小睡 / HeavenMS-Nap`；**網址未在畫面中出現，無法確認**。
  ⚠ 第 26 課 v009 的 Swing 帳號管理畫面（`添加账号`／`保存`／`删除`／`刷新`）與口述的 KOOK 收尾無關，
  無任何程式碼修改，判定為不同階段或不同來源的畫面。
  ⚠ 新舊版功能對照口述原文提到「指令管理沒有，庫客管理沒有」（新版本沒有這兩頁）——
  與 W11 指令管理頁的實作順序需另行對照。

## 本頁的坑總表

| ID | 坑 | 來源 |
|---|---|---|
| W12-001 | 口述 `MenuCook` vs 畫面 `MenuPush`，套件（`ui/menu`）也不同 | 第26課 00:00–03:00 |
| W12-002 | 口述四欄（accountId/receive/reply/bindCode）vs 畫面三欄（channelId/accountId/receiveCharacter）；`accountIc` 疑似拼字錯誤 | 第26課 06:00–09:00 |
| W12-003 | **`selectedIndex` 索引對調**：口述 0=未綁定／1=已綁定，畫面 v005 寫 1=`is null` | 第26課 06:00–12:00、21:00–24:00 |
| W12-003 | SQL 全部字串拼接；畫面把 `PreparedStatement` 版本刪掉改回拼接 | 第26課 12:00–15:00 |
| W12-003 | 目標類別衝突：口述 `KookMessageDao`／`kook_message` vs 畫面 `RoomMessageDao`／`room_message` | 第26課 06:00–09:00 |
| W12-004 | 表名不一致：`kook_message` vs `kook_message_log`；v007 欄位集含建表腳本沒有的 `is_receive_message` | 第26課 15:00–30:00 |
| W12-004 | 把 MySQL 當 SQLite 初始化 → `no such table: kook_message`、`missing database` | 第26課 15:00–18:00 |
| W12-004 | `ClassCastException: Long cannot be cast to Integer`（MySQL 的 `count` 是 `Long`，`RoomMessageDao.java:264`） | 第26課 18:00–21:00 |
| W12-005 | 綁定碼唯一性靠資料庫；清空資料庫會讓舊使用者拿到新碼（孤兒資料） | 第26課 33:00–36:00 |
| W12-006 | 預設值文字衝突：口述「綁定頻道」／「綁定」vs 畫面 `'默认频道'`／`'绑定 '`（含尾隨空白） | 第26課 33:00–36:00；第27課 03:00–06:00 |
| W12-007 | `setChannelName()` 被傳入純數字 channel ID，方法名與語義不符 | 第26課 25:00–32:24 |
| W12-007 | 「自動建立頻道」是隱式副作用，設定打錯會真的開出新頻道 | 第26課 30:00–33:00 |
| W12-008 | `Not on FX application thread; currentThread = Thread-4`：非 FX 執行緒改 UI | 第26課 24:00–27:00 |
| W12-008 | 下線顯示延遲（WebSocket 已關但 UI 仍顯示在線） | 第26課 27:00–33:00 |
| W12-008 | 口述的 `viewStyle`／`onlineStyle` 樣式封裝類在畫面中完全未出現 | 第26課 24:00–27:00 |
| W12-009 | ASR 對照只適用語音層；畫面層的誤讀方向不同（`RoomProp`／`BossProp`／`ReadDrop`／`KuoManager`） | 第27課 全課；第26課 全課 |
| W12-010 | **筆數衝突**：畫面 v000＝6 rows；口述＝七行（多的第六項是 `ws URL`＝`channelUrl`） | 第27課 03:00–06:00、24:00–27:00 |
| W12-010 | **`guildId` vs `qqId` 兩說相反**：口述「有 `guildId` 也沒有 `qqId`」／畫面「有 `qqId` 也沒有 `guildId`」 | 第27課 03:00–06:00 |
| W12-010 | 欄寬衝突：口述「改成 20」vs 畫面 `VARCHAR(255)` | 第27課 03:00–06:00 |
| W12-011 | 取值 API 衝突：口述 `MapCommonUtils.getString(map, "configName")` vs 畫面 `map.get("config_name").toString()`（null 會 NPE） | 第27課 06:00–09:00 |
| W12-011 | 駝峰／蛇形耦合：`config_name` 對 `botToken` 會每筆拋 `NoSuchFieldException` 並被吞掉 | 第27課 06:00–09:00 |
| W12-012 | **UPDATE 的 `where` 用 `field.getName()` 比對 `config_name` 會靜默影響 0 列** | 第27課 09:00–12:00 |
| W12-012 | 反射通用讀寫的代價：**失去編譯期檢查**，欄位改名只會執行時靜默失敗 | 第27課 09:00–12:00、第六節 (a) 13 |
| W12-012 | `updateKookProp` 放哪個類別互斥：口述 `KookConfigDao` vs 畫面 `Messages.java` | 第27課 09:00–12:00 |
| W12-013 | 建表 `config_data` vs 程式 `config_value`；`catch (Exception)` 吞例外使問題無聲 | 第27課 24:00–27:00 |
| W12-013 | 畫面錯誤是 `sql injection violation`（語法層，來自 `SqlSessionManager`），口述是讀不到值（結果層）——可能兩個 bug | 第27課 24:00–27:00 |
| W12-014 | 校驗失敗 `return` 忘記 `setDisable(false)` → 按鈕永久卡死 | 第27課 27:00–30:00 |
| W12-014 | 口述布林語義自我修正兩次（`not pass check`）；畫面為 `testPassBossProp()`，兩者語意相反 | 第27課 24:00–30:00 |
| W12-015 | `textProperty` listener 只在值變動時觸發，沿用預設值會把其他欄位清空 | 第27課 30:00–33:00 |
| W12-015 | v008 對話框只有四欄（`代表人物QQ` 等），為「綁定碼」時代舊版 UI | 第27課 30:00–33:00 |
| W12-016 | `isNull`（true=已取消）與 `isCtrl`（true=有效輸入）布林語義相反 | 第27課 18:00–21:00 |
| W12-016 | 按鈕顏色衝突：口述綠色 vs 畫面 `createShadowButton("配置", "配置")` | 第27課 00:00–03:00 |
| W12-016 | v004 的 `buildBossProp` 八欄屬 BOSS 語境，v005 畫面是「掉宝/刷怪 讀取配置」，皆為跨版本素材 | 第27課 15:00–24:00 |
| W12-016 | `List<String> defaults` 收 `Integer` 會編譯錯誤，須 `String.valueOf` | 第27課 15:00–18:00 |
| W12-017 | **開源專案不可沿用預設配置**（Token／guildId／channelId 會導致頻道資訊洩露） | 第27課 12:00–15:00 |
| W12-017 | 畫面 `setProp` 中 `setBindKeywords` 那一行是註解狀態，與必填校驗矛盾 | 第27課 30:00–33:00 |
| W12-017 | `asr1` 參數語意不明，無法由素材判定 | 第27課 30:00–33:00 |
| W12-018 | 講者對 401 成因自我改口（先說不是我們的問題、再說是我們的問題） | 第27課 30:00–33:00 |
| W12-019 | 視窗標題隨片段改變（兩課合計 15 種），單一影片不可能同時是 JavaFX 與 Swing | 第26課／第27課 全課 |
| W12-019 | v009 讀到 `cn.koo.heavenms.nap`、`HeavenMS-Nap v002 控制台`，疑為另一個專案版本 | 第27課 36:00–40:00 |
| W12-019 | v003（`cn.xiaowen.ui.pane` 副本切頻道限制）、v007（Spring Boot 痕跡）與本課主軸無關 | 第27課 12:00–16:00、28:00–32:00 |
| W12-020 | 「遷 2.x」「Readme 對比圖」在片尾**尚未完成**，屬計畫非既成事實 | 第27課 36:00–40:00 |
| W12-020 | 分支名三方並存：`v.0.4-course`（第26課畫面）、`simple`（第27課畫面）、`2.x`（口述） | 第26課 30:00–36:00；第27課 36:00–40:00 |
| W12-020 | GitHub（口述）vs Gitee（畫面）並存，倉庫網址未在畫面出現 | 第27課 36:00–40:00 |
