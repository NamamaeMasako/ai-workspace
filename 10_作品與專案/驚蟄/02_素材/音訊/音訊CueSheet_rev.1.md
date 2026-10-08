# 《驚蟄》音訊 Cue Sheet rev.1

狀態：施工中；BGM01–04 已正式定案並導入遊戲，BGM05 新版 03 懸疑方向獲認可，60 秒 `long_04` 樂句節奏一致修正版待試聽；BGM06–07、環境音與 SFX 尚待製作。  
範圍：BGM、環境音、關鍵 SFX；配音另案試鏡。  
基準腳本：`03_開發/JingZhe/game/script.rpy` v0.1.2。

## 1. 檔案與命名規格

遊戲內預定路徑：

```text
game/audio/music/
game/audio/ambience/
game/audio/sfx/ui/
game/audio/sfx/world/
game/audio/sfx/magic/
game/audio/sfx/battle/
```

- BGM／環境音：OGG、44.1 kHz、立體聲、可無縫循環。
- 短音效：OGG 或 WAV；如無品質差異，優先 OGG 控制包體。
- 名稱固定 ASCII、小寫、蛇形命名；不使用 `final`、`修正版`、日期。
- 音效檔不直接以腳本行號命名；使用穩定 cue ID，腳本行號只作定位參考。
- 導入前保留原始無損檔於 `02_素材/音訊/母檔/`，遊戲壓縮副本才進 `game/audio/`。
- BGM、SFX、環境音、語音分開混音通道；環境音不得吃掉角色語音頻段。

## 2. BGM 清單（7 組）

- `BGM01_LANTERN`／`bgm_lantern_theme.ogg`
  - 主選單與作品主題動機；目前不延續進短引。
  - 冷靜、節制，深藍夜色中只留一點暖光；不要史詩化。
  - 正式定案：ACE-Step 1.5 seed 2802 箏版，60 秒、44.1 kHz、立體聲 OGG；用於主選單循環，進入短引時淡出。
- `BGM02_MOON_INN_DAY`／`bgm_moon_inn_day.ogg`
  - 第一章清晨、早餐、前後院與日常互動；第六章清晨後院／餐廳短暫回歸。
  - 木質、輕柔、不甜膩。
  - 正式定案：seed 2904 尺八方向的 `long_04_smooth_continuity`，60 秒、44.1 kHz、立體聲 OGG；第一章白天與第六章清晨以 `music` 通道循環，入夜或進入調查時以 1.5 秒淡出。
- `BGM03_MOON_INN_NIGHT`／`bgm_moon_inn_night.ogg`
  - 第一章傍晚、第二章房內，以及第四至六章月下庄夜間。
  - 主題旋律的稀薄夜間變奏，可容納不安感。
  - 正式定案：seed 3003 柔鋼琴 `loop_xfade06` 循環版，54 秒、44.1 kHz、立體聲 OGG；尾端 6 秒與開頭 6 秒交叉淡化，以 `music` 通道循環。日間曲切入時交叉淡化，離開月下庄夜間日常或進入尚未配樂的異場景時以 1.5 秒淡出。
- `BGM04_BLACK_CARD_MEMORY`／`bgm_black_card_memory.ogg`、`bgm_black_card_memory_variant.ogg`
  - 第三章小酒館回憶、黑卡與郵箱說明。
  - 疏離、神祕、略帶異國色彩。
  - 2026-10-02 正式採用：酒館進場播放 seed 3101 `long_03` 循環處理版（約 56.47 秒）；全黑卡片出現在桌上時以 1.5 秒交叉淡切至黑鍵懸疑 `long_04`（60 秒），進第四章時再交叉淡切至 `BGM03`。兩首皆為 44.1 kHz 立體聲 OGG；生前實機試聽後確認兩首均可採用。
