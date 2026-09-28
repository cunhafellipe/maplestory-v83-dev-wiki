# W1-2 — Opcode Collision Analysis

**Date:** 2026-09-27  
**Scope:** Pure technical extraction. No conclusions, no recommendations.  
**Sources scanned:**
- CheckIn: `C:\MUWORK\GAME\MAPLESOTRY\待分類\簽到表\`
- BeautySalon: `C:\Users\e7896\AppData\Local\Temp\peek1\BeautySalonv83\`
- CashShop: `C:\Users\e7896\AppData\Local\Temp\peek_cash\cashshop-window\`
- Cosmic opcodes: `C:\MUWORK\GAME\MAPLESOTRY\04-Emulators\GMS-v083-Cosmic\src\main\java\net\opcodes\`

---

## 1. Opcodes claimed by each feature package

Extracted from each package's README/INTEGRATION docs and `.java` / `.cpp` / `.h` source.

### CheckIn (Daily Check-In)
| Direction | Enum constant | Hex | Dec | Source citation |
|---|---|---|---|---|
| Recv (client → server) | `RecvOpcode.DAILY_CHECKIN` | `0x11A` | 282 | `README.md:53,94` |
| Send (server → client) | `SendOpcode.DAILY_CHECKIN` | `0x17C` | 380 | `README.md:60,99` |

README warns (`README.md:77`): "0x11A and 0x17C must be **free** in your `RecvOpcode`/`SendOpcode`."

### BeautySalon
| Direction | Enum constant | Hex | Dec | Source citation |
|---|---|---|---|---|
| Recv | `RecvOpcode.BEAUTY_ACTION` | `0x174` | 372 | `FILE_LIST.md:47`; `README.md:76`; `java/README.md:24` |
| Send | `SendOpcode.BEAUTY_RESULT` | `0x174` | 372 | `FILE_LIST.md:48`; `README.md:77`; `java/README.md:29` |

Same opcode `0x174` used in **both** directions (one enum constant per direction, same numeric value).

README warns (`README.md:83`, `java/README.md:32`): "0x174 must be **unused** in both enums."

### CashShop
| Direction | Enum constant | Hex | Dec | Source citation |
|---|---|---|---|---|
| Recv (client → server) | `RecvOpcode.CASHSHOP_WINDOW_ACTION` | `0x3730` | 14128 | `INTEGRATION.md:61`; `client/cashshopwnd.h:20` (`kCashShopActionOpcode`) |
| Send (server → client) | `SendOpcode.CASHSHOP_WINDOW_SYNC` | `0x3731` | 14129 | `INTEGRATION.md:67`; `client/cashshopwnd.h:21` (`kCashShopSyncOpcode`) |

INTEGRATION.md:78 warns: "Pick a different pair if `0x3730`/`0x3731` collide with something of yours — but change `cashshopwnd.h` to match, since nothing enforces that the two sides agree."

**Reference only (NOT a claim):** `CashShopWindowHandler.java:18` mentions `CashOperationHandler (0xE5)` in a Javadoc to explain why that handler is *deliberately not used*. `0xE5` is **not** claimed by CashShop.

---

## 2. Cross-feature collision matrix (between the three packages)

| Hex | CheckIn | BeautySalon | CashShop | Conflict? |
|---|---|---|---|---|
| `0x11A` | Recv.DAILY_CHECKIN | — | — | n/a (single claim) |
| `0x17C` | Send.DAILY_CHECKIN | — | — | n/a (single claim) |
| `0x174` | — | Recv.BEAUTY_ACTION **and** Send.BEAUTY_RESULT | — | n/a (same package, both directions) |
| `0x3730` | — | — | Recv.CASHSHOP_WINDOW_ACTION | n/a (single claim) |
| `0x3731` | — | — | Send.CASHSHOP_WINDOW_SYNC | n/a (single claim) |

**Result: No collisions among the three packages.** All claimed hex values are pairwise distinct.

---

## 3. Cosmic existing opcodes (full enum tables)

Pulled from `RecvOpcode.java` (216 lines) and `SendOpcode.java` (366 lines) in `C:\MUWORK\GAME\MAPLESOTRY\04-Emulators\GMS-v083-Cosmic\src\main\java\net\opcodes\`.

### 3.1 RecvOpcode — values already declared

| Hex | Dec | Constant |
|---|---|---|
| 0x10 | 16 | NAME_TRANSFER |
| 0x12 | 18 | WORLD_TRANSFER |
| 0x13 | 19 | CHAR_SELECT |
| 0x14 | 20 | PLAYER_LOGGEDIN |
| 0x15 | 21 | CHECK_CHAR_NAME |
| 0x16 | 22 | CREATE_CHAR |
| 0x17 | 23 | DELETE_CHAR |
| 0x18 | 24 | PONG |
| 0x19 | 25 | CLIENT_START_ERROR |
| 0x1A | 26 | CLIENT_ERROR |
| 0x1B | 27 | STRANGE_DATA |
| 0x1C | 28 | RELOG |
| 0x1D | 29 | REGISTER_PIC |
| 0x1E | 30 | CHAR_SELECT_WITH_PIC |
| 0x1F | 31 | VIEW_ALL_PIC_REGISTER |
| 0x20 | 32 | VIEW_ALL_WITH_PIC |
| 0x26 | 38 | CHANGE_MAP |
| 0x27 | 39 | CHANGE_CHANNEL |
| 0x28 | 40 | ENTER_CASHSHOP |
| 0x29 | 41 | MOVE_PLAYER |
| 0x2A | 42 | CANCEL_CHAIR |
| 0x2B | 43 | USE_CHAIR |
| 0x2C | 44 | CLOSE_RANGE_ATTACK |
| 0x2D | 45 | RANGED_ATTACK |
| 0x2E | 46 | MAGIC_ATTACK |
| 0x2F | 47 | TOUCH_MONSTER_ATTACK |
| 0x30 | 48 | TAKE_DAMAGE |
| 0x31 | 49 | GENERAL_CHAT |
| 0x32 | 50 | CLOSE_CHALKBOARD |
| 0x33 | 51 | FACE_EXPRESSION |
| 0x34 | 52 | USE_ITEMEFFECT |
| 0x35 | 53 | USE_DEATHITEM |
| 0x38 | 56 | MOB_BANISH_PLAYER |
| 0x39 | 57 | MONSTER_BOOK_COVER |
| 0x3A | 58 | NPC_TALK |
| 0x3B | 59 | REMOTE_STORE |
| 0x3C | 60 | NPC_TALK_MORE |
| 0x3D | 61 | NPC_SHOP |
| 0x3E | 62 | STORAGE |
| 0x3F | 63 | HIRED_MERCHANT_REQUEST |
| 0x40 | 64 | FREDRICK_ACTION |
| 0x41 | 65 | DUEY_ACTION |
| 0x42 | 66 | OWL_ACTION |
| 0x43 | 67 | OWL_WARP |
| 0x44 | 68 | ADMIN_SHOP |
| 0x45 | 69 | ITEM_SORT |
| 0x46 | 70 | ITEM_SORT2 |
| 0x47 | 71 | ITEM_MOVE |
| 0x48 | 72 | USE_ITEM |
| 0x49 | 73 | CANCEL_ITEM_EFFECT |
| 0x4B | 75 | USE_SUMMON_BAG |
| 0x4C | 76 | PET_FOOD |
| 0x4D | 77 | USE_MOUNT_FOOD |
| 0x4E | 78 | SCRIPTED_ITEM |
| 0x4F | 79 | USE_CASH_ITEM |
| 0x50 | 80 | *(commented — `//USE_OWL_ITEM(0x50), ... no idea`)* |
| 0x51 | 81 | USE_CATCH_ITEM |
| 0x52 | 82 | USE_SKILL_BOOK |
| 0x54 | 84 | USE_TELEPORT_ROCK |
| 0x55 | 85 | USE_RETURN_SCROLL |
| 0x56 | 86 | USE_UPGRADE_SCROLL |
| 0x57 | 87 | DISTRIBUTE_AP |
| 0x58 | 88 | AUTO_DISTRIBUTE_AP |
| 0x59 | 89 | HEAL_OVER_TIME |
| 0x5A | 90 | DISTRIBUTE_SP |
| 0x5B | 91 | SPECIAL_MOVE |
| 0x5C | 92 | CANCEL_BUFF |
| 0x5D | 93 | SKILL_EFFECT |
| 0x5E | 94 | MESO_DROP |
| 0x5F | 95 | GIVE_FAME |
| 0x61 | 97 | CHAR_INFO_REQUEST |
| 0x62 | 98 | SPAWN_PET |
| 0x63 | 99 | CANCEL_DEBUFF |
| 0x64 | 100 | CHANGE_MAP_SPECIAL |
| 0x65 | 101 | USE_INNER_PORTAL |
| 0x66 | 102 | TROCK_ADD_MAP |
| 0x6A | 106 | REPORT |
| 0x6B | 107 | QUEST_ACTION |
| 0x6D | 109 | GRENADE_EFFECT |
| 0x6E | 110 | SKILL_MACRO |
| 0x70 | 112 | USE_ITEM_REWARD |
| 0x71 | 113 | MAKER_SKILL |
| 0x74 | 116 | USE_REMOTE |
| 0x75 | 117 | WATER_OF_LIFE |
| 0x76 | 118 | ADMIN_CHAT |
| 0x77 | 119 | MULTI_CHAT |
| 0x78 | 120 | WHISPER |
| 0x79 | 121 | SPOUSE_CHAT |
| 0x7A | 122 | MESSENGER |
| 0x7B | 123 | PLAYER_INTERACTION |
| 0x7C | 124 | PARTY_OPERATION |
| 0x7D | 125 | DENY_PARTY_REQUEST |
| 0x7E | 126 | GUILD_OPERATION |
| 0x7F | 127 | DENY_GUILD_REQUEST |
| 0x80 | 128 | ADMIN_COMMAND |
| 0x81 | 129 | ADMIN_LOG |
| 0x82 | 130 | BUDDYLIST_MODIFY |
| 0x83 | 131 | NOTE_ACTION |
| 0x85 | 133 | USE_DOOR |
| 0x87 | 135 | CHANGE_KEYMAP |
| 0x88 | 136 | RPS_ACTION |
| 0x89 | 137 | RING_ACTION |
| 0x8A | 138 | WEDDING_ACTION |
| 0x8B | 139 | WEDDING_TALK *(+ WEDDING_TALK_MORE — same value, two names)* |
| 0x8F | 143 | ALLIANCE_OPERATION |
| 0x90 | 144 | DENY_ALLIANCE_REQUEST |
| 0x91 | 145 | OPEN_FAMILY_PEDIGREE |
| 0x92 | 146 | OPEN_FAMILY |
| 0x93 | 147 | ADD_FAMILY |
| 0x94 | 148 | SEPARATE_FAMILY_BY_SENIOR |
| 0x95 | 149 | SEPARATE_FAMILY_BY_JUNIOR |
| 0x96 | 150 | ACCEPT_FAMILY |
| 0x97 | 151 | USE_FAMILY |
| 0x98 | 152 | CHANGE_FAMILY_MESSAGE |
| 0x99 | 153 | FAMILY_SUMMON_RESPONSE |
| 0x9B | 155 | BBS_OPERATION |
| 0x9C | 156 | ENTER_MTS |
| 0x9D | 157 | USE_SOLOMON_ITEM |
| 0x9E | 158 | USE_GACHA_EXP |
| 0x9F | 159 | NEW_YEAR_CARD_REQUEST |
| 0xA1 | 161 | CASHSHOP_SURPRISE |
| 0xA2 | 162 | CLICK_GUIDE |
| 0xA3 | 163 | ARAN_COMBO_COUNTER |
| 0xA7 | 167 | MOVE_PET |
| 0xA8 | 168 | PET_CHAT |
| 0xA9 | 169 | PET_COMMAND |
| 0xAA | 170 | PET_LOOT |
| 0xAB | 171 | PET_AUTO_POT |
| 0xAC | 172 | PET_EXCLUDE_ITEMS |
| 0xAF | 175 | MOVE_SUMMON |
| 0xB0 | 176 | SUMMON_ATTACK |
| 0xB1 | 177 | DAMAGE_SUMMON |
| 0xB2 | 178 | BEHOLDER |
| 0xB5 | 181 | MOVE_DRAGON |
| 0xB7 | 183 | CHANGE_QUICKSLOT |
| 0xBC | 188 | MOVE_LIFE |
| 0xBD | 189 | AUTO_AGGRO |
| 0xBF | 191 | FIELD_DAMAGE_MOB |
| 0xC0 | 192 | MOB_DAMAGE_MOB_FRIENDLY |
| 0xC1 | 193 | MONSTER_BOMB |
| 0xC2 | 194 | MOB_DAMAGE_MOB |
| 0xC5 | 197 | NPC_ACTION |
| 0xCA | 202 | ITEM_PICKUP |
| 0xCD | 205 | DAMAGE_REACTOR |
| 0xCE | 206 | TOUCHING_REACTOR |
| 0xCF | 207 | PLAYER_MAP_TRANSFER |
| 0xD3 | 211 | SNOWBALL |
| 0xD4 | 212 | LEFT_KNOCKBACK |
| 0xD5 | 213 | COCONUT |
| 0xD6 | 214 | MATCH_TABLE |
| 0xDA | 218 | MONSTER_CARNIVAL |
| 0xDC | 220 | PARTY_SEARCH_REGISTER |
| 0xDE | 222 | PARTY_SEARCH_START |
| 0xDF | 223 | PARTY_SEARCH_UPDATE |
| 0xE4 | 228 | CHECK_CASH |
| 0xE5 | 229 | CASHSHOP_OPERATION |
| 0xE6 | 230 | COUPON_CODE |
| 0xEC | 236 | OPEN_ITEMUI |
| 0xED | 237 | CLOSE_ITEMUI |
| 0xEE | 238 | USE_ITEMUI |
| 0xFD | 253 | MTS_OPERATION |
| 0x100 | 256 | USE_MAPLELIFE |
| 0x104 | 260 | USE_HAMMER *(enum terminator)* |
| 0x3713 | 14099 | CUSTOM_PACKET |
| 0xFFFE | 65534 | MAPLETV |

