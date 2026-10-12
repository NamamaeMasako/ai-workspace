# 《驚蟄》音訊 Cue Sheet rev.1

狀態：BGM01–07 與兩項 UI 音效已正式採用。依 2026-10-12 生前指示，全部持續非 BGM 環境音停用，原六組 AMB 取消製作／導入待辦。劇情短音效依七批完整場景順序驗收；第一批六個動作音檔已正式核可，序章無 BGM；空白橋段是否補配樂另議。

範圍：BGM、UI 與關鍵動作 SFX；持續環境音已停用，配音另案試鏡。
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
  - 主選單與作品主題動機；黑底短引與舊道序章不配樂。
  - 冷靜、節制，深藍夜色中只留一點暖光；不要史詩化。
  - 正式定案：ACE-Step 1.5 seed 2802 箏版，60 秒、44.1 kHz、立體聲 OGG；用於主選單循環，進入短引時淡出。2026-10-12 序章試用後已依生前指示撤下，序章維持無配樂。
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
  - 2026-10-08 選定並實裝：生前採用 `long_04` 悶音弦樂；`long_04_phrase_guided_muted_strings_seed3203_loop_intro.ogg` 首次 60 秒、後續由 3.75 秒起循環（56.25 秒週期），前 56.25 秒保留選定母檔。遊戲副本 `game/audio/music/bgm_silk_under_door.ogg`，SHA-256 `0D5199BC0B8EB16D4C5504089A149EC7A67B08DB8FE8D2B63D1432B2BF5E4645`，44.1 kHz 立體聲；第四章林道／走廊、第五章受控、第六章調查／封味後以 music 通道播放，各轉場 1.5 秒。曲目已選定，場景適配及循環待生前實機確認。
  - 2026-10-08 實機確認：生前於第四章林道試聽後回覆「OK」，正式採用 long_04 循環版及目前遊戲配置；BGM05 定案。
  - 2026-10-12 第五章受控段確認：生前實機試聽後表示目前 BGM 搭配合適，不需另做。受控段沿用 long_04 悶音弦樂，獨立受控低頻變體取消，不再列為待辦。
- `BGM06_FOREST_ASSAULT`／`bgm_forest_assault.ogg`
  - 第七、八章戰鬥。
  - 一般戰鬥與苦香強化戰鬥共用已核可的「弦鼓追殺」主題；2026-10-12 生前實機確認不需另製強化變奏。
  - 2026-10-09：四首 20 秒短版候選完成，seed 3301–3304 分別探索低弦推進、低鼓壓迫、撥弦切刃、低管陰影。用於第七章林道遇襲／式神交戰與第八章林間決戰，先選一般戰鬥主題，再延伸苦香強化；尚未正式採用、做循環或導入。詳見[候選製作紀錄](候選/BGM06_FOREST_ASSAULT/README.md)。
  - 2026-10-09 修正：首輪四首被生前否決「都太歡樂了」，保留作歷程、不採用。已完成 take02 四首 20 秒新版：弦壓逼近、沉鼓搏命、弓弦絞殺、低管獵殺（seed 3311–3314）。改用 Turbo 直接擴散、不使用 LM audio codes，降低輕巧旋律及跳躍感，強化搏命、陰暗與壓迫方向；實際場景適配仍待試聽。
  - 2026-10-11 節奏修正：生前確認 BGM06 主用途是已經交戰，認為 take02 有不安感但迫切感不足。已完成 take03 四首約 20 秒短版（seed 3321–3324），方向為急弦迎擊、緊鼓攻防、弦鼓追殺、失控圍攻；提高低弦與鼓點密度，節奏提示 124–140 BPM，延續陰暗感、避免歡樂與凱旋。待試聽，尚未正式採用或導入。
  - 2026-10-11 選曲：生前選定 take03 第三版「弦鼓追殺」。已上傳原短版作 reference_audio，並以樂句 source template 引導完成約 60 秒長版；前 18 秒保留原短版內容，18–19 秒交疊至延伸段，待確認節奏一致性與戰鬥迫切感。詳見[長版紀錄](候選/BGM06_FOREST_ASSAULT/longform/README.md)。
  - 2026-10-11 長版核可與實裝：生前回覆「可以，就這版」。已沿用核可 WAV 製作 `long_01_phrase_guided_pursuit_strings_seed3323_loop_intro.ogg`，首次 60 秒、後續 `<loop 3.4285625>` 回接（56.5714375 秒週期），前 56.5714375 秒保留母檔。遊戲副本 `game/audio/music/bgm_forest_assault.ogg`，SHA-256 `fe1d4cd1a7aefd2b63cae15d9be7cece88597c4623f56981b309a4f5d91f2271`；第七章四條林間路線、兩次門口反擊及第八章決戰於出手時播放，離開戰鬥淡出。已開到第七章髮切迎戰土蜘蛛場景，回報新檔播放中、音量 1.0 且未靜音，畫面正常。長版音樂已核可，場景及循環待實機確認；苦香強化段先沿用同一主題。
  - 2026-10-11 實機確認：生前於第七章髮切迎戰土蜘蛛場景回覆「可以」，正式採用 long_01 弦鼓追殺循環副本與現行遊戲配置；BGM06 定案。
  - 2026-10-12 苦香強化段確認：生前於第八章強化交戰場景試聽後回覆「應該也不用，用同一首戰鬥曲就好」，確定沿用 long_01 弦鼓追殺，不另製強化變奏；相關待辦與選配取消。
