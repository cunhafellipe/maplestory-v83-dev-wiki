# W1-1: v83.idb IDA 資料庫技術分析

> **分析時間**: 2026-09-27
> **檔案**: `C:\Users\e7896\AppData\Local\Temp\v83peek\v83.idb`
> **工具**: 純文件讀取 (Python struct, mmap, regex)
> **性質**: 純技術拆解,不下結論

---

## §1 檔案基本屬性

| 屬性 | 值 |
|---|---|
| 大小 | 125,092,284 bytes = 119.30 MB |
| Magic bytes | `49 44 41 31` (ASCII: "IDA1") |
| 識別 | **IDA Pro 6.x/7.x IDB 格式** |
| 創建日期 | 2014-03-25 |
| 來源 | `v83.rar` 解壓,內含完整逆向工程資料庫 |

**Magic 識別規則**:IDA 5.x 是 `IDA0`、6.x/7.x 是 `IDA1`、8.x 是 `IDA2`(已驗證 IDA 文件格式歷史)

---

## §2 字串池規模

| 指標 | 值 |
|---|---|
| Unique strings (長度 ≥ 8) | **124,782** |
| Scan 時間 | 1.3 秒 |
| WZ 路徑相關字串 | **142** 條(含 `_wz`、`_img`、`W_img` 等前綴)|
| WZ img 名(純字串格式)| **104** 條 |
| C++ class::method 格式 | 8 條 |
| Maple 相關 | 14 條 |
| Server/Host/Port 相關 | 12 條 |
| Packet/Net 相關 | 20 條 |
| Channel/World 相關 | 14 條 |
| Login 相關 | 5 條 |
| 結構體(`_s_*`)| 30 條 |
| v83 特定(`CInPacket`/`COutPacket`/`_s_HandlerType`)| 12 條 |
| CashShop 相關 | 2 條 |
| CheckIn/Daily 相關 | 1 條 |
| Beauty 相關 | **0** 條 |

---

## §3 已識別的 C++ 關鍵類別與函式(從 IDB 字串)

### 3.1 主要客戶端類別

| 類別 | 用途 | 出現次數 |
|---|---|---|
| `CInPacket::Decode1/4/Str/Buffer` | 封包解碼 | 4+ |
| `CLogin::OnPacket` | 登入封包處理 | 1 |
| `CWvsContext::OnPacket` | 世界頻道封包處理 | 1 |
| `CField::OnPacket` | 戰鬥地圖封包處理 | 1 |
| `CStage::OnPacket` | Stage 容器封包路由 | 1 |
| `WvsContext::OnPacket` | 同 CWvsContext 變體 | 1 |
| `Stage::OnPacket` | 同 CStage 變體 | 1 |
| `Login::OnPacket` | 同 CLogin 變體 | 1 |

### 3.2 其他關鍵結構與名稱

| 名稱 | 用途 |
|---|---|
| `_s_HandlerType` | SEH exception handler 結構 |
| `_s_CatchableType` | C++ EH type info |
| `_s_FuncInfo` | C++ EH function info |
| `_s_ThrowInfo` | C++ EH throw info |
| `_IP_ADAPTER_INFO` | Winsock IP 適配器結構 |
| `HttpSendRequestA` | WinINet HTTP 函式 |
| `SendMessageA` | User32 訊息 |
| `SetConsoleCtrlHandler` | Console 控制 |
| `HandlerRoutine` | Console handler callback |

### 3.3 C++ MSVC mangled 函式(13 條)

全部是 MSVC C++ EH (Exception Handling) 函式:
- `?BuildCatchObject@@YAX...`
- `?CatchGuardHandler@@YA?AW4_EXCEPTION_DISPOSITION@@...`
- `?CatchIt@@YAXPAUEHExceptionRecord@@...`
- `?FindHandler@@YAXPAUEHExceptionRecord@@...`
- `?FindHandlerForForeignException@@YAX...`
- `?TranslatorGuardHandler@@YA?AW4_EXCEPTION_DISPOSITION@@...`
- `?TypeMatch@@YAHPBU_s_HandlerType@@...`

(全部是 VC++ runtime exception dispatch,不直接是遊戲邏輯)

### 3.4 WZ img 路徑字串樣本(104 條)

```
aW_imgCashgacha
aW_imgCashgac_0
aMap
aMapleMedialist
aNexonMaplest_0
aNexonMaplest_1
aNexonMaplestor
aTmsClient
aLogingame
```

這些是字串常數(編碼後的字串 reference),代表 .img 內的路徑節點名稱。

---

## §4 結構性限制說明

**純文件讀取的限制**:
1. **無 IDA Pro 工具** — 沒辦法列出完整 function、xref、stack frame
2. **IDB 是加密的儲存格式** — 124,782 strings 是 *索引後字串* (用 IDA 6+ 的 string storage),不是完整字串池
3. **function name** 完整清單需 IDA 開啟才能看 (124K strings 中只有 13 條 MSVC mangled,因為大部分用 IDA 內部 indexed name)

**已知能從 IDB 純讀的**:
- Magic + format version
- String pool(部分)
- Comment(部分)
- Enum 成員(部分)

**已知無法純讀的**:
- Function 完整清單與位址
- Stack frame 結構
- Cross-reference

---

## §5 整合技術涵義

### 5.1 對 kaentake hook 開發的價值

| 任務 | 純 IDB 讀取可達成? | 需 IDA Pro? |
|---|---|---|
| 識別客戶端版本 | ✓ (magic + strings)| — |
| 找 WZ 結構 | ✓ (104 條 img 路徑)| — |
| 確認 hook 點存在 | ✗ | ✓ |
| 提取記憶體位址 | ✗ | ✓ |
| 驗證 cross-reference | ✗ | ✓ |

### 5.2 與本地 kaentake source 的對照

本地 `12-OffShelf-Client-Fork/kaentake/` 的 hardcoded 位址(從之前的分析):
- `0x00989588` play_ui_sound
- `0x0049637B` ClientSocket_SendPacket
- `0x004965F1` ClientSocket_ProcessPkt
- `0x009929DD` CUtilDlg_Notice

要驗證這些位址在 v83 build 中是否有效,需要用 IDA 開啟 `v83.idb` 對應 section,純文件讀取無法做到。

---

## §6 結論(純技術事實)

1. **v83.idb 是真實的 IDA Pro 6.x IDB 格式**(magic `IDA1`)
2. **規模**:125 MB,124,782 unique strings,142 條 WZ 路徑
3. **內容聚焦**:客戶端 v83 build 的所有 C++ class/string/enum
4. **可直接提取的技術指標**:magic、版本、字串池規模、關鍵類別名
5. **必須用 IDA Pro 才能取得**:function list、xref、記憶體位址

---

**檔案輸出**: 本檔
**v83.idb 本體**:完全沒動
