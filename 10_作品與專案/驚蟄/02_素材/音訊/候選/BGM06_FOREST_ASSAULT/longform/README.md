# BGM06 弦鼓追殺長版試聽

2026-10-11：生前選定 take03 第三版「弦鼓追殺」。已完成一首約 60 秒長版，待確認延伸段的緊迫感、前後節奏與銜接；尚未正式定案。

## 場景與方向

第七章式神與土蜘蛛已經交戰、第八章林間決戰；延續選中短版的弦鼓推進與陰暗危險感，支撐追擊、連續攻防和搏命。實際場景適配仍由生前試聽判斷。

- 試聽：[long_01_phrase_guided_pursuit_strings_seed3323.ogg](long_01_phrase_guided_pursuit_strings_seed3323.ogg)
- 原短版：[03 弦鼓追殺](../candidate_03_pursuit_strings_seed3323_take03.ogg)

## 參考與製作

- 將選中短版以 multipart `reference_audio` 實際上傳；完整來源檔名與 SHA-256 記於同名 JSON。
- 同時以短版樂句組成 65 秒 source template，作為 `src_audio` 上傳，固定樂句回歸、避免接續段另換節奏。樂句週期約 18.857 秒、交疊約 1.143 秒，按 140 BPM 生成提示估算 11 小節；此為編排參考，不代表已量測原曲實際速度或證明拍點吻合。
- ACE-Step 1.5 Turbo cover、thinking=false、8 steps、seed 3323、audio_cover_strength=1.0、cover_noise_strength=0.65。延伸指示維持原弦鼓密度與迫切感、避免慢速中段及明亮凱旋。
- 原始生成 65 秒；審聽版前 18 秒保留短版內容，18–19 秒與生成長版交疊，19 秒後沿用生成後段，取總長 60 秒並在末尾 0.5 秒淡出。
- 先匹配接續音量，再作固定增益和 -2.5 dBFS 峰值限制、延遲補償；保留處理前 WAV／OGG。前 18 秒組合時已核對為原短版解碼樣本乘以全曲一致增益；最後音量處理可能限制局部峰值，不重新生成前段內容。
- source template、65 秒原始 WAV、60 秒 premaster／審聽 WAV 存於 `@/workspace/10_作品與專案/驚蟄/02_素材/音訊/母檔/BGM06_FOREST_ASSAULT/longform/`。本資料夾保留 OGG、完整請求與處理紀錄、generation_manifest_long_01.json、technical_check_long_01.json。

## 技術結果與下一步

WAV／OGG 均完整解碼成功；OGG 為 44.1 kHz 立體聲、60.000000 秒，實測 -16.05 LUFS／-2.09 dBTP。未偵測到低於 -45 dB 且持續至少 0.5 秒的近靜音。

技術檢查不代替聽感判斷。待生前確認長版後，再處理循環與開發版場景試聽；苦香強化段待主題確立再延伸。