### 3.2 SendOpcode — values already declared

| Hex | Dec | Constant |
|---|---|---|
| 0x10 | 16 | CHANGE_CHANNEL |
| 0x11 | 17 | PING |
| 0x12 | 18 | KOREAN_INTERNET_CAFE_SHIT |
| 0x14 | 20 | CHANNEL_SELECTED |
| 0x15 | 21 | HACKSHIELD_REQUEST |
| 0x16 | 22 | RELOG_RESPONSE |
| 0x19 | 25 | CHECK_CRC_RESULT |
| 0x1A | 26 | LAST_CONNECTED_WORLD |
| 0x1B | 27 | RECOMMENDED_WORLD_MESSAGE |
| 0x1C | 28 | CHECK_SPW_RESULT |
| 0x1D | 29 | INVENTORY_OPERATION |
| 0x1E | 30 | INVENTORY_GROW |
| 0x1F | 31 | STAT_CHANGED |
| 0x20 | 32 | GIVE_BUFF |
| 0x21 | 33 | CANCEL_BUFF |
| 0x22 | 34 | FORCED_STAT_SET |
| 0x23 | 35 | FORCED_STAT_RESET |
| 0x24 | 36 | UPDATE_SKILLS |
| 0x25 | 37 | SKILL_USE_RESULT |
| 0x26 | 38 | FAME_RESPONSE |
| 0x27 | 39 | SHOW_STATUS_INFO |
| 0x28 | 40 | OPEN_FULL_CLIENT_DOWNLOAD_LINK |
| 0x29 | 41 | MEMO_RESULT |
| 0x2A | 42 | MAP_TRANSFER_RESULT |
| 0x2B | 43 | WEDDING_PHOTO *(commented `//ANTI_MACRO_RESULT(0x2B)`)* |
| 0x2D | 45 | CLAIM_RESULT |
| 0x2E | 46 | CLAIM_AVAILABLE_TIME |
| 0x2F | 47 | CLAIM_STATUS_CHANGED |
| 0x30 | 48 | SET_TAMING_MOB_INFO |
| 0x31 | 49 | QUEST_CLEAR |
| 0x32 | 50 | ENTRUSTED_SHOP_CHECK_RESULT |
| 0x33 | 51 | SKILL_LEARN_ITEM_RESULT |
| 0x34 | 52 | GATHER_ITEM_RESULT |
| 0x35 | 53 | SORT_ITEM_RESULT |
| 0x37 | 55 | SUE_CHARACTER_RESULT |
| 0x39 | 57 | TRADE_MONEY_LIMIT |
| 0x3A | 58 | SET_GENDER |
| 0x3B | 59 | GUILD_BBS_PACKET |
| 0x3D | 61 | CHAR_INFO |
| 0x3E | 62 | PARTY_OPERATION |
| 0x3F | 63 | BUDDYLIST |
| 0x41 | 65 | GUILD_OPERATION |
| 0x42 | 66 | ALLIANCE_OPERATION |
| 0x43 | 67 | SPAWN_PORTAL |
| 0x44 | 68 | SERVERMESSAGE |
| 0x45 | 69 | INCUBATOR_RESULT |
| 0x46 | 70 | SHOP_SCANNER_RESULT |
| 0x47 | 71 | SHOP_LINK_RESULT |
| 0x48 | 72 | MARRIAGE_REQUEST |
| 0x49 | 73 | MARRIAGE_RESULT |
| 0x4A | 74 | WEDDING_GIFT_RESULT |
| 0x4B | 75 | NOTIFY_MARRIED_PARTNER_MAP_TRANSFER |
| 0x4C | 76 | CASH_PET_FOOD_RESULT |
| 0x4D | 77 | SET_WEEK_EVENT_MESSAGE |
| 0x4E | 78 | SET_POTION_DISCOUNT_RATE |
| 0x4F | 79 | BRIDLE_MOB_CATCH_FAIL |
| 0x50 | 80 | IMITATED_NPC_RESULT |
| 0x51 | 81 | IMITATED_NPC_DATA |
| 0x52 | 82 | LIMITED_NPC_DISABLE_INFO |
| 0x53 | 83 | MONSTER_BOOK_SET_CARD |
| 0x54 | 84 | MONSTER_BOOK_SET_COVER |
| 0x55 | 85 | HOUR_CHANGED |
| 0x56 | 86 | MINIMAP_ON_OFF |
| 0x57 | 87 | CONSULT_AUTHKEY_UPDATE |
| 0x58 | 88 | CLASS_COMPETITION_AUTHKEY_UPDATE |
| 0x59 | 89 | WEB_BOARD_AUTHKEY_UPDATE |
| 0x5A | 90 | SESSION_VALUE |
| 0x5B | 91 | PARTY_VALUE |
| 0x5C | 92 | FIELD_SET_VARIABLE |
| 0x5D | 93 | BONUS_EXP_CHANGED |
| 0x5E | 94 | FAMILY_CHART_RESULT |
| 0x5F | 95 | FAMILY_INFO_RESULT |
| 0x60 | 96 | FAMILY_RESULT |
| 0x61 | 97 | FAMILY_JOIN_REQUEST |
| 0x62 | 98 | FAMILY_JOIN_REQUEST_RESULT |
| 0x63 | 99 | FAMILY_JOIN_ACCEPTED |
| 0x64 | 100 | FAMILY_PRIVILEGE_LIST |
| 0x65 | 101 | FAMILY_REP_GAIN |
| 0x66 | 102 | FAMILY_NOTIFY_LOGIN_OR_LOGOUT |
| 0x67 | 103 | FAMILY_SET_PRIVILEGE |
| 0x68 | 104 | FAMILY_SUMMON_REQUEST |
| 0x69 | 105 | NOTIFY_LEVELUP |
| 0x6A | 106 | NOTIFY_MARRIAGE |
| 0x6B | 107 | NOTIFY_JOB_CHANGE |
| 0x6D | 109 | MAPLE_TV_USE_RES |
| 0x6E | 110 | AVATAR_MEGAPHONE_RESULT |
| 0x6F | 111 | SET_AVATAR_MEGAPHONE |
| 0x70 | 112 | CLEAR_AVATAR_MEGAPHONE |
| 0x71 | 113 | CANCEL_NAME_CHANGE_RESULT |
| 0x72 | 114 | CANCEL_TRANSFER_WORLD_RESULT |
| 0x73 | 115 | DESTROY_SHOP_RESULT |
| 0x74 | 116 | FAKE_GM_NOTICE |
| 0x75 | 117 | SUCCESS_IN_USE_GACHAPON_BOX |
| 0x76 | 118 | NEW_YEAR_CARD_RES |
| 0x77 | 119 | RANDOM_MORPH_RES |
| 0x78 | 120 | CANCEL_NAME_CHANGE_BY_OTHER |
| 0x79 | 121 | SET_EXTRA_PENDANT_SLOT |
| 0x7A | 122 | SCRIPT_PROGRESS_MESSAGE |
| 0x7B | 123 | DATA_CRC_CHECK_FAILED |
| 0x7C | 124 | MACRO_SYS_DATA_INIT |
| 0x7D | 125 | SET_FIELD |
| 0x7E | 126 | SET_ITC |
| 0x7F | 127 | SET_CASH_SHOP |
| 0x80 | 128 | SET_BACK_EFFECT |
| 0x81 | 129 | SET_MAP_OBJECT_VISIBLE |
| 0x82 | 130 | CLEAR_BACK_EFFECT |
| 0x83 | 131 | BLOCKED_MAP |
| 0x84 | 132 | BLOCKED_SERVER |
| 0x85 | 133 | FORCED_MAP_EQUIP |
| 0x86 | 134 | MULTICHAT |
| 0x87 | 135 | WHISPER |
| 0x88 | 136 | SPOUSE_CHAT |
| 0x89 | 137 | SUMMON_ITEM_INAVAILABLE |
| 0x8A | 138 | FIELD_EFFECT |
| 0x8B | 139 | FIELD_OBSTACLE_ONOFF |
| 0x8C | 140 | FIELD_OBSTACLE_ONOFF_LIST |
| 0x8D | 141 | FIELD_OBSTACLE_ALL_RESET |
| 0x8E | 142 | BLOW_WEATHER |
| 0x8F | 143 | PLAY_JUKEBOX |
| 0x90 | 144 | ADMIN_RESULT |
| 0x91 | 145 | OX_QUIZ |
| 0x92 | 146 | GMEVENT_INSTRUCTIONS |
| 0x93 | 147 | CLOCK |
| 0x94 | 148 | CONTI_MOVE |
| 0x95 | 149 | CONTI_STATE |
| 0x96 | 150 | SET_QUEST_CLEAR |
| 0x97 | 151 | SET_QUEST_TIME |
| 0x98 | 152 | ARIANT_RESULT |
| 0x99 | 153 | SET_OBJECT_STATE |
| 0x9A | 154 | STOP_CLOCK |
| 0x9B | 155 | ARIANT_ARENA_SHOW_RESULT |
| 0x9D | 157 | PYRAMID_GAUGE |
| 0x9E | 158 | PYRAMID_SCORE |
| 0x9F | 159 | QUICKSLOT_INIT |
| 0xA0 | 160 | SPAWN_PLAYER |
| 0xA1 | 161 | REMOVE_PLAYER_FROM_MAP |
| 0xA2 | 162 | CHATTEXT |
| 0xA3 | 163 | CHATTEXT1 |
| 0xA4 | 164 | CHALKBOARD |
| 0xA5 | 165 | UPDATE_CHAR_BOX |
| 0xA6 | 166 | SHOW_CONSUME_EFFECT |
| 0xA7 | 167 | SHOW_SCROLL_EFFECT |
| 0xA8 | 168 | SPAWN_PET |
| 0xAA | 170 | MOVE_PET |
| 0xAB | 171 | PET_CHAT |
| 0xAC | 172 | PET_NAMECHANGE |
| 0xAD | 173 | PET_EXCEPTION_LIST |
| 0xAE | 174 | PET_COMMAND |
| 0xAF | 175 | SPAWN_SPECIAL_MAPOBJECT |
| 0xB0 | 176 | REMOVE_SPECIAL_MAPOBJECT |
| 0xB1 | 177 | MOVE_SUMMON |
| 0xB2 | 178 | SUMMON_ATTACK |
| 0xB3 | 179 | DAMAGE_SUMMON |
| 0xB4 | 180 | SUMMON_SKILL |
| 0xB5 | 181 | SPAWN_DRAGON |
| 0xB6 | 182 | MOVE_DRAGON |
| 0xB7 | 183 | REMOVE_DRAGON |
| 0xB9 | 185 | MOVE_PLAYER |
| 0xBA | 186 | CLOSE_RANGE_ATTACK |
| 0xBB | 187 | RANGED_ATTACK |
| 0xBC | 188 | MAGIC_ATTACK |
| 0xBD | 189 | ENERGY_ATTACK |
| 0xBE | 190 | SKILL_EFFECT |
| 0xBF | 191 | CANCEL_SKILL_EFFECT |
| 0xC0 | 192 | DAMAGE_PLAYER |
| 0xC1 | 193 | FACIAL_EXPRESSION |
| 0xC2 | 194 | SHOW_ITEM_EFFECT |
| 0xC4 | 196 | SHOW_CHAIR |
| 0xC5 | 197 | UPDATE_CHAR_LOOK |
| 0xC6 | 198 | SHOW_FOREIGN_EFFECT |
| 0xC7 | 199 | GIVE_FOREIGN_BUFF |
| 0xC8 | 200 | CANCEL_FOREIGN_BUFF |
| 0xC9 | 201 | UPDATE_PARTYMEMBER_HP |
| 0xCA | 202 | GUILD_NAME_CHANGED |
| 0xCB | 203 | GUILD_MARK_CHANGED |
| 0xCC | 204 | THROW_GRENADE |
| 0xCD | 205 | CANCEL_CHAIR |
| 0xCE | 206 | SHOW_ITEM_GAIN_INCHAT |
| 0xCF | 207 | DOJO_WARP_UP |
| 0xD0 | 208 | LUCKSACK_PASS |
| 0xD1 | 209 | LUCKSACK_FAIL |
| 0xD2 | 210 | MESO_BAG_MESSAGE |
| 0xD3 | 211 | UPDATE_QUEST_INFO |
| 0xD6 | 214 | PLAYER_HINT |
| 0xD9 | 217 | MAKER_RESULT |
| 0xDB | 219 | KOREAN_EVENT |
| 0xDC | 220 | OPEN_UI |
| 0xDD | 221 | LOCK_UI |
| 0xDE | 222 | DISABLE_UI |
| 0xDF | 223 | SPAWN_GUIDE |
| 0xE0 | 224 | TALK_GUIDE |
| 0xE1 | 225 | SHOW_COMBO |
| 0xEA | 234 | COOLDOWN |
| 0xEC | 236 | SPAWN_MONSTER |
| 0xED | 237 | KILL_MONSTER |
| 0xEE | 238 | SPAWN_MONSTER_CONTROL |
| 0xEF | 239 | MOVE_MONSTER |
| 0xF0 | 240 | MOVE_MONSTER_RESPONSE |
| 0xF2 | 242 | APPLY_MONSTER_STATUS |
| 0xF3 | 243 | CANCEL_MONSTER_STATUS |
| 0xF4 | 244 | RESET_MONSTER_ANIMATION |
| 0xF6 | 246 | DAMAGE_MONSTER |
| 0xF9 | 249 | ARIANT_THING |
| 0xFA | 250 | SHOW_MONSTER_HP |
| 0xFB | 251 | CATCH_MONSTER |
| 0xFC | 252 | CATCH_MONSTER_WITH_ITEM |
| 0xFD | 253 | SHOW_MAGNET |
| 0x101 | 257 | SPAWN_NPC |
| 0x102 | 258 | REMOVE_NPC |
| 0x103 | 259 | SPAWN_NPC_REQUEST_CONTROLLER |
| 0x104 | 260 | NPC_ACTION |
| 0x107 | 263 | SET_NPC_SCRIPTABLE |
| 0x109 | 265 | SPAWN_HIRED_MERCHANT |
| 0x10A | 266 | DESTROY_HIRED_MERCHANT |
| 0x10B | 267 | UPDATE_HIRED_MERCHANT |
| 0x10C | 268 | DROP_ITEM_FROM_MAPOBJECT |
| 0x10D | 269 | REMOVE_ITEM_FROM_MAP |
| 0x10E | 270 | CANNOT_SPAWN_KITE |
| 0x10F | 271 | SPAWN_KITE |
| 0x110 | 272 | REMOVE_KITE |
| 0x111 | 273 | SPAWN_MIST |
| 0x112 | 274 | REMOVE_MIST |
| 0x113 | 275 | SPAWN_DOOR |
| 0x114 | 276 | REMOVE_DOOR |
| 0x115 | 277 | REACTOR_HIT |
| 0x117 | 279 | REACTOR_SPAWN |
| 0x118 | 280 | REACTOR_DESTROY |
| 0x119 | 281 | SNOWBALL_STATE |
| **0x11A** | **282** | **HIT_SNOWBALL** |
| 0x11B | 283 | SNOWBALL_MESSAGE |
| 0x11C | 284 | LEFT_KNOCK_BACK |
| 0x11D | 285 | COCONUT_HIT |
| 0x11E | 286 | COCONUT_SCORE |
| 0x11F | 287 | GUILD_BOSS_HEALER_MOVE |
| 0x120 | 288 | GUILD_BOSS_PULLEY_STATE_CHANGE |
| 0x121 | 289 | MONSTER_CARNIVAL_START |
| 0x122 | 290 | MONSTER_CARNIVAL_OBTAINED_CP |
| 0x123 | 291 | MONSTER_CARNIVAL_PARTY_CP |
| 0x124 | 292 | MONSTER_CARNIVAL_SUMMON |
| 0x125 | 293 | MONSTER_CARNIVAL_MESSAGE |
| 0x126 | 294 | MONSTER_CARNIVAL_DIED |
| 0x127 | 295 | MONSTER_CARNIVAL_LEAVE |
| 0x129 | 297 | ARIANT_ARENA_USER_SCORE |
| 0x12B | 299 | SHEEP_RANCH_INFO |
| 0x12C | 300 | SHEEP_RANCH_CLOTHES |
| 0x12D | 301 | WITCH_TOWER_SCORE_UPDATE |
| 0x12E | 302 | HORNTAIL_CAVE |
| 0x12F | 303 | ZAKUM_SHRINE |
| 0x130 | 304 | NPC_TALK |
| 0x131 | 305 | OPEN_NPC_SHOP |
| 0x132 | 306 | CONFIRM_SHOP_TRANSACTION |
| 0x133 | 307 | ADMIN_SHOP_MESSAGE |
| 0x134 | 308 | ADMIN_SHOP |
| 0x135 | 309 | STORAGE |
| 0x136 | 310 | FREDRICK_MESSAGE |
| 0x137 | 311 | FREDRICK |
| 0x138 | 312 | RPS_GAME |
| 0x139 | 313 | MESSENGER |
| 0x13A | 314 | PLAYER_INTERACTION |
| 0x13B | 315 | TOURNAMENT |
| 0x13C | 316 | TOURNAMENT_MATCH_TABLE |
| 0x13D | 317 | TOURNAMENT_SET_PRIZE |
| 0x13E | 318 | TOURNAMENT_UEW |
| 0x13F | 319 | TOURNAMENT_CHARACTERS |
| 0x140 | 320 | WEDDING_PROGRESS |
| 0x141 | 321 | WEDDING_CEREMONY_END |
| 0x142 | 322 | PARCEL |
| 0x143 | 323 | CHARGE_PARAM_RESULT |
| 0x144 | 324 | QUERY_CASH_RESULT |
| 0x145 | 325 | CASHSHOP_OPERATION |
| 0x146 | 326 | CASHSHOP_PURCHASE_EXP_CHANGED |
| 0x147 | 327 | CASHSHOP_GIFT_INFO_RESULT |
| 0x148 | 328 | CASHSHOP_CHECK_NAME_CHANGE |
| 0x149 | 329 | CASHSHOP_CHECK_NAME_CHANGE_POSSIBLE_RESULT |
| 0x14A | 330 | CASHSHOP_REGISTER_NEW_CHARACTER_RESULT |
| 0x14B | 331 | CASHSHOP_CHECK_TRANSFER_WORLD_POSSIBLE_RESULT |
| 0x14C | 332 | CASHSHOP_GACHAPON_STAMP_RESULT |
| 0x14D | 333 | CASHSHOP_CASH_ITEM_GACHAPON_RESULT |
| 0x14E | 334 | CASHSHOP_CASH_GACHAPON_OPEN_RESULT |
| 0x14F | 335 | KEYMAP |
| 0x150 | 336 | AUTO_HP_POT |
| 0x151 | 337 | AUTO_MP_POT |
| 0x155 | 341 | SEND_TV |
| 0x156 | 342 | REMOVE_TV |
| 0x157 | 343 | ENABLE_TV |
| 0x15B | 347 | MTS_OPERATION2 |
| 0x15C | 348 | MTS_OPERATION |
| 0x15D | 349 | MAPLELIFE_RESULT |
| 0x15E | 350 | MAPLELIFE_ERROR |
| 0x162 | 354 | VICIOUS_HAMMER |
| 0x166 | 358 | VEGA_SCROLL *(enum terminator)* |

