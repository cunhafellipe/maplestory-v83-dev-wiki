# MapleStory 0.83.exe 逆向方法評估

> **來源**: 全部主張可用 `python verify_wiki_claims.py` 重跑驗證
> **目標**: 修正上一版把保護層誤判為 Themida 的結論

---

## §0 重要更正:保護層不是 Themida

上一版本文件宣稱本檔案由 **Themida 3.x** 保護。**這個結論是錯的**,而且證據就在本 wiki 自己的字串表裡。

> 本文件在下方仍會引用 "Themida" 這個詞,但僅用於說明「上一版錯在哪」與「為何 MapleDumper 等工具不適用」,
> **不是**對本檔案保護層的認定。本檔案的保護層是 **Nexon CSecurity**。

### 簽章掃描結果

對 `MapleStory 0.83.exe` 原始 bytes 做簽章掃描:

| 簽章 | 命中次數 |
|---|---|
| `.themida` / `.winlice` / `Themida` / `WinLicense` | **0** |
| `.vmp0`–`.vmp3`(VMProtect) | **0** |
| `.aspack` / `ASProtect` | **0** |
| `.enigma`(Enigma) | **0** |
| `UPX0` / `UPX1` / `UPX!` | **0** |

### 真正的識別依據:RTTI

解包後的 client(`msv83_trad.exe`)字串池中,每個 RTTI 類別名各出現 1 次:

```
.?AVZException@@               Nexon 內部基礎例外
.?AVCMSException@@             Client Message System(客戶端通訊層)
.?AVCTerminateException@@      伺服器指令斷線
.?AVCPatchException@@          補丁管線失敗
.?AVCSecurityException@@       ← 保護層基底
.?AVCSecurityInitFailed@@      ← 保護層初始化失敗
.?AVCSecurityUpdateFailed@@    ← 保護層更新失敗
.?AVCSecurityThreatDetected@@  ← 偵測到威脅
.?AVCSecurityClearFailed@@     ← 保護層清除失敗
```

這是 **Nexon / Wizet 自家的 CSecurity 模組**,不是任何商業加殼器。

> 上一版文件在 §2.2 引用的 "Evidence: Themida/WinLicense 3.x is not supported" 是一個**工具 README 的限制說明**,被誤讀成對本檔案的識別結果。該句描述的是 MapleDumper 這支工具能處理什麼,與目標檔案是什麼無關。

---

## §1 保護層的實際行為(實測)

| 項目 | 值 | 驗證方式 |
|---|---|---|
| 格式 | PE32, i386, Windows GUI | pefile |
| ImageBase | `0x400000` | PE header |
| EntryPoint RVA | `0x00A8C000` | PE header |
| EntryPoint 所在 section | `tfqhbstk`(僅 4 KB) | section table |
| TimeDateStamp | `0x4B879403` = **2010-02-26 09:27:31 UTC** | PE header |
| Section 數 | 7 | PE header |
| Section 名 | `(空)` / `.rsrc` / `.idata` / `(空)` / `uilplxhk` / `tfqhbstk` / `gndhordv` | section table |
| 首要 section entropy | **7.98** | pefile |
| Import | **1 個** — `kernel32.dll!FileTimeToLocalFileTime` | import table |
| Export | 3 個 — `ZtlTaskMemAllocImp` / `ZtlTaskMemFreeImp` / `ZtlTaskMemReallocImp` | export table |
| Version resource lang | `0x0412`(韓文 Johab) | resource tree |

### 上一版文件的欄位讀取錯誤

| 上一版寫法 | 實際值 | 問題 |
|---|---|---|
| `TimeDateStamp \| 7,270,400 (≈2018)` | `1,267,176,451` = 2010-02-26 | `7,270,400` 是 **SizeOfCode**,不是 timestamp |
| `1 個 import — 推測為 LoadLibraryA` | `FileTimeToLocalFileTime` | 函式名錯 |
| `.mackt` 是 WzPack**er** 標誌段名 | `b'.mackt\x00t'` = `.macktt` | 段名解析錯 + 工具名不存在 |

`7,270,400` 同時是原版與繁化版的 `SizeOfCode`,`W1-3-exe-diff.md` 的表格中它出現在 `SizeOfCode` 行 — 這是欄位歸屬錯誤的直接證據。

### 繁化版的來源:SolidDaima

繁化版(`msv83_trad.exe`)最後一個 section(4 KB,entropy 2.23)內含:

```
E:\ACGame_GL\BinTool\SolidDaima_Rev8_200901029\setting.ini
```

**SolidDaima** 是真實存在的 WZ 修改工具,`ACGame_GL\BinTool` 是其工作路徑。**沒有任何名為「WzPacker」的工具存在** — 那個名稱是誤植,出現在本 wiki 的 7 個檔案共 11 處。

