# BGM07 箏與微光長版試聽

2026-10-12：生前喜歡第一版與主選單呼應的「回歸主題」感，選定 take01 第一首「箏與微光」製作長版。已完成 60 秒審聽版，待生前確認。

## 場景與方向

真結局重聚後回到月下庄、三人的影子靠近、一起走到明天，延續至清晨最後的煙斗苦味。以選中短版引導熟悉的主題回歸，探索劫後安定、仍帶餘痛的溫柔陪伴；避免歡樂跳躍或凱旋高潮。實際配器、主題辨識與收束感仍由生前試聽判斷。

- 長版：[long_01_phrase_guided_lantern_guzheng_seed3401.ogg](long_01_phrase_guided_lantern_guzheng_seed3401.ogg)
- 原短版：[01 箏與微光](../candidate_01_lantern_guzheng_seed3401_take01.ogg)

## 參考與製作

- 將選中 BGM07 第一首短版實際以 multipart `reference_audio` 上傳，完整檔名與 SHA-256 記於同名 JSON。
- 同時用短版樂句組成 65 秒 source template 作 `src_audio` 上傳：0／19／38／57 秒回歸，交疊 1 秒。這是固定時間的樂句編排參考，不代表已量測實際拍點或證明拍點吻合。
- ACE-Step 1.5 Turbo cover、thinking=false、8 steps、seed 3401、audio_cover_strength=1.0、cover_noise_strength=0.65；72 BPM、D minor、4/4 延用短版生成提示，不是實測保證。延伸指示維持箏主題、柔和音符間距與克制伴奏，只作小幅和聲／配器變化。
- 原始生成 65 秒；審聽版前 18 秒保留選中短版內容，18–19 秒與生成長版交疊，19 秒後使用生成後段，取 60 秒並在末尾 0.5 秒淡出。
- 組合時核對前 18 秒為原短版解碼樣本乘以一致增益；接續段先匹配音量，再處理全曲固定增益及 -2.5 dBFS 峰值限制、延遲補償與連續時間戳。最後音量處理可能限制局部峰值，不重新生成前段內容。
- source template、原始 WAV、premaster WAV 與審聽 WAV 位於 `@/workspace/10_作品與專案/驚蟄/02_素材/音訊/母檔/BGM07_DAWN_TOGETHER/longform/`。本資料夾保留 OGG、premaster OGG、完整請求與處理紀錄、generation_manifest_long_01.json、technical_check_long_01.json。

## 技術結果與下一步

全部 WAV／OGG 完整解碼成功，無錯誤輸出。最終 OGG 為 44.1 kHz 立體聲、60.000000 秒，實測 -16.10 LUFS／-2.05 dBTP。未偵測到低於 -45 dB 且持續至少 0.5 秒的近靜音。

目前是長版候選。待生前確認主題回歸感、18–19 秒接續與後段情緒，再處理循環及開發版場景試聽。