### 3.3 Free-range observations
- **RecvOpcode 0x100–0x3712:** only `0x100` (USE_MAPLELIFE) and `0x104` (USE_HAMMER) are used. The whole range `0x105–0x3712` is **free**.
- **RecvOpcode 0x105–0x36FF** specifically is fully unallocated.
- **SendOpcode 0x167–0x372F** is fully unallocated (last defined is `0x166` VEGA_SCROLL).
- Reserved/special: `0x3713` (RecvOpcode.CUSTOM_PACKET), `0xFFFE` (RecvOpcode.MAPLETV).

---

## 4. Package-vs-Cosmic collision table

For each opcode a package wants to add, check both enums:

| Package | Opcode | Direction (enum to edit) | In Cosmic RecvOpcode? | In Cosmic SendOpcode? | Hard conflict? |
|---|---|---|---|---|---|
| CheckIn | `0x11A` | Recv (RecvOpcode.DAILY_CHECKIN) | ❌ NOT used | ✅ USED — `HIT_SNOWBALL` (line 288) | **No hard conflict** (different enums, different wire directions). RecvOpcode has no entry at `0x11A`. |
| CheckIn | `0x17C` | Send (SendOpcode.DAILY_CHECKIN) | ❌ NOT used | ❌ NOT used | **No conflict.** |
| BeautySalon | `0x174` (Recv) | Recv (RecvOpcode.BEAUTY_ACTION) | ❌ NOT used | ❌ NOT used | **No conflict.** |
| BeautySalon | `0x174` (Send) | Send (SendOpcode.BEAUTY_RESULT) | ❌ NOT used | ❌ NOT used | **No conflict.** |
| CashShop | `0x3730` | Recv (RecvOpcode.CASHSHOP_WINDOW_ACTION) | ❌ NOT used | ❌ NOT used | **No conflict.** |
| CashShop | `0x3731` | Send (SendOpcode.CASHSHOP_WINDOW_SYNC) | ❌ NOT used | ❌ NOT used | **No conflict.** |

