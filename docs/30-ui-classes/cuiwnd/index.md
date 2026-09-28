# CUIWnd — 所有 UI 視窗的 Base Class

> **來源**:RaGEZONE UI position thread 1165487 + CConfig struct 分析
>
> **作用**:所有 UI 視窗 (`CUIItem`, `CUIEquip`, `CUISkill`, etc.) 都繼承 `CUIWnd`
>
> **二次開發**:UI 位置儲存、UI 顯示/隱藏都透過 CUIWnd 處理

## CUIWnd 結構

```c
class CUIWnd {
    int m_nUIType;        // UI 類型 ID (對應 CConfig::m_nUIWnd_X[43])
    int m_nPosX;          // 當前 X 位置
    int m_nPosY;          // 當前 Y 位置
    bool m_bVisible;      // 是否可見
    bool m_bEnabled;      // 是否啟用
    int m_nWidth;         // 寬度
    int m_nHeight;        // 高度
    // ... 其他
};
```

## 43 個 UI 類型(RaGEZONE 教學)

| Index (m_nUIType) | 推測的 Class | 用途 |
|---|---|---|
| 0 | CUIStatusBar | 狀態列 |
| 1 | CUIItem | 道具視窗 |
| 2 | CUIEquip | 裝備視窗 |
| 3 | CUISkill | 技能視窗 |
| 4 | CUIQuestInfo | 任務視窗 |
| 5-42 | 其他 | 其他 UI 視窗 |

**注意**:RaGEZONE 上沒有完整對照表,只有 `m_nUIType = 3 → CUISkill` 已知。

## CConfig 結構(RaGEZONE 教學)

```c
class CConfig {
    int m_nUIWnd_X[43];       // 43 個 UI 視窗的 X 位置
    int m_nUIWnd_Y[43];       // 43 個 UI 視窗的 Y 位置
    bool bSysOpt_LargeScreen; // 大螢幕模式
    bool bSysOpt_WindowedMode;// 視窗模式
    // ... 其他
};
```

## CUIWnd::CreateUIWndPosSaved

```c
// 儲存 UI 視窗位置
CUIWnd::CreateUIWndPosSaved() {
    int type = this->m_nUIType;
    CConfig->m_nUIWnd_X[type] = this->m_nPosX;
    CConfig->m_nUIWnd_Y[type] = this->m_nPosY;
    // 寫入 registry 持久化
    SaveToRegistry();
}
```

## 在 v83.idb 內的對應

| Class | 已驗證位置 | 來源 |
|---|---|---|
| `CUIStatusBar` | 有 references | IDC + RaGEZONE |
| `CUIQuestInfo::LoadData` | `"QuestID : %d"` string | IDC |
| `CUIWorldSelect::MakeAdvice` | `"Please select the World..."` | IDC |
| `CUIGuildBBS::FormatDate` | `"%d/%02d/%02d %02d:%02d"` | IDC |

## 二次開發情境

| 想改 | 改哪裡 |
|---|---|
| UI 預設位置 | `CConfig` struct 內 `m_nUIWnd_X/Y[i]` 預設值 |
| UI 大小 | `CUIWnd::OnCreate` 內 `m_nWidth/m_nHeight` |
| UI 持久化位置 | registry 內 `SOFTWARE\Microsoft\Windows\CurrentVersion` 對應 key |
| UI 顯示/隱藏 | `CUIWnd::SetVisible(bool)` |

## WZ 對應

每個 CUIWnd 對應到 WZ 內的一個 `.img`:

```
UI/UIWindow.img/Item/backgrnd     ← CUIItem
UI/UIWindow.img/Equip/backgrnd    ← CUIEquip
UI/UIWindow.img/Skill/backgrnd    ← CUISkill
UI/UIWindow.img/Quest/backgrnd    ← CUIQuestInfo
UI/StatusBar.img/base/backgrnd    ← CUIStatusBar
UI/Login.img/ViewAllChar/back     ← CUIWorldSelect
```

## 參考連結

- [RaGEZONE UI position thread](https://forum.ragezone.com/threads/where-does-maplestory-record-the-ui-position.1165487/)
- [RaGEZONE v83 resolution changes thread](https://forum.ragezone.com/threads/v83-client-resolution-changes.1179964/)
