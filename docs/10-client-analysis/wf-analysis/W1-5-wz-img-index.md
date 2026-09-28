# W1-5 WZ / IMG 索引報告

> 範圍:5 個工作區根目錄內的所有 `.wz` / `.img`
> 工具:Python 3.14 + GNU `strings` 2.45.1
> 不修改任何檔案。

---

## 1. 總量統計

| 指標 | 全部 | `.wz` | `.img` |
|---|---:|---:|---:|
| 檔案數 | 19 | 5 | 14 |
| 總位元組 | 11,110,528 B (~10.6 MB) | 453,739 B (~443 KB) | 10,656,789 B (~10.2 MB) |
| 平均大小 | 584,764 B | 90,748 B | 761,199 B |
| 中位數大小 | 82,652 B | 50,108 B | 76,322 B |
| 最大檔案 | 3,073,102 B | 288,946 B (`BeautySalonv83/UI.wz`) | 3,073,102 B (`原版商店 1280/CashShop.img`) |
| 最小檔案 | 1,176 B | 1,176 B (`BeautySalonv83/Item.wz`) | 1,724 B (`原版商店 1280/CashShopPreview.img`) |

`strings -n 4` 抽出的字串總數:71,490 行(WZ:4,416、IMG:67,074)。

---

## 2. WZ vs IMG 格式差異(對照)

| 維度 | `.wz` (PKG1 容器) | `.img` (解開後子檔) |
|---|---|---|
| Magic (offset 0) | `50 4B 47 31` = `PKG1`(固定明文) | 4-byte XOR/AES key(隨每個 WZ 不同,**非明文 magic**)|
| 檔頭長度 | 固定 60 bytes(`0x3C`) | 變動(key + type + 子節點數 + 屬性樹)|
| 內容加密 | 是 — 內容以 zlib + XOR/AES 加密 | 是 — 屬性名 / 字串仍 XOR-編碼 |
| 子節點數欄位 | offset `0x0C` 為 60(=header size);子節點數藏於加密區,無法純檔頭估計 | offset `0x08` 為子節點數(uint32,已驗 `0x17`/`0x0F`/`0x0C`/`0x01`/`0x05`)|
| 明文字串 | header 內有 `Package file v1.0 Copyright 2002 Wizet, ZMS` 可辨識版本 | 通常 0 條明文;全部 XOR 後的亂碼 |
| `strings` 結果 | 313 / 536 / 1000 / 2561(隨資料量) | 多為 0;少數樣本出現混淆亂碼 |
| 用途 | 客戶端實際派發容器 | `gmspeek` / WZ 解包後的單一子檔 |

> WZ 是**加密 + 壓縮**的容器;IMG 是把 WZ 內部的單一子節點資料 dump 出的離散檔,內容仍保留同把 XOR key 因此非明文。

---

## 3. 每個檔案明細

### 3.1 `.wz` 檔案 (5)

| # | 路徑 | 大小 | Magic | 版本/內容大小 (@0x04) | 子節點數 (檔頭估) | 字串數 |
|---:|---|---:|---|---|---:|---:|
| 1 | `C:\MUWORK\GAME\MAPLESOTRY\待分類\簽到表\wz\UI.wz` | 25,375 | PKG1 | 25,315 (0x62E3) | 60 (@0x0C,header size) | 313 |
| 2 | `C:\Users\e7896\AppData\Local\Temp\peek1\BeautySalonv83\Item.wz` | 1,176 | PKG1 | 1,116 (0x045C) | 60 (@0x0C,header size) | 6 |
| 3 | `C:\Users\e7896\AppData\Local\Temp\peek1\BeautySalonv83\Sound.wz` | 50,108 | PKG1 | 50,048 (0xC380) | 60 (@0x0C,header size) | 536 |
| 4 | `C:\Users\e7896\AppData\Local\Temp\peek1\BeautySalonv83\String.wz` | 88,134 | PKG1 | 88,074 (0x1580A) | 60 (@0x0C,header size) | 1,000 |
| 5 | `C:\Users\e7896\AppData\Local\Temp\peek1\BeautySalonv83\UI.wz` | 288,946 | PKG1 | 288,886 (0x46876) | 60 (@0x0C,header size) | 2,561 |

WZ header 前 16 bytes 樣本(`簽到表/wz/UI.wz`):
`50 4b 47 31 e3 62 00 00 00 00 00 00 3c 00 00 00`
→ `PKG1` + encrypted_size(0x62E3 = 25,315) + 4 zero bytes + 0x3C(60,header size)

### 3.2 `.img` 檔案 (14)

