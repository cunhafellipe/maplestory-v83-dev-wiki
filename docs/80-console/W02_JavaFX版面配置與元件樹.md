# W02　JavaFX 版面配置與元件樹

> 本頁為主題式重組，內容全部來自原始的 42 份逐片教學筆記，未引入外部資訊。
> 每條可獨立引用；條目 ID 穩定，請勿隨意改號。

## 覆蓋來源

| 課次 | 筆記檔 | 本頁取用範圍 |
|---|---|---|
| 第一課 | `第一課_教學筆記.md` | 20:00–46:00（佈局全段，含六種佈��與程式碼骨架） |
| 第二課 | `L02_第二课_教學筆記.md` | 佈局選型比對段、`setPadding`／`Insets` 段 |

## 速查

| ID | 一句話 |
|---|---|
| W02-001 | 佈局決定介面上限，選型要把候選逐一比對完 |
| W02-002 | AnchorPane：釘住某個角落，拖視窗不動 |
| W02-003 | BorderPane：上／下／左／右／中五區，中間自動吃滿 |
| W02-004 | FlowPane：自適應換行，像 Word |
| W02-005 | GridPane：行列從 0 開始，可跨行跨列 |
| W02-006 | GridPane 的按鈕不會自動撐滿，必須 `setMaxSize` |
| W02-007 | VBox：垂直一列，永不換列 |
| W02-008 | HBox：水平一列，**超出直接截斷不換行** |
| W02-009 | StackPane：全部疊在一起，用於翻頁與場景切換 |
| W02-010 | `Insets` 四值順序是**上、右、下、左** |
| W02-011 | FlowPane 與 HBox 的差別就在「會不會換行」 |
| W02-012 | `ColumnConstraints`／`RowConstraints` 用百分比撐滿網格 |

## 條目

### W02-001　佈局決定介面上限，選型要把候選逐一比對完

- **關鍵字**：`BorderPane` `FlowPane` `GridPane` `HBox` `VBox` `AnchorPane` `StackPane` `VBox`
- **來源**：第一課 20:00–24:00；第二課 佈局選型段｜`第一課_教學筆記.md`、`L02_第二课_教學筆記.md`
- **要點**：講者的核心觀念是「**功能好做、介面難做**，所以一開始就要敲定佈局」，
  **佈局是貫穿整個開發的東西**。實作時是把需求在七種佈局間**逐一比對**：
  第二課的口述流程是 `BorderPane`／`FlowPane`／`GridPane`／`HBox`／`VBox`／`AnchorPane`／`StackPane`
  七項都試過，最後選 **`VBox`** 作為根節點。
  `StackPane` 被排除的理由講者講得很直接：「**它把元素堆疊在一起，我們明顯不是堆疊在一起**」。
- **坑**：⚠️ **口述與畫面記錄的完整度不同**——口述逐一比對了七項，
  但第二課畫面只記錄到三項。筆記已標明以口述為準。
  講者也自嘲「調試 UI 就是這樣的……要不停地去看，然後改」，實際排版是**一輪輪試出來的**。

### W02-002　AnchorPane：釘住某個角落，拖視窗不動

- **關鍵字**：`AnchorPane` `setTopAnchor` `setBottomAnchor` `setLeftAnchor` `setRightAnchor` `10.0`
- **來源**：第一課 24:00–28:00｜`第一課_教學筆記.md`
- **要點**：錨點佈局＝**設定一個元素距離上、下、左、右各多少像素**。
  用途是自適應：拖動視窗大小時按鈕永遠維持在角落不動。示範程式碼：

  ```java
  Button btn4 = new Button("test4");
  AnchorPane root = new AnchorPane();
  root.getChildren().add(btn4);
  AnchorPane.setBottomAnchor(btn4, 10.0);
  AnchorPane.setRightAnchor(btn4, 10.0);
  Scene scene = new Scene(root, 500, 500);
  primaryStage.setScene(scene);
  ```

  執行結果：視窗 500×500，標題「冒險島」，右下角有 `test4`；拖曳改變視窗大小，
  按鈕**永遠保持距離右下各 10 像素**。
- **坑**：⚠️ **口述與畫面的按鈕編號對不上**——口述是「六顆按鈕、btn1 在左下、btn2 在右上」，
  畫面卻是註解掉 `btn1`–`btn3`、只留 `btn4` 在右下角。重點一致（示範錨點的固定效果），
  **細節以畫面程式碼為準**。

### W02-003　BorderPane：上／下／左／右／中五區，中間自動吃滿

