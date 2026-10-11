# BGM07_DAWN_TOGETHER 短版候選

狀態：2026-10-11，已完成 take01 四首約 20 秒短版，待生前挑選。BGM01–06 已正式採用；本曲尚未正式定案。

## 使用場景與情緒

真結局重聚後回到月下庄、三人的影子靠近、一起走到明天，以及清晨最後的煙斗苦味。音訊 Cue Sheet 指定回收 BGM01 主題動機，讓樂句更完整、更有呼吸。這輪以已核可的主選單箏曲作音訊參考，探索劫後安定、含著餘痛的溫柔與陪伴；避免歡樂跳躍或凱旋高潮。

| 編號 | 製作方向 | 場景情緒意圖 | 試聽 |
| --- | --- | --- | --- |
| 01 | 箏與微光 | 以箏主題與柔鋼琴、低弦探索熟悉燈火下的重聚，保留主選單的音樂辨識。 | [candidate_01_lantern_guzheng_seed3401_take01.ogg](candidate_01_lantern_guzheng_seed3401_take01.ogg) |
| 02 | 鋼琴相依 | 以柔鋼琴與大提琴探索三人相依、沒有說出口的安慰，箏只作輕柔回聲。 | [candidate_02_close_piano_seed3402_take01.ogg](candidate_02_close_piano_seed3402_take01.ogg) |
| 03 | 弦樂歸途 | 以連音室內弦樂探索疲憊過後回家的鬆弛，保留傷痛、逐漸溫暖。 | [candidate_03_homeward_strings_seed3403_take01.ogg](candidate_03_homeward_strings_seed3403_take01.ogg) |
| 04 | 竹笛晨風 | 以氣息感竹笛與低弦、箏探索清晨淡風，安定陪伴中仍有一點昨夜餘味。 | [candidate_04_dawn_bamboo_seed3404_take01.ogg](candidate_04_dawn_bamboo_seed3404_take01.ogg) |

以上為製作意圖，實際配器、主題辨識與結局情緒是否成立，須由生前試聽判斷。

## 參考來源與製作

- 原主題：`BGM01_LANTERN/guzheng_longform/bgm01_lantern_guzheng_long_02_seed2802.ogg`，已正式核可的箏版；實際透過 multipart `reference_audio` 上傳。另取同名 WAV 母檔前 25 秒作 `src_audio`，用來源旋律與結構引導四種配器方向。原始 BGM01 保持原版本。
- ACE-Step 1.5 Turbo cover、thinking=false、8 steps、audio_cover_strength=1.0、cover_noise_strength=0.45，seed 3401–3404。72 BPM、D minor、4/4 是生成提示，不是已量測的實際速度或調性保證。採用來源引導不代表已證明輸出完整保留原旋律。
- 四首原始 WAV 25 秒，試聽取前 20 秒、30 ms 淡入與末尾 0.5 秒淡出。先處理響度，再依實測音量匹配並作 -2.5 dBFS 峰值限制與延遲補償。限制器後以 `asetpts=N/SR/TB` 重建連續時間戳，修正部分編碼的 DTS 警告；成品完整解碼皆無錯誤輸出。保留 `_premaster.ogg`、完整請求、來源雜湊及處理前後資料。
- 母檔與參考節錄位於 `@/workspace/10_作品與專案/驚蟄/02_素材/音訊/母檔/BGM07_DAWN_TOGETHER/`；本資料夾保留 44.1 kHz 立體聲 Vorbis q5 OGG、同名 JSON、generation_manifest_take01.json、technical_check_take01.json。

## 技術結果

| 編號 | 實際 OGG 秒數 | LUFS | dBTP | 近靜音 |
| --- | --- | --- | --- | --- |
| 01 | 20.000000 | -15.99 | -2.20 | 未偵測到 |
| 02 | 20.000000 | -16.01 | -2.19 | 未偵測到 |
| 03 | 19.999977 | -16.09 | -2.19 | 未偵測到 |
| 04 | 19.999977 | -15.97 | -2.21 | 未偵測到 |

近靜音門檻為低於 -45 dB 且持續至少 0.5 秒。WAV 與 OGG 均完整解碼成功；技術結果不能代替音樂與場景的聽感判斷。

待生前挑選後，以選中短版作 reference_audio 製作約 60 秒長版，再依既定流程確認、處理循環及開發遊戲試聽。
