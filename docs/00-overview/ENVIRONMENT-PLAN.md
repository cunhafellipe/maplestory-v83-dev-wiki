# HERMES WORK ENVIRONMENT 完善計畫

> **目標**:讓 Hermes 在 MapleStory v83 開發任務上**任何工作都可以完成**
> **原則**:強驗證、穩、現實、肯定、完整、專業
> **最後更新**:2026-09-28

---

## §0 完整目標

### 0.1 規劃的 MCP 工具集(整合進 Hermes)

| MCP 名稱 | 用途 | 狀態 |
|---|---|---|
| `ida-pro-mcp` | IDA Pro 9.3 headless 反組譯 + decompile | ✓ 已驗證(本機有安裝) |
| `idalib-mcp` | 跟 ida-pro-mcp 一樣(舊版 alias)| 待整合 |
| `wzimg` (WzImg-MCP-Server) | 74 tools 讀寫 .wz / .img 檔 | 🔧 安裝中 |
| `maplestory-api` (kcw2034) | 查 Nexon OpenAPI 現實遊戲資料 | 🔧 安裝中 |
| `omp` | LLM 委託(背景任務)| ✓ 已驗證 |

### 0.2 已驗證的本地資料

| 資源 | 位置 | 大小 |
|---|---|---|
| IDA Pro 9.3 (cracked) | `C:\MUWORK\apps\Ida pro\` | 6.7 MB |
| Mapledumper v0.7.2 | `C:\MUWORK\GAME\MAPLESOTRY\tools\mapledumper\` | 2.7 MB |
| maple-unpack-native | 同上 | 65 MB |
| v83.idb → v83-copy.i64 | `C:\MUWORK\GAME\MAPLESOTRY\v83-copy.i64` | 107 MB |
| MapleStory 0.83.exe (Themida 加殼) | `C:\MUWORK\GAME\MAPLESOTRY\待分類\` | 4.3 MB |
| 簽到表/wz/UI.wz | 同上 | 25 KB |
| 已 clone 的 server 源碼 | `C:\MUWORK\GAME\MAPLESOTRY\04-Emulators\` | 多個 |

---

## §1 完整工作流程設計

### 1.1 客戶端逆向(IDA 分析)

```
Step 1: 載入 binary
  ├─ .idb 已有 → 直接用 `v83-copy.i64`(已 32→64-bit 轉檔)
  ├─ 原始 .exe → 用 `idalib-mcp` headless
  │   ├─ 完整跑 auto-analysis(等 5-10 分鐘,不等 supervisor 假 ready)
  │   ├─ 用 Hex-Rays decompile 拿 pseudocode
  │   └─ 強制 undefine + reanalyze 自定義 section(如果 IDA 漏 code)
  └─ 已加殼 .exe → 先嘗試 mapledumper(只支援 Themida 2.x)

Step 2: dump 結構化資料
  ├─ functions.json (54K functions)
  ├─ strings.json (1.2K strings)
  ├─ decompiles.json (核心 6 個函數)
  ├─ string_xrefs.json (重要 strings xref)
  └─ segments.json (PE segments)

Step 3: 套用歷史 renames
  ├─ diamondo25 IDC script(16/24 命中)
  └─ angel ToolTip addresses (13 個)

Step 4: 寫到 Wiki
  └─ C:\MUWORK\GAME\MAPLESOTRY\wiki\docs\
```

### 1.2 WZ 檔案操作

```
Step 1: 用 WzImg-MCP-Server 讀 .wz / .img
  ├─ 列出所有 strings / numbers / vectors / booleans
  ├─ search by name / value / type
  └─ read string by full path

Step 2: 修改 .wz
  ├─ 用 WzImg-MCP-Server 直接改
  ├─ 改完用 HaRepacker 重新加密 (如有需要)
  └─ 備份原檔

Step 3: 把改完的結構寫進 Wiki
  └─ 用 WzImg 的 export JSON / XML / CSV
```

### 1.3 Packet 分析

```
Step 1: dump 在 v83.idb 內的 opcode handlers
  └─ 4 個 OnPacket dispatcher 的 pseudocode 已 dump

Step 2: 找特定 opcode 對應的 sub_xxx
  ├─ 用 xrefs_to 找引用
  ├─ decompile 對應 sub_xxx
  └─ 對照 HeavenMS server 端的 opcode 實作

Step 3: 修改 packet handler
  ├─ kaentake hook DLL 攔截
  ├─ 或 patch EXE(需要脫殼後)
  └─ server 端加對應 RecvOpcode
