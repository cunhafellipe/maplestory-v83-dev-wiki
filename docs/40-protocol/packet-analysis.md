# MapleStory v83 Packet 分析(強驗證版)

> **來源**: `wf-output/maple083-direct/packet_analysis_v2.json`
> **方法**: Spirit analyzer v2 — 從 4 個 OnPacket dispatcher 抽出所有 `sub_xxxxx` 呼叫,再 decompile 每個 sub_xxx 找 `CInPacket::Decode*` / `CInPacket::CInPacket::DecodeStr` 呼叫
> **最後更新**: 2026-09-28

## §1 統計

| 指標 | 數值 |
|---|---|
| 從 OnPacket 抽出的 sub_xxx | **163 個 unique** |
| 成功 decompile | 100 個 |
| 找到 Decode/Encode 呼叫 | **74 個** |
| decompile 失敗(encrypted code)| 1 個 |
| 沒有 Decode 呼叫 | 25 個 |

## §2 全部 Decode 分析結果(74 個 sub_xxx)

### §2.1 CField::OnPacket 的 sub_xxx

| sub_xxx | Decode 序列 |
|---|---|
| `0x53185C` | `Decode1` |
| `0x531A08` | `Decode1` |
| `0x531E00` | `Decode1`, `DecodeStr` (×2) |
| `0x532087` | `Decode1`, `DecodeStr` (×2), `Decode1` |
| `0x53228E` | `Decode1`, `DecodeStr` (×2), `Decode1` |
| `0x532FCF` | `Decode1` |
| `0x53300B` | `DecodeStr`, `Decode4` |
| `0x533057` | `Decode4`, `DecodeStr`, `Decode4` |
| `0x5330F7` | `Decode1` (×2), `Decode4` (×2), `Decode1` |
| `0x53347C` | `Decode1`, `Decode4` |
| `0x5335A3` | `Decode1`, `Decode4` |
| `0x535179` | `Decode1`, `Decode4`, `DecodeStr` |
| `0x535224` | `Decode4`, `DecodeStr` |
| `0x5352E9` | `Decode1`, `DecodeStr`, `Decode1`, `Decode1`, `Decode1` |
| `0x535A57` | `Decode1` (×2), `Decode2` |
| `0x5360C0` | `Decode1` |
| `0x5364C5` | `DecodeStr` |
| `0x5378CD` | `Decode1`, `Decode4`, `DecodeBuffer` (×2) |
| `0x537A1E` | `DecodeStr`, `Decode4` |
| `0x537A6A` | `Decode4` (×2), `Decode1`, `DecodeStr`, `Decode4` |
| `0x65DF4C` | `Decode1` |
| `0x6F56EA` | `Decode1`, `Decode1`, `Decode4`, `Decode1`, `DecodeStr` |
| `0x72B82A` | `Decode1`, `DecodeBuffer` (32 bytes) |
| `0x73FFF1` | `Decode1`, `Decode4` |
| `0x756DA7` | `Decode1`, `Decode4`, `Decode4`, `Decode1`, `DecodeStr` |
| `0x79B382` | `Decode1`, `Decode1`, `Decode4` (×2), `Decode1` |
| `0x7C8A4C` | `Decode1`, `Decode1`, `DecodeStr` |
| `0x8511FC` | `Decode1` |

### §2.2 CLogin::OnPacket 的 sub_xxx

| sub_xxx | 推測用途 | Decode 序列 |
|---|---|---|
| `0x5F82F4` | case 26 | `Decode4` |
| `0x5F8340` | case 27 | `Decode1`, `Decode4`, `DecodeStr` |
| **`0x5F83EE`** | **case 0 (ban handler)** | **`Decode1`, `Decode1`, `Decode4`, `Decode1`, `DecodeBuffer` (8), `Decode4`, `Decode1` (×4)** |
| `0x5F8F27` | case 1 | `Decode1`, `Decode1`, `Decode4`, `Decode1` (×2) |
| `0x5F92AE` | case 3 | `Decode1` (×2) |
| `0x5F92DF` | case 2 | `Decode1`, `Decode4`, `Decode1`, `Decode1` (×2) |
| `0x5F95B7` | case 10 | `Decode1`, `DecodeStr`, `Decode1`, `DecodeStr`, `Decode2` |
| `0x5F9891` | case 11 | `Decode1` (×2), `Decode1`, `DecodeBuffer` (16) |
| `0x5F9C72` | case 13 | `DecodeStr`, `Decode1` |
| `0x5F9D15` | case 15 | `Decode4`, `Decode1` |
| `0x5FA26C` | case 14 | `Decode1` |
| `0x5FACCA` | case 8 | `Decode1`, `Decode1` (×3), `DecodeBuffer` |
| `0x5FB245` | case 9 | `Decode1` (×2), `Decode4`, `Decode2`, `Decode4` |
| `0x5FB541` | case 12 | `Decode1`, `Decode1`, `Decode4`, `Decode2`, `Decode4` |
| `0x5FB83D` | case 22 | `Decode1` |
| `0x5FB950` | case 23 | `Decode1` (×2) |
| `0x5FBA49` | case 28 | `Decode1` |
| `0x5FC731` | case 4 | `Decode1`, `Decode1` |
| `0x5FC838` | case 5 | `Decode1` |
| `0x5FC89D` | case 6 | `Decode1` |
| `0x5FCBC1` | case 7 | `Decode1` |

