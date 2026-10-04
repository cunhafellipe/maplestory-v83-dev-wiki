# -*- coding: utf-8 -*-
"""產生 GitHub 專案書籤的單檔離線版。

資料來源:同目錄的 _repos.json(GitHub API 擷取結果 + 人工中文註解)
輸出:同目錄的 楓之谷專案書籤.html

WIKI 內嵌版由 ../../gen_github_bookmarks.py 從這個 HTML 轉換而來,
所以兩邊永遠來自同一份資料。
"""
import json, glob, io, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "_repos.json")
rows = json.load(open(P, encoding="utf-8"))
by = {r["full_name"]: r for r in rows}

# 分類: (key, 標題, 說明)
CATS = [
    ("render",  "★ 渲染層與解析度 (Gr2D / DX / HD)", "把 v83 從 1024x768 撐到高解析度而不拉伸。要『看起來像高版本』最核心的一層。"),
    ("hook",    "★ 客戶端修改 (Hook / DLL / Code Cave)", "注入 DLL、Detours 掛鉤、JMP+NOP 改寫。改 UI 座標、加功能、做插件的主力。"),
    ("trainer", "★ 外掛 / Trainer / 記憶體存取", "對遊戲進程做讀寫的框架。做插件、面板、輔助功能時的底層。"),
    ("imgmode", "★ 素材掛載 (IMG 模式 / .mod)", "不重打包 WZ,改掛載外部素材目錄。新版客戶端格式 (.mod) 的處理工具。"),
    ("client",  "★ 客戶端 (從零實作 / 開源)", "從零打造或開源的遊戲客戶端。想徹底擺脫原版限制看這區。"),
    ("wz",      "WZ / 素材檔案工具 (編輯 / 讀取)", "編輯、解析、重打包 .wz。改技能、道具、怪物、地圖素材的基礎設施。"),
    ("editor",  "編輯器與素材製作 (Editor / Animator)", "地圖編輯、GM 資料瀏覽、技能動畫製作工具。"),
    ("patch",   "補丁與客戶端分發 (Patcher)", "客戶端檔案修補、自動更新、登入器。做出成品後要分發給玩家時用這區。"),
    ("reimpl",  "重新實作 (Unity / Rust / Web / MS2)", "用其他技術堆疊重做一個楓之谷,或研究新版客戶端架構。"),
    ("packet",  "封包分析 (Packet / Sniffer)", "抓包、解析結構、發送自訂封包。要新增伺服器端不支援的功能時的入口。"),
    ("server",  "私服伺服器 (Server / Emulator)", "遊戲伺服器端。客戶端加的功能要有伺服器配合時,從這裡找基礎。"),
    ("launcher","登入器與驗證 (Launcher / Auth)", "自訂登入器、驗證伺服器、導向特定伺服器。"),
    ("misc",    "其他工具與周邊", "小工具、Bot、文件、Web 管理介面等。"),
]