- `BGM07_DAWN_TOGETHER`／`bgm_dawn_together.ogg`
  - 真結局重聚、月下庄夜晚收束與清晨。
  - 回收 `BGM01` 動機，但更完整、更有呼吸。
  - 2026-10-11：take01 四首約 20 秒候選完成，方向為箏與微光、鋼琴相依、弦樂歸途、竹笛晨風（seed 3401–3404）。已核可 BGM01 箏曲以 reference_audio 上傳、其 WAV 前 25 秒作 src_audio，引導結局主題回歸與配器變化；情緒為劫後安定、帶餘痛的溫柔陪伴，避免歡樂跳躍與凱旋。待試聽挑選，尚未製作長版或導入。詳見[候選製作紀錄](候選/BGM07_DAWN_TOGETHER/README.md)。

  - 2026-10-12：生前喜歡第一版與主選單呼應的回歸主題感，選定「箏與微光」。已上傳原短版作 reference_audio、65 秒樂句模板作 src_audio，完成 60 秒長版；前 18 秒保留短版內容，18–19 秒交疊至延伸段。待確認銜接、主題辨識及結局情緒，詳見[長版紀錄](候選/BGM07_DAWN_TOGETHER/longform/README.md)。

  - 2026-10-12 長版核可與實裝：生前回覆「好，就用這版」，採用 long_01 箏與微光長版。已沿用核可 WAV 製作 `long_01_phrase_guided_lantern_guzheng_seed3401_loop_intro.ogg`，前 57 秒保留、末尾 3 秒交疊；首次 60 秒、後續 `<loop 3.0>` 回接，57 秒週期。遊戲副本 `game/audio/music/bgm_dawn_together.ogg`，SHA-256 `2484ed9fc1b46b450d77210e4533cbadb233c626d503ed6f0f7dd9d6b180be07`；真結局回月下庄時播放，延續至清晨煙斗餘味，end_game 切黑時淡出，使用 music 通道與既有音量設定。已開到 script.rpy:2605「月下庄的燈重新點起來。」畫面正常、新檔播放中且未靜音。場景與循環待生前實機確認。

  - 2026-10-12 實機確認：生前於真結局回月下庄場景回覆「好」，正式採用 long_01 箏與微光循環副本及現行配置；BGM07 定案，七組主 BGM 全數完成。

## 3. 停用環境音（原 6 組，取消待辦）

2026-10-12：生前要求移除所有持續播放的非 BGM 背景音。以下六組均停用，不再安排製作或導入；已生成的候選／母檔保留為歷程。

