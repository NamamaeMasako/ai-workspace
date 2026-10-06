# BGM02_MOON_INN_DAY 候選／定案紀錄

用途：第一章清晨、早餐、前後院與日常互動，以及第六章清晨短暫回歸日常的段落。

## 定案

- 2026-09-20：生前確認 `longform/bgm02_moon_inn_day_shakuhachi_long_04_smooth_continuity.ogg` 可採用並導入遊戲。
- 遊戲副本：`game/audio/music/bgm_moon_inn_day.ogg`，SHA-256 `B88DFE6E21D64C84449938F298EDC8CA2FAB9BD5A4572A33B863EF175649309D`。
- 第一章白天段落及第六章清晨後院／餐廳以 Ren'Py `music` 通道循環播放；入夜或進入調查段落時以 1.5 秒淡出。

共同方向：木質、輕柔、不甜膩的月下庄白天；不含環境音、無人聲、無流行節拍、無祭典感、無電影式堆疊或高潮。

## 候選

- `bgm02_moon_inn_day_candidate_01_seed2901.ogg`
  - Seed：2901
  - 箏主旋律；柔鋼琴、低弓弦與極克制木質打擊。
- `bgm02_moon_inn_day_candidate_02_seed2902.ogg`
  - Seed：2902
  - 琵琶主旋律；柔鋼琴、輕低音提琴與稀疏手作木質打擊。
- `bgm02_moon_inn_day_candidate_03_seed2903.ogg`
  - Seed：2903
  - 柔鋼琴主旋律；箏泛音、低弦與細緻木琴質地。
- `bgm02_moon_inn_day_candidate_04_seed2904.ogg`
  - Seed：2904
  - 尺八主旋律；稀疏箏、柔鋼琴、低弦與木質打擊。

## 共同參數

- ACE-Step 1.5 Turbo + 0.6B LM
- 20 秒、76 BPM、D major、4/4
- 44.1 kHz、立體聲 Vorbis OGG 審聽版
- WAV 母檔位於 `02_素材/音訊/母檔/BGM02_MOON_INN_DAY`

短候選階段已完成，最終沿 seed 2904 尺八方向延伸並定案為 `long_04`；其餘短候選僅供回溯。

## 已選方向的長版試作

- 生前選定候選 04（seed 2904）的尺八方向。
- 長版審聽檔：`longform/bgm02_moon_inn_day_shakuhachi_long_01_seed2904.ogg`
- 規格：60 秒、76 BPM、D major、4/4、44.1 kHz、立體聲 Vorbis OGG。
- 編排：尺八主旋律；稀疏箏、柔鋼琴、低弦與極克制木質打擊。
- WAV 母檔：`02_素材/音訊/母檔/BGM02_MOON_INN_DAY/longform/`

`long_01` 在約 25 秒後的節奏感偏重，保留作比較，不作定案。

## 節奏修正版

- 長版審聽檔：`longform/bgm02_moon_inn_day_shakuhachi_long_02_seed2904.ogg`
- 規格：60 秒、76 BPM、D major、4/4、44.1 kHz、立體聲 Vorbis OGG。
- 編排：保留尺八、稀疏箏、柔鋼琴與低弦；移除木質打擊、規律型低音與節拍型編排，改為較自由的呼吸與留白。
- WAV 母檔：`02_素材/音訊/母檔/BGM02_MOON_INN_DAY/longform/`

`long_01`、`long_02` 均未採用，保留作為節奏修正歷程。

## 月下庄風格重構版（澪候選）

- 長版審聽檔：`longform/bgm02_moon_inn_day_shakuhachi_long_03_seed2904.ogg`
- 規格：60 秒、68 BPM、D major、4/4、44.1 kHz、立體聲 Vorbis OGG。
- 編排：尺八改為偶爾出現的呼吸式點綴；主體使用柔鋼琴單音、極稀疏箏泛音／孤立撥音與近乎靜止的柔和低弦。
- 動態：全曲維持安靜、疏落與近似自由速度的留白；禁止後半段增加打擊、規律低音、固定節拍、漸進堆疊或高潮。
- 場景意象：柔和晨光中的小型木造旅店，有生活溫度但不喧鬧；作為視覺小說日常對話底樂，不搶台詞。
- 生成：ACE-Step 1.5 Turbo + 0.6B LM，8 steps，固定 seed 2904；未使用格式重寫。
- WAV 母檔：`02_素材/音訊/母檔/BGM02_MOON_INN_DAY/longform/bgm02_moon_inn_day_shakuhachi_long_03_seed2904.wav`

此版未採用，保留作為 `long_04` 的修補基準。

## 斷點銜接修正版（澪；正式採用）

- 長版審聽檔：`longform/bgm02_moon_inn_day_shakuhachi_long_04_smooth_continuity.ogg`
- 基準：完整保留 `long_03` 的編曲、速度、音色與整體動態。
- 修正：針對約 4 秒與 33 秒附近突然降至近乎靜音的樂句斷點，僅在低音量區疊入柔化、低通的既有尾音，使鋼琴與低弦自然延續；未重新生成整首，也未增加打擊、固定節拍或新旋律。
- 規格：60 秒、44.1 kHz、立體聲 Vorbis OGG。
- WAV 母檔：`02_素材/音訊/母檔/BGM02_MOON_INN_DAY/longform/bgm02_moon_inn_day_shakuhachi_long_04_smooth_continuity.wav`

此版已正式採用並導入遊戲；遊戲端以 Ren'Py 音樂通道循環，不另改編曲或增加節奏。後續僅在確認首尾回接有技術性爆音、斷裂時按 bug 修正。