# 手動指定分類 (比關鍵字可靠)
MANUAL = {
    "ronancpl/HeavenMS": "server", "aatxe/Orpheus": "server", "retep998/Vana": "server",
    "ryantpayton/Vana": "server", "Toxocious/Moonlight": "server", "Kaioru/Edelstein": "server",
    "AlanMorel/MapleServer2": "server", "sgessa/ms2ex": "server", "Bratah123/ElectronMS": "server",
    "Bratah123/Spirit": "server", "Kevin-Jin/argonms-server": "server", "aatxe/tomato": "server",
    "conan513/MoopleDEV": "server", "RamVakad/AsgardDEV": "server", "Bia10/DestinyFork": "server",
    "BiosSystem/OriginalMS": "server", "hugogrochau/VoidMS": "server", "ErwinsExpertise/ValhallaV48": "server",
    "67-6f-64/Rebirth95.Server": "server", "chenbaiyu0414/NeoMapleStory": "server", "jonnylin13/omega": "server",
    "jonnylin13/Maple83": "server", "jonnylin13/perion": "server", "ahao0150/MapleStory-Server-079-vscode": "server",
    "Mellowz/TMSCore": "server", "CCasusensa/ZZMS-for-Windows": "server", "Khuwanko/MapleCore-v1": "server",
    "CohortMinseok/v83MaplestoryCPP": "server", "koolkdev/TitanMS": "server", "Bia10/junoms": "server",
    "P0nk/Cosmic-client": "server", "themrzmaster/augurms": "server", "NoetherEmmy/intransigentms": "server",
    "izarooni/LucianMS": "server", "dngo13/SiriusMS": "server", "marcosppastor/MSV83": "server",
    "kelvinoue/KelMS83_Extension": "server", "rage123450/Edelstein-archive": "server",
    "LankMasterFlex/chronicle-emulator": "server", "TicTacTris/swordie-v232-fork": "server",
    "oxysoft/swiftbison": "server", "defaultmagi/kagami": "server", "knowlet/kagami": "server",
    "ezer1025/RustyMaple": "server", "takashato/MSAuthServer": "server",

    "ryantpayton/MapleStory-Client": "client", "YohananTzeviyah/LibreMaple-Client": "client",
    "Libre-Maple/LibreMaple-Client": "client", "HypatiaOfAlexandria/MortalClient": "client",
    "Kaioru/Blackwings": "client", "lain3d/HeavenClientNX": "client",
    "rdiol12/OpenStory": "client", "Elem8100/MapleStory-GM-Client": "client",
    "Elem8100/MapleNecrocer": "client", "SpiralMoon/maplestory.openapi": "misc",

    "444Ro666/MapleEzorsia-v2": "hook", "izarooni/MapleEzorsia": "hook",
    "Hucaru/maplestory-client-hook": "hook", "MapleMyth/ClientImageLoader": "hook",
    "moody-nl/maplestoryv83hacks": "hook", "lastbattle/maplepacket-optimizations": "hook",
    "maplestoryDwang/dwang-maplestory-053-client": "hook", "shuabritze/Agarcium": "hook",
    "Kustale/MapleStory2-Client": "hook",
    "aaaddress1/CrackShield-MapleStory-Hack": "hook", "welshe/MapleStory-V259-CRC-Bypass": "hook",
    "welshe/MapleStory-V259-P-Invoke-Bypass": "hook",
    "MapleStory-Archive/athene-noctua": "hook", "MapleStory-Archive/TerraStory": "hook",

    # ★ 渲染層
    "vdsk/gr2dpatcher": "render", "vdsk/gr2dpatcher64": "render",
    "Sheilem/maplewright": "render", "Riremito/MapleStoryWindowMode": "render",

    # ★ Trainer / 記憶體
    "jnpl95/Timelapse": "trainer", "67-6f-64/Firefly": "trainer",
    "unsafeblackcat/MapleStoryEx": "trainer",

    # ★ 素材掛載 / .mod
    "Munbin-Lee/ModPacker": "imgmode", "seokgukim/MSWConvert": "imgmode",
    "Maple-Story/xml-modifier": "imgmode",

    # ★ 補丁 / 分發
    "mechpaul/NXPatcher": "patch", "diamondo25/WvsBeta.PatchCreator": "patch",
    "noobtra/MapleStory-Auto-Patcher": "patch", "Sheilem/exodus-launcher": "patch",
    "v3921358/MapleStory072": "patch", "MapleStory-Archive/MapleClientEditTemplate": "patch",
    "oung/MapleClientEditTemplate": "patch",

    # 編輯器
    "angelsl/MSIT": "editor",
    "SpiralMoon/maplestory-ring-assets-extractor": "editor",
    "YohananTzeviyah/nx_edit": "editor",
    "qwas0514/WZKey": "wz", "yihleego/dotwz": "wz", "sqx6781268/MapleWzMeta": "wz",
    "Inumedia/NXLDownloader": "wz", "HypatiaOfAlexandria/NoLifeNx": "wz",
    "Hucaru/gonx": "wz",

    # ★ 記憶體 / 外部整合
    "zhyonc/MemorySDK": "trainer", "vinmorel/MapleWrapper": "trainer",
    "siriusdemon/WGCapturer": "trainer", "y785/script-api": "server",
    "y785/moe-miho": "misc", "zhyonc/msnet": "server",

    # 客戶端
    "HypatiaOfAlexandria/MortalMS": "client", "HypatiaOfAlexandria/MortalDocs": "client",
    "Bratah123/ElectronClient": "client",

    # 登入器
    "starmcc/qs-beanfun-5": "launcher", "topK-li/MapleGate": "launcher",
    "Tikas/TMS-little-helper": "launcher", "zhyonc/CMSLauncherLite": "launcher",

    # 輔助 / 自動化
    "aron-666/Aron.MaplestoryArtale": "misc", "ALiangLiang/artale-agent": "misc",
    "Lyze96/MANIA-Maplestory-Bot": "misc", "nemesisprime1/maplestorybot": "misc",
    "XingTongTools/XingTong-MStarBot": "misc", "pid011/kms-guild-extractor": "misc",
    "spd789562/Maplesalon": "editor", "ikasuu/grandislibrary": "misc",
    "hiddenhosts/awesome-maplestory-servers": "misc",
    "starpia-forge/maplestory-world-llms-txt": "misc", "NEXPACE-Limited/msu-skills": "misc",
    "TEAM-SPIRIT-Productions/MapleStoryJobIDs": "misc",
    "TEAM-SPIRIT-Productions/SpiritMS-Script-Spider": "misc",

    # 伺服器 / 架構參考
    "SoulGirlJP/AzureV316": "server", "BeiDouMS/BeiDou-Server": "server",
    "shoftee/OpenStory": "server", "gilmatok/Destiny": "server",
    "Bratah123/SpiritMS": "server", "unsafeblackcat/MapleStoryServer": "server",
    "unsafeblackcat/kms391": "server", "conchlin/boswell": "server",
    "zlindner/slate": "server", "fanzai0311/MapleStoryServer": "server",
    "sewil/OpenMG": "server", "andrewcell/Perry": "server",
    "fairms/MapleServer": "server", "Descended/Henesys": "server",
    "mmdevelop/MapleGlobal": "server", "Zintixx/MapleStory2-English": "server",
    "TEAM-SPIRIT-Productions/AuthHook176_RPC": "hook",
    "D363N6UY/MapleStory-tool": "hook",
    "sqx6781268/MapleWzMeta": "wz", "yihleego/dotwz": "wz",
    "vinmorel/MapleWrapper": "trainer", "Bratah123/SwordieDB": "server",
    "KOOKIIEStudios/SpiritSuite": "server", "MapleStoryUnity/awesome-maplestory": "misc",
    "neeerp/RustMS": "server",
    # 其他
    "Maple-Helper/maple-helper": "misc", "telunc/maplestory.io": "misc",
    "maplestoryDwang/gms-232": "misc", "branw/gms-v40-beta-client-mods": "misc",

    "lastbattle/Harepacker-resurrected": "wz", "Kagamia/WzComparerR2": "wz",
    "Elem8100/WzComparerR2-Plus": "wz", "flwmxd/WzTools": "wz", "Xterminatorz/WZ-Dumper": "wz",
    "toyobayashi/wz": "wz", "MapleStoryUnity/wzData": "wz", "MapleStoryUnity/UnityWzLib": "wz",
    "anydream/WzLib": "wz", "spd789562/wz-reader-rs": "wz", "zhyonc/wzlib": "wz",
    "anonymous5l/wzexplorer": "wz", "icelemon1314/HaRepacker": "wz", "angelsl/wz2nx": "wz",
    "Maple-Story/wz2nx-convertor": "wz", "a894985459/CoffeeWzRepacker": "wz",
    "PirateIzzy/WzComparerR2-Old": "wz", "tpdnd2651/WzComparerR2-KMS-": "wz",
    "lastbattle/WzImg-MCP-Server": "wz", "sirLimbs/Limbs_XML_Parser": "wz",
    "PhilippSchwab/MapleStory-node-resources": "wz", "TajuC/MapleDumper-rs": "wz",
    "lastbattle/MapleLib": "wz",

    "koolkdev/wzmapeditor": "editor", "spd789562/MapleSalon2": "editor",
    "izarooni/WzVisualizer": "editor", "Elem8100/GM-HandTool": "editor",
    "Elem8100/GM-HandToolV3": "editor", "xkiro-dev/MapleBench": "editor",
    "MapleStoryGameHack/MSEA-WZSearcher-HackTool": "editor",

    "itsadriam/Maple-Pshark-Sniffer": "packet", "zhyonc/MaplePE": "packet",
    "kOchirasu/MaplePE": "packet", "Bratah123/MaplePacketPuller": "packet",
    "KOOKIIEStudios/Spirit-PacketPuller": "packet", "KOOKIIEStudios/Spirit-PacketPuller-OLD": "packet",
    "obstriker/Maple_Pshark": "packet", "chenbaiyu0414/MapleStoryPacketAnalyzer": "packet",
    "kOchirasu/MaplePacketLib": "packet", "LankMasterFlex/MaplePacketLib": "packet",
    "taida957789/MapleSniffer": "packet", "jmartinimena/Caraota": "packet",
    "Waty/PacketSenderPlz": "packet", "JamesDonnelly/wxPloiter": "packet",
    "existence3022/wxPloiterPublicKMS": "packet", "CohortMinseok/Maplestory-Packet-Editor": "packet",
    "pelegweiss/WhitePackets": "packet", "tracker93/Packet-Utility": "packet",
    "icelemon1314/mapleSniffer": "packet", "Hazzytje/maplestory_packet_logger": "packet",
    "Bratah123/SpiritIDAPlugin": "packet",

    "zhyonc/TMSLauncher": "launcher", "zhyonc/CMSLauncher": "launcher",
    "s884812/Advanced-MapleLauncher": "launcher", "iMonkeyz/Advanced-MapleLauncher": "launcher",
    "Ezzpify/MapleLegend": "launcher",

    "flwmxd/MapleStory-Porting": "reimpl", "nmnsnv/maplestory-wasm": "reimpl",
    "MapleStoryUnity/MapleStoryUnity": "reimpl", "wuzekang/maple-rs": "reimpl",
    "aatxe/OpenMaple": "reimpl", "diamondo25/webstory": "reimpl",

    "leeqiufeng/maple-web-gui": "misc", "Descended/MaplestoryDiscBot": "misc",
    "Rudigus/HeavenBase": "misc", "defaultmagi/maplelib": "misc",
    "Bratah123/AESKeyFormatter": "misc", "TEAM-SPIRIT-Productions/Lazuli": "misc",
    "Nite-Core/maplestorybot": "misc", "erickqc2/VotingSystem": "misc",
    "mimidib/Top100VoteAutomation": "misc", "NoetherEmmy/intransigentms-tools": "misc",
}

