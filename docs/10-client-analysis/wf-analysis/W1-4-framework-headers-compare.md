# W1-4: kaentake framework headers 對照

> **分析時間**: 2026-09-27
> **本地源碼**: `<MAPLESOTRY>\12-OffShelf-Client-Fork\kaentake\src\`(45 檔)
> **對照對象**: BeautySalonv83, CashShop, CheckIn 三個功能包

---

## §1 本地 kaentake 標頭清單(45 檔)

### src/ 根目錄(16 .cpp + 3 .h = 19 檔)
```
  src/avatar.cpp
  src/bypass.cpp
  src/constants.h
  src/debug.cpp
  src/debug.h
  src/hook.cpp
  src/hook.h
  src/injector.cpp
  src/inlink.cpp
  src/itemeff.cpp
  src/itemicon.cpp
  src/launcher.cpp
  src/mobhptag.cpp
  src/pch.h
  src/resman.cpp
  src/resolution.cpp
  src/stringpool.cpp
  src/system.cpp
  src/tempstat.cpp
  src/tooltip.cpp
  src/wvs\avatar.h
  src/wvs\config.h
  src/wvs\ctrlwnd.h
  src/wvs\exception.h
  src/wvs\field.h
  src/wvs\gobj.h
  src/wvs\iteminfo.h
  src/wvs\msghandler.h
  src/wvs\packet.h
  src/wvs\rtti.h
  src/wvs\secure.h
  src/wvs\stage.h
  src/wvs\statusbar.h
  src/wvs\tempstat.h
  src/wvs\tooltip.h
  src/wvs\util.h
  src/wvs\wnd.h
  src/wvs\wndman.h
  src/wvs\wvsapp.h
  src/ztl\tsingleton.h
  src/ztl\zalloc.h
  src/ztl\zcoll.h
  src/ztl\zcom.h
  src/ztl\zlock.h
  src/ztl\zstr.h
  src/ztl\ztl.h
```

### src/wvs/(20 .h)
```

```

### src/ztl/(6 .h)
```