- `AMB01_ROAD_WIND`／`amb_road_twilight_wind.ogg`：舊道傍晚風、遠處潮氣與草木。2026-10-12 生前場景回饋後，舊道／前院停用，既有候選保留。
- `AMB02_INN_WOOD_ROOM`／`amb_inn_wood_room.ogg`：室內木構、極遠處生活聲；清淡。
- `AMB03_COURTYARD_WATER_WIND`／`amb_courtyard_water_wind.ogg`：後院水聲與風聲。
- `AMB04_NIGHT_INSECTS`／`amb_night_insects.ogg`：房間／月下庄夜間蟲鳴，可逐步淡弱營造異常。
- `AMB05_FOREST_NIGHT`／`amb_forest_night.ogg`：濕地、葉聲、竹林與低風。
- `AMB06_RAIN`／`amb_rain_cold.ogg`：第七章死亡路線、時間回退後與真結局尾段的雨。

## 4. 音效資產清單（34 個：介面 2 個＋劇情 32 個）

2026-10-12 第一批確認：生前回覆「這批次的音效我認為都可以」，正式採用 SFX01／03／07／13／15 與 SFX08 包布變體，共六個動作音檔。SFX08 基礎摺紙仍待第二批；其餘劇情音效依批次接續。

### UI

2026-10-12 實機確認：生前回覆「好，系統音效OK」，正式採用第一版確認／返回音效及現行介面配置；兩項結案。

2026-10-12 後續：生前回覆「好，套進遊戲我看看」。兩種單次音效已導入 `game/audio/sfx/ui/`，確認用於一般介面按下，返回用於返回／取消／關閉選單。已啟用音效並加入設定頁「音效音量」與「試聽」；開發遊戲主選單啟動正常，實機樣式引用新檔。待生前確認實際音量與操作感，尚未正式結案。

2026-10-12：依生前要求，確認與返回各完成一版短音效候選，待試聽。單次 0.28／0.30 秒，另提供相同音檔重複三次的試聽檔；母檔與原創程序合成來源均保留。詳見[介面音效候選](候選/UI_INTERFACE/README.md)。

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
- `scene bg road_twilight`：依 2026-10-12 生前指示恢復無 BGM，連續風聲也維持停用，保留動作音效。
- 「煙草燃起時」：`SFX13_KISERU_IGNITE`，之後只在必要處補 `SFX15_EMBER`，不循環貼耳燃燒聲。
- 「推門而入時，木鈴輕輕響了幾聲」：`SFX01_SLIDING_DOOR`＋稍後 `SFX03_WOOD_BELL` take02 五下漸弱輕響。
- 進月下庄後：交談不配 BGM，也不播放室內循環底聲；進第一章清晨才淡入 BGM02。

### 第一章（`chapter_1`）

- 清晨房間／早餐：`BGM02_MOON_INN_DAY`，不加循環室內底聲。
- 後院「只有水聲和風聲」：由文本表達，沿用既有 BGM，不加持續水風聲。
- 包布與薙刀出現：`SFX08_PAPER_FOLD` 可換成更厚布料音；不使用戰鬥刃聲。
- 「低頭擦過刀柄」：極輕的木柄摩擦；若無獨立素材，留白比亂塞金屬聲好。
- 傍晚回大廳：轉 `BGM03_MOON_INN_NIGHT`。

### 第二章（`chapter_2`）

- 房間夜晚：`BGM03_MOON_INN_NIGHT`，不加循環蟲鳴。
- 「煙草點燃」：`SFX13_KISERU_IGNITE`；火光／影子加深時不另塞 jump scare。
- 「魔法郵箱」首次完整出現：`SFX16_MAILBOX_REVEAL`。
- 「一頁紙折起，放進郵箱」：`SFX07_WRITING` → `SFX08_PAPER_FOLD` → `SFX17_MAILBOX_OPEN`。
- 「窗外傳來幾聲蟲鳴」：由文本表達，不加入循環蟲鳴。
- 「門外很輕的腳步聲」：`SFX04_FOOTSTEP_WOOD`，位置感偏門外。

### 第三章（`chapter_3`）