- **關鍵字**：`BorderPane` `setTop` `setBottom` `setLeft` `setRight` `setCenter` `IDEA` `VS Code`
- **來源**：第一課 28:00–30:00｜`第一課_教學筆記.md`
- **要點**：把介面分成**五個區域：頂部、底部、左部、右側、中心**，
  **中心會自動擴展吃掉剩餘空間**。API 為 `setTop(...)`、`setBottom(...)`、`setLeft(...)`、
  `setRight(...)`、`setCenter(...)`，每個位置都能放元素或整個佈局。
  用途是主框架——講者直接開了 **IDEA 與 VS Code** 當例子（都是「上／左／右／下／中間」結構）。
- **坑**：（本條未發現坑）

### W02-004　FlowPane：自適應換行，像 Word

- **關鍵字**：`FlowPane` `setHgap` `setVgap` `setOrientation` `Orientation.VERTICAL` `換行`
- **來源**：第一課 30:00–33:00、38:00–45:00｜`第一課_教學筆記.md`
- **要點**：**按加入順序排列，當元件寬度超過容器寬度就自動換到下一行**。
  講者強調重點不在「會換行」，而在**改變容器大小時會自動重新排列以求最佳展示**：
  視窗變寬，原本掉到第二排的按鈕會自己回到第一列；變窄又會掉下去。用途是**自適應效果的最佳選擇**。
  可用 `setHgap`／`setVgap` 設水平垂直間隙，用 `setOrientation` 改成水平排列：

  ```java
  FlowPane root = new FlowPane();
  root.setOrientation(Orientation.VERTICAL);   // 查了百度翻譯才確定這個單字
  root.getChildren().addAll(btn1, btn2, btn3, btn4, btn5, btn6);
  ```

  並可設對齊：

  ```java
  root.setAlignment(Pos.CENTER_LEFT);
  ```

  執行後按鈕群組從「靠上」變成「左側垂直置中」，拖曳改視窗大小仍維持左側置中。
- **坑**：（本條未發現坑）

### W02-005　GridPane：行列從 0 開始，可跨行跨列

- **關鍵字**：`GridPane` `add(child, columnIndex, rowIndex, colspan, rowspan)` `ColumnConstraints` `RowConstraints`
- **來源**：第一課 33:00–38:00｜`第一課_教學筆記.md`
- **要點**：把元件排進網格，可自訂**行與列**，每個元件可佔一格、多格。
  **行列都從 0 開始**（和 List、Map、陣列一樣，0 就是第一）。
  跨行跨列簽名（JavaDoc 原文）：

  ```java
  public void add(Node child, int columnIndex, int rowIndex, int colspan, int rowspan)
  // Adds a child to the gridpane at the specified column,row position and spans.
  ```

  口述的元件位置（由上而下）：`button 1` 第 0 行第 0 列；`button 2` 第 0 行第 2 列；
  `button 3` 第 1 行第 2 列；`button 4` 第 2 行第 3 列（**用 `add` 逐一指定，不用 `addAll`**）；
  `button 5` 第 3 行第 0 列佔 2 列 1 行；`button 6` 第 3 行第 2 列同樣佔 2 列 1 行
  （前兩列已被 button 5 佔用所以必須從第三列開始）。
  欄列比例設定：

  ```java
  ColumnConstraints cc1 = new ColumnConstraints();
  cc1.setPercentWidth(33.33);      // 欄寬 1/3
  RowConstraints rc1 = new RowConstraints();
  rc1.setPercentHeight(50);        // 列高 1/2
  ```

  案例：`root.add(btn1, 0, 0, 2, 1);`、`root.add(btn2, 2, 0, 1, 2);`、`root.add(btn3, 0, 1, 2, 1);`
- **坑**：⚠️ **佔格順序不能亂**——`button 5` 佔掉第 0、1 列後，`button 6` 只能從第 2 列開始。
  跨格後必須配合 W02-006 的 `setMaxSize`，否則按鈕不會撐滿。
  ⚠️ 講者明講這課只需要知道它長什麼樣，**實際運用留待後面**。

### W02-006　GridPane 的按鈕不會自動撐滿，必須 `setMaxSize`

- **關鍵字**：`setMaxSize` `Double.MAX_VALUE` `GridPane` `撐滿`
- **來源**：第一課 33:00–38:00、38:00–40:00｜`第一課_教學筆記.md`
- **要點**：按鈕預設**不會撐滿它跨越的格子**，必須對每顆按鈕加：

  ```java
  btn.setMaxSize(Double.MAX_VALUE, Double.MAX_VALUE);
  ```

  這是 GridPane 情境的**必要解法**。
- **坑**：⚠️⚠️ **`setMaxSize` 的結論不可跨情境套用**——講者在 **VBox** 情境裡把 `setMaxSize(...)`
  評為「**這個沒意義**」，但在 **GridPane** 情境裡它是必要的。
  兩個結論都對，但**絕對不能互相套用**。這是本批教學裡最容易被記錯的一條。

