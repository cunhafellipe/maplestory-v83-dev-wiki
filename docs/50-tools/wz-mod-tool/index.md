# WZ Mod Tool — C# WZ 工具

> **狀態**:已 clone(02-Tools/WZ-Mod-Tool-Suite/)
> **用途**:C# WZ 檔編輯工具
> **搭配**:SoloMapling-wisteria-Wz-Mod-Tool-Suite

## WZ 檔是什麼

MapleStory v83 client 的資料檔,用 .wz 加密壓縮儲存:
Client 在執行期載入 **15 個** WZ 封存檔(由 `FUN_009f7159` 的 15 槽位表確認):

| WZ | 內容 | WZ | 內容 |
|---|---|---|---|
| `Character.wz` | 角色動作 | `UI.wz` | UI 視窗、圖片 |
| `Mob.wz` | 怪物 | `Quest.wz` | 任務 |
| `Skill.wz` | 技能 | `Item.wz` | 道具 |
| `Reactor.wz` | 反應爐 | `Effect.wz` | 特效 |
| `Npc.wz` | NPC | `String.wz` | 字串 |
| `Map.wz` | 地圖、背景 | `Etc.wz` | 雜項 |
| `Morph.wz` | 變身 | `TamingMob.wz` | 馴養怪 |
| `Sound.wz` | 音效 | | |

> **更正**:上一版此處列出 `List.wz`「物品清單」— 該檔案**不在** client 載入的 15 個 WZ 之中,
> 也未出現在本專案的資產目錄。同時上一版僅列 11 個,遺漏 `Quest` / `Effect` / `Morph` /
> `TamingMob` / `Sound` 五個。

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