**Result: No hard conflicts.** `0x11A` is the only target value that exists in any Cosmic enum — and it exists in the **opposite** enum (SendOpcode.HIT_SNOWBALL), so adding `RecvOpcode.DAILY_CHECKIN = 0x11A` does not collide at runtime (different wire directions).

---

## 5. Files each package needs to modify

### 5.1 CheckIn (Daily Check-In)

**New files to COPY:**
- `net/server/channel/handlers/DailyCheckinHandler.java`
- `server/DailyCheckinRewards.java`
- `client/command/commands/gm0/CheckinCommand.java`
- `server/sql/daily_checkin.sql`
- `client/src/dailycheckin.cpp` (+ accompanying client-side headers)
- `wz/UI.wz → UIWindow.img/DailyCheckin/backgrnd` (data, not source)

**Existing Cosmic files to EDIT:**
- `net/opcodes/RecvOpcode.java` — add `DAILY_CHECKIN(0x11A),`
- `net/opcodes/SendOpcode.java` — add `DAILY_CHECKIN(0x17C),`
- `net/PacketProcessor.java` — register `RecvOpcode.DAILY_CHECKIN → DailyCheckinHandler`
- `tools/PacketCreator.java` — add `dailyCheckinSnapshot(...)` builder
- `client/Character.java` — add 3 fields (`checkinDay`, `checkinClaimed`, `checkinLastClaim`) + accessors + streak logic
- `net/server/channel/handlers/PlayerLoggedinHandler.java` — invoke `refreshCheckin()` on login
- `client/command/CommandsExecutor.java` — register `@daily` / `@checkin` command

