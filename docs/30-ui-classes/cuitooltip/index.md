# CUIToolTip — 滑鼠 Hover Tooltip 系統

> **來源**:angel RaGEZONE thread 1193418(直接給出 13 個地址)+ diamondo25 IDC
>
> **作用**:玩家滑鼠移到裝備/技能/NPC 上面會出現的 tooltip 視窗
>
> **二次開發**:改 ToolTip 文字、顏色、新增 field 都需要改這 13 個方法之一

## 13 個 CUIToolTip 子方法(地址 + 用途)

| Address | Function | 對應的物件 |
|---|---|---|
| `0x008E6F35` | `CUIToolTip::SetToolTip_String` | 一般字串(公告、訊息)|
| `0x008E70C5` | `CUIToolTip::SetToolTip_MultiLine` | 多行字串 |
| `0x008E7317` | `CUIToolTip::SetToolTip_String2` | 一般字串 (variant 2) |
| `0x008E7716` | `CUIToolTip::SetToolTip_WorldMap` | 世界地圖 |
| `0x008E7E49` | `CUIToolTip::SetToolTip_Ring` | 戒指裝備 |
| `0x008E97D2` | `CUIToolTip::SetToolTip_Equip` | **裝備**(最常用)|
| `0x008EDBCF` | `CUIToolTip::SetToolTip_Pet` | 寵物 |
| `0x008EEEF1` | `CUIToolTip::SetToolTip_Bundle` | 捆綁包 |
| `0x008F0460` | `CUIToolTip::SetToolTip_Package` | 包裹 |
| `0x008F1D6B` | `CUIToolTip::SetToolTip_SlotInc` | 插槽強化 |
| `0x008F214B` | `CUIToolTip::SetToolTip_EquipExt` | 裝備擴展(進階資訊)|
| `0x008F22BB` | `CUIToolTip::SetToolTip_MacroSys` | 巨集系統 |
| `0x008F2876` | `CUIToolTip::SetToolTip_Skill` | 技能 |

## angel 釋出的 ToolTip 改色範例

```asm
;改 ToolTip 顏色為藍黑色 (BB000000)
;Data 部分:int toolTipColors = 0xBB000000;

WriteInt(0x008E6F35 + 1, toolTipColors);   ;CUIToolTip::SetToolTip_String
WriteInt(0x008E70C5 + 1, toolTipColors);   ;CUIToolTip::SetToolTip_MultiLine
WriteInt(0x008E7317 + 1, toolTipColors);   ;CUIToolTip::SetToolTip_String2
WriteInt(0x008E7716 + 1, toolTipColors);   ;CUIToolTip::SetToolTip_WorldMap
WriteInt(0x008E7E49 + 1, toolTipColors);   ;CUIToolTip::SetToolTip_Ring
WriteInt(0x008E97D2 + 1, toolTipColors);   ;CUIToolTip::SetToolTip_Equip
WriteInt(0x008EDBCF + 1, toolTipColors);   ;CUIToolTip::SetToolTip_Pet
WriteInt(0x008EEEF1 + 1, toolTipColors);   ;CUIToolTip::SetToolTip_Bundle
WriteInt(0x008F0460 + 1, toolTipColors);   ;CUIToolTip::SetToolTip_Package
WriteInt(0x008F1D6B + 1, toolTipColors);   ;CUIToolTip::SetToolTip_SlotInc
WriteInt(0x008F214B + 1, toolTipColors);   ;CUIToolTip::SetToolTip_EquipExt
WriteInt(0x008F22BB + 1, toolTipColors);   ;CUIToolTip::SetToolTip_MacroSys
WriteInt(0x008F2876 + 1, toolTipColors);   ;CUIToolTip::SetToolTip_Skill
```

## CUIToolTip 在 v83.idb 的對應

| Function | Address in v83.idb | Source |
|---|---|---|
| `CUIToolTip::CUIToolTip` (constructor) | `0xb3bc54` (xref to `itemLEV`) | diamondo25 IDC |
| `CUIToolTip::SetToolTip_Equip` | (待 decompile) | `%d (MAX)` string |
| 其他 12 個 SetToolTip_* | `0x008E6F35 ~ 0x008F2876` | angel ToolTip addresses |

## 相關 WZ 路徑

```
UI/UIWindow.img/ToolTip/Equip/GrowthDisabled
UI/UIWindow.img/ToolTip/Equip/GrowthEnabled
```

## 二次開發情境

| 想改 | 改哪裡 |
|---|---|
| ToolTip 顏色 | 上面 13 個 `WriteInt(0x...+1, color)` |
| ToolTip 文字內容 | UI.wz `UI/UIWindow.img/ToolTip/*` 內的字串(由 CItemInfo::GetItemDesc 處理)|
| ToolTip 新增欄位 | `CUIToolTip::SetToolTip_Equip` 內的 pseudocode 邏輯 |
| ToolTip 顯示時機 | 滑鼠 hover handler(在 CUIItem / CUIEquip / CUISkill 內)|