---

## §2 已經產出的分析成果(已完成)

與其規劃「怎麼脫殼」,更有效的是:目錄中已經有兩份可用的分析產物。

### 2.1 Ghidra 全量分析(本專案已完成)

| 項目 | 數值 |
|---|---|
| 函式 | **52,083** |
| 符號 | **254,338** |
| 字串 | 1,663 |
| Import | **238**,分佈於 17 個 DLL |
| 已 decompile 的 C 函式 | 69 份 |

Import 分布:

| DLL | 數量 | 角色 |
|---|---|---|
| KERNEL32.DLL | 131 | Win32 核心 |
| USER32.DLL | 27 | 視窗 / 訊息迴圈 |
| WS2_32.DLL | 12 | **TCP/UDP socket — 遊戲連線** |
| MSS32.DLL | 12 | **Miles Sound System(`_AIL_*`)** |
| OLEAUT32.DLL | 11 | OLE automation |
| WININET.DLL | 9 | **HTTP — 補丁下載、廣告** |
| NMCOGAME.DLL | 8 | **Nexon 帳號 / 社交模組** |
| ADVAPI32.DLL | 8 | Registry、token privileges |
| GDI32.DLL | 7 | 2D 繪圖、`CreateDIBSection` |
| IJL15.DLL | 4 | **Intel JPEG Library — WZ canvas 解碼** |
| VERSION / WINMM / NETAPI32 / IPHLPAPI / DINPUT8 / OLE32 / SHELL32 | 各 1–3 | — |

> **上一版文件未提及 IJL15 與 MSS32。** IJL15 是 WZ 資源讀取鏈的關鍵:WZ canvas 以 JPEG 儲存,由 `ijlInit` / `ijlRead` / `ijlWrite` / `ijlFree` 在執行期解碼,這四個符號在解包版中以具名函式存在。

### 2.2 `v83.idb`(IDA 6 資料庫,2014-03-25)

| 項目 | 值 |
|---|---|
| 大小 | 125,092,284 bytes |
| 原檔名 | **`MapleAeon.exe`** |
| 原路徑 | `…\My Stuff\MapleStory IDBs\GMS\v83\MapleAeon.exe` |
| 函式總數 | 54,357 |
| Named 函式 | 204 |
| Strings ≥4B | 1,262 |