**Existing client (C++) files to EDIT:**
- `client/src/hook.h` (or equivalent)
- `client/src/pch.h`
- Various `wvs/*.h` and `ztl/ztl.h` headers (per `README.md` snippets)

### 5.2 BeautySalon

**New files to COPY:**
- `net/server/channel/handlers/BeautyHandler.java`
- `server/beauty/BeautyData.java`
- `server/beauty/BeautyPackets.java`
- `server/beauty/BeautyStorage.java`
- `resources/db/tables/025-beauty.sql`
- `resources/db/tables/026-beauty-unlock.sql`
- `client/src/beautyshop.cpp`

**Existing Cosmic files to EDIT:**
- `net/opcodes/RecvOpcode.java` — add `BEAUTY_ACTION(0x174),`
- `net/opcodes/SendOpcode.java` — add `BEAUTY_RESULT(0x174),`
- `net/PacketProcessor.java` — `import net.server.channel.handlers.BeautyHandler;` + register `RecvOpcode.BEAUTY_ACTION → BeautyHandler`
- `net/server/channel/handlers/GeneralChatHandler.java` — add `@beauty` block
- `resources/db/changelog-tables.xml` — register changeSets `25` and `26`

**Existing client (C++) files to EDIT:**
- `client/src/hook.h` — declare + call `AttachBeautyShopMod()`
- `client/src/CMakeLists.txt` — add `beautyshop.cpp` to injector sources

