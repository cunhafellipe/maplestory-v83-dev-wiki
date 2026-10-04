# W1-3: MapleStory 0.83.exe (原版) vs MapleStory v83(已繁化).exe (繁化版) — Binary Diff

_Generated: 2026-09-27T22:48:53_

## 1. 檔案 Hash 與基本資訊

| 項目 | 原版 | 繁化版 |
|---|---|---|
| 檔案大小 | 4,281,928 bytes (4.28 MB) | 9,920,523 bytes (9.92 MB) |
| MD5 | `09d00a6ebd70aaf0026d6feb764a1f21` | `727a9ac610bf0b4b788356e5c9b54289` |
| SHA256 | `2040e4481e2c545eeb4cd6556a07094dff6466449144ffe2be06b46f499e8da8` | `faa284ec6048bd582570fe6111ee9d6c72e109f581d16ced215ab97e7a39c12c` |

- 大小差: **+5,638,595 bytes (+131.7%)**, 比例 **2.317x**
- 兩個檔案完全不重複 (MD5/SHA256 全異) — 已非單純的字串替換,而是 PE 重組。

## 2. PE Header 對照

| 欄位 | 原版 | 繁化版 | 差異 |
|---|---|---|---|
| Machine | 0x014c (i386) | 0x014c (i386) | 相同 |
| Magic | PE32 | PE32 | 相同 |
| NumSections | 7 | 6 | **-1** |
| TimeDateStamp | 2010-02-26 09:27:31 UTC | 2010-02-17 16:14:01 UTC | 早 9 天(編譯/重組時間不同) |
| Characteristics | 0x010f | 0x010f | 相同 |
| EntryPoint | 0x00a8c000 | 0x00663ff3 | 移動 |
| ImageBase | 0x400000 | 0x400000 | 相同 |
| BaseOfCode | 0x00001000 | 0x00001000 | 相同 |
| SizeOfCode | 7,270,400 | 7,270,400 | **相同** |
| SizeOfInitializedData | 1,216,512 | 1,216,512 | **相同** |
| SizeOfUninitializedData | 0 | 0 | 相同 |
| SizeOfImage | 11,067,392 | 11,096,064 | +28,672 (繁化 +28KB virtual) |

> 觀察:`SizeOfCode` 與 `SizeOfInitializedData` 兩版數值完全相同,但實體檔案大小差 5.6 MB;差異幾乎
> 全部來自 section 內部資料(non-header 區段填補)與 packing。

## 3. Section Table 對照

### 原版 (7 sections)

| # | Name | VAddr | VSize | RawOff | RawSize |
|---|---|---|---|---|---|
| 0 | `<empty>` (.text?) | 0x00001000 | 8,355,840 | 0x00001000 | 3,006,464 |
| 1 | .rsrc | 0x007f9000 | 128,208 | 0x002df000 | 36,864 |
| 2 | .idata | 0x00819000 | 4,096 | 0x002e8000 | 4,096 |
| 3 | `<empty>` (.data?) | 0x0081a000 | 1,404,928 | 0x002e9000 | 4,096 |
| 4 | **uilplxhk** | 0x00971000 | 1,159,168 | 0x002ea000 | 1,159,168 |
| 5 | **tfqhbstk** | 0x00a8c000 | 4,096 | 0x00405000 | 4,096 |
| 6 | **gndhordv** | 0x00a8d000 | 4,096 | 0x00406000 | 4,096 |

### 繁化版 (6 sections)

| # | Name | VAddr | VSize | RawOff | RawSize |
|---|---|---|---|---|---|
| 0 | `<empty>` (.text?) | 0x00001000 | 8,355,840 | 0x00001000 | 8,355,840 |
| 1 | .rsrc | 0x007f9000 | 131,072 | 0x007f9000 | 128,208 |
| 2 | .idata | 0x00819000 | 4,096 | 0x00819000 | 4,096 |
| 3 | `<empty>` (.data?) | 0x0081a000 | 2,588,672 | 0x0081a000 | 1,413,120 |
| 4 | **.macktt** | 0x00a92000 | 8,192 | 0x00973000 | 8,192 |
| 5 | `<empty>` | 0x00a94000 | 4,096 | 0x00975000 | 4,096 |