**`MapleAeon.exe` 是原持有者的重新命名** — 路徑中的 `GMS\v83\` 明確標示為 GMS v83。這不是韓版客戶端。

`v83.idb` 的價值不在命名量(它幾乎全是自動命名),而在它證明了映像 import `nmcogame.dll`,並保留了該模組完整的公開介面:

```
NMCO_SetLocale                  NMCO_SetLocaleAndRegion
NMCO_SetPatchOption             NMCO_SetUseFriendModuleOption
NMCO_SetUseNGMOption            NMCO_SetVersionFileUrlA
NMCO_CallNMFunc                 NMCO_MemoryFree
```

以及 4 個 OnPacket dispatcher:`CLogin::OnPacket` (`0x5F80FF`)、`CField::OnPacket` (`0x531325`)、`CWvsContext::OnPacket` (`0xA07A08`)、`CStage::OnPacket` (`0x644446`)。

### 2.3 `.i64` 與 `.asm` 的歸屬

`MapleStory 0.83.exe.i64`(16.9 MB)是 **對打包原檔** 的 IDA 資料庫 — 對被打包的檔案做分析,看到的自然是 loader stub,不是遊戲邏輯。

`MapleStory 0.83.exe.asm`(15.7 MB / 209,699 行)同樣是對打包原檔的反組譯,開頭是連續的 `dd` 密文。

**這兩者都不含遊戲邏輯。** 上一版 `project-map.md` 只寫「IDA 自動分析的 IDB (17 MB)」而未標明目標,容易誤導。

---

## §3 WZ 架構:為什麼 client 裡找不到 WZ 解析

### 3.1 WZ 層由 Pixi 框架驅動,不是 Windows COM

`FUN_00796022`(解包版)是唯一的綁定寫入點:

```c
int FUN_00796022(HMODULE h) {
    DAT_00bf0cc0 = GetProcAddress(h, "PcCreateObject");
    DAT_00bf0cc4 = GetProcAddress(h, "PcFreeUnusedLibraries");
    DAT_00bf0cc8 = GetProcAddress(h, "PcSerializeObject");
    DAT_00bf0ccc = GetProcAddress(h, "PcSerializeString");
    DAT_00bf0cd0 = GetProcAddress(h, "PcRootNameSpace");
    for (p = &DAT_00bf0cc0; p < &DAT_00bf0cd4; p++)
        if (*p == 0) return 0;
    return 1;
}
```

**Pixi** 是 Wizet 自家的物件框架。`CoCreateInstance` 在解包版中出現 **0 次**;`ole32.dll` 的實際用途是 `CoCreateGuid`。上一版 `W1-3-exe-diff.md` 稱 `ole32/oleaut32` 用於「UI ActiveX/COM 元件互操作」,與實測不符。

### 3.2 容器解析器不在 client image 內

| 探測 | 結果 |
|---|---|
| `PKG1` 作為 byte string | 0 次 |
| 公開 v83 AES key(`13 00 00 00 08 00 …`) | 0 次 |
| `Package file` 描述字串 | 0 次 |
| `Wizet` 字串 | 0 次 |

把公開 v83 key 套用在 `String.wz` 前 0x20 bytes 上,得到 `bf 00 14 04 fb 7b 70 f6 …` 無結構輸出;同一組 key 讓明文描述字串變成亂碼。**負結果不是 offset 對齊造成的假象。**

結論:WZ 容器讀取程式碼在執行期由 `PcCreateObject` 從外部模組綁定,**沒有編譯進這個 exe**。

### 3.3 Client 載入的 15 個 WZ 檔案

`FUN_009f7159` 迭代一個 **15 槽位**的表(loop bound `0xF`),並以 UTF-16LE 的 `"%s.wz"` 格式化檔名:

| 槽位 | 名稱 | 槽位 | 名稱 |
|---|---|---|---|
| `0x00B3F480` | `Character` | `0x00B3F454` | `Effect` |
| `0x00B3F47C` | `Mob` | `0x00B3F44C` | `String` |
| `0x00AF64DC` | `Skill` | `0x00B3F448` | `Etc` |
| `0x00B3F474` | `Reactor` | `0x00B3F440` | `Morph` |
| `0x00B3F470` | `Npc` | `0x00B3F434` | `TamingMob` |
| `0x00B3F46C` | `UI` | `0x00B3F42C` | `Sound` |
| `0x00B3F464` | `Quest` | `0x00B3F428` | `Map` |
| `0x00B3F45C` | `Item` | | |

完整清單(15 個):**Character, Mob, Skill, Reactor, Npc, UI, Quest, Item, Effect, String, Etc, Morph, TamingMob, Sound, Map**

> 上一版文件在三處給出不同數字(16 / 28 / 28),且無一處列出實際檔名。`28 個` 出自 `W3-2-...analysis.md`,那是 **韓版 JourneyClient** 的分檔結構,與 GMS v83 不同 — 該文件自己也註明「GMS v83 通常沒有 `Map001/002/2.wz`」。

目錄中實際存在 4 個:`UI.wz`、`String.wz`、`Quest.wz`、`Etc.wz`。**其餘 11 個缺失。**

### 3.4 WZ 與 IMG 是兩種不同容器

| | WZ 封存檔 | 散落的 `.img` |
|---|---|---|
| 位元組 0 | `PKG1`(`50 4B 47 31`) | `73 f8 6c 77`(無 header) |
| 描述字串 | `Package file v1.0 Copyright 2002 Wizet, ZMS` | 無 |
| offset `0x0C` | 60(header size) | — |
| 前 4 KB entropy | — | 7.84 |
| 範例 | `UI.wz` / `String.wz` / `Quest.wz` / `Etc.wz` | `Data/UI/Login.img` / `Data/Map/Obj/login.img` |

`W1-5-wz-img-index.md` 對 WZ 側的描述(header size 60、`Package file` 描述字串)是**正確的**,已保留。差異在 IMG 側:這些檔案沒有 `PKG1` header,開頭是固定的 `73 f8 6c 77`,是 WZ 節點 blob 被抽出的形式。目錄中的 `更正启动错误补丁 支持WZ，IMG端.rar` 存在的目的,就是讓 client 同時接受兩種佈局。

---

## §4 腳本層:最高價值的修改面

`scripts/` 內含 **2,294 個 JavaScript 檔**,編碼為 **GB18030**:

| 目錄 | 檔數 |
|---|---|
| `npc/` | 1,101 |
| `portal/` | 409 |
| `quest/` | 330 |
| `reactor/` | 269 |
| `event/` | 108 |
| `map/` | 72 |
| `item/` | 2 |

`event/0_EXAMPLE.js` 定義了完整的 instance event 契約:`setup` / `playerEntry` / `playerExit` / `monsterKilled` / `respawnStages` / `scheduledTimeout` / `clearPQ` / `dispose` 等。

**任務、NPC 對話、傳送門、反應堆、事件邏輯全部可以純文字修改,不必碰執行檔。** 這是本專案性價比最高的介入點。

> 數字修正:`W1-6-js-script-index.md` 已正確記錄 2,294(並說明口述的 2,297 包含 41 個非 `.js` 條目),但 `scan-original.md` 仍在使用 2,297 與 2,300。**以 2,294 為準。**

---

## §5 解析度修改鏈

三支 DLL 協同工作:

| DLL | 大小 | 建置日期 | 機制 |
|---|---|---|---|
| `nmconew2.dll` | 1,638,400 | 2009-07-26 | `NMCO_CallNMFunc` / `NMCO_MemoryFree`;攔截 `Direct3DCreate8`;ImageBase `0x10000000`;1.7 MB `.data` |
| `nmconew.dll` | 50,176 | 2020-11-06 | Microsoft Detours(`.detourc` / `.detourd`);`NMCO_CallNMFunc2` trampoline;攔截 `GetModuleFileNameW` 隱藏自身 |
| `dinputc.dll` | 21,504 | 2019-04-16 | 匯出替代的 `DirectInput8Create`;為非原生解析度縮放滑鼠 / 鍵盤輸入 |

**`nmconew2.dll` 是第一方 Nexon 元件,不是第三方 hack。** 其 PDB 路徑:

```
e:\Work\PlatformDev\_tag\NorthAmerica\20090721_df\
  Messenger\MessengerNew\ClientDLL\UnicodeRelease\nmconew.pdb
