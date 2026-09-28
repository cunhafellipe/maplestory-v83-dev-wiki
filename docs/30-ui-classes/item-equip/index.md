# 裝備 / 道具欄位結構

> **目的**:MapleStory v83 的 Inventory 與 Equip 視窗結構,給二次開發者新增/修改欄位用

## Inventory 類型(從 server side 對照)

HeavenMS 服務端有完整的 Inventory type 定義,跟 client 對應:

| MapleInventoryType | 對應視窗 | 欄位範圍 |
|---|---|---|
| `EQUIP` (1) | CUIEquip | 1 ~ 40(裝備欄位)|
| `USE` (2) | CUIItem | 1 ~ 96(消耗道具,上限 96)|
| `ETC` (4) | CUIItem | 1 ~ 96(其他)|
| `CASH` (3) | CUIItem | 1 ~ 96(商城道具)|

## 裝備欄位定義(從 RaGEZONE 教學)

裝備視窗有以下固定欄位:

```
裝備視窗:
┌────────────────────────────────────┐
│  [帽子]    [臉飾]   [眼飾]   [耳環]│
│  [披風]    [上衣]   [褲子]   [腰帶]│
│  [鞋子]    [手套]   [盾牌]   [墜飾]│
│  [武器]    [副手]                  │
│  [胸章]    [勳章]                  │
└────────────────────────────────────┘
```

## 在 v83.idb 內找到的相關 strings

| Address | String | 推測用途 |
|---|---|---|
| `0xaf4524` | `allowedItem` | 道具類型判斷 |
| `0xaf4530` | `mobequip` | 怪物裝備欄位 |
| `0xaf4548` | `saddle` | 坐騎鞍 |
| `0xaf4568` | `pendant` | 墜飾 |
| `0xaf4570` | `ring4` | 戒指 4 |
| `0xaf687c` | `reqEquip` | 需求裝備 |
| `0xaf6888` | `reqItem` | 需求道具 |
| `0xaf63d0` | `epicItem` | Epic 等級道具 |
| `0xaf63e8` | `equipTradeBlock` | 裝備交易限制 |
| `0xaf63fc` | `itemid` | 道具 ID |
| `0xaf6528` | `slotIndex` | 欄位索引 |
| `0xaf68b4` | `itemNum` | 道具數量 |

## 道具資訊的 WZ 路徑

```
Etc/SetItemInfo.img        ← 套裝道具
Item/Etc/0425.img          ← 未知類型 1
Item/Etc/0426.img          ← 未知類型 2
Item/Etc/0400.img          ← 未知類型 3
Item/Etc/0429.img/%08d/effect  ← 道具特效
Skill/ItemSkill.img        ← 道具技能
Etc/ItemMake.img           ← 道具製作
Etc/NpcLocation.img/       ← NPC 位置
```

## 對應函數(diamondo25 IDC)

| Function | String ref | 推測用途 |
|---|---|---|
| `CItemInfo::RegisterSetItemInfo` | `Etc/SetItemInfo.img` | 註冊套裝道具資料 |
| `CItemInfo::RegisterEquipItemInfo` | `epicItem` | 註冊裝備道具資料 |
| `CItemInfo::GetItemDesc` | `Can be equipped on #cone-handed sword or two-handed sword.#` | 取得道具描述 |

## HeavenMS 端 對應(MIT v83 server source)

從 `client/inventory/MapleInventory.java`:

```java
public class MapleInventory {
    private Map<Short, IItem> inventory;
    private byte slotLimit;
    private MapleInventoryType type;
    public byte getSlotLimit();     // 96 = max
    public IItem findById(int itemId);
    public void addSlot(byte slot); // 增加 slot 上限
}
```

## 二次開發情境

| 想改 | 改哪裡 |
|---|---|
| 加新裝備欄位(如 v83 沒有 SHOULDER)| WZ 內 `UI/UIWindow.img/Equip/backgrnd` + server side `MapleInventoryType` |
| 加新道具類型 | WZ 內 `Item/Etc/xxxx.img` + server side `Item.java` |
| 改欄位上限 | server `slotLimit`(上限 96 寫死)|
| 改裝備 tooltip | `CUIToolTip::SetToolTip_Equip` (0x008E97D2) |

## 參考連結

- [RaGEZONE importing new item type](https://forum.ragezone.com/threads/importing-new-type-of-item-from-v100-to-v83.1223253/)
- [HeavenMS MapleInventory source](https://github.com/HuiMS079/MapleStory-v83/blob/main/src/client/inventory/MapleInventory.java)