### 差異分析

- **.text (首段,空名)**:
  - 原版 RawSize 3.0 MB vs VSize 8.4 MB (差 5.3 MB 為 BSS/uninitialized)
  - 繁化版 RawSize = VSize = 8.4 MB (**整段實體寫入檔案,5.6 MB 增量主要來自此處**)
- **.rsrc**:
  - 原版 RawSize 36,864 vs VSize 128,208 (差 91,344 為 virtual-only)
  - 繁化版 RawSize 128,208 vs VSize 131,072 (整段實體寫入,並 padding +2,864)
  - 檔頭相同(同個 VS_VERSION_INFO/manifest),內部 data entry 的 RVA 偏移被重排
- **.idata**: 兩版皆 4 KB,內容相同(只是搬移到不同 raw offset)
- **.data (空名)**: 從 RawSize 4 KB / VSize 1.4 MB → RawSize 1.4 MB / VSize 2.6 MB
  - **VSize +1,183,744 (+84%)**、RawSize +1,409,024 — 繁化版把大量資料從 BSS 拉進實體檔案
- **自訂段名徹底換掉**:
  - 原版 3 個奇怪命名:`uilplxhk`、`tfqhbstk`、`gndhordv` (VSize 各 4 KB~1.1 MB)
  - 繁化版只剩一個 `.macktt` (8 KB) + 1 個空名 (4 KB)
  - 段名在檔案中實際存為 `b'.mackt\x00t'`
  - 繁化版的最後一個 section 內含 SolidDaima_Rev8_200901029\setting.ini
    — **SolidDaima** 是真實存在的 WZ 工具,`ACGame_GL\BinTool` 是其工作路徑。
    不存在名為「WzPacker」的工具。

## 4. Import Table 對照

### 原版:1 個 DLL,1 個函式

```
kernel32.dll    (僅 1 個 import — FileTimeToLocalFileTime)
```

### 繁化版:17 個 DLL,靜態函式表為空

```
advapi32.dll, dinput8.dll, gdi32.dll, kernel32.dll, netapi32.dll,
oleaut32.dll, shell32.dll, user32.dll, version.dll, wininet.dll,
winmm.dll, ws2_32.dll, ijl15.dll, iphlpapi.dll, mss32.dll,
nmcogame.dll, ole32.dll
```

> 注意:繁化版的 `IMAGE_IMPORT_DESCRIPTOR.OriginalFirstThunk` 全部為 **0**;僅 `FirstThunk`
> 有 pre-bound RVAs。`LoadLibraryA` 與 `GetProcAddress` 仍在 import 表中,部分 API 在執行期解析。
> Ghidra 12.1.4 分析可還原出 **238 個具名 import**(分佈於 17 個 DLL)。

### DLL 集合差異

- 只在原版:*(無)*
- 只在繁化版:`advapi32.dll, dinput8.dll, gdi32.dll, netapi32.dll, ole32.dll, oleaut32.dll, 
  shell32.dll, user32.dll, version.dll, wininet.dll, winmm.dll, ws2_32.dll, 
  ijl15.dll, iphlpapi.dll, mss32.dll, nmcogame.dll` (+16 DLLs)
- 兩版共有:`kernel32.dll`

> 推測新增 imports 的目的:
> - `user32.dll / gdi32.dll / shell32.dll`:UI 渲染、視窗管理(繁化 UI hook)
> - `version.dll`:取得檔案版本(啟動檢查)
> - `advapi32.dll / netapi32.dll`:註冊表 / 網路設定
> - `ijl15.dll / mss32.dll / nmcogame.dll`:遊戲圖形、音效、網路(原本可能動態載入,現改靜態)
> - `dinput8.dll`:DirectInput 鍵盤/滑鼠(解析度切換需要)
> - `winmm.dll / ws2_32.dll / wininet.dll / iphlpapi.dll`:音訊、socket、HTTP、IP helper
> - `ole32.dll`:實際只用於 `CoCreateGuid`(`CoCreateInstance` 出現 0 次)
- `oleaut32.dll`:OLE automation
- WZ 層不走 Windows COM,而是綁定 Wizet 自家的 **Pixi** 框架:`PcCreateObject`、
  `PcRootNameSpace`、`PcSerializeObject` 等,經由 `GetProcAddress(h, ...)` 取得

