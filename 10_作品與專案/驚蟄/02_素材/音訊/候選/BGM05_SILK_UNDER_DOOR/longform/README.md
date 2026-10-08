# BGM05 長版候選

用途：第四章怪物逼近、第五章受控、第六章調查；營造不自然的安靜與逐漸逼近的壓迫感，維持細碎、克制的懸疑，不先進入完整戰鬥節奏。

2026-10-08 最新狀態：生前已選定 long_04 樂句節奏一致修正版。已完成保留原開頭的循環副本並導入開發遊戲；生前於第四章林道實機試聽後回覆「OK」，正式採用現行遊戲配置。歷次母檔與候選全數保留。

## long_01 製作紀錄（不採用）

| 短版編號 | 配器方向 | 長版試聽 OGG | 參考短版 |
| --- | --- | --- | --- |
| 02 | 低音單簧管／懸置弦音 | `long_01_reference_guided_bass_clarinet_seed3202.ogg` | `../candidate_02_bass_clarinet_seed3202_take02.ogg` |
| 03 | 悶音弦樂／細絲般不協和 | `long_01_reference_guided_muted_strings_seed3203.ogg` | `../candidate_03_muted_strings_seed3203_take02.ogg` |

- 以生前實際聽過的 20 秒 OGG 作 `reference_audio`，透過本機 API 的 multipart 檔案上傳；保留來源 SHA-256。這是風格參考生成，長版的旋律與編排仍需生前試聽確認。
- ACE-Step 1.5 Turbo + 0.6B LM、8 steps、`thinking=true`，64 BPM、E minor、4/4，seed 3202／3203，`task_type=text2music`、`audio_cover_strength=0.35`。
- 延續短版提示詞與配器描述，新增持續背景織度、小幅樂句變化、不以終止式收束的指示；不加入人聲、鼓、固定節拍、環境音或電影式高潮。
- 為避免短版生成時曾出現的末端空白，原始生成長度設為 65 秒，試聽版固定取前 60 秒；開頭 30 ms 淡入、末端 0.5 秒淡出。這是本輪審聽處理，尚未製作無縫循環。
- 原始母檔位於 `@/workspace/10_作品與專案/驚蟄/02_素材/音訊/母檔/BGM05_SILK_UNDER_DOOR/longform/`，檔名為對應的 `*_raw.wav`；試聽版為本資料夾中的 44.1 kHz 立體聲 Vorbis q5 OGG，目標 -16 LUFS／-1.5 dBTP。
- 每首同名 JSON 記錄完整請求、生成結果、參考與成品雜湊；彙整紀錄為 `generation_manifest_long_01.json`，實測報告為 `technical_check_long_01.json`。
- 兩首原始 WAV 與 OGG 均完整解碼成功；OGG 均為 60 秒、44.1 kHz、立體聲。02 實測 -16.09 LUFS／-2.75 dBTP，03 為 -15.88 LUFS／-2.11 dBTP；均未偵測到低於 -45 dB 且持續至少 0.5 秒的近靜音區段。此檢查不取代生前對配器、旋律與場景情緒的試聽判斷。
- `long_01_reference_guided_bass_clarinet_seed3202_request_rejected.json` 保留初次直接提供 workspace 絕對音訊路徑時的請求。API 限制該用法，回覆 HTTP 400，未生成音檔；正式請求已改用文件支援的檔案上傳。

## 後續

`long_01` 不再進入循環或遊戲實裝；新版須先讓生前確認懸疑感與場景適配，再處理循環與實機試聽。

## long_02 懸疑修正版

