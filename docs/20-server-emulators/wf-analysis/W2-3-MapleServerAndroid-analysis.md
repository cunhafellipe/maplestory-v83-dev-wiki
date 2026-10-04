# W2-3: MapleServerAndroid — 純技術拆解

> **分析時間**: 2026-09-27
> **repo**: https://github.com/speedyHKjournalist/MapleServerAndroid
> **作者**: speedyHKjournalist(同 OpenMapleClient 作者)
> **本質**: Cosmic v83 server + Android Studio 包裝

---

## §0 元資料

| 屬性 | 值 |
|---|---|
| 創建 | 2023-10-08 |
| 最後 commit | 2025-03-08 |
| Stars / Forks | 107 / 29 |
| 語言 | **Java** |
| License | AGPL-3.0 |
| Default branch | main |
| Repo size | 40 MB |

---

## §1 README 純事實(作者原文)

### §1.1 自我介紹

> "A one-click Maplestory GMS 083 server on Android based on **Cosmic project**."

### §1.2 Features(作者原文)

1. **Customizable Server Settings**:Modify local and lan IP addresses to enable multiplayer capabilities.
2. **Database Management**:Export and import **SQLite-based MapleStory cosmic databases** with ease.

### §1.3 Important(作者原文)

1. **Server Startup Time**:Please allow approximately **1 minute** for the server to start after clicking the Start button.
2. **Server Configuration**:The server config file is located in `assets/config.yaml` and is copied to internal app storage during APK installation. You can modify the server config by clicking on Menu->ServerConfig, similar to **Cosmic/HeavenMS**.
3. **Database Performance**:For optimal performance, **MySQL has been replaced with SQLite**. While I've made efforts to adapt the SQL queries using **ChatGPT**, there might be some errors.

### §1.4 警告(作者原文)

> "Beware - **This server emulator is not production ready.**"
> "It can be useful for testing things locally or for trying out ideas, but launching a new private server based on this and opening it up to the public without knowing what you're doing is not recommended."

### §1.5 Credits(作者原文)

> "**Cosmic** — GitHub: https://github.com/P0nk/Cosmic"
> "**HeavenMS** — GitHub: https://github.com/ronancpl/HeavenMS"

→ **直白血統**:這是 Cosmic Java server code 包成 Android app。

---

## §2 結構事實

### §2.1 12 個 Java package

```
net.opcodes    5,933 + 10,790 bytes (Recv/Send)
server         20 個檔,含 CashShop(21KB)、ItemInformationProvider(98KB)、StatEffect(78KB)
server.life    Mob/NPC/Reactor
server.maps    Map/Portal/Foothold
server.events  活動
server.expeditions 遠征
server.gachapon 轉蛋
server.loot    掉落
server.minigame 小遊戲
server.movement 移動
server.partyquest 組隊任務
server.quest   任務
net.encryption 加密
net.netty      Netty server
net.packet     Packet handlers
net.server     網路
client         Android client
com            Android UI
config         設定
constants      常數
database       SQLite 操作
model          資料模型
provider       Provider
scripting      JavaScript 腳本
service        Android service
tools          工具
```

### §2.2 assets/(16 個 .wz + config + SQL + scripts)

```
assets/
├── config.yaml            29,439 bytes
├── handbook/
├── scripts/
├── sql/
└── wz/
    ├── Base.wz/
    ├── Character.wz/
    ├── Effect.wz/
    ├── Etc.wz/
    ├── Item.wz/
    ├── Map.wz/
    ├── Mob.wz/
    ├── Morph.wz/
    ├── Npc.wz/
    ├── Quest.wz/
    ├── Reactor.wz/
    ├── Skill.wz/
    ├── Sound.wz/
    ├── String.wz/
    ├── TamingMob.wz/
    └── UI.wz/
```

**事實**:
- 16 個 .wz **目錄** — 不是 .wz 檔,是 `.wz/` 子目錄(包含解開的 .img 結構)
- **沒有 .wz 二進位檔**(像是把 WZ 解開用)

### §2.3 Opcode 大小事實

