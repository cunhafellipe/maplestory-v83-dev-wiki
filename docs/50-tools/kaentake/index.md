# kaentake — C++ Detours Hook Client

> **狀態**:已 clone(02-Tools/kaentake/)
> **用途**:Hook MapleStory client 的 C++ 框架,不需 patch 主程序加功能
> **語言**:C++ + Detours

## 概要

kaentake 是 MapleStory 客戶端的 hook 框架,使用微軟 Detours library 攔截函數呼叫。

## 工作原理

```
MapleStory 0.83.exe (原始)
    ↓ 載入
kaentake.dll (hook DLL)
    ↓ 攔截
kaentake 自訂邏輯 (C++ 函數)
    ↓
呼叫原函數 / 修改參數 / 回傳修改結果
```

## 與 MapleEzorsia V2 的差異

| 項目 | kaentake | MapleEzorsia V2 |
|---|---|---|
| Hook 方法 | DLL 注入 | DLL 注入 |
| 對 client | hook 任何 client | 限定 `localhostv83_clean.exe` |
| HD 解析度 | 無 | 內建 |
| 開發狀態 | 已停 | 活躍 |

## 安裝 / 編譯

```bash
cd C:\MUWORK\GAME\MAPLESOTRY\02-Tools\kaentake
# 編譯需要 Visual Studio + Detours SDK
msbuild kaentake.sln
```

## 常用 hook target

```c
// hook CClientSocket::SendPacket
DETOUR_TRAMPOLINE(int, RealSendPacket, (CClientSocket* this, COutPacket* pkt), this, pkt);
// ... 加自訂邏輯

// hook CLogin::OnPacket
// hook CField::OnPacket
// hook CWvsContext::OnPacket
// hook CUIStatusBar::Draw (改 UI)
```

## 二次開發情境

| 想做 | 用 kaentake |
|---|---|
| 加外掛功能 | ✓ |
| Hook socket | ✓ |
| 動態注入 UI 修改 | ✓ |
| 攔截 packet | ✓ |
| 修補主程序 | ✗(用 OllyDbg / IDA)|

## 參考資料

- [kaentake repo](https://github.com/iw2d/kaentake)
- [Detours SDK](https://github.com/microsoft/Detours)
- [MapleEzorsia V2](https://github.com/phantomeis/MapleEzorsia-v2/wiki/v83%E2%80%90Client%E2%80%90Setup%E2%80%90and%E2%80%90Development%E2%80%90Guide)