```

### 1.4 Server 端整合

```
Step 1: 用 Cosmic 或 HeavenMS 跑 local server
Step 2: 用 client 連線測試
Step 3: 用 packet sniffer(MapleSniffer / MaplePE)驗證協議
Step 4: 開發新功能:
  ├─ WZ 改 UI 視覺(WzImg-MCP-Server)
  ├─ EXE 改 UI 行為(kaentake / MapleEzorsia)
  └─ Server 改 packet handler (Cosmic Java)
```

---

## §2 立即執行的步驟(順序)

### Step 1: 安裝 WzImg-MCP-Server
- 原因:74 tools 直接讀寫 .wz,大幅加速 WZ 分析
- 風險:需要 .NET 9 SDK
- 驗證:`wzimg` MCP server 在 Hermes 中可呼叫

### Step 2: 整合現有 idalib-mcp 到 Hermes
- 原因:之前 disabled,讓 LLM 可呼叫反組譯工具
- 風險:supervisor 假 ready 問題已知
- 驗證:實際 decompile 結果可讀

### Step 3: 安裝 maplestory-mcp-server
- 原因:可查現實遊戲資料(雖然 v83 不一定有 API key)
- 風險:需要 Nexon API key(可能要申請)
- 驗證:即使沒 API key 也可看到 tool schema

### Step 4: 補完 v83.idb 全量 dump
- 原因:目前只有 6 個 decompile,但 54K 個 sub_xxx 都沒 decompile
- 風險:decompile 整個 IDB 需要很長時間
- 驗證:每個 named function 都有 pseudocode

### Step 5: 解壓 v83.rar
- 原因:可能含有 HeavenMS-localhost-WINDOW.exe(已脫殼 client)
- 風險:需要 unrar 工具
- 驗證:解壓後看是否有可分析的 client

### Step 6: 補完 MapleStory 0.83.exe 的脫殼
- 原因:Themida 3.x 無法靜態分析
- 風險:需要人工 OEP 找尋 + unpack
- 驗證:OEP 找到後能 decompile CLogin::OnPacket 等核心函數

---

## §3 不做的事

- ❌ 上傳任何 binary 到公開 repo
- ❌ 自動嘗試破解商業加殼(Themida 是商業軟體)
- ❌ 把已脫殼 client binary 加進 wiki

---

## §4 強驗證原則

每完成一個步驟,**必須**:
1. **測試**:實際跑過,不只看文件
2. **記錄**:輸出檔案 + 大小 + timestamp
3. **對照**:跟已知 reference 對比(如 RaGEZONE 教學地址)
4. **失敗要說**:不能假裝成功

---

## §5 預期最終狀態

完成所有步驟後,我的工作環境可以:

1. **任何 v83 client 逆向任務** — 從 IDB 到 decompile 全鏈條
2. **任何 WZ 檔案操作** — 74 個 tools 直接 MCP 呼叫
3. **任何 packet 分析** — 從 v83.idb dump + 對照 server 源碼
4. **任何 server 端修改** — Cosmic Java 編譯 + 測試
5. **任何文件輸出** — Wiki + GitHub Pages 自動更新
6. **任何委派任務** — OMP 平行子代理


---

## §6 重新評估的優先級

> 重要:**自由規劃不急**。不要貪多。

### 實際優先順序(已驗證可行性)

| # | 任務 | 重要性 | 已驗證 | 下次動作 |
|---|---|---|---|---|
| **1** | 修 `idalib-mcp` 在 Hermes 的整合(改用 idat.exe + IDAPython)| ⭐⭐⭐⭐⭐ | 確認 IDA 真的能用 | 寫新 MCP entry,直接呼叫 idat.exe |
| **2** | 解 `v83.rar`(用 7z 或裝 unrar)| ⭐⭐⭐⭐ | 7z 不能解 .rar | 裝 unrar |
| **3** | 整合 `MapleLib` 寫 WZ→IMG 工具 | ⭐⭐⭐ | 需 clone | clone + 寫 tool |
| **4** | 整合 `WzImg-MCP-Server` | ⭐⭐⭐ | 需 .img | 等 step 3 完成 |
| **5** | 補完 v83.idb 全量 decompile | ⭐⭐ | 1-2 小時 | 寫 IDAPython batch script |
| **6** | 嘗試脫殼 MapleStory 0.83.exe (Themida 3.x)| ⭐ | 高難度 | 需要人工 OEP 找尋 |

### 暫時不做
- 任何涉及自動脫殼的成功(Themida 3.x 超出當前工具能力)
- 上傳任何 binary
