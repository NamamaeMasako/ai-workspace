# BGM07 箏與微光長版試聽

2026-10-12：生前喜歡第一版與主選單呼應的「回歸主題」感，選定 take01 第一首「箏與微光」製作長版。60 秒長版已核可，循環副本已導入開發遊戲，生前實機確認後正式定案。

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

長版已核可，循環及開發遊戲配置見下節；待生前確認實機場景與循環聽感。

## 2026-10-12 長版核可與開發版場景試聽

生前回覆「好，就用這版」，核可 long_01 箏與微光長版。循環副本已導入開發遊戲，待生前確認循環與結局場景聽感。

- 循環副本：[long_01_phrase_guided_lantern_guzheng_seed3401_loop_intro.ogg](long_01_phrase_guided_lantern_guzheng_seed3401_loop_intro.ogg)，同名 JSON 保存來源雜湊與處理紀錄；無損 WAV 存於對應母檔 longform。
- 沿用核可 WAV，不重新生成或改配器。前 57 秒逐樣本保留，最大 PCM 誤差 0；末尾 3 秒與原開頭作 smoothstep 凸組合交疊。首次播放 60 秒，之後 `<loop 3.0>` 回接，重複週期 57 秒；週期參照三個固定 19 秒 source-template 樂句，不宣稱實測拍點吻合。
- OGG 為 44.1 kHz 立體聲、60 秒；完整解碼成功、無錯誤輸出，-16.04 LUFS／-2.05 dBTP；未偵測到低於 -45 dB 且持續至少 0.5 秒的近靜音。SHA-256 `2484ed9fc1b46b450d77210e4533cbadb233c626d503ed6f0f7dd9d6b180be07`。
- 開發遊戲副本 `@/workspace/10_作品與專案/驚蟄/03_開發/JingZhe/game/audio/music/bgm_dawn_together.ogg` 與候選 OGG 雜湊相同。真結局回月下庄時以 music 通道 1.5 秒淡入，延續三人相依與清晨煙斗餘味；end_game 切黑時 1.5 秒淡出，沿用設定頁音樂音量。
- 已指定開發 basedir，以 `--warp script.rpy:2605` 開到「月下庄的燈重新點起來。」夜間大廳背景；引擎截圖確認畫面無錯誤。實機回報新檔播放中、音樂音量 1.0、未靜音；詳見 runtime_observation_long_01_loop.json。待生前確認場景與循環後才列為正式定案。

## 2026-10-12 實機確認與正式採用

生前在真結局回月下庄場景試聽後回覆「好」，確認 long_01 箏與微光循環副本及現行遊戲配置，BGM07 正式定案。上文「待確認」為當時歷程紀錄。至此 BGM01–07 七組主 BGM 全數完成、核可並導入開發遊戲，共八個 OGG（BGM04 含酒館與黑卡兩首）。2026-10-12 受控場景確認後，BGM05 確定沿用同曲，不另製受控低頻變體；BGM06 苦香強化場景也已於 2026-10-12 確認同曲即可，不另製強化變體；兩項獨立變奏待辦均已取消；環境音六組與 SFX 三十二個仍待製作。
