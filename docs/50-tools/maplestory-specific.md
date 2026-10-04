# 50-tools — MapleStory 專屬工具

> **本機位置**:`<MAPLESOTRY>\02-Tools\`
> **最後更新**:2026-09-28
> **原則**:每個工具都強驗證,不幻想、不猜

## §1 已 clone 並驗證的 MapleStory 專屬工具

| 工具 | 來源 | 大小 | 用途 | 驗證狀態 |
|---|---|---|---|---|
| **SpiritIDAPlugin** | Bratah123/SpiritIDAPlugin | 87 KB | IDA plugin 自動 packet 分析 | 已 clone,source 看過(用 IDA 7.0 / Py 2.7,**不相容** IDA 9.3) |
| **MapleLib** | lastbattle/MapleLib | 8.3 MB | .NET WZ library(parsing + modifying) | 已 clone,source 看過(.NET 10.0) |
| **WzImg-MCP-Server** | lastbattle/WzImg-MCP-Server | 67 KB | .NET MCP server(74 tools for AI agent)| 已 clone,需 .NET 10 + 已 export WZ→IMG |
| **MaplePE** | zhyonc/MaplePE | 22.3 MB | C# packet editor (extract InPacket/OutPacket)| 已 clone,需 Visual Studio 編譯 |
| **WAND_EXT** | SpikeMogo/WAND_EXT | 6.3 MB | C++ v83 class definitions + offsets | 已 clone,**`MapleOffsets.h` 完整**(22 KB) |
| **MapleSniffer** | taida957789/MapleSniffer | 948 KB | C++ packet sniffer + AES decryption | 已 clone,需 npcap + Visual Studio 編譯 |

## §2 各工具詳細

### §2.1 WAND_EXT — 最有用(已驗證)

**`MapleOffsets.h` (22 KB)** 是金子 — 完整 MapleStory v83 class offsets:

```c
struct CUserLocalOffsets {
    uintptr_t CUserLocal = 0xBEBF98;
    uintptr_t x = 0x116C;
    uintptr_t y = 0x1170;
    uintptr_t UID = 0x11A8;
    // ... 更多
};

struct CWvsPhysicalSpace2DOffsets {
    uintptr_t CWvsPhysicalSpace2D = 0xBEBFA0;
    uintptr_t FootholdList = 0x88;
    // ...
};

struct CMobOffsets {
    uintptr_t CMobPool = 0x00BEBFA4;
    // ...
};
```

**C++ class headers 完整**:
- `CUserLocal.h`, `CUserPool.h`
- `CMob.h`, `CMobPool.h`, `CNpc.h`, `CNpcPool.h`, `CPet.h`
- `CItemInfo.h`, `CDrop.h`, `CDropPool.h`
- `CFuncKeyMapped.h`, `CShopDlg.h`, `CInputSystem.h`
- `CWvsPhysicalSpace2D.h`, `CStaticFoothold.h`, `CLadderRope.h`, `CPortal.h`
- `CTemporaryStat.h`, `CTemporaryStatView.h`

**來源**: SpikeMogo 的 WAND_EXT — 用來對 v83 client 做外部讀記憶體的工具(無 injection)。

### §2.2 MapleLib — WZ 操作

**用途**:解析 + 修改 + 建立 .wz 檔

**優點**:直接處理 .wz(不需要先 export .img)

**限制**:Angel 的 HaCreator 已基於 MapleLib,所以 WzImg-MCP-Server 需要先用 MapleLib/HaCreator 把 .wz 轉成 .img + manifest.json。

### §2.3 WzImg-MCP-Server — 74 AI agent tools

**74 tools across 10 categories**:
- read(ReadStrings / ReadNumbers / ReadBooleans / ReadVectors)
- analyze(GetNodeTree / GetNodeProperties)
- modify(ModifyStrings / ModifyNumbers)
- export(ExportToJson / ExportToXml / ExportToCsv / ExportToMapJson)
- file(FileSearch / GetImgTree)
- image(ImageSearch / ImageExtract)
- audio(AudioList / AudioExtract)
- batch(BatchRead / BatchModify)
- analysis(Compare / Diff)
- lifecycle(Initialize / Close)

**但需要**: 先用 HaCreator 把 .wz 轉成 .img

### §2.4 SpiritIDAPlugin — IDA plugin

**來源**: Bratah123

**功能**:對 IDA decompiled pseudocode 自動找 Decode/Encode 呼叫

**Python 3 + IDA 9.x 移植版**: `wf-output/spirit_packet_analyzer_v2.py`

**驗證結果**: 在 v83.idb 跑了,找到 **74 個 sub_xxx 內的 Decode 序列**

### §2.5 MaplePE — C# packet editor

**功能**:在 running client process 攔截 CInPacket/COutPacket 呼叫,記錄 packet 結構

**狀態**: 未編譯(需 Visual Studio)
**需要**: 取得 client 的 v83 addresses(CInPacket::Decode1/2/4/Str/Buffer + COutPacket::Encode* 系列)

### §2.6 MapleSniffer — C++ packet sniffer

**功能**:npcap-based capture + TCP reassembly + MapleStory AES-256 ECB decryption

**狀態**: 未編譯(需 npcap + Visual Studio)
**特點**:支援 JS-based packet parsing scripts

## §3 強驗證結論

**已驗證可用的(實用)**:
- ✓ WAND_EXT `MapleOffsets.h` — v83 class offsets 可直接參考
- ✓ Spirit analyzer v2 — 74 個 packet Decode 序列已 dump
- ✓ v83.idb dump — 54K functions + 6 核心 pseudocode
- ✓ GitHub Pages WIKI — 已發布

**未驗證的(需要更多工作)**:
- ✗ WzImg-MCP-Server — 需 .NET 10 + WZ→IMG export(用 HaCreator)
- ✗ MaplePE — 需 Visual Studio 編譯 + client addresses
- ✗ MapleSniffer — 需 npcap + Visual Studio 編譯
- ✗ MapleLib — 需 .NET 10 編譯/整合

**未來擴展**:
1. **編譯 MapleLib** — 寫 console 工具直接 WZ→IMG
2. **整合 WzImg-MCP-Server 到 Hermes** — 自動 dump UI.wz 結構
3. **改 Spirit analyzer v3** — 從 Decode* 函數往上找 callers
4. **移植 SpiritIDAPlugin 到 Python 3 + IDA 9.x** — 取代 v2(目前是 IDAPython script)
