# BGM04 酒館底曲長版

- 檔案：`long_01_muted_accordion_seed3101.ogg`
- 用途：小酒館進場至黑卡出現前的基礎 BGM。
- 生成：ACE-Step 1.5 Turbo + 0.6B LM，seed `3101`，60 秒，68 BPM，E minor，4/4。
- 編排：悶音手風琴主旋律、柔和雙低音、稀疏柔鋼琴；維持室內回憶感與距離感。
- 排除：人聲、鼓、打擊、明顯節拍、ostinato、環境音、高潮。
- 狀態：候選，尚未製作循環或導入遊戲。

## long_02（2026-09-23）

- 檔案：`long_02_reference_guided_muted_accordion_seed3101.ogg`
- 參考短版：`candidate_01_muted_accordion_seed3101.wav`（20 秒）。
- 生成：ACE-Step 1.5 Turbo，以短版作 `reference_audio`，`audio_cover_strength=0.35`，seed `3101`，60 秒，68 BPM，E minor，4/4。
- 目的：修正 `long_01` 只靠文字與 seed 重生、和短版風格偏離的問題；維持悶音手風琴、柔和雙低音、稀疏柔鋼琴與貼近室內的回憶感。
- 規格：WAV 母檔 48 kHz／立體聲／60 秒；OGG 候選 44.1 kHz／立體聲／60 秒。
- 狀態：已複製為 `game/audio/music/bgm_black_card_memory.ogg` 進行第三章酒館底曲實機試聽；Ren'Py 以 `music` 通道循環，待生前確認頭尾與場景適配後再定案。

## long_03（2026-09-23）

- 檔案：`long_03_seamless_loop_muted_accordion_seed3101.ogg`
- 來源：`long_02_reference_guided_muted_accordion_seed3101.wav`。
- 修正：按 68 BPM 取一小節（約 3.529 秒）作等功率首尾交疊，將交疊區移入曲內，使檔案尾端接回開頭時沿著原波形與樂句連續。
- 內容：未重新生成或更換配器；除循環接縫外維持 `long_02` 的酒館底曲內容。
- 規格：WAV 母檔 48 kHz／立體聲／約 56.47 秒（16 小節）；OGG 候選 44.1 kHz／立體聲／約 56.47 秒。
- 狀態：2026-10-02 替換遊戲內同名酒館底曲副本並由生前實機試聽確認採用；SHA-256 `65D1906A7B0C43EF234F7FCAACD93EB27067EBA78E32FA03CBE811A5F47AFF8A`。
