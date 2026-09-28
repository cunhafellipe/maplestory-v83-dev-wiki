# 30-ui-classes — MapleStory UI Class 結構

> **目的**:把 v83 client 的 UI class hierarchy 整理出來,給二次開發者改 UI 用
>
> **資料來源**:v83.idb 分析 + diamondo25 IDC + angel ToolTip addresses + RaGEZONE 教學

## MapleStory UI 架構

```
MapleStory v83 Client UI 系統
├── WZ 檔案 (UI.wz, Map.wz, etc.)    ← 視覺佈局
│   ├── UI/UIWindow.img/*           ← 主要視窗 (Item, Equip, Skill, etc.)
│   ├── UI/Login.img/*              ← 登入視窗
│   ├── UI/StatusBar.img/*          ← 狀態列
│   ├── UI/ITC.img/*                ← NPC 對話
│   └── UI/StatusBar.img/*          ← 狀態列 / 快捷鍵
│
├── EXE 內部 (v83.idb 看到的)        ← UI 行為邏輯
│   ├── CUIWnd                      ← 所有視窗 base class
│   │   ├── CUIItem                 ← 道具視窗
│   │   ├── CUIEquip                ← 裝備視窗
│   │   ├── CUISkill                ← 技能視窗
│   │   ├── CUIQuestInfo            ← 任務視窗
│   │   ├── CUIStatusBar            ← 狀態列視窗
│   │   ├── CUIWorldSelect          ← 世界選擇視窗
│   │   ├── CUIQuest                ← 任務視窗
│   │   ├── CUIParty                ← 隊伍視窗
│   │   ├── CUIGuild                ← 公會視窗
│   │   ├── CUIGuildBBS             ← 公會佈告欄
│   │   └── CCashShop               ← 商城視窗
│   ├── CUIToolTip                  ← 滑鼠 hover tooltip
│   │   ├── SetToolTip_String       ← 一般字串 tooltip
│   │   ├── SetToolTip_MultiLine    ← 多行 tooltip
│   │   ├── SetToolTip_String2
│   │   ├── SetToolTip_WorldMap
│   │   ├── SetToolTip_Ring
│   │   ├── SetToolTip_Equip        ← 裝備 tooltip
│   │   ├── SetToolTip_Pet          ← 寵物 tooltip
│   │   ├── SetToolTip_Bundle
│   │   ├── SetToolTip_Package
│   │   ├── SetToolTip_SlotInc
│   │   ├── SetToolTip_EquipExt     ← 裝備擴展 tooltip
│   │   ├── SetToolTip_MacroSys
│   │   └── SetToolTip_Skill        ← 技能 tooltip
│   ├── CItemInfo                   ← 道具資料庫
│   │   ├── RegisterSetItemInfo     ← 註冊套裝道具
│   │   ├── RegisterEquipItemInfo   ← 註冊裝備道具
│   │   └── GetItemDesc             ← 取得道具描述
│   └── 其他控制項 class
└── Packet Opcode → UI Mapping     ← 哪個 packet 觸發哪個 UI
    ├── CLogin::OnPacket case X     ← Login UI
    ├── CField::OnPacket case X     ← Field UI (battle, NPC, etc.)
    ├── CWvsContext::OnPacket case X ← World UI (inventory, etc.)
    └── CStage::OnPacket case X     ← Stage UI (cash shop, etc.)
```

## 子章節

- [CUIWnd 視窗系統](cuiwnd/index.md) — 所有 UI 視窗的 base class
- [CUIToolTip 13 個 Tooltip 方法](cuitooltip/index.md) — 滑鼠 hover 提示
- [裝備/道具欄位](item-equip/index.md) — Inventory / Equip 視窗結構