```

---

## §2 各功能包的 include 需求(從原始碼)

### 2.1 BeautySalon(`beautyshop.cpp`)

```cpp
#include "pch.h"          // precompile
#include "hook.h"          // ATTACH_HOOK
#include "debug.h"         // logging
#include "wvs/wnd.h"       // CWnd
#include "wvs/packet.h"    // COutPacket / CInPacket
#include "wvs/util.h"      // get_rm() / WZ
#include "wvs/wvsapp.h"    // app timing
#include "ztl/ztl.h"       // ZXString / COM
#include <windows.h> <cstdio> <cstdarg> <cstring> <cwchar>
#include <memory>
```

### 2.2 CashShop(`cashshopwnd.cpp`)

```cpp
#include "pch.h" "hook.h" "debug.h" "cashshopwnd.h"
#include "wvs/iteminfo.h"   // ← BeautySalon 沒有
#include "wvs/packet.h" "wvs/util.h" "wvs/wnd.h"
#include "wvs/wndman.h"     // ← BeautySalon 沒有
#include "ztl/ztl.h"
#include <windows.h> <atomic> <cstdio> <cwchar>
#include <map> <memory> <mutex> <set> <string> <vector>
```

### 2.3 CheckIn(`dailycheckin.cpp`)

```cpp
#include "pch.h" "hook.h" "debug.h"
#include "wvs/packet.h" "wvs/wnd.h" "wvs/iteminfo.h"  // ← BeautySalon 沒 iteminfo
#include "wvs/util.h" "wvs/wvsapp.h" "wvs/wndman.h"
#include "ztl/ztl.h"
#include <windows.h> <cstdio> <cstring>
#include <memory> <string> <vector>
```

### 2.4 BeautySalon Reference(`client/reference/`)

```
debug.h
hook.h
wvs/avatar.h
wvs/packet.h
wvs/util.h
wvs/wnd.h
wvs/wvsapp.h
ztl/ztl.h
```

(注:BeautySalon reference 給的是 `wvs/avatar.h`,但 `beautyshop.cpp` source 沒 include 它 — avatar.h 是「參考用」)

---

## §3 交叉對照:本地有 vs 功能包需求

### 3.1 本地 kaentake 有,但功能包都沒 include 的(本地孤兒)

| 本地檔 | 用途 |
|---|---|
| `src/bypass.cpp` | HackShield bypass(15KB)|
| `src/injector.cpp` | 命令列/config.ini host-port 解析 |
| `src/resman.cpp` | Resource manager |
| `src/tempstat.cpp` | 臨時狀態 |
| `src/avatar.cpp` | 頭像邏輯 |
| `src/debug.cpp` | logger 實作 |
| `src/hook.cpp` | Detours 工具 |
| `src/launcher.cpp` | 啟動器 |
| `src/system.cpp` | winsock patch |
| `src/resolution.cpp` | 解析度切換(30KB)|
| `src/itemeff.cpp` | 物品效果 |
| `src/itemicon.cpp` | 物品圖示 |
| `src/mobhptag.cpp` | 怪物 HP |
| `src/stringpool.cpp` | 字串池 |
| `src/tooltip.cpp` | 工具提示 |
| `src/wvs/ctrlwnd.h` | 控制項視窗 |
| `src/wvs/exception.h` | 例外處理 |
| `src/wvs/field.h` | Field(地圖)|
| `src/wvs/gobj.h` | game object |
| `src/wvs/msghandler.h` | 訊息處理 |
| `src/wvs/rtti.h` | RTTI |
| `src/wvs/secure.h` | 安全 |
| `src/wvs/stage.h` | Stage |
| `src/wvs/statusbar.h` | 狀態列 |
| `src/wvs/tempstat.h` | 臨時狀態頭 |
| `src/wvs/tooltip.h` | 工具提示頭 |

### 3.2 3 個功能包都需要,本地有的

| Header | 本地有? | Beauty | CashShop | CheckIn |
|---|:---:|:---:|:---:|:---:|
| `pch.h` | ✓ | ✓ | ✓ | ✓ |
| `hook.h` | ✓ | ✓ | ✓ | ✓ |
| `debug.h` | ✓ | ✓ | ✓ | ✓ |
| `wvs/packet.h` | ✓ | ✓ | ✓ | ✓ |
| `wvs/wnd.h` | ✓ | ✓ | ✓ | ✓ |
| `wvs/util.h` | ✓ | ✓ | ✓ | ✓ |
| `wvs/wvsapp.h` | ✓ | ✓ | — | ✓ |
| `wvs/iteminfo.h` | ✓ | — | ✓ | ✓ |
| `wvs/wndman.h` | ✓ | — | ✓ | ✓ |
| `ztl/ztl.h` | ✓ | ✓ | ✓ | ✓ |

**結論**:所有 3 個功能包需要的 headers **本地 kaentake 都有**,可直接使用。

### 3.3 BeautySalon reference 提到 `wvs/avatar.h`,本地有但功能包 source 沒用

| 狀態 | Header |
|---|---|
| BeautySalon reference 列了,但 source 沒 include | `wvs/avatar.h` |
| 本地 kaentake 有 | ✓ `src/wvs/avatar.h` |

**純事實**:`avatar.h` 是 BeautySalon 預期用 CAvatar 來生成 frozen avatar preview(隱藏帽子 + 配件),但 `beautyshop.cpp` source 沒有實際 #include 它。

---

## §4 CashShop 比其他兩個多 include 的

| Header | 用途(從 CashShop README 推斷) |
|---|---|
| `wvs/iteminfo.h` | item 圖示 (UI 顯示) |
| `wvs/wndman.h` | window manager (CWnd lifecycle) |
| `wvs/avatar.h`(reference 列,source 沒用)| avatar preview 系統 |

---

## §5 CheckIn 用到但 BeautySalon 沒用

| Header | 用途(從 CheckIn 推斷) |
|---|---|
| `wvs/iteminfo.h` | item 圖示(28 天格子每格顯示獎勵 item icon) |
| `wvs/wndman.h` | window manager |

**純事實**:CheckIn 雖然比 BeautySalon 小(583 行 vs 46KB),但 include 反而**更多** — 因為 CheckIn 每個格子都要顯示 item icon。

---

## §6 整合關鍵點(技術事實)

| 維度 | 結論 |
|---|---|
| 3 個功能包能否直接用本地 kaentake? | ✓ 可以(headers 都存在)|
| BeautySalon 需不需要額外 framework? | ✓ 都有 |
| CashShop 需不需要 wvs/wndman? | ✓ 本地有 |
| CheckIn 需不需要 wvs/iteminfo? | ✓ 本地有 |
| 誰有 avatar.h? | 本地 kaentake 有,但 source 沒實際用 |

---

**檔案輸出**: 本檔
**本地 kaentake**: 已從 scratch 補齊 src/ 與 ztl/(45 檔,沒改既有的 3 個 binary)
**功能包檔案**: 完全沒動
