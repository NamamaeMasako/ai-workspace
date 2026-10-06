# BGM03_MOON_INN_NIGHT 長版候選／定案紀錄

用途：第二章房內，以及第四至六章的月下庄夜間。

共同方向：承接主題的稀薄夜間變奏；安靜、微冷，容納一點不安。無人聲、無鼓／打擊、無規律型節奏、無環境音、無電影式堆疊或高潮。

## 本次候選（2026-09-21）

共同參數：ACE-Step 1.5 Turbo + 0.6B LM、64 BPM、D minor、4/4、60 秒；WAV 母檔為 48 kHz 立體聲，審聽版為 44.1 kHz 立體聲 Vorbis OGG。

| 檔案 | 主導方向 | Seed |
| --- | --- | --- |
| `long_01_felt_piano_seed3003.ogg` | 柔鋼琴、箏泛音與低弦 | 3003 |
| `long_02_muted_erhu_seed3004.ogg` | 悶音二胡、箏泛音與低弦 | 3004 |

鋼琴請求額外產生了一個未指定 seed 的 API 暫存備份；本資料夾只保留固定 seed `3003` 的第一個輸出。

## 定案

- 2026-09-21：先採用 `long_01_felt_piano_seed3003.ogg` 進行遊戲實測；確認頭尾直接回接不自然後，改採 `long_01_felt_piano_seed3003_loop_xfade06.ogg` 為正式循環版。
- 遊戲副本：`game/audio/music/bgm_moon_inn_night.ogg`，SHA-256 `6D8E71ECD6F65C906D778F6B755AE7B474CFB7782ED71763C03714E8B10D6590`。
- 原始 60 秒鋼琴版與 `long_02_muted_erhu_seed3004.ogg` 均保留供回溯，不再作遊戲正式副本。

## 循環實測修正

- 2026-09-21：遊戲內循環實測確認原曲頭尾無法自然銜接。
- `long_01_felt_piano_seed3003_loop_xfade06.ogg`：保留原曲內容，將尾端 6 秒與開頭 6 秒交叉淡化；循環版從原曲第 6 秒開始，並在尾端回到同一位置，長度 54 秒。
- 生前指定改用此版後，已覆蓋正式遊戲副本；腳本沿用穩定檔名 `bgm_moon_inn_night.ogg`，播放位置不變。
