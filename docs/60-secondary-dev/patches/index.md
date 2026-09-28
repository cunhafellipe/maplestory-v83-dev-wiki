# Client Patches — 常見範例

> **目的**:把已知可改 client 的 patch 列出,給二次開發者參考

## 已驗證可改的 Patches (angel RaGEZONE 釋出)

### 1. ToolTip 顏色統一

```asm
;改所有 CUIToolTip 顏色為藍黑色 (BB000000)
int toolTipColors = 0xBB000000;

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

### 2. Bypass /pet 等級 15 限制

```asm
PatchNop(0x007050D3, 2);    ;Bypass lv15 for /pet <text> command
```

### 3. 鍵盤設定

```asm
WriteByte(0x008339A1 + 2, 0x2C);   ;Keyboard
WriteInt(0x004B7379 + 3, 0);       ;Cash Shop
```

## 推測可做的 Patches (需要 decompile 驗證)

### A. 改 Inventory 大小上限

HeavenMS server 端 `slotLimit` 寫死 96,但 client 端可能有對應顯示邏輯
- 找 CUIItem::OnCreate / CUIItem::Draw
- 改 slot 渲染上限
- 注意:server 不會送超過 96 的 slot 給 client

### B. 解析度修正

angel 提到幾個區域需要修:

```
- Shortcut Menu (CUIStatusBar::ToggleQuickslot / CUIStatusBar::OnCreate)
- Medal message / map effects (CField::ShowScreenEffect)
- HP/MP/EXP bars (CUIStatusBar::OnCreate + sub_8D850B)
```

對應本 IDB 位置:
- `CUIStatusBar::ChatLogDraw` 已知 → IDC 對照
- 其他需 decompile CUIStatusBar 相關函數

### C. 大螢幕 / 寬螢幕修正

`bSysOpt_LargeScreen` + `bSysOpt_WindowedMode`(在 CConfig)
- Patch 這兩個 flag 讓 client 認為是大螢幕

### D. 移除 HP/MP/EXP bar 的灰色效果

```asm
;gray stuff on the hp/mp/exp bars 都在 CUIStatusBar::OnCreate + sub_8D850B
```

## 還沒驗證的 Patches

下面這些需要 decompile 才能確認:

| 想改 | 需要 |
|---|---|
| 加裝備欄位 | WZ 改 + server 改 + client 改 三邊同步 |
| 改 ToolTip 文字 | UI.wz + CItemInfo::GetItemDesc |
| 改視窗大小 | CUIWnd::OnCreate 內 width/height |
| 加新 OPCode | CField::OnPacket 內加 case + server 配合 |

## 工具鏈

| 工具 | 用途 |
|---|---|
| OllyDbg 1.10 | 即時 debugger + patch |
| IDA Pro 9.3 | 反組譯 + patch |
| kaentake | DLL hook(不需 patch EXE)|
| HaRepacker | WZ 檔編輯 |
| WZ Mod Tool Suite | C# WZ 工具 |

## 注意事項

- angel 的 patch addresses (`0x008E...`, `0x008F...`) 是基於某個特定 v83 client 版本
- 我們的 `MapleStory 0.83.exe` 是 WzPacker 加殼,**地址會不同**
- 必須先用 IDA decompile 找出對應函數,再 patch
- patch 前先備份原檔
