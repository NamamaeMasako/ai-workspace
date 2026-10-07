# BGM05 長版候選

用途：第四章怪物逼近、第五章受控、第六章調查；營造不自然的安靜與逐漸逼近的壓迫感，維持細碎、克制的懸疑，不先進入完整戰鬥節奏。

2026-10-07：生前挑選短版 02、03，兩個方向各完成一首 60 秒長版供試聽，尚未正式定案。

## 候選與參考

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

兩版先供生前比較情緒與配器，選定後再處理循環、導入開發版並實機試聽。目前不更動遊戲配樂或發行包。
