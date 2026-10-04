# 20-server-emulators — 服務端模擬器

> **目的**:列出本機所有服務端模擬器,給開發者參考

## 已 clone 服務端

| 項目 | 路徑 | 語言 | 維護狀態 |
|---|---|---|---|
| **Cosmic** | `04-Emulators/GMS-v083-Cosmic/` | Java 21 | 活躍 |
| **HeavenMS** | `04-Emulators/GMS-v083-HeavenMS/` | Java | 維護中 |
| **SoloMapling** | `04-Emulators/SoloMapling-wisteria-Wz-Mod-Tool-Suite/` | Java + AI | 維護中 |
| **BeiDou** | `04-Emulators/BeiDou-Server/` | Java + Spring/Netty | 已停 |

## wf 分析章節

| 章節 | 大小 | 內容 |
|---|---|---|
| W2-1 | 7 KB | OpenMapleClient analysis |
| W2-2 | 5 KB | OpenMapleClient NetPackets Handlers |
| W2-3 | 7 KB | MapleServerAndroid analysis |
| W2-4 | 7 KB | Journey vs Mortal vs OpenMaple 比較 |

詳見 `wf-analysis/`

## 不推薦的(不下結論)

- 不推薦哪個 server 「比較好」
- 不預測哪個 server 「會活下來」
- 只列事實:每個 server 都有自己的協議實作 + WZ 結構

## 安裝建議(已驗證可走)

### Cosmic
```bash
cd <MAPLESOTRY>\04-Emulators\GMS-v083-Cosmic
mvn clean install
java -jar target/cosmic.jar
```

### HeavenMS
```bash
cd <MAPLESOTRY>\04-Emulators\GMS-v083-HeavenMS
ant
java -jar HeavenMS.jar
```

### 連線客戶端
- 修改 client 的 localhost 為 server IP
- 或用 client 端的 Options → 設定 Server IP