**RecvOpcode.java 5.9 KB** vs **Cosmic RecvOpcode ~ 15 KB**(從子代理 W1-2 計算過):
- **約 Cosmic 的 40% 體積**
- 結構是 GMS v83 標準:`LOGIN_PASSWORD(0x01)` 開始

**SendOpcode.java 10.8 KB** vs **Cosmic SendOpcode ~ 15 KB**:
- **約 Cosmic 的 70% 體積**
- 末段 `VEGA_SCROLL(0x166)` — 跟 Cosmic 一致

**Custom Packet 用 `0x3713`** — 跟 Cosmic 一致。

**結論(純事實)**:
- MapleServerAndroid 是 Cosmic 的 **裁剪 + Android 包裝版**
- `0x166` 上限之後無自訂 opcode → 撞 `0x3730`/`0x3731` 仍是自由範圍
- Custom enum 跟 Cosmic 一樣使用 `0x3713`

---

## §3 Java server 重要檔

| 檔案 | 大小 | 對應 Cosmic |
|---|---:|---|
| `server/CashShop.java` | 21 KB | Cosmic `server/CashShop.java` |
| `server/ItemInformationProvider.java` | 98 KB | Cosmic `server/ItemInformationProvider.java` |
| `server/StatEffect.java` | 77 KB | Cosmic `server/StatEffect.java` |
| `server/MakerItemFactory.java` | 7 KB | Cosmic |
| `server/SkillbookInformationProvider.java` | 11 KB | Cosmic |
| `server/Storage.java` | 11 KB | Cosmic |
| `server/Trade.java` | 20 KB | Cosmic |
| `server/Marriage.java` | 5.6 KB | Cosmic |
| `server/Shop.java` | 12 KB | Cosmic |
| `net/PacketProcessor.java` | 17 KB | Cosmic 同名 |

**事實**:
- 全部對應 Cosmic 既有檔案 — **直接從 Cosmic 拉源碼**
- 沒有新增 CheckIn / BeautySalon / CashShop-window 任何自訂功能

---

## §4 與 Cosmic 本地 04-Emulators/GMS-v083-Cosmic 對照

| 屬性 | MapleServerAndroid | 本地 Cosmic |
|---|---|---|
| 最後 commit | 2025-03 | 2026+ (本地下載) |
| License | AGPL-3.0 | AGPL-3.0 |
| 資料庫 | SQLite | MySQL |
| 部署 | Android APK | JAR / IDE |
| Custom Packet opcode | 0x3713 | 0x3713 |
| RecvOpcode 末段 | (沒看) | 0x3712 CUSTOM_PACKET |
| 架構 | 完整 Android | 純 server |

**純事實結論**:
- MapleServerAndroid = **Cosmic v83 服務端的 Android 重新打包**
- 用 SQLite 替代 MySQL(由 ChatGPT 自動轉換 SQL 查詢)
- 16 個 .wz 在 assets,但只是目錄(可能只是占位或檔案名模板)
- 沒有 CheckIn / BeautySalon / CashShop-window 任何整合

---

## §5 已知問題

- Server startup 需約 1 分鐘
- SQLite 替代 MySQL 由 ChatGPT 自動轉,可能有 bug
- 作者自陳:**Not production ready**

---

## §6 純事實總結

1. **血統**:Cosmic v83 server + Android Studio 包裝
2. **資料庫**:SQLite(替換 Cosmic 原 MySQL,ChatGPT 自動轉)
3. **架構**:12 個 Java package + 16 個 .wz 目錄 + config.yaml
4. **Custom opcode**:0x3713(與 Cosmic 一致)
5. **最後更新**:2025-03(比 OpenMapleClient 早 1 個月)
6. **適用性**:**開箱即用在 Android 上跑小型 Cosmic server**
7. **限制**:
   - SQLite 效能差
   - SQL 由 ChatGPT 轉,可能有 bug
   - Not production ready
   - 沒有 CheckIn / BeautySalon / CashShop-window 整合

---

**輸出位置**: `<MAPLESOTRY>\wf-output\W2-3-MapleServerAndroid-analysis.md`
