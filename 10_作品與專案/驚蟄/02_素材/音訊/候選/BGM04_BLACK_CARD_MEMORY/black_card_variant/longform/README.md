# BGM04 黑卡變體長版

- 檔案：`long_01_muted_accordion_black_card_seed3111.ogg`
- 用途：黑卡登場後由酒館底曲淡切進來的緊張層。
- 生成：ACE-Step 1.5 Turbo + 0.6B LM，seed `3111`，60 秒，68 BPM，E minor，4/4。
- 編排：手風琴殘影、低音大提琴／低音提琴延音、稀疏不協和柔鋼琴。
- 排除：人聲、鼓、打擊、規律低音、ostinato、環境音、高潮。
- 狀態：候選，尚未製作循環或導入遊戲。

## long_02（2026-09-23）

- 檔案：`long_02_reference_guided_muted_accordion_black_card_seed3111.ogg`
- 參考短版：`bgm04_black_card_variant_muted_accordion_seed3111.wav`（20 秒）。
- 生成：ACE-Step 1.5 Turbo，以短版作 `reference_audio`，`audio_cover_strength=0.35`，seed `3111`，60 秒，68 BPM，E minor，4/4。
- 目的：延長同一個黑卡變體；保留手風琴殘影與貼近室內的質感，只用延音低弦和稀疏不協和柔鋼琴增加緊張，不改成另一首曲子。
- 音量：長版原始生成比已選短版高約 4.51 dB；候選已等量降益至短版 RMS，原始 WAV 另存為 `long_02_reference_guided_muted_accordion_black_card_seed3111_raw.wav`。
- 規格：WAV 母檔 48 kHz／立體聲／60 秒；OGG 候選 44.1 kHz／立體聲／60 秒。
- 狀態：已複製為 `game/audio/music/bgm_black_card_memory_variant.ogg` 進行黑卡登場後實機試聽；Ren'Py 以 `music` 通道循環，待生前確認頭尾與場景適配後再定案。

## long_03（2026-09-23）

- 檔案：`long_03_immediate_suspense_intro_seed3112.ogg`
- 基底：`long_02_reference_guided_muted_accordion_black_card_seed3111.wav`。
- 新前奏來源：以已選黑卡短版作聲音參考，ACE-Step 1.5 Turbo，seed `3112`，生成 14 秒立即懸疑的手風琴／低弦／稀疏不協和柔鋼琴前奏。
- 修正：0 秒即出現未解決的手風琴短句與低弦暗流；前 10.8 秒使用新前奏，10.8–12.0 秒柔順交疊，12 秒後與 `long_02` 逐樣本相同。
- 排除：暖調中性開場、開頭留白、恐怖突刺、人聲、鼓與打擊、規律節拍、電影式高潮。
- 規格：WAV 母檔 48 kHz／立體聲／60 秒；OGG 候選 44.1 kHz／立體聲／60 秒。
- 狀態：懸疑開場候選，尚未替換遊戲內 `long_02` 測試檔。

## long_04（2026-10-02）

- 檔案：`long_04_black_key_suspense_no_gap_seeds3113_3114.ogg`
- 修正目標：移除 `long_03` 約 8–10 秒接近無聲的空洞，並讓開頭以鋼琴黑鍵帶來的半音摩擦、未解決增四度與低 E 持續音加強懸疑感。
- 前奏來源：以已選黑卡短版作聲音參考，ACE-Step 1.5 Turbo、無 5Hz LM；seed `3113` 生成 14 秒版本，seed `3114` 生成 20 秒持續演奏版本。
- 組接：使用 seed `3113` 的 0–6.5 秒與 seed `3114` 的 5.5–12 秒，在 5.5–6.5 秒做 1 秒等功率交疊；兩段均降低 4.5 dB 對齊 `long_02`。10.8–12.0 秒再等功率交疊回 `long_02`。
- 連續性：前 12 秒未偵測到低於 -45 dB 且持續 0.25 秒以上的靜音；原本 8–9／9–10 秒平均音量約 -43.8／-58.9 dB，修正後約 -20.5／-21.7 dB。
- 保留範圍：12 秒後與 `long_02_reference_guided_muted_accordion_black_card_seed3111.wav` 的 PCM SHA-256 完全相同，未改動後段編曲。
- 規格：WAV 母檔 48 kHz／立體聲／60 秒；OGG 候選 44.1 kHz／立體聲／60 秒。
- SHA-256：WAV `6090F874231C0F10BCECCB840AF0E50DF592589BD4DA162552803E217B10C6BE`；OGG `B6083F22E2D5044D22FDF09196B887F05696FED06007A5498E2C8F8100738727`。
- 狀態：依 2026-10-02 回饋製作的黑鍵懸疑版；同日替換遊戲內同名黑卡變體副本並由生前實機試聽確認採用。