- 小酒館：`BGM04_BLACK_CARD_MEMORY`，不另做室內循環底聲。
- 「把一張全黑卡片放在桌上」：`SFX09_CARD_PLACE`。
- 「把卡片推近」：`SFX10_CARD_SLIDE`。
- 「撕開就知道了」：不要提早播放撕裂聲，只讓 `SFX18_CARD_PULSE` 極輕出現一次。
- 「低頭續火」：`SFX13_KISERU_IGNITE` 或 `SFX15_EMBER`。

### 第四章（`chapter_4`）

- 月下庄入夜前以 `BGM03` 開場；「不是聲音，而是一種被注視的重量」後以 1.5 秒轉 `BGM05_SILK_UNDER_DOOR`，林道偵察持續。回庄大廳恢復 `BGM03`；夜深走廊燈滅／白絲處再次切入 BGM05，延續至第五章。
- 林道怪物偵察：沿用既有 BGM，不加森林循環底聲；土蜘蛛出現用 `SFX24_SPIDER_STEPS`，絡新婦放出細物用 `SFX22_SILK_WHISPER`。
- 「走廊裡的燈滅了一盞」：`SFX11_LAMP_SWAY` 後保留安靜，不加循環環境音。
- 「牆上極細白線」：`SFX22_SILK_WHISPER` 極低音量，不做明顯怪叫。

### 第五章（`chapter_5`）

- 受控段：維持 `BGM05` long_04 悶音弦樂。2026-10-12 生前於花見受控場景實機試聽後確認目前曲目搭配合適，不需另做；取消原規劃「比第四章少低頻」的獨立變體。
- 「指尖敲了兩下桌面」：`SFX06_TABLE_TAP`。
- 「花見敲了他的門」：`SFX02_DOOR_KNOCK`，再接 `SFX01_SLIDING_DOOR`。
- 控制解除、角色呼吸混亂：不額外加音效，必要時只以 BGM 突然抽空處理。
- 走廊門縫影子與屋簷白影：`SFX22_SILK_WHISPER`、`SFX24_SPIDER_STEPS`，避免同時播放。

### 第六章（`chapter_6`）

- 清晨後院／餐廳：短暫回到 `BGM02`，但減少明亮樂器。
- 午後走廊調查切入 BGM05；入夜前畫圖暫回 BGM03。
- 「灰裡混著極細的殼」：`SFX21_INSECT_SUMMON` 的反向／弱化變體；第一批可由同素材處理，不新增檔。
- 畫圖、記錄與收郵箱：`SFX07_WRITING`、`SFX17_MAILBOX_OPEN`。
- 「淡淡蟲香封住氣味」後：已轉入 BGM05，延續至大廳決定同行；進第七章前 1.5 秒淡出。`SFX15_EMBER` 尚待製作。

### 第七章共通戰鬥（四個路線 label）

適用：`chapter_7_hanami_1`、`chapter_7_yumemi_1`、`chapter_7_hanami_2`、`chapter_7_yumemi_2`。

- 交卡：`SFX10_CARD_SLIDE`＋極淡 `SFX18_CARD_PULSE`。
- 進林道：依現行交戰起點播放 `BGM06_FOREST_ASSAULT`，不加森林循環底聲。
- 式神召喚 CG：`SFX21_INSECT_SUMMON`；CG 顯示後讓音尾延續，不連打四種怪聲。
- 土蜘蛛逼近：`SFX24_SPIDER_STEPS`＋單次 `SFX25_TSUCHIGUMO_HISS`。
- 髮切切入：`SFX28_KAMIKIRI_BLADES`。
- 大百足衝撞：`SFX29_OMUKADE_ARMOR` 預備、命中時 `SFX30_OMUKADE_IMPACT`。
- 花見薙刀：`SFX26_NAGINATA_WHOOSH`；命中甲殼才用 `SFX27_NAGINATA_HIT`。
- 絡新婦偷襲：`SFX22_SILK_WHISPER` → `SFX23_SILK_CUT`。
- 死亡路線：BGM 在傷勢確認後淡出，不加循環雨聲；倒下時 `SFX31_BODY_FALL`，不要加誇張低頻爆點。
- 「撕開」／時間回退：`SFX19_CARD_TEAR` 後以 `BGM01` 的不完整殘響或短暫全靜音銜接下一輪。

