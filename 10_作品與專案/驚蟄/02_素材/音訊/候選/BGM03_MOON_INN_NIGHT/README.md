# BGM03_MOON_INN_NIGHT 候選／定案紀錄

用途：第一章傍晚、第二章房內，以及第四至六章的月下庄夜間。

## 定案

- 2026-09-21：先以 `longform/long_01_felt_piano_seed3003.ogg` 導入實測；確認頭尾直接回接不自然後，改採 `longform/long_01_felt_piano_seed3003_loop_xfade06.ogg` 為正式版。
- 正式循環版長 54 秒：保留原曲內容，尾端 6 秒與開頭 6 秒交叉淡化，播放起點對應原曲第 6 秒；2026-09-21 生前在遊戲第一章傍晚大廳實際聽過循環後確認沒問題。
- 遊戲副本：`game/audio/music/bgm_moon_inn_night.ogg`，SHA-256 `6D8E71ECD6F65C906D778F6B755AE7B474CFB7782ED71763C03714E8B10D6590`。
- 以 Ren'Py `music` 通道循環播放；從日間曲切入時交叉淡化，離開月下庄夜間日常或進入尚未配樂的異場景時以 1.5 秒淡出。

共同方向：承接作品主題的稀薄夜間變奏；安靜、微冷，可容納不安感。無人聲、無明顯節拍、無環境音、無電影式堆疊或高潮。

## 候選方向

- `candidate_01_seed3001`：箏泛音主導。
- `candidate_02_seed3002`：尺八主導。
- `candidate_03_seed3003`：柔鋼琴主導。
- `candidate_04_seed3004`：二胡主導。

短候選均為 20 秒、44.1 kHz、立體聲 Vorbis OGG；WAV 母檔位於 `02_素材/音訊/母檔/BGM03_MOON_INN_NIGHT`。其中柔鋼琴 seed 3003 已延伸為 60 秒長版並正式導入遊戲，其餘短候選僅供回溯。

## 本次試作紀錄（2026-09-21）

共同參數：64 BPM、D minor、4/4、20 秒、ACE-Step Turbo + 0.6B LM；無人聲、無鼓／打擊、無規律型節奏、無環境音、無電影式堆疊或高潮。

| 檔案 | 主導方向 | Seed |
| --- | --- | --- |
| `candidate_01_guzheng_harmonics_seed3001.ogg` | 箏泛音 | 3001 |
| `candidate_02_shakuhachi_seed3002.ogg` | 尺八 | 3002 |
| `candidate_03_felt_piano_seed3003.ogg` | 柔鋼琴 | 3003 |
| `candidate_04_muted_erhu_seed3004.ogg` | 悶音二胡 | 3004 |

所有候選的 WAV 母檔已保留；柔鋼琴 seed 3003 長版已定案，其他版本僅供回溯。
