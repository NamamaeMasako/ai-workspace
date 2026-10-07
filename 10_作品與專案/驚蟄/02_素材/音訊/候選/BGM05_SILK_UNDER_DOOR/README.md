# BGM05_SILK_UNDER_DOOR 短版候選

用途：第四章怪物逼近、第五章受控、第六章調查。

狀態：2026-10-07 四首 20 秒短版候選完成，待生前挑選；本輪只提供配器方向試聽，選定後再製作長版。

## 共同方向

安靜木造旅店裡逐步逼近的異常：細碎、壓迫、不自然的安靜，使用未解決音程與克制的音色變化。全段維持低動態，不提前進入完整戰鬥節奏。純音樂；不含人聲、鼓／打擊、規律節拍、固定反覆型、突發大音量、驚嚇音效、電影式堆疊、高潮或環境音。

## 本輪候選

| 編號 | OGG 檔名 | 主導配器 | Seed |
| --- | --- | --- | --- |
| 01 | `candidate_01_felt_piano_seed3201_take02.ogg` | 柔鋼琴、微弱低弦、遠弦泛音 | 3201 |
| 02 | `candidate_02_bass_clarinet_seed3202_take02.ogg` | 低音單簧管、悶音大提琴泛音、稀疏鋼琴 | 3202 |
| 03 | `candidate_03_muted_strings_seed3203_take02.ogg` | 悶音中提琴／大提琴、細絲般不協和、遠鋼琴 | 3203 |
| 04 | `candidate_04_guzheng_harmonics_seed3204_take02.ogg` | 箏泛音、稀疏撥弦、微弱低弦與柔鋼琴 | 3204 |

## 生成與檔案規格

- ACE-Step 1.5 `acestep-v15-turbo` + `acestep-5Hz-lm-0.6B`，8 steps，`thinking=true`。
- 第二輪生成 25 秒、64 BPM、E minor、4/4；每次只產生一個固定 seed 輸出，試聽版取前 20 秒。
- `use_format=false`、`use_cot_caption=false`、`use_cot_language=false`，保留人工撰寫的配器方向。
- 原始 WAV 母檔：`@/workspace/10_作品與專案/驚蟄/02_素材/音訊/母檔/BGM05_SILK_UNDER_DOOR/`；本輪使用同名 `_take02.wav`，25 秒、48 kHz、立體聲。
- OGG 試聽版：本資料夾；取前 20 秒，開頭 30 ms 淡入、結尾 0.5 秒淡出，44.1 kHz、立體聲、Vorbis q5；單次響度正規化，目標 -16 LUFS、true peak -1.5 dBTP。
- 完整提示詞、請求參數、結果資訊、實際時長與 SHA-256 保存在各候選同名 JSON，彙整至 `generation_manifest_take02.json`。
- 四首均已完整解碼核對，時長皆為 20 秒；未偵測到低於 -45 dB 且持續至少 0.5 秒的近靜音區段。實測響度為 -16.58 至 -15.34 LUFS，true peak 為 -1.39 至 -1.23 dBTP，詳見 `technical_check_take02.json`。此為技術檢查，配器與情緒仍待生前試聽確認。
- 本輪只做固定截取與邊界淡化，未處理無縫循環，也尚未導入遊戲。

## 初版保留與修正紀錄

首輪以相同提示詞與 seed 生成 20 秒，但四首末端均有約 5 秒近靜音，故第二輪延長生成至 25 秒，再取前 20 秒作為本次試聽版。首輪無 `_take02` 後綴的 WAV、OGG 與 JSON 全數保留；紀錄為 `generation_manifest.json` 與 `technical_check.json`，不作本輪推薦試聽版本。

## 後續流程

生前選定短版後，將該短版作為長版的參考音訊；相同 seed 不等於沿用短版旋律。長版完成後才處理首尾循環及技術性斷點，再放入 `03_開發/JingZhe` 實機試聽，確認後定案。

## 本機生成環境

本次使用澪這台 Windows 設備的既有安裝：`F:\AI\ACE-Step-1.5`、RTX 3080 10 GB，以及本機 FFmpeg。ACE-Step API 僅綁定本機 `127.0.0.1:8001`；此安裝路徑是本機環境紀錄，不是跨設備共用路徑。
