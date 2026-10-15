# BGM10「返路不安」長版 long_01

2026-10-16：生前要求第四首 take02 做成長版。已完成 60 秒長版，待試聽；尚未正式採用、處理循環或導入遊戲。

## 使用場景與方向

用於第七章花見同行路線的月下庄屋內搜尋、夢見遇襲，以及回到森林後花見持續不安、返回月下庄的途中。維持選中短版低沉音樂底層、稀疏鋼琴音型與未解脈動；實際交戰另切 BGM06，死亡悲痛另由 BGM11 規劃。

## 實際參考與來源

- `reference_audio` 實際上傳：`../candidate_04_piano_dark_pulse_seed3714_take02.ogg`，SHA-256 `00a2c4f8db1dd5ebeb1f1006782b2fc03974ab3b2448d45c7f21392ada543fb5`。
- 自然尾音來源：同版本未淡出的原始 25 秒 `candidate_04_piano_dark_pulse_seed3714_take02_raw.wav`，SHA-256 `811626399a45043b7762c7371b312f16a74fabbef6bad99d3a3e6de1633cf8bd`。
- 65 秒 `src_audio` 以原始母檔前 24.5 秒為樂句範圍，23.75 秒週期、0.75 秒 smoothstep 交疊，起點為 0／23.75／47.5 秒。尾段依波形能量衰減選取，是固定時間模板，並非實測拍點。
- 外部魔王魂音檔未參與上傳、模板、取樣或訓練；長版只引用本專案自行生成並由生前選定的第四首。

## 生成與組合

- 本機 ACE-Step 1.5 Turbo，`cover`、`thinking=false`、8 steps、seed 3714、`audio_cover_strength=1.0`／`cover_noise_strength=0.55`。
- 62 BPM、E minor 與配器均為提示，非實測或保證。
- 保留短版前 18 秒；18–19 秒交疊回同版未淡出母檔，讓 20 秒處的原音繼續自然延伸；23.75–24.5 秒交疊至生成後段。
- 取總長 60 秒，尾端 0.5 秒淡出供審聽。固定增益與峰值限制整理音量，輸出 48 kHz float WAV、44.1 kHz 立體聲 Vorbis OGG。
- 原始生成、來源模板、premaster、母檔、完整請求／回應、SHA-256、解碼與音量紀錄均保存。
- 可編輯製作程式：`../../../母檔/BGM10_INN_HUNTED/longform/produce_long_01_natural_phrase.py`。需已啟動的本機 ACE-Step API、Python／numpy、ffmpeg／ffprobe；不覆寫既有輸出。

## 待確認

長版的陰森感、稀疏程度、前後節奏及尾音銜接由生前試聽確認；本輪不宣稱已人耳審聽。選中短版不等於長版或遊戲場景核可。

## 成品與量測

- 試聽：`long_01_natural_phrase_piano_dark_pulse_seed3714.ogg`（60 秒、44.1 kHz 立體聲）。
- 音量：-16.13 LUFS；真峰值 -2.37 dBTP；完整解碼無錯誤輸出。
- 低於 -45 dB 且持續至少 0.5 秒的區間：34.31–34.95 秒（約 0.64 秒）、58.05–58.70 秒（約 0.65 秒）。保留這兩處短暫空隙，音樂呼吸與聽感待生前確認。
- 詳細數據見 `technical_check_long_01.json`，請求／來源與處理紀錄見 `generation_manifest_long_01.json`。
