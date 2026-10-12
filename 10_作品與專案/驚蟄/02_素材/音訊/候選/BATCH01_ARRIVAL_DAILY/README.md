# 第一批：抵達月下庄與日常場景

2026-10-12：生前核可七批場景順序。現為第四輪：全部持續非 BGM 環境音停用，保留既有 BGM 與六個動作音檔（木鈴 take02），待整段場景試聽。

## 本批素材（含留存的停用候選）

| Cue | 方向／用途 | 長度 | 音檔 |
| --- | --- | --- | --- |
| AMB01_ROAD_WIND | 舊道風聲候選；現行停用 | 45.00 秒 | [amb_road_twilight_wind_take01.ogg](amb_road_twilight_wind_take01.ogg) |
| AMB02_INN_WOOD_ROOM | 室內底聲候選；現行停用 | 45.00 秒 | [amb_inn_wood_room_take01.ogg](amb_inn_wood_room_take01.ogg) |
| AMB03_COURTYARD_WATER_WIND | 後院水風候選；現行停用 | 45.00 秒 | [amb_courtyard_water_wind_take01.ogg](amb_courtyard_water_wind_take01.ogg) |
| SFX01_SLIDING_DOOR | 序章推門入庄 | 0.86 秒 | [world_sliding_door_take01.ogg](world_sliding_door_take01.ogg) |
| SFX03_WOOD_BELL | 門扇帶動的五下漸弱木鈴 | 1.55 秒 | [world_wood_bell_take02.ogg](world_wood_bell_take02.ogg) |
| SFX13_KISERU_IGNITE | 序章煙草燃起 | 0.72 秒 | [magic_kiseru_ignite_take01.ogg](magic_kiseru_ignite_take01.ogg) |
| SFX15_EMBER | 第一章前院煙草餘燼 | 1.15 秒 | [magic_kiseru_ember_take01.ogg](magic_kiseru_ember_take01.ogg) |
| SFX07_WRITING | 第一章後院寫下與重寫句子 | 1.05 秒 | [world_writing_pen_take01.ogg](world_writing_pen_take01.ogg) |
| SFX08_PAPER_FOLD | SFX08 包布摩擦變體；摺紙基礎音仍待第二批 | 0.68 秒 | [world_cloth_wrapped_naginata_take01.ogg](world_cloth_wrapped_naginata_take01.ogg) |

SFX07 因第一章後院已有寫字動作，本批提前納入。SFX08 僅完成包布摩擦變體，摺紙基礎聲仍於第二批製作，不將該 cue 全項認列為完成。

## 連續場景檢查

1. 序章舊道 → 煙草點火 → 抵達旅店 → 拉門、木鈴 → 室內交談。起點 `script.rpy:44`。
2. 第一章清晨房間 → 早餐 → 前院煙斗餘燼；清晨、前院均沿用 BGM，室內與戶外不加循環環境聲。起點 `script.rpy:106`。
3. 後院 BGM → 寫下與重寫句子 → 花見攜帶包著薙刀的布料 → 傍晚回到大廳。起點 `script.rpy:194`。

請連同既有 BGM 一起判斷音色、強弱、遠近、動作觸發、循環與場景接續。包布只在物件出現時輕補，不加入未發生的拆布動作；擦刀柄處保持留白。每次修正以相同場景重聽為準。

## 製作與配置