# 中文用途註解
NOTE = {
"ronancpl/HeavenMS":"最知名的 v83 Java 伺服器開源專案,後續多數私服 (Cosmic / SiriusMS 等) 都是它的分支。看多伺服器架構先從這裡下手最有效。",
"lastbattle/Harepacker-resurrected":"HaRepacker 復刻版,目前最活躍的 WZ 編輯工具。支援匯出成 IMG 檔案系統,方便用 git diff 追蹤改動 —— 維護多份 WZ 差異時很實用。",
"Kagamia/WzComparerR2":"進階 WZ 編輯器,可跨版本比對、抽檔、轉換。資源占用高但功能最全。",
"Elem8100/MapleStory-GM-Client":"離線客戶端模擬器 (Pascal)。不上網直接跑,適合快速驗證物品 / 怪物 / 技能資料。",
"AlanMorel/MapleServer2":"楓之谷 2 的伺服器模擬器,結構現代化,適合研究新世代協定。",
"Elem8100/MapleNecrocer":"客戶端模擬器,可離線執行新版客戶端。",
"ryantpayton/MapleStory-Client":"為 HeavenMS 客製的客戶端 (C 語言實作)。",
"flwmxd/MapleStory-Porting":"Pharaoh 專案 —— 用 C++ + Lua 從零重寫整個客戶端,自帶編輯器。證明「重寫客戶端」是可行的,代價是全案重做。",
"444Ro666/MapleEzorsia-v2":"★ v83 高解析度客戶端 DLL。★ 做法是『換掉整個 DX8 渲染層』(Gr2D_DX8/DX9.dll)而非 hook,比改版本乾淨;附 localhost 導向。★ 做『v83 變高版本外觀』的第一個要看。",
"izarooni/MapleEzorsia":"修改 v83 客戶端記憶體以支援自訂解析度。用了 Microsoft Detours + code cave (JMP/NOP 填充),是 hook 技術的教科書範例。README 明確記錄:視窗置中、最小化按鈕、開場動畫跳過、聊天紀錄 64→127、LimitedView 修正。",
"MapleMyth/ClientImageLoader":"★ 可注入客戶端的 DLL,從外部目錄載入圖片素材。★ 關鍵設計:掛載 `Data` 資料夾給 `IWzFileSystem`,WZ 封存檔完全不被解析 —— 改素材不必重打包 WZ,是 Kaentake Custom.wz 模式的推廣。",
"MapleStory-Archive/MapleClientEditTemplate":"客戶端編輯框架,含繞過反作弊與 CRC 檢查的 Windows API hooks。相關技術文件提到 v083 client dll 的做法。",
"Elem8100/WzComparerR2-Plus":"WzComparerR2 繁體中文版,中文環境下比較順手。",
"nmnsnv/maplestory-wasm":"把楓之谷客戶端編成 WebAssembly,可以在瀏覽器裡玩。技術 showcase 為主。",
"Kaioru/Edelstein":"v95.1 C#/.NET 伺服器模擬器,系列作品另有客戶端 Blackwings。",
"MapleStoryUnity/MapleStoryUnity":"用 Unity 打造楓之谷 MMO 的框架,含 WZ 讀取與 UI 重建。",
"P0nk/Cosmic-client":"Cosmic 伺服器的客戶端檔案。Cosmic 是目前維護最活躍的 v83 私服分支之一。",
"aatxe/Orpheus":"v83 開源伺服器模擬器,設計較乾淨,適合研究如何重構。",
"Toxocious/Moonlight":"v214 (KMS 雲端) 私服原始碼,年代較新。",
"MapleMyth/ClientImageLoader":"可注入客戶端的 DLL,從外部載入圖片資源。改素材不必重打包 WZ 的做法。",
"retep998/Vana":"經典 C++ 楓之谷私服原始碼 (SVN 鏡像)。",
"flwmxd/WzTools":"C++ 的 WZ 讀取工具庫,各種語言實作WZ解析時的參考。",
"spd789562/MapleSalon2":"造型間預覽工具,可預覽髮型 / 臉型 / 染色 / 服飾。",
"lastbattle/MapleLib":"C# 的 WZ 解析 + 改寫 + 創建函式庫,想做程式化生成 WZ 就用這個。",
"wuzekang/maple-rs":"用 Rust 實作 v83 客戶端。",
"Xterminatorz/WZ-Dumper":"WZ 批量轉 XML 工具。",
"izarooni/MapleEzorsia":"修改 v83 客戶端記憶體以支援自訂解析度。用了 Microsoft Detours + code cave (JMP/NOP 填充),是 hook 技術的教科書範例。",
"itsadriam/Maple-Pshark-Sniffer":"PacketShark 替代品,楓之谷封包攔截與記錄。",
"toyobayashi/wz":"Node.js 與瀏覽器用的 WZ 讀取器。",
"YohananTzeviyah/LibreMaple-Client":"開源自由客戶端。",
"Elem8100/GM-HandTool":"WZ 資料庫瀏覽工具 (GM 手冊形式)。",
"Hucaru/maplestory-client-hook":"示範如何製作 hook 客戶端函式的 DLL,附說明。",
"lain3d/HeavenClientNX":"從零實作的客戶端移植到 Nintendo Switch。",
"SpiralMoon/maplestory.openapi":"楓之谷 Nexon 官方 OpenAPI 客戶端函式庫。",
"HypatiaOfAlexandria/MortalClient":"開源 (FLOSS) v83 客戶端。",
"Kevin-Jin/argonms-server":"v0.62 極早期版本的伺服器模擬器。",
"zhyonc/TMSLauncher":"台服 v113-v194 自訂登入器。",
"Bratah123/ElectronMS":"v316 KMS 伺服器,Azure316 的改進版。",
"izarooni/WzVisualizer":"C# 寫的 WZ 視覺化工具。",
"MapleStory-Archive/MapleClientEditTemplate":"客戶端編輯框架,內含繞過反作弊與 CRC 檢查所需的 Windows API hooks。開啟 Custom.wz 外掛檔案模式的參考。",
"Libre-Maple/LibreMaple-Client":"從零實作的客戶端 (JourneyClient 分支)。",
"lastbattle/WzImg-MCP-Server":"讓 AI agent 操作 WZ / IMG / PACK 檔的 MCP 伺服器。用 AI 輔助批次改 WZ 的工具鏈入口。",
"MapleStoryUnity/wzData":"楓之谷 WZ 檔案集合。",
"Bratah123/SpiritIDAPlugin":"IDA Python 外掛,輔助分析楓之谷客戶端二進位。逆向分析技能 / UI 結構時會用到。",
"PhilippSchwab/MapleStory-node-resources":"Node.js 的 WZ 抽取與伺服器。",
"themrzmaster/augurms":"v83 私服 + AI Game Master,架構在 Cosmic 上。",
"MapleStoryUnity/UnityWzLib":"Unity 版 WzLib。",
"Kaioru/Blackwings":"v95.1 客戶端。",
"zhyonc/CMSLauncher":"國服 v79-v125 自訂登入器。",
"rdiol12/OpenStory":"Cosmic 伺服器用的 v83 客戶端。",
"zhyonc/MaplePE":"封包編輯器,可解析封包結構並發送自訂封包給客戶端。",
"jonnylin13/omega":"用 TypeScript 寫的 v83 伺服器模擬器。",
"xkiro-dev/MapleBench":"視覺化 WZ 工作台,支援批次搜尋、稽核、修補、跨版本比對。",
"anydream/WzLib":"另一套 C 語言的 WZ 解析器。",
"spd789562/wz-reader-rs":"Rust 的 WZ 讀取器,執行緒安全。",
"aatxe/OpenMaple":"注重效能的伺服器模擬器。",
"diamondo25/webstory":"用 Phaser + NodeJS + WebSocket 做的網頁版客戶端。",
"Elem8100/GM-HandToolV3":"WZ 資料庫與抽取工具第三版。",
"Bratah123/MaplePacketPuller":"Python 寫的封包結構分析器,從封包流量反推結構。",
"67-6f-64/Rebirth95.Server":"v95 伺服器模擬器 (C# + Python)。",
"a894985459/CoffeeWzRepacker":"功能完整的 WZ 編輯器。",
"KOOKIIEStudios/Spirit-PacketPuller":"分析 IDA 產生的偽代碼以推導封包結構的 GUI 工具。",
"sgessa/ms2ex":"用 Elixir 寫的楓之谷 2 伺服器。",
"koolkdev/wzmapeditor":"WZ 地圖編輯器。",
"angelsl/wz2nx":"把 WZ 轉成新版 PKG4 格式的工具。",
"Waty/PacketSenderPlz":"歐服封包發送工具。",
"chenbaiyu0414/NeoMapleStory":"C# 寫的楓之谷私服。",
"oung/MapleClientEditTemplate":"客戶端編輯框架的另一個分支。",
"jonnylin13/perion":"Node.js 建構伺服器模擬器的套件集合。",
"icelemon1314/HaRepacker":"支援新版 WZ 格式的 HaRepacker。",
"Khuwanko/MapleCore-v1":"完整的 v83 私服網站方案。",
"Bratah123/Spirit":"v176 伺服器模擬器 (Python)。",
"defaultmagi/maplelib":"Go 語言的楓之谷工具集 (加密、封包等)。",
"jonnylin13/Maple83":"v83 伺服器模擬器。",
"ahao0150/MapleStory-Server-079-vscode":"v079 私服。",
"TajuC/MapleDumper-rs":"跨版本簽章與位移工具組,用來定位客戶端記憶體位置。AVX2 加速搜尋。",
"obstriker/Maple_Pshark":"MapleRoyals 封包記錄攔截器。",
"TEAM-SPIRIT-Productions/Lazuli":"與 AzureMSv316 資料庫互動的 Python 工具。",
"izarooni/LucianMS":"v83 私服。",
"Descended/MaplestoryDiscBot":"私服用的 Discord 機器人。",
"ezer1025/RustyMaple":"Rust 寫的楓之谷伺服器。",
"NoetherEmmy/intransigentms":"IntransigentMS 私服。",
"Maple-Story/wz2nx-convertor":"Windows 系統的 WZ → NX 轉換工具。",
"PirateIzzy/WzComparerR2-Old":"舊版 WzComparerR2。",
"sirLimbs/Limbs_XML_Parser":"解析 Map.wz 抽取地圖元素資訊。",
"Rudigus/HeavenBase":"顯示裝備與寶貝的相關資訊。",
"s884812/Advanced-MapleLauncher":"進階自訂登入器。",
"CCasusensa/ZZMS-for-Windows":"台灣楓之谷伺服器模擬器。",
"Bia10/DestinyFork":"以另一種設計思路實作的 C# 模擬器。",
"chenbaiyu0414/MapleStoryPacketAnalyzer":"國服 (CMS) 封包分析器。",
"hugogrochau/VoidMS":"v62 楓之谷私服。",
"leeqiufeng/maple-web-gui":"私服管理 Web 介面。",
"Bratah123/AESKeyFormatter":"把 32 個整數格式化為 Nexon AES 金鑰的小工具。",
"BiosSystem/OriginalMS":"v62 原版重現,含所有 PQ、Boss、Cygus 騎士團。",
"MapleStoryGameHack/MSEA-WZSearcher-HackTool":"WZ 搜尋器與封包工具。",
"tpdnd2651/WzComparerR2-KMS-":"韓服版 WzComparerR2。",
"kOchirasu/MaplePacketLib":"含客戶端驗證的楓之谷封包函式庫。",
"lastbattle/maplepacket-optimizations":"以基準測試驅動的封包加解密與 I/O 最佳化。",
"ryantpayton/Vana":"Vana 基礎的改進版。",
"ErwinsExpertise/ValhallaV48":"v48 模擬器 (Go)。",
"takashato/MSAuthServer":"NodeJS 實作的私服驗證伺服器。",
"conan513/MoopleDEV":"Java 楓之谷伺服器模擬器。",
"aatxe/tomato":"v111 Java 伺服器模擬器。",
"zhyonc/wzlib":"Go 語言的 WZ 解析套件。",
"taida957789/MapleSniffer":"Vue 寫的封包擷取工具。",
"iMonkeyz/Advanced-MapleLauncher":"進階自訂登入器 (另一分支)。",
"dngo13/SiriusMS":"HeavenMS 分支。",
"mimidib/Top100VoteAutomation":"自動投票腳本。",
"kelvinoue/KelMS83_Extension":"HeavenMS 擴充套件包。",
"marcosppastor/MSV83":"v83 Java 伺服器模擬器。",
"RamVakad/AsgardDEV":"C# 楓之谷伺服器模擬器。",
"anonymous5l/wzexplorer":"解壓 WZ 檔案。",
"Hazzytje/maplestory_packet_logger":"記錄楓之谷封包。",
"KOOKIIEStudios/Spirit-PacketPuller-OLD":"MaplePacketPuller 的舊版 GUI 實作。",
"CohortMinseok/v83MaplestoryCPP":"可運作的 v83 私服 (C++)。",
"koolkdev/TitanMS":"TitanMS 存檔 (C++)。",
"TicTacTris/swordie-v232-fork":"v232.2 私服,含自訂倍率與 GUI 登入器。",
"NoetherEmmy/intransigentms-tools":"IntransigentMS 輔助腳本。",
"moody-nl/maplestoryv83hacks":"v83 私服相關的 hack / 修改。",
"Ezzpify/MapleLegend":"楓之谷客戶端內嵌工具。",
"Nite-Core/maplestorybot":"進階楓之谷機器人。",
"erickqc2/VotingSystem":"私服投票系統 (PHP)。",
"defaultmagi/kagami":"Go 語言伺服器模擬器嘗試。",
"knowlet/kagami":"Go 語言伺服器模擬器嘗試。",
"Bia10/junoms":"不到 3 萬行的 C 語言 v62 模擬器。",
"oxysoft/swiftbison":"楓之谷伺服器模擬器。",
"rage123450/Edelstein-archive":"v95 伺服器模擬器存檔。",
"LankMasterFlex/MaplePacketLib":"楓之谷網路函式庫。",
"jmartinimena/Caraota":"v62 封包攔截與記錄器。",
"LankMasterFlex/chronicle-emulator":"gMS v75 伺服器模擬器。",
"Mellowz/TMSCore":"泰國楓之谷伺服器模擬器。",
"kOchirasu/MaplePE":"楓之谷封包編輯器。",
"JamesDonnelly/wxPloiter":"開源輕量多行封包編輯器,支援收發攔截與注入。",
"existence3022/wxPloiterPublicKMS":"韓服版 wxPloiter,可自動更新。",
"icelemon1314/mapleSniffer":"封包擷取。",
"CohortMinseok/Maplestory-Packet-Editor":"楓之谷封包編輯器。",
"pelegweiss/WhitePackets":"v83 封包編輯器。",
"tracker93/Packet-Utility":"封包讀寫工具。",
}

