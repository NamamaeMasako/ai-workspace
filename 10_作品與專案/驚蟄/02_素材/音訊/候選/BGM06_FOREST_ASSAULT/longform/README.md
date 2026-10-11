# BGM06 弦鼓追殺長版試聽

2026-10-11：生前選定 take03 第三版「弦鼓追殺」。60 秒長版已獲核可，循環副本已接入開發遊戲，待場景與循環聽感確認。

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

技術檢查不代替聽感判斷。長版已核可，循環與開發遊戲配置見下節；苦香強化變體待後續決定。

## 2026-10-11 長版選定與開發遊戲試聽

生前回覆「可以，就這版」，確認採用 long_01 弦鼓追殺長版。已沿用核可的 WAV 製作循環副本，不重新生成或改配器；遊戲場景與循環聽感仍待生前實機確認。

- 循環副本：[long_01_phrase_guided_pursuit_strings_seed3323_loop_intro.ogg](long_01_phrase_guided_pursuit_strings_seed3323_loop_intro.ogg)，同名 JSON 保存來源與處理紀錄；WAV 位於對應母檔 longform。
- 前 56.5714375 秒逐樣本保留核可審聽 WAV，最大誤差 0；末尾 3.4285625 秒與原開頭以 smoothstep 凸組合交疊。首次播放 60 秒，之後 `<loop 3.4285625>` 回接，週期 56.5714375 秒。週期參照三個 source-template 樂句，並非已量測的實際拍點保證。
- OGG 44.1 kHz 立體聲、60 秒；完整解碼成功，-16.04 LUFS／-2.09 dBTP，未偵測到低於 -45 dB 且持續 0.5 秒以上的近靜音。SHA-256 `fe1d4cd1a7aefd2b63cae15d9be7cece88597c4623f56981b309a4f5d91f2271`。
- 遊戲副本 `@/workspace/10_作品與專案/驚蟄/03_開發/JingZhe/game/audio/music/bgm_forest_assault.ogg`，與候選 OGG 雜湊相同；music 通道沿用設定音量，交戰起點 0.5 秒淡入、離開戰鬥 1.5 秒淡出。
- 第七章四條林間路線在髮切／大百足出手時播放；花見路線切回月下庄時淡出，返庄門口反擊時再起，反擊結束淡出。夢見路線維持至髮切追殺絡新婦結束，再於戰後對話前淡出。第八章在林間決戰第一波鐮光時播放，最後敵人倒下、驚蟄跪下前淡出；本輪苦香段沿用核可主題，獨立強化變體尚未製作。
- 已用現有本機 RenPy 引擎指定開發 basedir，`--warp script.rpy:1122` 開到第七章土蜘蛛交戰 CG；畫面顯示髮切先衝上去的台詞，無錯誤畫面。實機回報新檔正在播放、音樂音量 1.0、未靜音；記錄見 runtime_observation_long_01_loop.json。未重建發行包或升版。