### W02-007　VBox：垂直一列，永不換列

- **關鍵字**：`VBox` `setSpacing` `垂直排列` `setPadding` `setStyle`
- **來源**：第一課 38:00–40:00、40:00–45:00｜`第一課_教學筆記.md`
- **要點**：**非常簡單直覺**的佈局：按垂直方向一個一個往下排。案例元件間隔設 20，
  加入 `button 1`～`button 6`。逐顆加入的推理：第一行被佔 → 第二行 → 第三行……
  所有元件都只能垂直排列。示範外框設定：

  ```java
  // VBox
  VBox root = new VBox();
  root.setPadding(new Insets(10));
  root.setStyle("-fx-border-color: red; -fx-border-radius: 1; -fx-pref-width: 700; -fx-pref-height: 500;");
  ```

  講者一開始設了靠右對齊，中途自己說「還不到時候」把它移掉了。
- **坑**：見 W02-006——`setMaxSize` 在 VBox 情境被講者評為「沒意義」，與 GridPane 相反。
- **相關**：見 W04（選單系統），VBox 是選單容器的基礎

### W02-008　HBox：水平一列，超出直接截斷不換行

- **關鍵字**：`HBox` `setSpacing` `不換行` `截斷` `Horizontal`
- **來源**：第一課 38:00–45:00｜`第一課_教學筆記.md`
- **要點**：HBox 與 VBox 的差別就是一個水平、一個垂直。講者的記憶法是**各自取英文第一個字母**：
  `Horizontal` → 水平 → **H**Box；`Vertical` → 垂直 → **V**Box
  （講者笑說不敢亂念怕口誤，還打開百度翻譯查單字）。示範：

  ```java
  // HBox：線性排版
  HBox root = new HBox();
  root.setSpacing(10);
  ```

  測試手法是**把同一個 `pane` 重複 `addAll` 十多個**來看換行行為，
  結果是 HBox **全部擠在同一條水平線上，超出部分直接被截斷，不換行**。
- **坑**：⚠️ **HBox 不換行**。想要換行必須用 `FlowPane`（見 W02-011）。
  註解裡講者的原話是 `// 2) 线性排版 类似直男，一条路走到黑`。
  講者還提醒口述容易把 HBox 與 VBox 講反（`button 1` 佔第一列 vs 第一行），
  **以畫面示範為準**。

### W02-009　StackPane：全部疊在一起，用於翻頁與場景切換

- **關鍵字**：`StackPane` `setAlignment(Pos.…)` `button center` `場景切換` `翻頁`
- **來源**：第一課 40:00–45:00；第二課 佈局選型段｜`第一課_教學筆記.md`、`L02_第二课_教學筆記.md`
- **要點**：效果是**把所有元件疊在一起**。案例加入六顆按鈕，預設對齊是 `button center`（中間偏下），
  只有第一顆單獨設成靠左中，所以畫面上**只看得到最上面兩顆**（button 1 與 button 6）。
  講者加點擊事件「逐層剝開」才發現六顆按鈕全都疊在同一個位置。
  **實際用途是場景切換／翻頁**：把所有頁面先畫出來疊在一起，切頁時把最上面的移走或隱藏、
  露出下面那頁；返回時再放回最上層。講者評價這種做法「可能不太優雅，但確實是一種實現方式」。
- **坑**：⚠️ **忘記設對齊位置就會出現「元件不見」的錯覺**——因為全部疊在一起，後加入的會蓋住先前的。
  ⚠️ 第二課選型時 `StackPane` 被排除，理由是「我們明顯不是堆疊在一起」。
  同一個容器在不同需求下結論相反，要看需求決定。

### W02-010　`Insets` 四值順序是上、右、下、左

- **關鍵字**：`setPadding` `Insets` `上、右、下、左` `單值` `四值`
- **來源**：第二課 35:00–40:00｜`L02_第二课_教學筆記.md`
- **要點**：口述原話：「`set padding` 裡面有一個 **in…要傳一個 inset**。
  這個 inset **可以傳一個值，也可以傳四個值**。這四個值就是**距離上、右、下、左各個的距離**。
  我們直接設置一個的話，它就會自動把**上下左右全部設置成這個值**。」
  實作上先統一用單值 10，再改成非對稱：
  「設置距離上半部分我們可以設置成 **5**……**距離右边，我們可以設置成 10**。
  然後距離下邊，**它是一個順時針的。上、右、下、左**」→ **`Insets(5, 10, 5, 10)`**。
  原因記錄為「把 44px 撐高修正到實測 31px」，最終窗頭高度**接受 31**。