def note(r):
    n = r.get("note")
    if n: return n
    fn = r["full_name"]
    if fn in NOTE: return NOTE[fn]
    return r["desc"] or "（無專案說明）"

def pick_cat(r):
    fn = r["full_name"]
    if fn in MANUAL: return MANUAL[fn]
    s = (fn + " " + r["desc"]).lower()
    if re.search(r"wz|harepacker|wzcompare", s): return "wz"
    if re.search(r"packet|sniffer|pl(o|a)iter|wshook", s): return "packet"
    if re.search(r"server|emulator|privateserver|auth", s): return "server"
    if re.search(r"hook|inject|detour|edit", s): return "hook"
    if re.search(r"editor|visual|mapedit|gm-hand", s): return "editor"
    if re.search(r"launcher", s): return "launcher"
    if re.search(r"client", s): return "client"
    return "misc"

# 語言顯示
LANG_LABEL = {"C#":"C#","C++":"C++","Java":"Java","Python":"Python","JavaScript":"JavaScript",
              "TypeScript":"TypeScript","Go":"Go","C":"C","Rust":"Rust","Pascal":"Pascal",
              "Lua":"Lua","HTML":"HTML","CoffeeScript":"CoffeeScript","Dart":"Dart","Elixir":"Elixir",
              "Vue":"Vue","PHP":"PHP","Batchfile":"Batch",None:"—"}