- 本批是原創程序合成：週期性濾波噪聲、柔和木質共振、摩擦與火星瞬態；未使用外部錄音或音樂模型。自然感與場景適配為設計方向，由生前審聽確認。
- 環境音各 45 秒、48 kHz 雙聲道 PCM 24-bit 母檔；週期性合成與末端 20 ms 修整讓母檔首尾 PCM 值一致。OGG 為 44.1 kHz 立體聲 Vorbis q6；此技術結果不代表已獲無縫聽感核可。
- 動作音效為 48 kHz 單聲道 PCM 24-bit 母檔、44.1 kHz 單聲道 OGG。參數、固定種子、音量與雜湊見同名 JSON／generation_manifest_take01.json；全部 OGG 完整解碼，無錯誤輸出。
- 可編輯來源 `produce_batch01_take01.py` 與母檔存於 `@/workspace/10_作品與專案/驚蟄/02_素材/音訊/母檔/BATCH01_ARRIVAL_DAILY/`。
- `game/scene_audio.rpy` 保留舊 ambience 通道供存檔相容，互動／讀檔時清除並靜音。動作與 UI 音效由「音效音量」控制；音樂由既有 music mixer 控制。
- 現行配置不播放任何循環環境音，保留動作音效原檔副本。門聲結束後留 0.12 秒，再響木鈴；場景播放不插入額外等待閱讀的 pause。
- 全部環境音已停用；返回主選單與重新開始仍停止舊環境／劇情音效，兼容舊狀態。第二批尚未導入。
- 已指定開發 basedir，開到序章舊道；引擎截圖與環境通道狀態確認啟動正常，現行配置見 scene_integration_take04.json，第一輪配置保留於 scene_integration_take01.json。尚未替生前確認實際聽感，未重建發行包或升版。

## 2026-10-12 第二輪場景修正

生前指出舊道無 BGM、風聲單獨聽無聊且與音樂混合像雜訊；木鈴單下太不明顯。

- 舊道序章改播已核可的 BGM01 箏主題，延續至入庄交談；第一章清晨以 1.5 秒切到既有 BGM02。黑底短引沿用原有安靜配置。
- 舊道與第一章前院均停用連續風聲，AMB01 第一版候選與母檔保留，現行不採用。室內底聲、後院水風與其他音效本輪維持待審聽配置。
- 木鈴改用 [world_wood_bell_take02.ogg](world_wood_bell_take02.ogg)，1.55 秒內五下輕響，起點 0／0.19／0.43／0.74／1.04 秒，強度逐漸衰減，音高小幅變化，峰值 -14 dBFS。原單下 take01 保留，現行遊戲副本已換為 take02。
- 台詞「木鈴輕輕響了一下」改為「木鈴輕輕響了幾聲」，與門扇餘晃相符。評估為可採用：事件因果、時間點、角色行動與既定物件設定一致，維持短促的入庄節奏；詳見 scene_integration_take02.json。
- 現行檢查起點：序章 script.rpy:44、清晨 script.rpy:108、後院 script.rpy:197。已重新開到序章首句，回報 BGM01 正在播放且 ambience 為空。木鈴與整段接續待生前確認。

## 2026-10-12 第三輪：序章恢復無配樂

生前回覆「也不要用這首，先維持原本沒有配樂的版本」。舊道與入庄交談已撤下 BGM01，恢復原有無配樂配置；舊道／前院連續風聲保持停用，五下漸弱木鈴及其他動作音效保留。第一章清晨沿用 BGM02 原有 1.5 秒淡入。已重新開到 script.rpy:44 舊道首句；後續入庄交談的實機紀錄回報 music 為空、僅播放室內底聲；現行配置見 scene_integration_take03.json，前兩輪保存為歷程。整批仍待場景確認。

## 2026-10-12 第四輪：停用全部持續環境音

生前指出推門入庄後的持續背景聲也不需要，要求移除所有類似的非 BGM 背景聲。室內底聲、後院水風與其餘循環環境全數停用；原六組 AMB 均取消製作／導入待辦。既有 BGM、UI 確認／返回，以及推門、五下木鈴、點火、餘燼、寫字與包布等短動作聲保留。

- 已移除 script.rpy 所有 `play ambience`；登錄的舊 ambience 通道僅保留存檔相容用途，每次互動與讀檔後停止並設通道音量為 0，避免舊存檔恢復持續背景聲。
- 三組已生成的環境候選與母檔留存為歷程，不代表現行採用；其餘三組不再列入後續製作。音效仍按七批完整場景順序驗收。
- 目前檢查起點：舊道 44、推門前 66、清晨 106、後院 194。已開到「旅店比他想像得更安靜。」；實機回報 ambience 為空、序章 music 為空，按下一句可聽推門與木鈴。現行配置為 scene_integration_take04.json。
- 本輪只調整聲音配置及待辦，不修改劇情事件；整批動作音效仍待生前確認。