- 02：`long_02_suspense_bass_clarinet_seed3202.ogg`，保留低音單簧管與低弦，以長連音、半音擦音與懸置低音壓住輕快短句。
- 03：`long_02_suspense_muted_strings_seed3203.ogg`，保留悶音中提琴／大提琴，以持續運弓、冷泛音、緩慢滑音與不協和間隔營造細絲般的壓迫。
- 兩首仍使用原 `_take02.ogg` 20 秒短版作 `reference_audio`，不以被否決的長版作參考。
- 本輪改為 ACE-Step 1.5 Turbo 直接擴散生成（`thinking=false`，不使用 0.6B LM 生成 audio codes），8 steps，固定 seed 3202／3203；48 BPM 僅為生成提示，要求自由速度、無可辨識的固定節拍。
- 提示詞改為低 E 持續音、未解決半音／增四度、長連音、緩慢漂移；排除俏皮、搖擺、爵士、華爾滋、舞曲、撥弦、斷奏、固定脈衝、鋼琴、鈴音與木琴等方向。希望恢復懸疑感，是否符合仍由生前試聽判斷。
- 參數釐清：本機原始碼中 `audio_cover_strength` 控制 cover／非 cover 條件混合，不能直接稱為「參考短版強度」。上一輪 `thinking=true` 生成 audio codes 後會切為 cover；本輪不產生該 codes，維持 text2music，使用中性預設 `audio_cover_strength=1.0`。參考短版依然透過獨立音訊條件輸入。
- 原始生成 65 秒 WAV，固定取前 60 秒；維持既有邊界淡化與 44.1 kHz 立體聲 Vorbis q5 試聽規格，不藉重複短版拼接成長版，也尚未製作循環。
- 完整請求與成品資訊存於同名 JSON，彙整為 `generation_manifest_long_02.json`，技術報告為 `technical_check_long_02.json`。
- 兩首原始 65 秒 WAV 與 60 秒 OGG 均完整解碼成功。02 實測 -15.77 LUFS／-1.08 dBTP；03 實測 -15.18 LUFS／-2.05 dBTP，均無滿刻度峰值。以 -45 dB、持續 0.5 秒門檻檢測，02 在 52.21–52.74 秒有約 0.52 秒近靜音，03 在 20.97–22.01 秒及 37.37–38.00 秒分別有約 1.04 秒與 0.64 秒近靜音；原樣保留供生前判斷這些短暫低音量區段是否合適。本輪未處理循環，技術檢查不代表情緒適配已通過。

## long_03 原短版接續長版

- 檔案：`long_03_short_continuation_muted_strings_seed3203.ogg`。
- 依生前回饋，保留新版 03 的懸疑方向，將原短版 03 作為樂句與配器的基準；上一輪提示詞偏重長音與不協和，本輪恢復原短版的細膩樂句、音色層次及少量遠處柔鋼琴。
- 使用生前實際聽過的 `candidate_03_muted_strings_seed3203_take02.ogg`，同時作 `reference_audio` 與 `src_audio`；透過本機 API multipart 上傳。
- 改用接續生成：ACE-Step 1.5 Turbo、8 steps、seed 3203、`thinking=false`、`task_type=repaint`；指定 18–65 秒為續寫區間、`chunk_mask_mode=explicit`、`repaint_mode=aggressive`，由已存在的前段作上下文完成後段。
- 回到短版的 64 BPM／E minor／4/4 生成提示，延續安靜旅店異常、未解決音程與克制的配器；仍排除俏皮、爵士搖擺、舞曲、人聲、鼓、環境音及高潮。
- 原始生成 65 秒 WAV 另存 `*_raw.wav`；將原短版前 18 秒保留在 60 秒審聽母檔中，18–19 秒與生成後段作一秒等功率交疊，尾端 0.5 秒淡出。後段音量依原短版前段的 RMS 作固定增益匹配，另作全曲一致的峰值降益；不對原前段作新的編曲。
- 審聽母檔為同名 48 kHz 立體聲浮點 WAV；OGG 為 44.1 kHz 立體聲 Vorbis q5。保留原前段的 PCM 比對結果、增益與 SHA-256，詳見同名 JSON；彙整紀錄為 `generation_manifest_long_03.json`，技術報告為 `technical_check_long_03.json`。
- 技術檢查完成：原始 WAV 為 65 秒、審聽 WAV／OGG 均為 60 秒，均完整解碼成功；OGG 實測 -16.24 LUFS／-1.98 dBTP，未偵測到低於 -45 dB 且持續至少 0.5 秒的近靜音區段。後段固定增益 +2.66 dB、全曲一致降益 -2.95 dB；審聽母檔前 18 秒已核對與原短版解碼後 PCM 相同（計入同一全曲增益），保留音符、樂句、配器與相對動態。
- 生前試聽重點：18–19 秒接續是否自然、原短版音樂感是否延續，以及後段場景懸疑感是否保留。本輪尚未製作無縫循環或導入遊戲。

## long_04 樂句節奏一致修正版

