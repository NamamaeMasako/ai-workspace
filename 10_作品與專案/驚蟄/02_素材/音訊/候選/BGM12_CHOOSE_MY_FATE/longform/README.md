# BGM12 把結局留下：long_01

2026-10-16：生前回覆「用第四版」，選中 take02 第四首「把結局留下」。已依「套進遊戲試試」製作循環並接入開發版選後場景，待完整情緒、轉場與循環確認，尚未正式定案。

## 使用場景與情緒

- 嚴格從第八章玩家選下「把卡留給自己」之後起曲，選項出現前維持無 BGM。
- 承接驚蟄決定親自承擔、交代花見與夢見留下及告別的段落。
- 沉重的決定、明知代價仍承擔，保留恐懼、壓力與責任。維持第四版的低音承重、克制的前行感與未解和聲，避免日常輕鬆、抒情放鬆、喪禮感或英雄凱旋。
- 本次場景試用延續至獨自出發／苦香準備，交戰切 BGM06；是否保留這段延續待生前確認。
- 以上是生成提示與製作意圖，並非助理已聽辨的情緒或樂器；實際長版一致性待生前試聽。

## 選中音檔實際參與延伸

- `../candidate_04_cello_piano_cost_seed3914_take02.ogg` 實際上傳為 `reference_audio`，SHA-256 `4dd8db7e03c194e079ba42e97a7324acdca0dd861929c6ec009442cd231b6e37`。
- 對應未淡出的原始 25 秒 WAV 用於 source map，SHA-256 `0517cb448cd48b8b5aabbff62b33f7c79540201881b9a624da8f846558b4ab23`。
- 沿用短版固定增益 -10.38 dB、-16 dBFS PCM limiter 及 0.03 秒淡入，沒有套短版末尾的審聽淡出。
- 原始母檔尾音在 23.0／23.5／24.0／24.5 秒半秒窗 RMS 約 -28.7／-30.5／-34.4／-57.1 dBFS；取前 24.5 秒，以 23.75 秒週期、0.75 秒 smoothstep 交疊組成 65 秒 source map，實際上傳為 `src_audio`。
- 此為固定時間來源引導，不宣稱測得拍點。交付長版含模型生成延伸，並非把試聽短版直接循環三次。
- ACE-Step Turbo cover、thinking=false、8 steps、seed 3914、audio_cover_strength=1.0、cover_noise_strength=0.55。60 BPM／D minor／配器均為提示。

## 長版組合與音量

- 前 18 秒保留選中短版解碼內容，18–19 秒 smoothstep 接回未淡出來源，23.75–24.5 秒接生成延伸。
- 延伸段匹配參考強度，並以 -16 dBFS 限制延伸段峰值，固定增益 -14.40484 dB；全曲沒有額外增益，保留原短版開頭音量。
- 末 0.5 秒僅為本次試聽淡出，未處理正式循環；未淡出原始生成與 source map 均保留。
- OGG 44.1 kHz 立體聲 Vorbis q5，60 秒；完整解碼沒有錯誤輸出，實測 -30.46 LUFS／-15.55 dBTP，沒有低於 -45 dB 且持續至少 0.5 秒的近靜音。
- 交付 OGG SHA-256 `737b65a9d01502868516fb354dc438a99855c7b26a02de3dce46d98c9354d8bb`。

## 重製與保留

可編輯來源 `../../../母檔/BGM12_CHOOSE_MY_FATE/longform/produce_long_01_natural_phrase.py`；需本機 ACE-Step API、Python／numpy、ffmpeg／ffprobe，不覆寫既有來源。

保留 65 秒模型生成 WAV、65 秒 source map、25 秒未淡出音量整理來源、60 秒 WAV／OGG／premaster，以及參考雜湊、完整請求回應、處理參數、輸出格式與量測紀錄。長版生成階段未改遊戲；本次場景試用的接點與副本見下節，發行版本未重建。

## 下一步

在開發版確認選後起曲、留卡告別與出發的情緒、音量、切戰鬥曲和循環後，再正式定案。

## 開發版場景試用

2026-10-16：依「套進遊戲試試」，BGM12「把結局留下」long_01 已製作循環並接入第八章選下「把卡留給自己」後的 chapter_8_true_end（script.rpy:2087）；chapter_8_choice 入口明確 stop music，選項前無 BGM。留卡、交代兩人留下與告別延續至獨自出發／苦香準備，實際交戰沿用原 BGM06 入口 fadeout 1.5／fadein 0.5。遊戲檔 `bgm_choose_my_fate.ogg` SHA-256 `836978cc9d0b0ba844d5e35427a6ce7be6fcda134c41db9a9ecc58202e04779e` 與候選一致；前 57 秒母檔保留、末 3 秒 smoothstep 交疊，首次 60 秒、後續 `<loop 3.0>`／57 秒週期，未加整體增益。OGG -30.08 LUFS／-15.55 dBTP，無達門檻近靜音；起曲 fadein 0.8／fadeout 0.5，沿用 music 通道與使用者音量。已指定開發 basedir 開到選後首句 script.rpy:2090 花見「怎麼了？你臉色很差。」畫面正常，新檔播放中、位置前進、music／relative volume 1.0 且未靜音，ambience 空；初始實機畫面與快照保存。選後完整告別、出發、戰鬥轉場及循環聽感待生前確認，未宣稱已完整人工驗收，尚未正式定案。循環來源／程式、導入及實機紀錄已保存，未重建發行包或升版。

詳見 `game_integration_long01.json`、`game_runtime_long01_initial.json` 與 `game_scene_long01_initial.png`；循環來源 `../../../母檔/BGM12_CHOOSE_MY_FATE/longform/prepare_long_01_loop.py`。