groups = {}
for r in rows:
    groups.setdefault(pick_cat(r), []).append(r)
for k in groups: groups[k].sort(key=lambda r: -r["stars"])

def esc(s):
    return (s or "").replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

total = len(rows)
counts = {k: len(v) for k, v in groups.items()}

# ---- HTML ----
h = []
h.append("""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>楓之谷 GitHub 專案書籤</title>
<style>
:root{--bg:#0f1115;--panel:#161a22;--panel2:#1b2029;--line:#262d3a;--fg:#e6e9ef;--dim:#8b95a7;--acc:#5aa9ff;--acc2:#7ee0a8}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.6 "Segoe UI","Microsoft JhengHei",system-ui,sans-serif}
a{color:var(--acc);text-decoration:none}
a:hover{text-decoration:underline}
header{position:sticky;top:0;z-index:10;background:rgba(15,17,21,.95);backdrop-filter:blur(8px);border-bottom:1px solid var(--line);padding:14px 20px}
h1{margin:0 0 10px;font-size:19px;letter-spacing:.5px}
.sub{color:var(--dim);font-size:13px;margin-bottom:10px}
.bar{display:flex;gap:10px;flex-wrap:wrap;align-items:center}
input[type=search]{flex:1;min-width:220px;background:var(--panel2);border:1px solid var(--line);color:var(--fg);border-radius:8px;padding:9px 12px;font-size:14px;outline:none}
input[type=search]:focus{border-color:var(--acc)}
select{background:var(--panel2);border:1px solid var(--line);color:var(--fg);border-radius:8px;padding:9px 10px;font-size:14px;outline:none}
.count{color:var(--dim);font-size:13px;white-space:nowrap}
.wikilink{background:var(--panel2);border:1px solid var(--line);border-left:3px solid var(--acc2);
  border-radius:8px;padding:9px 12px;font-size:13px;color:#c3cddc;margin-bottom:11px;line-height:1.7}
.wikilink code{background:#0d1016;border:1px solid var(--line);border-radius:4px;padding:1px 6px;
  color:var(--acc2);font-size:12px}
.wikilink b{color:var(--fg)}
nav{display:flex;gap:7px;flex-wrap:wrap;margin-top:10px}
nav button{background:var(--panel2);border:1px solid var(--line);color:var(--dim);border-radius:999px;padding:5px 13px;font-size:13px;cursor:pointer;transition:.12s}
nav button:hover{color:var(--fg);border-color:var(--acc)}
nav button.on{background:var(--acc);border-color:var(--acc);color:#07101c;font-weight:600}
main{padding:22px 20px 60px;max-width:1500px;margin:0 auto}
section{margin-bottom:34px;scroll-margin-top:150px}
h2{font-size:17px;margin:0 0 4px;display:flex;align-items:baseline;gap:9px}
h2 .n{color:var(--acc);font-size:13px;font-weight:600}
.hint{color:var(--dim);font-size:13px;margin:0 0 12px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:10px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:12px 14px;transition:.12s}
.card:hover{border-color:var(--acc);transform:translateY(-1px)}
.top{display:flex;justify-content:space-between;align-items:flex-start;gap:10px}
.repo{font-weight:600;font-size:14.5px;word-break:break-all}
.repo:hover{color:var(--acc2)}
.tags{display:flex;gap:5px;flex-shrink:0}
.tag{font-size:11px;background:var(--panel2);border:1px solid var(--line);color:var(--dim);border-radius:5px;padding:1px 7px;white-space:nowrap}
.tag.st{color:#ffd479;border-color:#4a3d22}
.tag.ver{color:#c792ea;border-color:#3d2f52}
.tag.live{color:#7ee0a8;border-color:#26452f}
.tag.slow{color:#e0c07e;border-color:#4d402a}
.tag.dead{color:#7a8496;border-color:#333a47;text-decoration:line-through}
.tag.arch{color:#e08a8a;border-color:#4d2f2f}
.tags{flex-wrap:wrap;justify-content:flex-end;max-width:120px}
.desc{color:var(--dim);font-size:12.5px;margin-top:6px}
.cn{font-size:13px;margin-top:8px;padding-left:10px;border-left:2px solid var(--acc);color:#cdd6e4}
.empty{color:var(--dim);padding:50px;text-align:center}
footer{color:var(--dim);font-size:12.5px;text-align:center;padding:26px 20px;border-top:1px solid var(--line)}
</style>
</head>
<body>
<header>
<h1>楓之谷 GitHub 專案書籤</h1>
<div class="sub">共 %d 個專案 · 依功能分類 · 資料擷取自 GitHub API · %s</div>
<div class="wikilink">
  🔗 本頁是 <b>GitHub 專案索引</b>(廣度)。深度分析請見 WIKI:
  <code>wiki/docs/</code> — 內含 v83 客戶端 IDA 位址、UI 類別結構、封包協議、CUIWnd / CUIToolTip 反編譯。
  <br>WIKI 網站(<code>mkdocs serve</code>)的「原始資料 → GitHub 專案書籤」頁亦收錄本頁的可篩選版本。
  <br>機器可讀的事實索引:<code>wiki/docs/facts.json</code>
</div>
<div class="bar">
  <input type="search" id="q" placeholder="搜尋專案名稱、用途說明、版本…（例如 v83 / wz / 解析度）">
  <select id="lang"><option value="">所有語言</option>%s</select>
  <select id="ver"><option value="">所有版本</option>%s</select>
  <select id="age"><option value="">所有狀態</option><option value="活躍">活躍 (1年內)</option><option value="維護中">維護中 (2年內)</option><option value="靜止">靜止 (較久未動)</option><option value="已封存">已封存</option></select>
  <span class="count" id="cnt"></span>
</div>
<nav id="nav"></nav>
</header>
<main id="main"></main>
<footer>標註為整理用途,實際功能請以各專案 README 為準。更新方式:重新執行 _gen.py。</footer>
<script>
const DATA = %s;
let cat = "";
const qEl = document.getElementById('q');
const langEl = document.getElementById('lang');
const verEl = document.getElementById('ver');
const ageEl = document.getElementById('age');
const main = document.getElementById('main');
const nav = document.getElementById('nav');
const cnt = document.getElementById('cnt');

function esc(s){return (s||'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}

function buildNav(){
  nav.innerHTML = '<button class="'+(cat===''?'on':'')+'" data-c="">全部</button>' +
    DATA.map(c=>'<button class="'+(cat===c.key?'on':'')+'" data-c="'+c.key+'">'+esc(c.title)+' ('+c.items.length+')</button>').join('');
  nav.querySelectorAll('button').forEach(b=>b.onclick=()=>{cat=b.dataset.c;buildNav();render();window.scrollTo({top:0});});
}

function render(){
  const q = qEl.value.trim().toLowerCase();
  const lg = langEl.value;
  const vv = verEl.value;
  const ag = ageEl.value;
  let shown = 0;
  let html = '';
  for(const c of DATA){
    if(cat && c.key !== cat) continue;
    let items = c.items.filter(it=>{
      if(lg && it.lang !== lg) return false;
      if(vv && it.ver !== vv) return false;
      if(ag && it.age !== ag) return false;
      if(!q) return true;
      return (it.full_name+' '+it.desc+' '+it.note+' '+(it.lang||'')+' '+(it.ver||'')).toLowerCase().includes(q);
    });
    if(!items.length) continue;
    shown += items.length;
    html += '<section><h2>'+esc(c.title)+' <span class="n">'+items.length+' 個</span></h2>'
         + '<p class="hint">'+esc(c.hint)+'</p><div class="grid">'
         + items.map(it=>{
             let t = '';
             if (it.stars) t += '<span class="tag st">★ '+it.stars+'</span>';
             if (it.ver)  t += '<span class="tag ver">'+esc(it.ver)+'</span>';
             if (it.lang) t += '<span class="tag">'+esc(it.lang)+'</span>';
             if (it.age) {
               const cls = it.age==='活躍'?'live':(it.age==='維護中'?'slow':(it.age==='已封存'?'arch':'dead'));
               t += '<span class="tag '+cls+'">'+esc(it.age)+'</span>';
             }
             return '<div class="card"><div class="top">'
               + '<a class="repo" href="'+esc(it.url)+'" target="_blank" rel="noopener">'+esc(it.full_name)+'</a>'
               + '<span class="tags">'+t+'</span></div>'
               + (it.desc?'<div class="desc">'+esc(it.desc)+'</div>':'')
               + '<div class="cn">'+esc(it.note)+'</div></div>';
           }).join('')
         + '</div></section>';
  }
  if(!shown) html = '<div class="empty">找不到符合的專案</div>';
  main.innerHTML = html;
  cnt.textContent = shown + ' / ' + DATA.reduce((a,c)=>a+c.items.length,0) + ' 個專案';
}
qEl.addEventListener('input', render);
langEl.addEventListener('change', render);
verEl.addEventListener('change', render);
ageEl.addEventListener('change', render);
buildNav(); render();
</script>
</body>
</html>""" % (total, "2026-10-04",
    "".join('<option value="%s">%s</option>' % (LANG_LABEL.get(l,l), LANG_LABEL.get(l,l)) for l in sorted([l for l in set(LANG_LABEL.get(x["lang"],x["lang"]) for x in rows) if l])),
    "__VER_OPTS__", "[]"))