### 5.3 CashShop

**New files to COPY:**
- `net/server/channel/handlers/CashShopWindowHandler.java`
- `server/cashshop/CashShopCatalog.java`
- `server/cashshop/CashShopWindowPackets.java`
- `server/cashshop/CashShopWindowPurchase.java`
- `client/cashshopwnd.cpp`
- `client/cashshopwnd.h`
- `data/catalog.tsv` → placed at `<server working dir>/cashshop/catalog.tsv`
- `wz/UI/CashShop.img` (data, not source)

**Existing Cosmic files to EDIT:**
- `net/opcodes/RecvOpcode.java` — add `CASHSHOP_WINDOW_ACTION(0x3730),`
- `net/opcodes/SendOpcode.java` — add `CASHSHOP_WINDOW_SYNC(0x3731),`
- `net/PacketProcessor.java` — `import net.server.channel.handlers.CashShopWindowHandler;` + register handler

**Existing handler file to MODIFY (logic, not just register):**
- `EnterCashShopHandler` (whatever handles the cash shop button press — likely `net/server/channel/handlers/EnterCashShopHandler.java`) — replace stage transition with `CashShopWindowPackets.open(mc)` + `enableActions()`, gated by a `USE_STANDALONE_WINDOW` boolean

**Existing client (C++) files to EDIT:**
- The DLL's existing `CClientSocket::ProcessPacket` hook — route `nType == kCashShopSyncOpcode` to `CashShopWnd_HandleSync()`
- A per-frame update site (e.g. `CWvsApp::CallUpdate`) — call `CashShopWnd_Tick()`
- Add `cashshopwnd.cpp` to the build (C++17 required)

