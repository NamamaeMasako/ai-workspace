# BGM09 長版候選與場景比較

2026-10-16：生前認為 take03「好像還行」，要求製作長版試聽。已完成 60 秒候選 `long_01_natural_phrase_felt_piano_seed3632.ogg`；生前後續指示套進遊戲試聽，循環副本已接入開發版；目前場景試用中，尚未正式定案。

## 使用場景與方向

第七章交卡、同行選擇、離開月下庄、前往林道與交戰前的準備；兩輪四路線共用。情緒是察覺威脅、保持戒備與等待危險，保留短版的鋼琴脈動及克制音量，避免回到 take02 的悲傷感；交戰後才切既有 BGM06。

## 來源與自然尾音

- 選中的 `candidate_02_felt_piano_seed3632_take03.ogg` 已實際以 multipart reference_audio 上傳，SHA-256 `f7ff88053ff66ad7bd0fc12acf322e79866f1f143ce7857f0e42e20cc7bb6458`。
- 同版本未淡出的 25 秒原始 WAV 另作自然樂句來源，SHA-256 `18b4e5cab5174265ed6264795c8eccc4692c5ccd896c8977929d4fe0f4a2565d`；並非引用 take01／take02 來取代選中短版。
- 原母檔末次明顯起音約在 21.75 秒、22.5–23.25 秒自然衰減。因此模板保留前 23.25 秒，0／22.5／45 秒回歸，以 0.75 秒 smoothstep 交疊，組成 65 秒 src_audio 引導。此為依音量包絡安排的時間模板，未宣稱量測了拍點。
- 沒有把帶 19.5–20 秒淡出的試聽 OGG 固定每 19 秒拼接，避免 BGM08 曾遇到的短收音重複。
- 本機 ACE-Step 1.5 Turbo cover、thinking=false、8 steps、seed 3632、audio_cover_strength=1.0、cover_noise_strength=0.55；80 BPM／E minor／4拍是提示，未量測實際節奏。

## 長版組合與音量

- 前 18 秒保留選中短版的解碼內容；18–19 秒過渡到同版本未淡出母檔，帶出原本 20 秒後仍存在的自然樂句／餘音。
- 22–23.25 秒再與新生成延伸段 smoothstep 交疊，之後延續至 60 秒；最後 0.5 秒為試聽收尾淡出，尚非遊戲循環版。
- 延伸段匹配開頭 RMS，再統一增益、限制峰值與重建時間戳。前 18 秒內容一致的檢查在 premaster 階段完成，最終母帶另經 limiter／編碼，不宣稱逐樣本相同。
- WAV 為 48 kHz 立體聲浮點 PCM，試聽 OGG 為 44.1 kHz 立體聲 Vorbis q5；實測 -16.29 LUFS／-2.22 dBTP，完整解碼無錯誤輸出。
- 近靜音事件：[]。格式與波形紀錄不代表聽感已核可。
- 原始 65 秒生成、自然模板、premaster WAV、母帶 WAV 保存在 `../../../母檔/BGM09_BEFORE_STORM/longform/`；OGG、premaster OGG、完整請求／回傳與各檔 SHA-256 存於本資料夾。

## 待確認

請生前確認長版的緊張戒備感、前後節奏一致性、約 20 秒後自然樂句與 22–23.25 秒接續。長版確認後才處理循環、導入開發遊戲並從交卡起連續試聽；目前遊戲仍未導入 BGM09。

可編輯產製來源：`../../../母檔/BGM09_BEFORE_STORM/longform/produce_long_01_natural_phrase.py`，包含自然樂句模板、參考上傳、生成與組合流程；現有輸出存在時會停止，不覆寫舊版本。

## 開發版場景試用（2026-10-16）

- 生前回覆「感覺還行，套進遊戲我感覺一下」，以核可試用的長版 WAV 製作 `long_01_natural_phrase_felt_piano_seed3632_loop_intro.ogg`；前 57 秒逐樣本保留於循環 WAV，只將最後 3 秒與開頭 3 秒作 smoothstep 交疊，沒有重新生成。
- 首次 60 秒，後續 `<loop 3.0>` 回接、57 秒週期。此為保留長版與淡接的技術安排，未宣稱實測拍點或已經由生前確認無縫。
- 遊戲副本 `game/audio/music/bgm_before_storm.ogg` 與候選 SHA-256 `0df4c491076d35d4063bec1c40f184caadfd797cc27ed553cbf4eda6c9de5a57` 一致；OGG 為 44.1 kHz 立體聲，解碼無錯誤輸出，實測 -16.32 LUFS／-2.22 dBTP，無長段近靜音。
- 第一輪交卡選擇播放；四個交卡分支進場時只在此曲未播放時淡入，避免選擇後重新起曲。第二輪於回退黑幕之後、交卡分支進場才開始。交卡、出發、林道及召喚前沿用；各路線首次實際攻擊以既有 BGM06 cue 切換。
- 1.5 秒淡入／淡出，沿用 music mixer 與音量。持續環境音保持停用，死亡後及回退黑幕沿用現行靜音安排；BGM10／11 尚未製作。
- 已指定開發 basedir 並開到 `script.rpy:1057`「把卡片交給誰？」選擇畫面，截圖正常；引擎讀取的音檔雜湊一致、新曲播放中、音量 1.0、未靜音，ambience 為空。四路線配置已寫入，尚未宣稱四路線完整實機驗收。
- 導入清單 game_integration_long_01.json、觀察 runtime_observation_long_01_loop.json、畫面 runtime_scene_long_01_loop.png；循環可編輯來源 `../../../母檔/BGM09_BEFORE_STORM/longform/prepare_long_01_loop.py`。
- 待生前由選擇起連續試聽交卡與出發，確認場景、自然尾音、循環及轉戰鬥曲。未重建發行包或升版。

