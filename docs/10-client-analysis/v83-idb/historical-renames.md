# 已知歷史 Renames (來自 diamondo25 IDC + angel ToolTip)

> **來源 1**: [diamondo25 IDC script](https://gist.github.com/diamondo25/be95345a2875ab4342cd) (2015)
> **來源 2**: [angel RaGEZONE thread 1193418](https://forum.ragezone.com/threads/v83-idb-client-edit-dump.1193418/) (2020)
> **資料檔**: `wf-output/ida-v83-direct/historical_renames.json`

## §1 diamondo25 IDC script — String → Function Rename 對照

總共 24 條 renames,**16 條 string 在 v83.idb 內找到**(對應的 function 應為呼叫該 string 的函數)

| IDB Addr | String | Function |
|---|---|---|
| `0xaf13d8` | `SeDebugPrivilege` | `GetSEPrivilege` |
| `0xaf2104` | `Please visit the website to charge your account.` | `CCashShop::OnStatusCharge` |
| `0xaf21e8` | `GM can not transfer worlds.` | `CCashShop::CheckTransferWorldPossible` |
| `0xaf32ac` | `Delivered` | `?Decode@CharacterData@@QAE_KAAVCInPacket@@H@Z` |
| `0xaf4dd8` | `UI/UIWindow2.img/Reset/AP/stat%d/%d` | `GetStatCanvas` |
| `0xaf5598` | `jobCategory` | `Field::JobCategoryCond::Parse` |
| `0xaf55a4` | `battleFieldTeam` | `Field::BattlefieldTeamCond::Parse` |
| `0xaf63d0` | `epicItem` | `CItemInfo::RegisterEquipItemInfo` |
| `0xaf6cf0` | `%02X%02X%02X%02X%02X%02X_%02X%02X%02X%02X` | `CItemInfo::RegisterEquipItemInfo` |
| `0xafd330` | `SOFTWARE\\\\Microsoft\\\\Windows\\\\CurrentVersion` | `?Init@CSystemInfo@@QAEXXZ` |
| `0xafe5c4` | `Play!` | `StartUpWndProc` |
| `0xb0012c` | `DBGHELP.DLL` | `ZExceptionHandler::InitDbgHelpFunctions` |
| `0xb38fec` | `%d/%02d/%02d %02d:%02d` | `CUIGuildBBS::FormatDate` |
| `0xb3bc54` | `itemLEV` | `CUIToolTip::CUIToolTip` |
| `0xb3d8e8` | `Unknown error 0x%0lX` | `com_error::ErrorMessage` |
| `0xb3f400` | `http://maplestory.nexon.net` | `CClientSocket::GetGuestIDRegistrationURL` |

## §2 angel ToolTip Addresses(直接給出位址,不需要 xref)

共 13 個 CUIToolTip 子方法

| Address | Function |
|---|---|
| `0x008E6F35` | `CUIToolTip::SetToolTip_String` |
| `0x008E70C5` | `CUIToolTip::SetToolTip_MultiLine` |
| `0x008E7317` | `CUIToolTip::SetToolTip_String2` |
| `0x008E7716` | `CUIToolTip::SetToolTip_WorldMap` |
| `0x008E7E49` | `CUIToolTip::SetToolTip_Ring` |
| `0x008E97D2` | `CUIToolTip::SetToolTip_Equip` |
| `0x008EDBCF` | `CUIToolTip::SetToolTip_Pet` |
| `0x008EEEF1` | `CUIToolTip::SetToolTip_Bundle` |
| `0x008F0460` | `CUIToolTip::SetToolTip_Package` |
| `0x008F1D6B` | `CUIToolTip::SetToolTip_SlotInc` |
| `0x008F214B` | `CUIToolTip::SetToolTip_EquipExt` |
| `0x008F22BB` | `CUIToolTip::SetToolTip_MacroSys` |
| `0x008F2876` | `CUIToolTip::SetToolTip_Skill` |

## §3 如何套用到 v83.idb

### 方法 A:在 IDA Pro GUI 內套用 IDC script

```
File → Script file → 選擇 diamondo25 的 .idc → Run
```

注意:Angel 的 ToolTip addresses 是基於 32-bit v83 client 偏移,在 IDA 9.x 的 64-bit IDB 中可能需要 base address 重新計算