```

`PlatformDev` / `Messenger` / `NorthAmerica` / build tag `20090721_df` 是 Nexon 第一方建置樹。`Messenger` 正是 MapleStory client 的內部代號(與 `CNM*` 事件族、`nmcogame.dll` 呼應)。打包的原 client 只是把它的存在藏起來。

**`nmconew.dll` 才是第三方補丁**,PDB 路徑 `C:\Users\alexd\OneDrive\Desktop\resdll\Release\nmconew.pdb`。它讀 `Gms.083.ini`、驗證執行映像為 `MapleStory` / `client`、定位 `UI/Login.img/Common/frame`,然後載入 `nmconew2.dll` 並透過 `NMCO_CallNMFunc2` 驅動。

### 設定檔

```ini
[client]
resolutiontype= 0 ; (0)800:600, (1)1024:768, (2)1280:720,
                  ; (3)1440:900, (4)1680:1050, (5)1920x1080
```

### 登入介面限制

隨附的 `说明.txt` 要求:任何自訂 UI 必須提供 `UI/Login.img/Common/frame` 與 `frame0` … `frame5` 全部節點 — 解析度補丁引入了多幀登入畫面,client 會讀取每一個,缺任一個即結束程式。

---

## §6 若仍要做執行期脫殼

上一版文件規劃的「Themida 脫殼流程」不適用(見 §0)。若確實需要對**打包原檔**做執行期分析,實際步驟是:

1. 在隔離環境執行 `MapleStory 0.83.exe`,讓 CSecurity 完成解包
2. 從 process memory dump 已解密的映像
3. 將 dump 重新載入 Ghidra,重跑 auto-analysis
4. 以 dump 為基準比對靜態結果

**前置條件**:此步驟需要執行未知且刻意混淆、帶 anti-tamper 行為的程式碼,必須有獨立的隔離決策。

**但對本專案目標而言這是過度設計** — §2 已有 52,083 函式的完整分析,§4 的腳本層可直接文字修改,§5 的解析度鏈無需改 exe。

---

## §7 驗證

```bat
python verify_wiki_claims.py
```

每條主張都有對應的自動檢查,預期值為原始碼中的字面值。可修改任一預期值並觀察檢查轉紅,以確認該檢查確實有效。

---

## §8 參考連結

- [angel v83.idb](https://forum.ragezone.com/threads/v83-idb-client-edit-dump.1193418/) — 完整 IDB dump
- [diamondo25 IDC script](https://gist.github.com/diamondo25/be95345a2875ab4342cd) — 24 個 string rename
- [sunnyboy IDAQ.EXE 教學](https://forum.ragezone.com/threads/help-understanding-the-idaq-exe-file-and-how-to-find-methods-in-it.991744/) — STREDIT + xref
- [SpikeMogo/WAND_EXT](https://github.com/SpikeMogo/WAND_EXT) — 完整 v83 class offsets
- [BeiDou-ijl15](https://github.com/BeiDouMS/BeiDou-ijl15) — ijl15 插件源碼

> 上一版引用的 unlicense / MapleDumper-rs 連結已移除:它們是 Themida 導向的工具,與本檔案的實際保護層無關。MapleDumper 的 README 限制說明曾被誤讀為對本檔案的識別結果。