| # | 路徑 | 大小 | Magic | 子節點數 (@0x08) | 字串數 |
|---:|---|---:|---|---:|---:|
| 6 | `gmspeek\原版商店 1024\…\UI\CashShop.img` | 995,336 | `s\xf8lw` (`73 f8 6c 77`) | 23 (0x17) | 10,399 |
| 7 | `gmspeek\原版商店 1024\…\UI\CashShopPreview.img` | 2,043 | `s\xf8lw` | 15 (0x0F) | 0 |
| 8 | `gmspeek\原版商店 1280\…\UI\CashShop.img` | 3,073,102 | `s\xf8lw` | 23 (0x17) | 26,094 |
| 9 | `gmspeek\原版商店 1280\…\UI\CashShopPreview.img` | 1,724 | `s\xf8lw` | 15 (0x0F) | 0 |
| 10 | `gmspeek\多彩地图特效\…\Map\Tile\grassySoil.img` | 82,652 | `s\xf8lw` | 12 (0x0C) | 0 |
| 11 | `gmspeek\新版商店1280-720\…\UI\CashShop.img` | 3,035,980 | `s\xf8lw` | 23 (0x17) | 25,666 |
| 12 | `gmspeek\新版商店1280-720\…\UI\CashShopPreview.img` | 2,047 | `s\xf8lw` | 15 (0x0F) | 0 |
| 13 | `gmspeek\祝福混沌点卷掉落提示补丁\…\Item\Consume\0204.img` | 189,080 | `s\xf8lw` | 19,328 (0xF280) ⚠ | 0 |
| 14 | `gmspeek\祝福混沌点卷掉落提示补丁\…\Item\Consume\0234.img` | 3,407 | `s\xf8lw` | 1 (0x01) | 0 |
| 15 | `gmspeek\祝福混沌点卷掉落提示补丁\…\Item\Etc\0403.img` | 1,339,200 | `s\xf8lw` | 18,560 (0x4880) ⚠ | 0 |
| 16 | `peek_cash\cashshop-window\img\UI\CashShop.img` | 902,130 | (隨機 key) | 23 (0x17) | 9,617 |
| 17 | `peek_cash\cashshop-window\wz\UI\CashShop.img` | 902,130 | (隨機 key) | 23 (0x17) | 9,617 |
| 18 | `peek_crit\crit_and_range\wz\String\ToolTipHelp.img` | 59,965 | (隨機 key) | 5 (0x05) | 144 |
| 19 | `peek_crit\crit_and_range\wz\UIWindow.img` | 67,993 | (隨機 key) | 1 (0x01) | 642 |

> ⚠ 編號 13、15 的「子節點數」是 uint32 解讀後的常數,但 19,328 / 18,560 遠大於其他 IMG;很可能是 Item 屬性樹的 entry 數(Item 屬性是平的 key-value 結構而非子節點);`#14` 與 `#19` 都是 `0x01`,表示該 IMG 內只裝一個 root property。

#### 3.2.1 重複檔案

`peek_cash/img/UI/CashShop.img` 與 `peek_cash/wz/UI/CashShop.img`
兩者**大小相同 (902,130 B) 且字串數相同 (9,617)**,
推論為同一份 fixture 在兩個目錄下被複製,byte-for-byte 應相同。

#### 3.2.2 加密 key 觀察

gmspeek 內 10 個 IMG 全部以 `73 f8 6c 77` 起頭(共一把 XOR key),
代表 `gmspeek` 解包器把同一個來源 WZ 的所有子節點寫入時重用同一把 session key。
peek_cash 與 peek_crit 的 IMG magic 不同(每個 WZ 一把獨立 key)。

---

## 4. 來源檔案路徑對照

| 來源根目錄 | 找到的 .wz | 找到的 .img |
|---|---:|---:|
| `C:\Users\e7896\AppData\Local\Temp\gmspeek\` | 0 | 10 |
| `C:\Users\e7896\AppData\Local\Temp\peek1\BeautySalonv83\` | 4 | 0 |
| `C:\Users\e7896\AppData\Local\Temp\peek_cash\cashshop-window\` | 0 | 2 |
| `C:\MUWORK\GAME\MAPLESOTRY\待分類\簽到表\wz\` | 1 | 0 |
| `C:\Users\e7896\AppData\Local\Temp\peek_crit\crit_and_range\wz\` | 0 | 2 |
| **合計** | **5** | **14** |

---

## 5. 附錄:工具與限制

- **Magic 偵測**:`head[:4]` 直接讀位元組。
- **WZ 版本**:offset 0x04 實際是「加密後內容大小」,版本號藏於 zlib 解開後的 `version` 屬性,本索引未做 zlib 解壓。
- **WZ 子節點數**:header 只有 60 bytes 結構描述,真正的 property tree count 在 zlib 解開後才可讀,因此本表 WZ 全列為「60 (header size)」,僅供格式識別用。
- **IMG 子節點數**:取 offset 0x08 的 uint32,以 0 < n < 1,000,000 為啟發式過濾。
- **字串計數**:`strings -n 4`;IMG 因 XOR 編碼通常得 0,僅少數樣本抓到亂碼 token。
- **raw JSON**:`W1-5-wz-img-index.raw.json`(同目錄)含完整每檔 `first16_hex` / 子節點候選 / 字串樣本。
- **零修改**:未對任何輸入檔做寫入,僅讀取 + `strings` 讀取。