- **程式碼**：

  ```java
  stageHead.setPadding(new Insets(10));                  // 上、右、下、左 = 10
  HBox.setMargin(close, new Insets(0, 0, 0, 180));
  ```

- **坑**：⚠️ **四值順序是順時針的「上、右、下、左」，不是 CSS 的「上、右、下、左」之外的常見其他順序**——
  講者特別強調「**它是一個順時針的**」。寫非對稱邊距時務必記住這個順序，寫反不會報錯，只會排版錯亂。
  ⚠️ `Insets` 這個建構子與 Swing `JFrame` 的 `Insets` 同名但無關，
  第二課 v008 曾解析到 Swing `JFrame` 美化片段（`setUndecorated(true)`、`UIManager`、`setOpacity`），
  與本課「保留系統邊框、自訂窗頭」的策略**方向相反**，`setOpacity`／`UIManager` 在口述中完全未出現。

### W02-011　FlowPane 與 HBox 的差別就在「會不會換行」

- **關鍵字**：`FlowPane` `HBox` `換行` `截斷` `setHgap` `setVgap`
- **來源**：第一課 38:00–40:00｜`第一課_教學筆記.md`
- **要點**：講者用**同一組元件**（同一個 `pane` 重複 `addAll` 十多個）做對照實驗：

  ```java
  // FlowPane：空間不足自動換行
  FlowPane root = new FlowPane();
  root.setHgap(10);
  root.setVgap(10);

  // HBox：線性排版
  HBox root = new HBox();
  root.setSpacing(10);
  ```

  結果：`FlowPane` 橫向排到紅框邊界就**自動換行**到第二列；
  `HBox` 全部**擠在同一條水平線上，超出部分直接被截斷，不換行**。
  註解原文：`// 1) 流式排版 类似word排版，空间不足会自动换行`、
  `// 2) 线性排版 类似直男，一条路走到黑`。
- **坑**：⚠️ **選錯就是「東西不見」**——`HBox` 超出的部分不是換行而是**直接被截斷**，
  視窗變窄時元件會消失在畫面外。
- **相關**：見 W03（視窗與自訂標題列）——標題列就是 HBox 的典型應用

### W02-012　用百分比撐滿網格

- **關鍵字**：`ColumnConstraints` `setPercentWidth` `RowConstraints` `setPercentHeight` `33.33` `50`
- **來源**：第一課 33:00–38:00｜`第一課_教學筆記.md`
- **要點**：

  ```java
  ColumnConstraints cc1 = new ColumnConstraints();
  cc1.setPercentWidth(33.33);      // 欄寬 1/3
  RowConstraints rc1 = new RowConstraints();
  rc1.setPercentHeight(50);        // 列高 1/2
  ```

  搭配 `add(child, col, row, colspan, rowspan)` 使用，視窗大小改變時網格比例維持。
  示範時視窗標題為 `Java`，內含 `btn1`～`btn5`；用 `Ctrl + /` 在 FlowPane 與 GridPane 區塊間切換，
  `Shift + F10` 執行。
- **坑**：（本條未發現坑）

## 本頁的坑總表

| ID | 坑 | 來源 |
|---|---|---|
| W02-001 | 口述逐一比對七種佈局，畫面只記錄三項，以口述為準 | 第二課 佈局選型段 |
| W02-002 | 口述按鈕編號與畫面不符（口述 btn1 左下／畫面只留 btn4 右下） | 第一課 24:00–28:00 |
| W02-004 | 沒有坑，但強調重點在「容器變化時自動重排」而非單純換行 | 第一課 30:00–33:00 |
| W02-005 | 佔格順序會被前面的元件鎖死，跨格後要配 `setMaxSize` | 第一課 33:00–38:00 |
| W02-006 | ⚠️ `setMaxSize` 在 GridPane 必要、在 VBox 被評為「沒意義」，**不可互套** | 第一課 33:00–40:00 |
| W02-008 | HBox 不換行，超出直接被截斷 | 第一課 38:00–45:00 |
| W02-009 | 不設對齊會出現「元件不見」的錯覺；StackPane 在第二課又被排除 | 第一課 40:00–45:00 |
| W02-010 | `Insets` 四值是**上、右、下、左**（順時針）；Swing `JFrame` 同名類別是另一回事 | 第二課 35:00–40:00 |
| W02-011 | 選 HBox 忘記換行＝元件消失在畫面外 | 第一課 38:00–40:00 |
| — | 第一課解析 JSON 未保留，本頁該課內容無法做 token 級回溯驗證 | 素材稽核 |
| — | 第一課同時出現多個同名專案副本，追程式碼前先確認是哪一份 | 素材稽核 |