- `BGM05_SILK_UNDER_DOOR`／`bgm_silk_under_door.ogg`
  - 第四章怪物逼近、第五章受控、第六章調查。
  - 細碎壓迫，不先暴露完整戰鬥節奏。
  - 2026-10-07：四首 20 秒短版候選完成，方向為柔鋼琴、低音單簧管、悶音弦樂與箏泛音（seed 3201–3204）；目前提供 `_take02` 試聽版本，待生前挑選後才製作長版及循環。詳見[候選製作紀錄](候選/BGM05_SILK_UNDER_DOOR/README.md)，尚未導入遊戲。
  - 2026-10-07 後續：生前選中 02 低音單簧管與 03 悶音弦樂，各以選中短版作參考完成 60 秒長版，詳見[長版候選紀錄](候選/BGM05_SILK_UNDER_DOOR/longform/README.md)。兩版待試聽比較，尚未處理循環或正式採用。
  - 2026-10-08：生前認為 `long_01` 兩首少了懸疑感、偏俏皮，不符合場景，兩首均不採用。已以原短版 02／03 重新完成各 60 秒 `long_02`，方向收緊為低沉長音、半音／增四度摩擦與持續低音；待試聽確認，尚未導入遊戲。
  - 2026-10-08 後續：生前認為 `long_02` 新版 03 方向正確，但原 20 秒短版 03 更好聽。已完成 `long_03_short_continuation_muted_strings_seed3203.ogg`（60 秒），保留原短版前 18 秒，18–19 秒交疊後接續新生成的後段；待確認接續、音樂感與場景情緒，尚未正式採用。
  - 2026-10-08 再修正：生前認為 `long_03` 接續後的節奏與前段不一致。已完成 `long_04_phrase_guided_muted_strings_seed3203.ogg`（60 秒），以原短版樂句回歸作全曲結構參考，採 source-guided cover 限制節奏與樂句漂移；待試聽確認，歷次候選均保留。
- `BGM06_FOREST_ASSAULT`／`bgm_forest_assault.ogg`
  - 第七、八章戰鬥。
  - 同一主題可做一般／苦香強化兩段或兩個可無縫銜接版本。
- `BGM07_DAWN_TOGETHER`／`bgm_dawn_together.ogg`
  - 真結局重聚、月下庄夜晚收束與清晨。
  - 回收 `BGM01` 動機，但更完整、更有呼吸。

## 3. 環境音清單（6 組）

- `AMB01_ROAD_WIND`／`amb_road_twilight_wind.ogg`：舊道傍晚風、遠處潮氣與草木。
- `AMB02_INN_WOOD_ROOM`／`amb_inn_wood_room.ogg`：室內木構、極遠處生活聲；清淡。
- `AMB03_COURTYARD_WATER_WIND`／`amb_courtyard_water_wind.ogg`：後院水聲與風聲。
- `AMB04_NIGHT_INSECTS`／`amb_night_insects.ogg`：房間／月下庄夜間蟲鳴，可逐步淡弱營造異常。
- `AMB05_FOREST_NIGHT`／`amb_forest_night.ogg`：濕地、葉聲、竹林與低風。
- `AMB06_RAIN`／`amb_rain_cold.ogg`：第七章死亡路線、時間回退後與真結局尾段的雨。

## 4. SFX 資產清單（32 個）

### UI

- `UI01_CONFIRM`／`ui_confirm.ogg`
- `UI02_BACK`／`ui_back.ogg`

### 場景與物件

- `SFX01_SLIDING_DOOR`／`world_sliding_door.ogg`
- `SFX02_DOOR_KNOCK`／`world_door_knock_soft.ogg`
- `SFX03_WOOD_BELL`／`world_wood_bell.ogg`
- `SFX04_FOOTSTEP_WOOD`／`world_footstep_wood.ogg`
- `SFX05_FOOTSTEP_WET`／`world_footstep_wet.ogg`
- `SFX06_TABLE_TAP`／`world_table_tap_double.ogg`
- `SFX07_WRITING`／`world_writing_pen.ogg`
- `SFX08_PAPER_FOLD`／`world_paper_fold.ogg`
- `SFX09_CARD_PLACE`／`world_black_card_place.ogg`
- `SFX10_CARD_SLIDE`／`world_black_card_slide.ogg`
- `SFX11_LAMP_SWAY`／`world_lamp_sway.ogg`
- `SFX12_LAMP_DROP`／`world_lamp_drop.ogg`

### 菸斗與魔法

- `SFX13_KISERU_IGNITE`／`magic_kiseru_ignite.ogg`
- `SFX14_KISERU_DRAW`／`magic_kiseru_draw.ogg`
- `SFX15_EMBER`／`magic_kiseru_ember.ogg`
- `SFX16_MAILBOX_REVEAL`／`magic_mailbox_reveal.ogg`
- `SFX17_MAILBOX_OPEN`／`magic_mailbox_open.ogg`
- `SFX18_CARD_PULSE`／`magic_black_card_pulse.ogg`
- `SFX19_CARD_TEAR`／`magic_black_card_tear.ogg`
- `SFX20_MAGIC_RIFT`／`magic_night_rift.ogg`
- `SFX21_INSECT_SUMMON`／`magic_insect_summon.ogg`

### 戰鬥與妖怪

