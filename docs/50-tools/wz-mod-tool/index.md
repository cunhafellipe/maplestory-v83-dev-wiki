# WZ Mod Tool — C# WZ 工具

> **狀態**:已 clone(02-Tools/WZ-Mod-Tool-Suite/)
> **用途**:C# WZ 檔編輯工具
> **搭配**:SoloMapling-wisteria-Wz-Mod-Tool-Suite

## WZ 檔是什麼

MapleStory v83 client 的資料檔,用 .wz 加密壓縮儲存:
- `UI.wz` - UI 視窗、圖片
- `Map.wz` - 地圖、背景
- `Character.wz` - 角色動作
- `Mob.wz` - 怪物
- `Item.wz` / `Etc.wz` - 道具
- `String.wz` - 字串
- `List.wz` - 物品清單
- `Skill.wz` - 技能
- `Npc.wz` - NPC
- `Reactor.wz` - 反應爐

## 工作流程

```
原始 WZ 檔
  ↓ (用 HaRepacker 解密)
加密 IMG 節點
  ↓ (用 WZ Mod Tool 編輯)
修改後 IMG 節點
  ↓ (用 HaRepacker 加密)
修改後 WZ 檔
  ↓ (放回 client 目錄)
Client 載入新資料
```

## WZ Mod Tool 功能

- 批次修改 IMG 節點
- 字串替換
- 圖片匯出/匯入
- WZ 結構查詢

## 對應的 v83.idb UI strings

從 v83.idb 看到的 WZ 路徑:

```
UI/UIWindow.img/PartyRace/Stage/backgrd
UI/UIWindow.img/DualMobGauge/Mob/9700036
UI/ITC.img/Auction/backgrnd
UI/Login.img/ViewAllChar/Job/0
UI/StatusBar.img/base/chatTarget
UI/UIWindow.img/ToolTip/Equip/GrowthDisabled
UI/UIWindow.img/ToolTip/Equip/GrowthEnabled
```

這些都是 EXE 用 `sub_xxxxx` 載入,實際內容在 WZ 檔內。

## 安裝 / 編譯

```bash
cd C:\MUWORK\GAME\MAPLESOTRY\02-Tools\WZ-Mod-Tool-Suite
# 用 Visual Studio 編譯
msbuild WZModTool.sln
```

## 二次開發情境

| 想做 | 用 WZ Mod Tool |
|---|---|
| 改 UI 圖片 | ✓ |
| 加新 NPC 對話 | ✓ |
| 改道具名稱 | ✓ |
| 加新視窗 | ✗(需要 client patch)|
| 改 packet 行為 | ✗(需要 client patch)|

## 參考資料

- [SoloMapling-wisteria repo](https://github.com/MadaraGameDev/SoloMapling-wisteria-Wz-Mod-Tool-Suite)
- [HaRepacker 4.2.4](https://github.com/lastbattle/Harepacker)
- [MapleEzorsia V2 guide](https://github.com/phantomeis/MapleEzorsia-v2/wiki/v83%E2%80%90Client%E2%80%90Setup%E2%80%90and%E2%80%90Development%E2%80%90Guide)
