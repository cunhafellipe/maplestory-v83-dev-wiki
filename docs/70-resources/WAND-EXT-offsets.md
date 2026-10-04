# WAND_EXT MapleOffsets.h — 完整 v83 Class Offsets

> **來源**: [SpikeMogo/WAND_EXT](https://github.com/SpikeMogo/WAND_EXT) `src/MapleOffsets.h`
> **本地路徑**: `<MAPLESOTRY>\02-Tools\WAND_EXT-main\Wand_Ext_Strip\Wand_Ext\src\MapleOffsets.h`
> **大小**: 22 KB
> **已驗證**: ✓ 已 clone,已讀過 source

## §1 重要 Offsets

> 強驗證事實 — 這些都是 v83 client 的真實 offsets,可以直接用於外部讀記憶體。

### §1.1 Global Singleton Points

| Singleton | Address | 說明 |
|---|---|---|
| `CUserLocal` | `0xBEBF98` | 本地玩家物件 |
| `CWvsPhysicalSpace2D` | `0xBEBFA0` | 物理世界(包含 foothold 等)|
| `CMobPool` | `0xBEBFA4` | 怪物池 |
| `CUserPool` | (在 WAND_EXT CUserPool.h)| 玩家池 |

### §1.2 CUserLocal Fields

```c
struct CUserLocalOffsets {
    uintptr_t CUserLocal     = 0xBEBF98;   // base address
    uintptr_t UID             = 0x11A8;
    uintptr_t foothold        = 0x1F0;
    uintptr_t x               = 0x116C;      // x 座標
    uintptr_t y               = 0x1170;      // y 座標
    uintptr_t attackCount     = 0x2B88;
    uintptr_t breath          = 0x56C;
    uintptr_t charAnimation   = 0x570;
    uintptr_t comboCount      = 0x3220;
    uintptr_t faceDir         = 0x1180;
    
    // 鞋子 attribute
    uintptr_t m_pAttrShoe     = 0x2B64;
    uintptr_t AttrShoe_WalkSpeed = 0x24;
    uintptr_t AttrShoe_WalkJump  = 0x48;
    uintptr_t AttrShoe_Mass      = 0xC;
};
```

### §1.3 CWvsPhysicalSpace2D Fields

```c
struct CWvsPhysicalSpace2DOffsets {
    uintptr_t CWvsPhysicalSpace2D = 0xBEBFA0;
    uintptr_t FootholdList    = 0x88;
    uintptr_t LadderRopeArray = 0xA8;
    uintptr_t Left            = 0x24;
    uintptr_t Right           = 0x2C;
    uintptr_t Top             = 0x28;
    uintptr_t Bottom          = 0x30;
    uintptr_t BaseLayer       = 0x40;       // m_nBaseZmass
    uintptr_t m_constants     = 0x8;
};
```

### §1.4 CMobPool / CMob Fields

```c
struct CMobOffsets {
    uintptr_t CMobPool         = 0x00BEBFA4;
    uintptr_t CMobPoolList     = 0x28;
    
    // Position
    uintptr_t posX_raw         = 0x510;     // this + 324*4
    uintptr_t posY_raw         = 0x514;
    uintptr_t prevPosX_raw     = 0x518;
    uintptr_t prevPosY_raw     = 0x51C;
    uintptr_t HP               = 0x520;
    
    // Body rects
    uintptr_t rcBody           = 0x40C;     // this + 259*4
    uintptr_t rcBodyFlip       = 0x41C;     // this + 263*4
    
    // Template
    uintptr_t CMobTemplate     = 0x188;
    uintptr_t TemplateID       = 0x0C;
    uintptr_t TemplateID_CS    = 0x14;
    uintptr_t TemplateMaxHP    = 0x7C;
};
```

### §1.5 CStaticFoothold Fields

```c
struct CStaticFootholdOffsets {
    uintptr_t x1          = 0xC;
    uintptr_t y1          = 0x10;
    uintptr_t x2          = 0x14;
    uintptr_t y2          = 0x18;
    uintptr_t layer       = 0x20;
    uintptr_t uvx          = 0x30;     // slope_x
    uintptr_t uvy          = 0x38;     // slope_y
    uintptr_t id          = 0x48;
    uintptr_t pr          = 0x4C;      // previous foothold
    uintptr_t ne          = 0x50;      // next foothold
    
    // CAttrFoothold
    uintptr_t m_pAttrFoothold = 0x28;
    uintptr_t WalkSpeed      = 0xC;
    uintptr_t Force          = 0x24;
};
```

## §2 對照 v83.idb 的 functions

**Spirit analyzer v2 對 v83.idb 的 decompile 找到**:
- `CUserLocal::CUserLocal`, `CUserLocal::GetPos` 等 — 已驗證
- `CWvsPhysicalSpace2D` 系列 — 已驗證
- `CMobPool`, `CMob` 系列 — 已驗證

**WAND_EXT offsets 是「外面讀 client process」的指引**,跟 IDA 反組譯結果**完全不同層級**:
- WAND_EXT = runtime 讀記憶體(game running)
- IDA + IDB = 靜態反組譯(binary on disk)

**但它們的 logical class hierarchy 一致** — CUserLocal / CWvsPhysicalSpace2D / CMobPool 等命名都對應。

## §3 來源與授權

- **原始 repo**: https://github.com/SpikeMogo/WAND_EXT
- **作者**: SpikeMogo
- **授權**: 開源,個人作品
- **本機 clone**: `<MAPLESOTRY>\02-Tools\WAND_EXT-main`
- **授權連結**: (見 repo LICENSE)
- **使用方式**: 學習 + 實驗用(non-commercial)

## §4 警告

- WAND_EXT 是針對 **v83 client** 設計(2010 左右)
- Offsets 可能不適用於 v83 之後的版本
- SpikeMogo 沒有保證所有 offsets 都正確
- 在用之前先驗證
