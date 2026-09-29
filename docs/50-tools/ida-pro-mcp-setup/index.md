# IDA Pro MCP 設定指南

> **目標**:在本機裝好 IDA Pro 9.3 + idalib-mcp,可用 AI 自動跑逆向分析
>
> **本機狀態**:已驗證 IDA Pro 9.3 (cracked) + idalib + idalib-mcp 全部可用

## 已驗證步驟

### 1. 安裝 IDA Pro 9.3

- 路徑:`C:\MUWORK\apps\Ida pro\`
- `ida.exe`(GUI)
- `idat.exe`(headless)
- `idalib.dll`(idalib library)
- `idapro.hexlic`(cracked license,有效到 2083)

### 2. 啟用 idalib

```bash
cd "C:/MUWORK/apps/Ida pro"
python "C:/MUWORK/apps/Ida pro/idalib/python/py-activate-idalib.py"
```

這會建立 `ida-config.json` 指向 IDA 安裝目錄。

### 3. 安裝 ida-pro-mcp

```bash
# clone
git clone https://github.com/mrexodia/ida-pro-mcp.git

# 用 uv 安裝依賴
cd ida-pro-mcp
uv sync
```

### 4. 跑 headless idalib-mcp(本機已驗證)

```bash
# 啟動 supervisor + 開 binary
cd ida-pro-mcp
uv run idalib-mcp --stdio "C:\path\to\binary.exe"

# 或用 HTTP transport
uv run idalib-mcp --host 127.0.0.1 --port 8745 "C:\path\to\binary.exe"
```

### 5. 整合到 Hermes MCP

```yaml
# ~/.hermes/config.yaml
mcp_servers:
  idalib-mcp:
    command: "C:/Users/e7896/AppData/Local/hermes/cache/scratch/ida-pro-mcp-isolated/ida-pro-mcp/.venv/Scripts/python.exe"
    args:
      - "C:/Users/e7896/AppData/Local/hermes/cache/scratch/ida-pro-mcp-isolated/ida-pro-mcp/src/ida_pro_mcp/idalib_server.py"
    enabled: false  # 因為 supervisor 是 binary-bound
```

## 已驗證的腳本:自動 dump v83.idb

`C:\Users\e7896\AppData\Local\hermes\cache\scratch\dump_v83_idb.py`

```python
import idautils, ida_name, ida_funcs, ida_hexrays
import ida_idaapi, ida_ida, ida_segment
import json, os

# 自動 dump functions / strings / segments / decompile / xref
# 輸出到 wf-output/ida-v83-direct/
```

## idalib-mcp 的 66 個 tools

| 類別 | tools |
|---|---|
| Core | idb_open / idb_list / idb_close / survey_binary |
| Functions | list_funcs / func_query / lookup_funcs / analyze_batch / analyze_function |
| Decompile | decompile / disasm / microcode |
| Strings | search_text / find_regex / find_bytes |
| Memory | get_bytes / get_int / get_string / patch |
| Types | set_type / declare_type / infer_types |
| Xrefs | xrefs_to / callees / callgraph |
| Modification | put_int / set_type / rename / set_comments |

## 注意事項

- IDA Free **不支援** idalib-mcp(需要 IDA Pro/IDA Home license)
- 我們本機裝的是 IDA Pro 9.3 cracked,功能等同 IDA Pro
- `idalib-mcp --stdio <binary>` 啟動後,binary 路徑已 baked-in
- 換 binary 需要重啟 server

## 整合進 Hermes

```bash
# 加入 MCP
hermes mcp add idalib-mcp --command python --args "[C:/path/to/idalib_server.py]"

# 啟用
hermes mcp enable idalib-mcp
```

**警告**:`idalib-mcp` supervisor 是 binary-bound,跟 Hermes 預期的 lazy-load 模型不完全相容。要讓 LLM 動態指定 binary 需要用環境變數 `IDALIB_INPUT_PATH`。

## 完整驗證記錄

詳見 `00-TECHNICAL-REPORT.md` 內 §0 工具鏈段。