for c in CATS:
    key, title, hint = c
    items = groups.get(key, [])
    h.append(json.dumps({
        "key": key, "title": title, "hint": hint,
        "items": [{
            "full_name": r["full_name"], "url": r["url"], "stars": r["stars"],
            "lang": LANG_LABEL.get(r["lang"], r["lang"]) or "",
            "ver": r.get("_ver") or "", "age": r.get("_age") or "",
            "archived": bool(r.get("archived")),
            "desc": r["desc"], "note": note(r),
        } for r in items]
    }, ensure_ascii=False))

html = h[0].replace("[]", "[" + ",\n".join(h[1:]) + "]")

# 版本下拉選單(依出現次數排序,只列出現 >=2 次的,避免雜訊)
from collections import Counter as _C
_vc = _C(r.get("_ver") for r in rows if r.get("_ver"))
_vers = [v for v, c in _vc.most_common() if c >= 2]
_vopts = "".join('<option value="%s">%s</option>' % (esc(v), esc(v)) for v in _vers)
html = html.replace("__VER_OPTS__", _vopts)

out = os.path.join(os.path.dirname(P), "楓之谷專案書籤.html")
io.open(out, "w", encoding="utf-8").write(html)
print("written:", out, os.path.getsize(out), "bytes")
print("counts:", counts)
print("版本下拉項:", len(_vers))
