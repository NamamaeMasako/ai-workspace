# BGM04_BLACK_CARD_MEMORY 候選

用途：第三章小酒館回憶、黑卡與郵箱說明。

## 遊戲試聽導入（2026-09-23）

- 酒館底曲：`longform/long_02_reference_guided_muted_accordion_seed3101.ogg`，遊戲副本 `game/audio/music/bgm_black_card_memory.ogg`，SHA-256 `138B4FDA08A5D5CBAD712938C19B0361C5065CB5CBA9DF225637DCAAFED4C419`。
- 黑卡變體：`black_card_variant/longform/long_02_reference_guided_muted_accordion_black_card_seed3111.ogg`，遊戲副本 `game/audio/music/bgm_black_card_memory_variant.ogg`，SHA-256 `7EA69015C8487D71CBC5BE2C2193EC01F608818BC67315C0137383DCAAA6D12A`。
- 第三章進入小酒館時播放底曲；全黑卡片出現在桌上時以 1.5 秒交叉淡切至黑卡變體；進第四章時再交叉淡切回月下庄夜間曲。
- 兩首皆由 `music` 通道循環，沿用設定頁「音樂音量」控制。目前為實機試聽配置，待生前聽過後決定是否正式定案；尚未聲稱無縫循環。

共同方向：疏離、神祕、略帶異國色彩的室內記憶感；與月下庄夜間的留白不同，保持較近的房間質地，但不變成舞曲、驚悚高潮或環境音。

## 本次試作紀錄（2026-09-21）

共同參數：ACE-Step 1.5 Turbo + 0.6B LM、68 BPM、E minor、4/4、20 秒；無人聲、無鼓／打擊、無明顯節拍、無電影式堆疊或高潮。WAV 母檔為 48 kHz 立體聲，審聽版為 44.1 kHz 立體聲 Vorbis OGG。

| 檔案 | 主導方向 | Seed |
| --- | --- | --- |
| `candidate_01_muted_accordion_seed3101.ogg` | 悶音手風琴、低音提琴、柔鋼琴 | 3101 |
| `candidate_02_low_clarinet_seed3102.ogg` | 低音單簧管、揚琴觸點、低音提琴 | 3102 |
| `candidate_03_dulcimer_seed3103.ogg` | 揚琴、悶音大提琴、遠鋼琴殘響 | 3103 |
| `candidate_04_oud_seed3104.ogg` | 烏德琴、手風琴陰影、低音提琴 | 3104 |

短候選本身保留供回溯；reference-guided `long_02` 長版目前已做遊戲試聽導入，正式定案待實機聽感確認。

## 回饋修正版（2026-10-02）

- 酒館底曲：生前確認 `longform/long_03_seamless_loop_muted_accordion_seed3101.ogg` 目前試聽可用，暫不再修改。
- 黑卡變體：新增 `black_card_variant/longform/long_04_black_key_suspense_no_gap_seeds3113_3114.ogg`，修除約 8–10 秒的近靜音空洞，並以黑鍵鋼琴的半音摩擦與未解決音程加強開頭懸疑感。
- `long_04` 尚未替換遊戲內的 `long_02` 試聽副本，待生前確認後再導入。
