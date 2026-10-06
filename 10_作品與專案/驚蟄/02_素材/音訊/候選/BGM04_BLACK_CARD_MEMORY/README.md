# BGM04_BLACK_CARD_MEMORY 候選

用途：第三章小酒館回憶、黑卡與郵箱說明。

## 遊戲導入與採用（2026-10-02）

- 酒館底曲：`longform/long_03_seamless_loop_muted_accordion_seed3101.ogg`，遊戲副本 `game/audio/music/bgm_black_card_memory.ogg`，SHA-256 `65D1906A7B0C43EF234F7FCAACD93EB27067EBA78E32FA03CBE811A5F47AFF8A`。
- 黑卡變體：`black_card_variant/longform/long_04_black_key_suspense_no_gap_seeds3113_3114.ogg`，遊戲副本 `game/audio/music/bgm_black_card_memory_variant.ogg`，SHA-256 `B6083F22E2D5044D22FDF09196B887F05696FED06007A5498E2C8F8100738727`。
- 第三章進入小酒館時播放底曲；全黑卡片出現在桌上時以 1.5 秒交叉淡切至黑卡變體；進第四章時再交叉淡切回月下庄夜間曲。
- 兩首皆由 `music` 通道循環，沿用設定頁「音樂音量」控制。生前實機試聽後回覆「兩首都可以」，此兩版與目前遊戲配置採用定案；不以 lint 代替主觀聽感。尚未重建 Windows 發行包或升版。

共同方向：疏離、神祕、略帶異國色彩的室內記憶感；與月下庄夜間的留白不同，保持較近的房間質地，但不變成舞曲、驚悚高潮或環境音。

## 本次試作紀錄（2026-09-21）

共同參數：ACE-Step 1.5 Turbo + 0.6B LM、68 BPM、E minor、4/4、20 秒；無人聲、無鼓／打擊、無明顯節拍、無電影式堆疊或高潮。WAV 母檔為 48 kHz 立體聲，審聽版為 44.1 kHz 立體聲 Vorbis OGG。

| 檔案 | 主導方向 | Seed |
| --- | --- | --- |
| `candidate_01_muted_accordion_seed3101.ogg` | 悶音手風琴、低音提琴、柔鋼琴 | 3101 |
| `candidate_02_low_clarinet_seed3102.ogg` | 低音單簧管、揚琴觸點、低音提琴 | 3102 |
| `candidate_03_dulcimer_seed3103.ogg` | 揚琴、悶音大提琴、遠鋼琴殘響 | 3103 |
| `candidate_04_oud_seed3104.ogg` | 烏德琴、手風琴陰影、低音提琴 | 3104 |

短候選及 `long_02` 長版保留供回溯；2026-09-23 的 `long_02` 遊戲試聽未通過，後續改以 `long_03`／`long_04` 導入，生前於 2026-10-02 確認採用。

## 回饋修正版（2026-10-02）

- 酒館底曲：生前確認 `longform/long_03_seamless_loop_muted_accordion_seed3101.ogg` 目前試聽可用，暫不再修改。
- 黑卡變體：新增 `black_card_variant/longform/long_04_black_key_suspense_no_gap_seeds3113_3114.ogg`，修除約 8–10 秒的近靜音空洞，並以黑鍵鋼琴的半音摩擦與未解決音程加強開頭懸疑感。
- 2026-10-02 已依生前指示以 `long_03`／`long_04` 取代遊戲內舊 `long_02` 副本，實機試聽後由生前確認採用。