### §2.3 CStage::OnPacket 的 sub_xxx

| sub_xxx | Decode 序列 |
|---|---|
| `0x6449D2` | `Decode1`, `DecodeStr`, `Decode1` |

### §2.4 CWvsContext::OnPacket 的 sub_xxx

| sub_xxx | Decode 序列 |
|---|---|
| `0xA1E48C` | `Decode1`, `Decode2`, `Decode4` (×3) |
| `0xA1E5AF` | `Decode4`, `Decode1`, `Decode4`, `Decode4`, `Decode1` |
| `0xA1E943` | `Decode1` (×2) |
| `0xA1E96D` | `Decode1` (×2) |
| `0xA1EAD9` | `Decode1` (×4), `Decode2` |
| `0xA1F881` | `Decode1` (×2) |
| `0xA1FB52` | `Decode1`, `Decode1` |
| `0xA202BE` | `Decode2`, `Decode1` |
| `0xA2071F` | `DecodeBuffer` (16), `Decode1` |
| `0xA209B2` | `Decode1` |
| `0xA209D4` | `Decode1` |
| `0xA223DC` | `Decode1`, `DecodeStr` (×3), `Decode1` (×2) |
| `0xA23D79` | `Decode1` |
| `0xA2508B` | `Decode1` (×3) |
| `0xA25268` | `Decode1` (×2), `Decode4` |
| `0xA265C2` | `Decode1` (×2), `DecodeStr` (×4) |
| `0xA26D44` | `Decode2` |
| `0xA27891` | `Decode1` (×2), `Decode4` |
| `0xA27B38` | `Decode1` (×2) |
| `0xA27B61` | `Decode1` |
| `0xA27D75` | `Decode1` (×2), `Decode4` (×2), `Decode1` |
| `0xA29115` | `Decode4` (×4), `Decode1` |
| `0xA29739` | `Decode1` |

## §3 重點 packet: CLogin::OnPacket case 0 (Ban Handler)

> **重要**:`sub_5F83EE` 就是 sunnyboy 在 RaGEZONE 教學中提到的 ban message handler!

**驗證**: RaGEZONE 教學的 address `0x5F8569` 是 `StringPool::GetStringW`,而 `sub_5F83EE` 是它的 caller。

**`sub_5F83EE` 完整 Decode 序列**(從 packet_analysis_v2.json):

```c
v99 = CInPacket::Decode1(v4);                  // 1 byte (result code)
*((_BYTE *)this + 456) = CInPacket::Decode1(v2);  // 1 byte (account flag)
CInPacket::Decode4(v2);                          // 4 bytes (可能是 account id)
v6 = CInPacket::Decode1(v2);                     // 1 byte (msg type)
CInPacket::DecodeBuffer(v2, Dst, 8);            // 8 bytes buffer
v102 = CInPacket::Decode4(a2);                   // 4 bytes
... 還有 12+ 個 Decode
```

**完整解碼順序**: `1 + 1 + 4 + 1 + 8 + 4 + ... bytes` = ban message packet 結構

## §4 對應 RaGEZONE 教學

| 教學概念 | v83.idb 對應地址 | Spirit analyzer 找到的 Decode |
|---|---|---|
| `CField::OnPacket` | 0x531325 | ✓ 28 個 sub_xxx 找到 Decode |
| `CLogin::OnPacket` | 0x5F80FF | ✓ 22 個 sub_xxx 找到 Decode |
| `CWvsContext::OnPacket` | 0xA07A08 | ✓ 23 個 sub_xxx 找到 Decode |
| `CStage::OnPacket` | 0x644446 | ✓ 1 個 sub_xxx 找到 Decode |
| **`sub_5F83EE` (case 0 ban)** | 0x5F83EE | ✓ **5+ 個 Decode 完整序列** |

## §5 工具

| 工具 | 路徑 | 用途 |
|---|---|---|
| Spirit analyzer v2 | `wf-output/spirit_packet_analyzer_v2.py` | IDAPython 自動 packet 分析 |
| 結果 JSON | `wf-output/maple083-direct/packet_analysis_v2.json` | 74 個 decoded sub_xxx |

## §6 Spirit analyzer v2 程式碼位置

`C:\MUWORK\GAME\MAPLESOTRY\wf-output\spirit_packet_analyzer_v2.py`

主要邏輯:
1. 讀 `decompiles.json` 內 4 個 OnPacket dispatcher 的 pseudocode
2. 用 regex 找出所有 `sub_xxxxxx` 呼叫
3. 對 top 100 個 sub_xxx 跑 `ida_hexrays.decompile`
4. 提取所有 `CInPacket::Decode*` 呼叫
5. 輸出 JSON

**未來擴展**:
- Spirit analyzer v3:追蹤 xref 從 Decode* 往上找 callers
- Spirit analyzer v3:追蹤 COutPacket::Encode* 系列(angel 沒命名,需要手工)
- Spirit analyzer v3:把 Decode 序列轉成結構(struct)