## 5. 字串池比對 (ASCII + UTF-16LE,長度 ≥ 6)

| | 原版 | 繁化版 |
|---|---|---|
| 獨立字串數 | 7,038 | 4,593 |
| 共同字串數 | **48** | |
| 僅原版 | 6,990 | |
| 僅繁化 | | 4,545 |
| **Jaccard 相似度** | **0.0041** | |

> 共同字串幾乎全是 PE boilerplate:VS_VERSION_INFO 區塊、Manifest XML、DOS stub 訊息
> ("!This program cannot be run in DOS mode.")、`kernel32.dll`、`MapleStory.exe`、`Wizet MapleStory`。
> 實際遊戲字串/錯誤訊息幾乎沒有重疊 — 表示兩個 binary 的代碼段 layout 是各自獨立的。

### 關鍵字命中對照

| 關鍵字 | 原版 | 繁化版 | 觀察 |
|---|---|---|---|
| `Maple` | 3 | **20** | +17 處,Nexon/MapleTV/URL 路徑(如 `Nexon\MapleStory\MapleTV`、`patch.mapleglobal.com`) |
| `Cash` | 0 | **8** | +8 處,新增 Cash Shop 相關字串(如 `PayPal/PayByCash`) |
| `wz` | 82 | **23** | -59 處(.wz 載入相關的字串被刪減/替換) |

### 表面字串以外 — 觀察到的 CJK 編碼

- 用 UTF-16LE 解整檔得到的 CJK code-point 數量:原版 753,527 vs 繁化版 1,261,070
- **但這數字誤導性高**:把 x86 code bytes 當 UTF-16LE 解會誤命中 CJK 範圍。實際從 `.data` (VSize 2.6 MB)
  抽 UTF-16LE 字串後看到的「CJK 長字串」幾乎全部是 XOR 加密或 byte-shuffled 編碼的內部資料
  (例:某 byte 序列誤解讀為 `慣湮瑯爠湵甠摮牥愠嘠物畴污`,實際反序解回 ASCII 是 
  `cannot run under a Virtual...` — 這是 anti-VM 偵測訊息,並非中文)
- **結論**:繁化版的實際繁體中文字串**並沒有以可讀格式直接嵌在這個 PE 內**。它們屬於「MapleStory
  客戶端 String.wz 封包檔」,在 runtime 由客戶端從獨立資料檔載入(CSV 檔 5,658 列即為
  該 .wz 內文字串 ID 對照表)。

## 6. Resource Directory 對照

| 項目 | 原版 | 繁化版 |
|---|---|---|
| .rsrc RawSize | 36,864 | 128,208 |
| .rsrc VSize | 128,208 | 131,072 |
| 條目總數 | 31 | **31** |
| Resource SHA256 | `3a443f9e...0c500c4a80942` | `8d45e62f...8c8ef59d` |

### 結構 (兩版完全相同)

```
/BITMAP          (4 entries: #116, #117, #118, #119, 各 16,372 bytes)
/ICON            ├─ CURSOR     2,216 bytes
│                 └─ BITMAP     1,384 bytes
/DIALOG          (2 entries: #109=92B, #115=128B)
/RCDATA          (#27893: 56,620 bytes — 最大的單一 resource)
/GROUP_ICON      (#101: 34 bytes)
/VERSION         (840 bytes — 公司名 Wizet,檔案 1,0,0,1)
/MANIFEST        (607 bytes — requireAdministrator)
```

> 觀察:Resource 樹狀結構與各 leaf 的 size 兩版完全一致;只有 data entry 的 **RVA 偏移**
> 因為 .rsrc 重新 layout 而不同(原 0xa8xxxx → 繁化 0x7f9xxx ~ 0x80xxxx),以及前 36 KB 的 directory
> header 兩版完全相同。`RCDATA #27893` (56,620 bytes) 的內容(可能是字型/圖示二進位資料)在兩版中
> 也位置相同。