- `SFX22_SILK_WHISPER`／`battle_silk_whisper.ogg`
- `SFX23_SILK_CUT`／`battle_silk_cut.ogg`
- `SFX24_SPIDER_STEPS`／`battle_spider_steps.ogg`
- `SFX25_TSUCHIGUMO_HISS`／`battle_tsuchigumo_hiss.ogg`
- `SFX26_NAGINATA_WHOOSH`／`battle_naginata_whoosh.ogg`
- `SFX27_NAGINATA_HIT`／`battle_naginata_armor_hit.ogg`
- `SFX28_KAMIKIRI_BLADES`／`battle_kamikiri_blades.ogg`
- `SFX29_OMUKADE_ARMOR`／`battle_omukade_armor_move.ogg`
- `SFX30_OMUKADE_IMPACT`／`battle_omukade_impact.ogg`
- `SFX31_BODY_FALL`／`battle_body_fall_soft.ogg`
- `SFX32_COUGH_BLOOD`／`battle_cough_blood.ogg`

## 5. 逐章放置規劃

### 短引／序章（`start`、`prologue`）

- 主選單播放 `BGM01_LANTERN`；開始遊戲後以 1 秒淡出停止，短引維持安靜，讓黑底文字自行成立。
- `scene bg road_twilight`：淡入 `AMB01_ROAD_WIND`；是否另接極淡 BGM 留待 `BGM02`／`BGM03` 完成後實機判斷，不為換背景硬切新曲。
- 「煙草燃起時」：`SFX13_KISERU_IGNITE`，之後只在必要處補 `SFX15_EMBER`，不循環貼耳燃燒聲。
- 「推門而入時，木鈴輕輕響」：`SFX01_SLIDING_DOOR`＋稍後 `SFX03_WOOD_BELL`。
- 進月下庄後：環境風淡出，BGM 轉入 `BGM02_MOON_INN_DAY` 的傍晚尾段或 `BGM03` 極淡版本。

### 第一章（`chapter_1`）

- 清晨房間／早餐：`BGM02_MOON_INN_DAY`、`AMB02_INN_WOOD_ROOM`。
- 後院「只有水聲和風聲」：切 `AMB03_COURTYARD_WATER_WIND`。
- 包布與薙刀出現：`SFX08_PAPER_FOLD` 可換成更厚布料音；不使用戰鬥刃聲。
- 「低頭擦過刀柄」：極輕的木柄摩擦；若無獨立素材，留白比亂塞金屬聲好。
- 傍晚回大廳：轉 `BGM03_MOON_INN_NIGHT`。

### 第二章（`chapter_2`）

- 房間夜晚：`BGM03_MOON_INN_NIGHT`、`AMB04_NIGHT_INSECTS`。
- 「煙草點燃」：`SFX13_KISERU_IGNITE`；火光／影子加深時不另塞 jump scare。
- 「魔法郵箱」首次完整出現：`SFX16_MAILBOX_REVEAL`。
- 「一頁紙折起，放進郵箱」：`SFX07_WRITING` → `SFX08_PAPER_FOLD` → `SFX17_MAILBOX_OPEN`。
- 「窗外傳來幾聲蟲鳴」：短暫拉高 `AMB04` 後再回原音量。
- 「門外很輕的腳步聲」：`SFX04_FOOTSTEP_WOOD`，位置感偏門外。

### 第三章（`chapter_3`）

- 小酒館：`BGM04_BLACK_CARD_MEMORY`；另做極淡室內 room tone 時可歸入 `AMB02` 的酒館變體，第一批可先不新增第七組環境音。
- 「把一張全黑卡片放在桌上」：`SFX09_CARD_PLACE`。
- 「把卡片推近」：`SFX10_CARD_SLIDE`。
- 「撕開就知道了」：不要提早播放撕裂聲，只讓 `SFX18_CARD_PULSE` 極輕出現一次。
- 「低頭續火」：`SFX13_KISERU_IGNITE` 或 `SFX15_EMBER`。

### 第四章（`chapter_4`）

- 月下庄入夜前：由 `BGM03` 逐步轉 `BGM05_SILK_UNDER_DOOR`。
- 林道怪物偵察：`AMB05_FOREST_NIGHT`；土蜘蛛出現用 `SFX24_SPIDER_STEPS`，絡新婦放出細物用 `SFX22_SILK_WHISPER`。
- 「走廊裡的燈滅了一盞」：`SFX11_LAMP_SWAY` 後讓 `AMB04` 短暫消失，空白本身就是效果。
- 「牆上極細白線」：`SFX22_SILK_WHISPER` 極低音量，不做明顯怪叫。

### 第五章（`chapter_5`）

- 受控段：維持 `BGM05`，比第四章少低頻，讓不自然的安靜更突出。
- 「指尖敲了兩下桌面」：`SFX06_TABLE_TAP`。
- 「花見敲了他的門」：`SFX02_DOOR_KNOCK`，再接 `SFX01_SLIDING_DOOR`。
- 控制解除、角色呼吸混亂：不額外加音效，必要時只以 BGM 突然抽空處理。
- 走廊門縫影子與屋簷白影：`SFX22_SILK_WHISPER`、`SFX24_SPIDER_STEPS`，避免同時播放。