## long_02：前面偏悲傷 take02 的長版比較（2026-10-16）

生前認為警戒取向 long_01 套入交卡場景後「感覺不太對」，要求將前面描述為較悲傷、但節奏可以的鋼琴 take02 做成長版。

- 完整 60 秒 `long_02_natural_phrase_felt_piano_seed3622.ogg`，以 `candidate_02_felt_piano_seed3622_take02.ogg` 實際作 reference_audio，SHA-256 `e16bf5207f70d2b7ca60d239bb1d7db03c1d9d151e77e62466dd728095efbe5f`。這是先前加速不安版 take02 的延伸，不是原始 62 BPM take01，也沒有沿用警戒 take03 代替它。
- 忠實延續該短版鋼琴旋律、低弦音色、80 BPM 提示及內斂的情緒，沒有再要求改成非抒情的警戒短音型。音樂的悲傷／緊張程度與場景適配由生前試聽比較。
- 同版未淡出 25 秒原始 WAV 作自然樂句來源：最後明顯起音約 18.75 秒，至 21.5 秒自然衰減；保留前 21.75 秒，以 21 秒週期、0.75 秒 smoothstep 交疊，組成 65 秒 src_audio。依波形包絡安排，未宣稱量測拍點。
- Turbo cover、thinking=false、8 steps、seed 3622、audio_cover_strength=1.0、cover_noise_strength=0.55；80 BPM／E minor／4拍僅為提示。
- 前 18 秒保留選中短版內容，18–19 秒轉到未淡出原母檔，20.5–21.75 秒接續生成延伸，末尾 0.5 秒試聽淡出。未作遊戲循環，未替換目前遊戲的 long_01。
- WAV 為 48 kHz 立體聲浮點 PCM，OGG 為 44.1 kHz 立體聲 Vorbis q5；實測 -16.77 LUFS／-2.30 dBTP，完整解碼無錯誤輸出，近靜音事件 []。
- 原始生成、自然模板、premaster WAV、母帶與可編輯 `../../../母檔/BGM09_BEFORE_STORM/longform/produce_long_02_natural_phrase.py` 保留；來源、請求及處理／SHA-256 見同名 JSON 與 generation_manifest_long_02.json。
- 用途仍為第七章交卡與出發的配樂比較，長版確認後再決定是否替換遊戲；目前未正式採用或重建發行包。

## long_02 換入開發版試聽（2026-10-16）

- 生前回覆「好，套看看」，以較悲傷 take02 的 long_02 母檔製作 `long_02_natural_phrase_felt_piano_seed3622_loop_intro.ogg`，未重新生成。循環 WAV 前 57 秒保留，末尾 3 秒與開頭 3 秒 smoothstep 交疊；首次 60 秒，後續 `<loop 3.0>` 回接、57 秒週期。此為淡接安排，未宣稱實測拍點或場景聽感已核可。
- 原樣替換 `game/audio/music/bgm_before_storm.ogg`，SHA-256 `7d0d81a73a0dd8b9cde7a82dd1a0a067d930ffe1a8ecb1b655a3d11d8b730963` 與候選一致。long_01 原檔、循環副本及不合場景的回饋均保留。
- 交卡選擇與兩輪四路線使用原有接點，出發及交戰前延續，第一個實際攻擊切 BGM06；script.rpy 本輪未修改。music 通道、1.5 秒淡入淡出及停用環境音設定沿用。
- OGG 為 44.1 kHz 立體聲，完整解碼無錯誤輸出，實測 -16.86 LUFS／-2.30 dBTP，無長段近靜音。
- 已重新開到開發 basedir 的 `script.rpy:1057` 交卡選擇，畫面正常、引擎讀取 long_02 雜湊一致、music 播放中、音量 1.0、未靜音，ambience 為空；觀察與畫面為 runtime_observation_long_02_loop.json／runtime_scene_long_02_loop.png。
- 導入清單 game_integration_long_02.json，可編輯循環來源 `../../../母檔/BGM09_BEFORE_STORM/longform/prepare_long_02_loop.py`。整段情緒、對話搭配、循環及切戰鬥曲待生前確認，尚未正式採用或重建發行包。