---

## 6. Cross-package intersection — Cosmic files needing edits in MULTIPLE packages

| Cosmic file | CheckIn | BeautySalon | CashShop | Notes |
|---|---|---|---|---|
| `net/opcodes/RecvOpcode.java` | ✅ add `DAILY_CHECKIN` | ✅ add `BEAUTY_ACTION` | ✅ add `CASHSHOP_WINDOW_ACTION` | **All 3** — single edit point, 3 enum entries to append. No collision (different hex). |
| `net/opcodes/SendOpcode.java` | ✅ add `DAILY_CHECKIN` | ✅ add `BEAUTY_RESULT` | ✅ add `CASHSHOP_WINDOW_SYNC` | **All 3** — same as above. |
| `net/PacketProcessor.java` | ✅ register handler | ✅ register handler | ✅ register handler | **All 3** — single import block + 3 `registerHandler(...)` lines. No collision. |
| `net/server/channel/handlers/GeneralChatHandler.java` | ❌ | ✅ add `@beauty` block | ❌ | Beauty only |
| `client/Character.java` | ✅ add streak fields | ❌ | ❌ | CheckIn only |
| `tools/PacketCreator.java` | ✅ add `dailyCheckinSnapshot` | ❌ | ❌ | CheckIn only |
| `PlayerLoggedinHandler.java` | ✅ add refresh call | ❌ | ❌ | CheckIn only |
| `CommandsExecutor.java` | ✅ register command | ❌ | ❌ | CheckIn only |
| `resources/db/changelog-tables.xml` | ❌ | ✅ register `25`, `26` | ❌ | Beauty only |
| `EnterCashShopHandler.java` (or equivalent) | ❌ | ❌ | ✅ rewrite cash-shop entry | CashShop only |
| `client/src/hook.h` | ✅ declare/call hook | ✅ declare/call hook | ❌ (uses existing dispatcher) | CheckIn + Beauty |

