# v83.idb 已知 MapleStory Class Methods

> **來源**: `wf-output/ida-v83-direct/mapple_methods.json`
> **總計**: 6 個 MapleStory class / 10 個 named methods

## `CLogin` (1 methods)

| Method | Address | Size | Description |
|---|---|---|---|
| `OnPacket` | `0x5F80FF` | 385B | Login packet dispatcher (opcode 0~28) |

## `CField` (1 methods)

| Method | Address | Size | Description |
|---|---|---|---|
| `OnPacket` | `0x531325` | 1,201B | Field packet dispatcher (opcode 125~345,最複雜) |

## `CWvsContext` (1 methods)

| Method | Address | Size | Description |
|---|---|---|---|
| `OnPacket` | `0xA07A08` | 1,158B | World context packet dispatcher (opcode 29~62) |

## `CStage` (1 methods)

| Method | Address | Size | Description |
|---|---|---|---|
| `OnPacket` | `0x644446` | 60B | Stage packet dispatcher (opcode 128~130) |

## `StringPool` (2 methods)

| Method | Address | Size | Description |
|---|---|---|---|
| `GetString` | `0x406455` | 28B | 從 string pool 取 string ID 對應的 string |
| `GetInstance` | `0x79E805` | 123B | 取得 StringPool singleton |

## `CInPacket` (4 methods)

| Method | Address | Size | Description |
|---|---|---|---|
| `Decode1` | `0x4065F3` | 54B | Decode 1 byte from packet |
| `Decode2` | `0x42470C` | 57B | Decode 2 bytes (short) from packet |
| `Decode4` | `0x406629` | 56B | Decode 4 bytes (int) from packet |
| `DecodeBuffer` | `0x432257` | 71B | Decode buffer from packet |
