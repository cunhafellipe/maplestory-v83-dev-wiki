# 50-tools — 工具鏈

> **目的**:整理 v83 client / server 開發 / 逆向分析的工具

## 已驗證可用

### IDA Pro 9.3
- **狀態**:已安裝(<TOOLS>/Ida pro/)
- **license**:已破解(`idapro.hexlic`,hexlic 授權到 2083)
- **idalib**:已啟用
- **ida-pro-mcp**:已安裝(<USERPROFILE>/hermes/cache/scratch/)
- **用法**:`idat.exe -A -S<idapython_script> <binary>`

### ida-pro-mcp (AI 逆向)
- **版本**:v2.0(mrexodia)
- **模式**:GUI plugin / idalib headless
- **我們的選擇**:idalib headless
- **66 個 tools**:decompile / disasm / xrefs / search / patch 等
- **配置**:已加入 Hermes mcp_servers(disabled)

### HaRepacker
- **狀態**:未安裝(待下載)
- **用途**:WZ 檔編輯(.wz → .xml → 編輯 → .xml → .wz)
- **來源**:搜尋 "HaRepacker 4.2.4 GMS old"

### kaentake (C++ Detours hook client)
- **狀態**:已 clone(02-Tools/kaentake/)
- **用途**:Hook MapleStory client,不改主程序加功能
- **語言**:C++ + Detours
- **vs MapleEzorsia**:類似,但 kaentake 是獨立 DLL,MapleEzorsia 是 DLL 注入到 localhostv83_clean

### WZ Mod Tool Suite
- **狀態**:已 clone(02-Tools/)
- **用途**:C# WZ 批次修改工具
- **搭配**:MadaraGameDev/SoloMapling 開發

### Cosmic (Java 21 server)
- **狀態**:已 clone(04-Emulators/GMS-v083-Cosmic/)
- **用途**:v83 server emulator
- **Stars**:~1.5k
- **建議**:作為開發用 server

## 工具對照表

| 想做 | 用什麼工具 |
|---|---|
| 看 v83 client pseudocode | IDA Pro 9.3 |
| 自動 AI 逆向 | ida-pro-mcp (idalib-mcp --stdio) |
| 改 WZ 視覺 | HaRepacker + WZ Mod Tool Suite |
| Patch client EXE | OllyDbg 或 IDA |
| Hook client (不改 EXE)| kaentake / MapleEzorsia |
| 架 server | Cosmic / HeavenMS |
| 寫 AI bot | SoloMapling-wisteria |

## 子章節

- [kaentake](kaentake/index.md) — C++ Detours hook client
- [WZ Mod Tool](wz-mod-tool/index.md) — C# WZ 工具
- [IDA Pro MCP 設定](ida-pro-mcp-setup/index.md) — 安裝與配置
