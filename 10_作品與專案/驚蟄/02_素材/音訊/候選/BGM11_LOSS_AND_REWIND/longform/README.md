# BGM11 還不能放手：long_01

2026-10-16：生前選定 take03 第四版「還不能放手」，完成 60 秒長版供試聽。已依「套進遊戲試試」製作循環並導入開發版；生前之後回覆「OK，可以進行下一首」，現行長版、循環與場景配置正式採用。

## 使用場景與情緒

- 第七章確認夢見死亡，以及花見突然倒下、確認死亡與抱回月下庄的段落，先以同曲比較。
- 突然失去當下的震驚、不願接受、仍想挽救卻無能為力。延續第四版的克制追問與未解張力，不以喪禮儀式感、安定追憶或得到安慰收束。
- 撕卡／時間回退仍預留短暫靜音，下一輪交卡接 BGM05；負傷救援另由 BGM13 規劃。
- 上述是製作意圖，不能視為助理已聽辨情緒或樂器；是否適合由生前試聽判斷。

## 真正使用選中短版

- 選中 OGG `../candidate_04_cello_piano_plea_seed3824_take03.ogg` 實際以 multipart `reference_audio` 上傳。
- 參考 SHA-256：`2aa7a49341bd12da7cb363a80faea34232a9f0be12086141655022c9299c2d88`。
- 對應未淡出 25 秒 raw WAV 實際供 source template 使用，SHA-256：`879011353cbd426928030607bf171c97ef104df03140cab1a28eb3f15775c58d`。
- 原始尾音在 20.0／20.5／21.0／21.5 秒半秒窗的 RMS 約 -24.2／-26.7／-33.0／-58.6 dBFS；使用前 21.75 秒，以 21 秒週期、0.75 秒 smoothstep 交疊建立 65 秒 source map，實際作 `src_audio` 上傳。這是固定時間參考，不宣稱測得拍點。
- 原始來源先沿用短版 -10.64 dB 固定增益與 -16 dBFS limiter，保留柔和起音，沒有套 20 秒審聽淡出；source map 作生成引導，交付長版並非直接重複該模板。
- ACE-Step Turbo cover、thinking=false、8 steps、seed 3824、audio_cover_strength=1.0、cover_noise_strength=0.55；76 BPM／F minor／配器為生成提示。

## 交付組合與音量

- 60 秒長版前 18 秒保留選中短版解碼內容，18–19 秒 smoothstep 接回未淡出來源；20.5–21.75 秒接生成延伸。
- 延伸段匹配參考強度並以 -16 dBFS 控制其峰值，使用固定增益 -14.51463 dB；全曲不另加整體音量，保留開頭原本尺度。
- 末 0.5 秒為本次審聽淡出，尚未處理正式循環。不能將此淡出當未來長版來源。
- OGG 44.1 kHz 立體聲 Vorbis q5，60 秒，量測 -30.18 LUFS／-15.59 dBTP。
- 22.23–23.39 秒、42.89–44.31 秒各約 1.16／1.43 秒低於 -45 dB，保留短暫樂句間隙；沒有超過四秒的近靜音段。實際接續感仍待試聽。
- 正式遊戲音訊、劇本與發行版本未改。

## 來源與重製

- 可編輯來源：`../../../母檔/BGM11_LOSS_AND_REWIND/longform/produce_long_01_natural_phrase.py`。
- 保存 65 秒生成原始 WAV、65 秒 source template、25 秒未淡出音量整理來源、60 秒 premaster／WAV／OGG、完整請求回應、處理參數、來源與輸出 SHA-256、格式及量測紀錄。
- `unused_preflight_20s_master_level_conversion.wav` 是提交前來源欄位對接錯誤產生的 20 秒音量轉換中間檔，保留但未上傳模型、未作 source map 或交付素材。正式來源已對照 raw_wav 雜湊後才提交。
- 交付 OGG SHA-256：`3b6f641db254835636970dacf24b86b8f95d61c78d91857b3eec39229984b4b8`。

## 下一步

本曲已正式定案，接續 BGM12 最終選擇與告別，先製作四首短版。

## 開發版場景試用

2026-10-16：依「套進遊戲試試」，BGM11「還不能放手」long_01 已製作循環並接入開發版第七章兩輪四條死亡路線。遊戲檔 `game/audio/music/bgm_loss_and_rewind.ogg` SHA-256 `4f24e912daeee879dded6eb997b333176cd6ed1dc1aedbcfd98a23548b28f678` 與候選一致；前 57 秒母檔保留、末 3 秒 smoothstep 交疊，首次 60 秒、後續 `<loop 3.0>`／57 秒週期，未增加整體音量，OGG -29.75 LUFS／-15.59 dBTP。兩輪看見夢見身體時起曲；花見路線在倒下／injured 立繪前起曲，延續確認死亡、抱回月下庄與哀悼，四處撕卡前 0.5 秒淡出，回退段保留靜音。入口 fadein 0.8／fadeout 0.5，使用既有 music 通道與設定音量。已指定開發 basedir 開到 script.rpy:1439「花見倒下的聲音很輕。」畫面正常、新檔播放中、雜湊一致，relative/music volume 1.0、未靜音，ambience 為空；未宣稱已完整人工驗收四路線。循環母檔／製作程式、導入與實機快照／畫面保存；長版情緒、完整場景、轉場及循環待生前確認，尚未正式定案，未重建發行包或升版。

詳見 `game_integration_long01.json`、`game_runtime_long01_initial.json` 與 `game_scene_long01_initial.png`。本輪製作來源 `../../../母檔/BGM11_LOSS_AND_REWIND/longform/prepare_long_01_loop.py`。

## 正式採用

2026-10-16：生前於 BGM11 花見死亡場景試聽後回覆「OK，可以進行下一首」，正式採用「還不能放手」long_01 循環與現行兩輪死亡場景配置。遊戲檔 `bgm_loss_and_rewind.ogg` SHA-256 `4f24e912daeee879dded6eb997b333176cd6ed1dc1aedbcfd98a23548b28f678` 與循環候選再次比對一致；首次 60 秒、後續 `<loop 3.0>`／57 秒週期，撕卡前 0.5 秒淡出，音檔及播放程式本輪未再改。formal_adoption.json、導入紀錄與審聽歷程已更新。BGM01–08、BGM10–11 共十組配樂／十一個正式 OGG 已定案；BGM09 沿用 BGM05、不另製新曲。下一首 BGM12_CHOOSE_MY_FATE 為第八章最終選擇、留卡與告別，依流程先四首 20 秒方向；BGM13–14 待製作，未重建發行包或升版。
