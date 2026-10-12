# 介面音效第一版試聽

2026-10-12：依生前要求，確認與返回各製作一版，待試聽選定。

| Cue | 方向 | 單次音檔 | 重複三次的試聽檔 | 用途 |
| --- | --- | --- | --- | --- |
| UI01_CONFIRM | 較高、清楚的柔和木質敲擊方向，短尾音 | [ui_confirm_take01.ogg](ui_confirm_take01.ogg) | [ui_confirm_take01_preview.ogg](ui_confirm_take01_preview.ogg) | 主選單、設定、存讀檔與劇情選項確認 |
| UI02_BACK | 較低、收束更柔的木質敲擊方向 | [ui_back_take01.ogg](ui_back_take01.ogg) | [ui_back_take01_preview.ogg](ui_back_take01_preview.ogg) | 返回上一頁與關閉選單 |

## 製作與保存

- 採原創程序合成：衰減共振模態與固定亂數的濾波敲擊瞬態，沒有使用外部錄音、樣本庫或音樂生成模型。木質感為音色設計意圖，實際聽感由生前判斷。
- 確認 0.28 秒、返回 0.30 秒。沒有語音、旋律段落、長混響或 hover 候選；兩者使用同一合成設計，藉由共振頻率與衰減參數區分。
- 合成波形各作固定峰值 -10 dBFS 增益，保存 48 kHz 單聲道 PCM 24-bit WAV 母檔；試聽 OGG 為 44.1 kHz 單聲道 Vorbis q6。最終遊戲音量待核可後實機調整。
- `_preview` 是同一音效在 0.1／1.1／2.1 秒各播放一次，總長 3 秒，只便於審聽，不能作遊戲按鈕音檔。
- 全部 WAV／OGG 完整解碼，無錯誤輸出；同名 JSON 與 generation_manifest_take01.json 保存參數、音量、雜湊及狀態。
- 母檔、試聽序列 WAV 與可編輯合成來源 `produce_ui_take01.py` 保存於 `@/workspace/10_作品與專案/驚蟄/02_素材/音訊/母檔/UI_INTERFACE/`。

目前僅為候選。待生前確認後，才導入介面並確認按鈕音量、觸發時機與既有音效音量控制。