## 7. 結論 — 繁化版改了什麼?

### (a) PE 結構層

| 改動 | 細節 |
|---|---|
| Section 數 | 7 → 6 (原版 3 個自訂段合併為 1 個 `.macktt` + 1 個空名) |
| .text 段 | 從「3 MB 實體 + 5.4 MB virtual (BSS)」改為「8.4 MB 全實體」— 解壓並補齊 |
| .data 段 | VSize 1.4 MB → 2.6 MB (+1.18 MB)、RawSize 4 KB → 1.4 MB (+1.4 MB)— 大量原 BSS 區段寫入實體檔案,應為新增的 runtime 資料結構/lookup table |
| .rsrc 段 | RawSize 36 KB → 128 KB (從 BSS 拉進實體);VSize 128 KB → 131 KB (+3 KB padding);內容樹狀結構完全不變 |
| Imports | 從 1 個 DLL / 1 個函式擴展到 17 個 DLL / **238 個函式**;INT 為 0 但 Ghidra 可還原具名 import |
| EntryPoint | 0x00a8c000 → 0x00663ff3(由加殼解壓跳板轉為正常 .text 入口) |
| TimeDateStamp | 2010-02-26 → 2010-02-17(早 9 天) |

### (b) 內容層

| 改動 | 細節 |
|---|---|
| 共通字串 | 僅 48/7090(0.4%)是 PE/Manifest/version boilerplate,實際遊戲代碼完全獨立 |
| `Maple` / `Cash` / `wz` 關鍵字 | 分別 +17 / +8 / -59 處,顯示 Cash Shop 相關字串與 .wz 載入路徑被修改 |
| 繁體中文字串 | **沒有以可讀格式嵌入 PE 內**;實際繁體字串載入機制應在 runtime 從獨立 .wz 封包(未提供給本次比對)載入 |
| Resource 內容 | 31 個條目,所有 leaf 大小相同,RCDATA 等大塊資源原封不動搬遷 — 推測:解析度 patch + 繁化 UI hook 需要的字型/圖示直接複用既有 RCDATA |
| 自訂段名 | `uilplxhk / tfqhbstk / gndhordv` → `.macktt`(檔案中存為 `b'.mackt\x00t'`);同 section 內含 `SolidDaima_Rev8_200901029\setting.ini` 路徑 |

### (c) 已驗證的事實

1. **原版受 Nexon CSecurity 保護**:首要 section entropy 7.98、import 表僅
   `kernel32.dll!FileTimeToLocalFileTime` 一項、EntryPoint 位於 4 KB 隨機命名 section `tfqhbstk`。
   簽章掃描確認 **Themida / WinLicense / VMProtect / ASProtect / Enigma / UPX 全部 0 命中**。
   識別依據是解包版字串池中的 RTTI:`CSecurityException`、`CSecurityInitFailed`、
   `CSecurityUpdateFailed`、`CSecurityThreatDetected`、`CSecurityClearFailed`。
2. **繁化版已經解壓並以 SolidDaima 處理**:`.text` 完整落地、`238` 個 import 可還原、
   最後 section 內含 SolidDaima_Rev8_200901029\setting.ini。
   不存在名為「WzPacker」的工具。
3. **「繁化」並非 PE 內字串替換**:繁中字串不在 PE 內(可讀的繁體中文 0 條),
   由客戶端在執行期從獨立資源載入。
4. **「解析度調整」功能**:對應 `user32.dll / gdi32.dll / dinput8.dll` 的 import —
   UI、視窗、DirectInput 為解析度切換必要 API。實際實作見
   [exe-reverse-engineering §5](../exe-reverse-engineering.md#5)。

## 8. 附錄

- 工作目錄:`<MAPLESOTRY>\wf-output\`
- 原始資料快取:`_pe.json`、`_imports.json`、`_results.json`、`_all.json`(本次比對的中間結果)
- CSV 對照:5,658 列,格式 `ID;string`(ID 是 localization table 索引,內容是英文原文 — 
  本次比對無對應繁中 CSV,推測繁中字串由另一個檔案提供並注入 runtime)