- 檔案：`long_04_phrase_guided_muted_strings_seed3203.ogg`。
- 回饋：`long_03` 雖保留前段，但生成後段的節奏與樂句呼吸和原短版不一致。本輪改用完整樂句參考結構約束後段。
- 將選定的 20 秒短版 03 在 0、18.75、37.5、56.25 秒作相同樂句回歸，以 1.25 秒等功率交疊組成 65 秒 `*_source_template.wav`。18.75 秒為短版原請求 64 BPM 下的五小節安排；64 BPM 是生成提示，不能稱為已量測的實際速度。這份骨架會重複原短版樂句，用作全曲的旋律／節奏結構參考。
- 短版作 `reference_audio`，完整骨架作 `src_audio`，ACE-Step 1.5 Turbo cover，8 steps，seed 3203，`thinking=false`、`audio_cover_strength=1.0`、`cover_noise_strength=0.65`。提示要求沿用原來源的音符間隔、樂句時間、密度與配器層次，只作少量音色與表情變化。
- 審聽版保留原短版前 18 秒，18–19 秒與有完整結構參考的生成結果等功率交疊，取至 60 秒並處理尾端淡出、固定音量匹配及一致的峰值降益。
- 母檔資料夾保留 source template、原始生成 WAV 與 60 秒審聽 WAV；44.1 kHz 立體聲 Vorbis q5 OGG 存於本資料夾，同名 JSON、`generation_manifest_long_04.json` 與 `technical_check_long_04.json` 記錄來源、參數、結構與檢查。
- 統一試聽音量：保留處理前的 `*_premaster.wav`／`*_premaster.ogg`，正式候選在其上固定增益 +3.8 dB，採 -2 dBFS 峰值限制與延遲補償，讓比較音量接近前幾版。審聽 WAV 的前 17.95 秒已逐樣本核對僅有一致增益，最大誤差為 0；原前段音符、樂句與相對動態保留。
- 所有母檔與 OGG 完整解碼成功；最終 OGG 為 60 秒，實測 -16.15 LUFS／-1.76 dBTP，未偵測到低於 -45 dB 且持續至少 0.5 秒的近靜音區段。技術檢查完成，前後節奏與音樂感仍待生前試聽確認，曲目尚未正式定案或導入遊戲。

## long_04 選定版本的循環與遊戲配置

- 生前於 2026-10-08 回覆「好，就用這版」，選定 long_04；不重新生成、改旋律或配器。
- 循環 WAV：`long_04_phrase_guided_muted_strings_seed3203_loop_intro.wav`（對應母檔 longform）；本資料夾 OGG 為 `long_04_phrase_guided_muted_strings_seed3203_loop_intro.ogg`，處理及技術報告為同名 JSON。
- 前 56.25 秒與選定審聽 WAV 逐樣本相同（最大誤差 0）。末尾 3.75 秒與原開頭用 smoothstep 凸組合交疊，維持音量並避免首尾淡出留白；播放標記為 `<loop 3.75>`，第一次保留原開頭，後續循環從 3.75 秒接回，重複週期 56.25 秒。循環週期依 source template 的三個 18.75 秒樂句設定，並非宣稱已量測實際 BPM。
- 60 秒、44.1 kHz、立體聲 Vorbis q5；完整解碼成功，-16.16 LUFS／-1.76 dBTP，無低於 -45 dB 且持續 0.5 秒以上的近靜音。SHA-256 `0D5199BC0B8EB16D4C5504089A149EC7A67B08DB8FE8D2B63D1432B2BF5E4645`。技術檢查不代替循環聽感判斷。
- 遊戲副本：`@/workspace/10_作品與專案/驚蟄/03_開發/JingZhe/game/audio/music/bgm_silk_under_door.ogg`；與候選 OGG 雜湊相同。
- 第四章林道怪物逼近、走廊白絲起至第五章受控段、第六章走廊調查及封住郵箱氣味後播放；大廳日常／畫圖暫回既有 BGM03，清晨保留 BGM02，進第七章前淡出。各曲轉場 1.5 秒，沿用 music 音量。本輪第五章沿用同一核可版，不另製削低頻版本。
- Ren’Py 8.5.2 lint 通過；以 `--warp script.rpy:519` 啟動開發專案至第四章林道首句。實機確認新 BGM 檔正在播放、音樂音量 1.0、未靜音且畫面正常。遊戲場景與循環聽感待生前確認；未升版或重建發行包。
- 實機循環紀錄：`runtime_check_long_04_loop.json`。觀察間隔 127.19 秒，音樂位置跨過兩次 56.25 秒循環仍持續播放，時間誤差約 0.002 秒；一次性探針已移出遊戲，不留在正式配置。

## 2026-10-08 實機確認

生前於第四章林道實機試聽後回覆「OK」，確認 long_04 循環版及現行遊戲配置，BGM05 正式定案。上述各輪「待確認」為當時的製作紀錄。下一首為 BGM06_FOREST_ASSAULT（第七、八章戰鬥），先製作四首短版供挑選。