### 第六章（`chapter_6`）

- 清晨後院／餐廳：短暫回到 `BGM02`，但減少明亮樂器。
- 「灰裡混著極細的殼」：`SFX21_INSECT_SUMMON` 的反向／弱化變體；第一批可由同素材處理，不新增檔。
- 畫圖、記錄與收郵箱：`SFX07_WRITING`、`SFX17_MAILBOX_OPEN`。
- 「淡淡蟲香封住氣味」：`SFX15_EMBER`，尾端銜接 `BGM05`，準備進第七章。

### 第七章共通戰鬥（四個路線 label）

適用：`chapter_7_hanami_1`、`chapter_7_yumemi_1`、`chapter_7_hanami_2`、`chapter_7_yumemi_2`。

- 交卡：`SFX10_CARD_SLIDE`＋極淡 `SFX18_CARD_PULSE`。
- 進林道：`AMB05_FOREST_NIGHT`、`BGM06_FOREST_ASSAULT` 淡入。
- 式神召喚 CG：`SFX21_INSECT_SUMMON`；CG 顯示後讓音尾延續，不連打四種怪聲。
- 土蜘蛛逼近：`SFX24_SPIDER_STEPS`＋單次 `SFX25_TSUCHIGUMO_HISS`。
- 髮切切入：`SFX28_KAMIKIRI_BLADES`。
- 大百足衝撞：`SFX29_OMUKADE_ARMOR` 預備、命中時 `SFX30_OMUKADE_IMPACT`。
- 花見薙刀：`SFX26_NAGINATA_WHOOSH`；命中甲殼才用 `SFX27_NAGINATA_HIT`。
- 絡新婦偷襲：`SFX22_SILK_WHISPER` → `SFX23_SILK_CUT`。
- 死亡路線：BGM 在傷勢確認後淡出，切 `AMB06_RAIN`；倒下時 `SFX31_BODY_FALL`，不要加誇張低頻爆點。
- 「撕開」／時間回退：`SFX19_CARD_TEAR` 後瞬間切斷雨聲，再以 `BGM01` 的不完整殘響或短暫全靜音銜接下一輪。

### 第八章／真結局（`chapter_8_choice`、`chapter_8_true_end`）

- 「把卡留給自己」：`SFX18_CARD_PULSE`，不要播放 UI 勝利音。
- 苦香強化：`SFX13_KISERU_IGNITE`＋`SFX21_INSECT_SUMMON`，BGM06 進強化段。
- 林間決戰：沿用第七章戰鬥 cue，不為重複動作新增相近素材。
- 「把香捏碎」：紙／乾草碎裂可由 `SFX08_PAPER_FOLD` 加工變體，第二批再決定是否新增。
- 驚蟄受創／咳血：只在關鍵一次使用 `SFX32_COUGH_BLOOD`；其餘讓表演與停頓承擔。
- 花見準備撕卡：`SFX18_CARD_PULSE` 拉長，驚蟄抓住手腕後中止；不要真的播放 `SFX19_CARD_TEAR`。
- 「夜色被撕開一條縫」：`SFX20_MAGIC_RIFT`，BGM06 停止，影之魔女登場後可短暫引用 `BGM04` 的黑卡動機。
- 「雨也回來了」：淡入 `AMB06_RAIN`。
- 回月下庄：雨淡出，轉 `BGM07_DAWN_TOGETHER`。
- 清晨最後一句後：BGM 留尾，結局畫面才完整淡出。

## 6. UI 導入規則

- `UI01_CONFIRM`：主選單、設定、存讀檔、選項確認共用。
- `UI02_BACK`：返回／關閉選單共用。
- 預設不使用 hover 音；若未來實機確認需要，只能新增一個極輕 hover，不為每種按鈕做不同聲。
- 啟用音訊後，設定頁至少提供「音樂」「音效」兩條音量；配音導入時再增加「語音」。

## 7. 第一輪驗收標準

- 每個 BGM／環境音循環點無爆音、斷裂或可察覺空白。
- 音效不遮住閱讀節奏；自動播放 15 秒設定下仍能自然前進。
- 同一 cue 在四條第七章路線中的相同事件保持一致。
- 主選單、日常、壓迫、戰鬥、死亡回退與真結局六個情緒區段可只靠聲音辨識。
- 音樂／音效音量設為 0 時完全靜音，存讀檔後不重複疊播循環音。
- Windows 獨立版乾淨啟動，音檔全數存在且 Ren’Py lint 無缺檔。