### 第八章／真結局（`chapter_8_choice`、`chapter_8_true_end`）

- 「把卡留給自己」：`SFX18_CARD_PULSE`，不要播放 UI 勝利音。
- 苦香強化：`SFX13_KISERU_IGNITE`＋`SFX21_INSECT_SUMMON`，BGM06 沿用已核可戰鬥主題；2026-10-12 生前實機確認同曲即可，取消獨立苦香強化變奏。
- 林間決戰：沿用第七章戰鬥 cue，不為重複動作新增相近素材。
- 「把香捏碎」：紙／乾草碎裂可由 `SFX08_PAPER_FOLD` 加工變體，第二批再決定是否新增。
- 驚蟄受創／咳血：只在關鍵一次使用 `SFX32_COUGH_BLOOD`；其餘讓表演與停頓承擔。
- 花見準備撕卡：`SFX18_CARD_PULSE` 拉長，驚蟄抓住手腕後中止；不要真的播放 `SFX19_CARD_TEAR`。
- 「夜色被撕開一條縫」：`SFX20_MAGIC_RIFT`，BGM06 停止，影之魔女登場後可短暫引用 `BGM04` 的黑卡動機。
- 「雨也回來了」：由文本與畫面表達，不加循環雨聲。
- 回月下庄：轉 `BGM07_DAWN_TOGETHER`。
- 清晨最後一句後：BGM 留尾，結局畫面才完整淡出。

## 6. UI 導入規則

- `UI01_CONFIRM`：主選單、設定、存讀檔、選項確認共用。
- `UI02_BACK`：返回／關閉選單共用。
- 預設不使用 hover 音；若未來實機確認需要，只能新增一個極輕 hover，不為每種按鈕做不同聲。
- 啟用音訊後，設定頁至少提供「音樂」「音效」兩條音量；配音導入時再增加「語音」。

## 7. 第一輪驗收標準

- 每個 BGM 循環點無爆音、斷裂或可察覺空白；非 BGM 循環環境音保持停用。
- 音效不遮住閱讀節奏；自動播放 15 秒設定下仍能自然前進。
- 同一 cue 在四條第七章路線中的相同事件保持一致。
- 主選單、日常、壓迫、戰鬥、死亡回退與真結局六個情緒區段可只靠聲音辨識。
- 音樂／音效音量設為 0 時完全靜音，存讀檔後不重複疊播循環音。
- Windows 獨立版乾淨啟動，音檔全數存在且 Ren’Py lint 無缺檔。

## 8. 場景批次製作與驗收（2026-10-12 生前核可）

每批先列動作聲、BGM 接續、觸發文字與留白；完成全部必要素材後，套入開發版並調整整段搭配，再從場景前開始連續試聽到事件後。依場景回饋修正並重聽，生前核可後才認列場景定案。共用素材後續改版需回查既有場景。

| 批次 | 場景範圍 | 目前狀態 |
| --- | --- | --- |
| 1 | 序章抵達、第一章日常與後院 | 六個動作音檔已獲完整場景核可，音效結案；環境停用、序章無 BGM，補配樂另議；[製作與起點](候選/BATCH01_ARRIVAL_DAILY/README.md) |
| 2 | 第二章夜間房內與魔法郵箱 | 待製作 |
| 3 | 第三章酒館與黑卡 | 待製作 |
| 4 | 第四至六章異常、受控與調查，多個短段落 | 待製作 |
| 5 | 第七章林間交戰 | 待製作 |
| 6 | 第七章返庄遇襲、死亡與回退 | 待製作 |
| 7 | 第八章苦香決戰至真結局 | 待製作 |

最後統整全篇與四條第七章路線、自動播放、快轉及存讀檔接續。素材生成、遊戲導入、場景核可分別記錄；不以單一音效的孤立播放代替場景驗收。