### True cross-package intersection

**Server-side files touched by ALL 3 packages (the only true intersection):**
1. `net/opcodes/RecvOpcode.java`
2. `net/opcodes/SendOpcode.java`
3. `net/PacketProcessor.java`

**Server-side files touched by exactly 2 packages:** None.

**Client-side files touched by 2 packages:** `client/src/hook.h` (CheckIn + Beauty). CashShop intentionally does **not** install its own hook — it routes through the existing `ProcessPacket` dispatcher per `INTEGRATION.md:23`.

---

## 7. New files each package adds (path-conflict awareness)

If all three integrate into the same Cosmic tree, distinct new-file paths — **no path collisions**:

| Package | New server files (relative to `src/main/java/`) |
|---|---|
| CheckIn | `net/server/channel/handlers/DailyCheckinHandler.java`<br>`server/DailyCheckinRewards.java`<br>`client/command/commands/gm0/CheckinCommand.java` |
| BeautySalon | `net/server/channel/handlers/BeautyHandler.java`<br>`server/beauty/BeautyData.java`<br>`server/beauty/BeautyPackets.java`<br>`server/beauty/BeautyStorage.java` |
| CashShop | `net/server/channel/handlers/CashShopWindowHandler.java`<br>`server/cashshop/CashShopCatalog.java`<br>`server/cashshop/CashShopWindowPackets.java`<br>`server/cashshop/CashShopWindowPurchase.java` |

**New client files (C++):**
| Package | New client file |
|---|---|
| CheckIn | `<client>/src/dailycheckin.cpp` |
| BeautySalon | `<client>/src/beautyshop.cpp` |
| CashShop | `<client>/cashshopwnd.cpp`, `<client>/cashshopwnd.h` |

All distinct. No collision.

---

## 8. Summary fact table

| Question | Answer |
|---|---|
| Any two packages claiming the **same opcode value**? | **No.** |
| Any package claiming an opcode **already used in Cosmic's same-direction enum**? | **No.** |
| Does CheckIn's `0x11A` clash with anything? | `0x11A` exists in Cosmic **SendOpcode** (`HIT_SNOWBALL`). CheckIn uses it in **RecvOpcode**. Different enums, different wire directions. Runtime safe. |
| Does CashShop's `0xE5` reference create a conflict? | No — `0xE5` is *explicitly avoided* by CashShop; mentioned only in a Javadoc comment. |
| Single Cosmic file touched by **all 3 packages**? | Yes, exactly 3: `RecvOpcode.java`, `SendOpcode.java`, `PacketProcessor.java`. All edits are additive enum/registration lines; constants don't overlap. |
| Single Cosmic file touched by **exactly 2 packages**? | Server-side: none. Client-side: `client/src/hook.h` (CheckIn + Beauty). |
| New-file path conflicts? | None. All new `.java`/`.cpp`/`.h` paths are distinct. |

---

## 9. Raw grep evidence (file:line)

**CheckIn's `0x11A` / `0x17C` declarations:**
```
README.md:53  **Client → Server** (`RecvOpcode.DAILY_CHECKIN = 0x11A`):
README.md:60  **Server → Client** (`SendOpcode.DAILY_CHECKIN = 0x17C`):
README.md:94  DAILY_CHECKIN(0x11A),
README.md:99  DAILY_CHECKIN(0x17C),
README.md:77  > ⚠️ **Opcode collision:** `0x11A` and `0x17C` must be **free** …
```

**BeautySalon's `0x174` declarations:**
```
FILE_LIST.md:47  - `net/opcodes/RecvOpcode.java` — `BEAUTY_ACTION(0x174),`
FILE_LIST.md:48  - `net/opcodes/SendOpcode.java` — `BEAUTY_RESULT(0x174),`
README.md:76         - `net/opcodes/RecvOpcode.java` → add `BEAUTY_ACTION(0x174),`
README.md:77         - `net/opcodes/SendOpcode.java` → add `BEAUTY_RESULT(0x174),`
README.md:83  > ⚠️ **Opcode check:** `0x174` must be **free** …
client/README.md:83  - `kOpcode_SaveBeauty = 0x174` — must match the server.
java/README.md:24  BEAUTY_ACTION(0x174),
java/README.md:29  BEAUTY_RESULT(0x174),
```

**CashShop's `0x3730` / `0x3731` declarations:**
```
INTEGRATION.md:61  CASHSHOP_WINDOW_ACTION(0x3730),
INTEGRATION.md:67  CASHSHOP_WINDOW_SYNC(0x3731),
INTEGRATION.md:78  Pick a different pair if `0x3730`/`0x3731` collide …
cashshopwnd.h:20   static constexpr unsigned short kCashShopActionOpcode = 0x3730;   // client -> server
cashshopwnd.h:21   static constexpr unsigned short kCashShopSyncOpcode   = 0x3731;   // server -> client
CashShopWindowHandler.java:18  * <p>Deliberately NOT {@code CashOperationHandler} (0xE5). …
```

**Cosmic existing assignments at the target values (only `0x11A` matches):**
```
SendOpcode.java:288  HIT_SNOWBALL(0x11A),
RecvOpcode.java:198  CASHSHOP_OPERATION(0xE5),
RecvOpcode.java:25   CUSTOM_PACKET(0x3713),//13 37 lol
RecvOpcode.java:188  MAPLETV(0xFFFE),//Don't know
```

**Broader Cosmic-repo grep (`rg -i` in `src/main/java`):**
- `0x11A` → only `SendOpcode.java:288` (and unrelated BCrypt/AES bytes).
- `0x17C` → **no matches anywhere in Cosmic**.
- `0x174` → **no matches anywhere in Cosmic**.
- `0xE5` → `RecvOpcode.java:198` (CASHSHOP_OPERATION); also unrelated AES/BCrypt byte literals and `PacketCreator.java:6508` `p.writeByte(0xE5)` (cash-shop sub-opcode, not a top-level opcode).
- `0x3730` / `0x3731` → **no matches anywhere in Cosmic**.

---

*End of W1-2 opcode collision report.*

*No native Cosmic files were modified.*