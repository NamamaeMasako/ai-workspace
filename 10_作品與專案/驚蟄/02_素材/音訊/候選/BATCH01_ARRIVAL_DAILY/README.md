# 第一批：抵達月下庄與日常場景

2026-10-12：生前核可七批場景順序。第一批完成三組環境音、六個動作音檔並導入開發版，待整段場景試聽；尚未正式定案。

## 本批素材

| Cue | 方向／用途 | 長度 | 音檔 |
| --- | --- | --- | --- |
| AMB01_ROAD_WIND | 舊道暮色、低風與草木 | 45.00 秒 | [amb_road_twilight_wind_take01.ogg](amb_road_twilight_wind_take01.ogg) |
| AMB02_INN_WOOD_ROOM | 木造旅店清淡室內底聲與遠處木構 | 45.00 秒 | [amb_inn_wood_room_take01.ogg](amb_inn_wood_room_take01.ogg) |
| AMB03_COURTYARD_WATER_WIND | 後院柔水流與風 | 45.00 秒 | [amb_courtyard_water_wind_take01.ogg](amb_courtyard_water_wind_take01.ogg) |
| SFX01_SLIDING_DOOR | 序章推門入庄 | 0.86 秒 | [world_sliding_door_take01.ogg](world_sliding_door_take01.ogg) |
| SFX03_WOOD_BELL | 拉門後稍晚的木鈴 | 0.48 秒 | [world_wood_bell_take01.ogg](world_wood_bell_take01.ogg) |
| SFX13_KISERU_IGNITE | 序章煙草燃起 | 0.72 秒 | [magic_kiseru_ignite_take01.ogg](magic_kiseru_ignite_take01.ogg) |
| SFX15_EMBER | 第一章前院煙草餘燼 | 1.15 秒 | [magic_kiseru_ember_take01.ogg](magic_kiseru_ember_take01.ogg) |
| SFX07_WRITING | 第一章後院寫下與重寫句子 | 1.05 秒 | [world_writing_pen_take01.ogg](world_writing_pen_take01.ogg) |
| SFX08_PAPER_FOLD | SFX08 包布摩擦變體；摺紙基礎音仍待第二批 | 0.68 秒 | [world_cloth_wrapped_naginata_take01.ogg](world_cloth_wrapped_naginata_take01.ogg) |

SFX07 因第一章後院已有寫字動作，本批提前納入。SFX08 僅完成包布摩擦變體，摺紙基礎聲仍於第二批製作，不將該 cue 全項認列為完成。

## 連續場景檢查

1. 序章舊道 → 煙草點火 → 抵達旅店 → 拉門、木鈴 → 室內交談。起點 `script.rpy:43`。
2. 第一章清晨房間 → 早餐 → 前院煙斗餘燼；室內底聲轉為較淡的戶外風。起點 `script.rpy:107`。
3. 後院水風聲 → 寫下與重寫句子 → 花見攜帶包著薙刀的布料 → 傍晚回到大廳。起點 `script.rpy:196`。

請連同既有 BGM 一起判斷音色、強弱、遠近、動作觸發、循環與場景接續。包布只在物件出現時輕補，不加入未發生的拆布動作；擦刀柄處保持留白。每次修正以相同場景重聽為準。

## 製作與配置

- 本批是原創程序合成：週期性濾波噪聲、柔和木質共振、摩擦與火星瞬態；未使用外部錄音或音樂模型。自然感與場景適配為設計方向，由生前審聽確認。
- 環境音各 45 秒、48 kHz 雙聲道 PCM 24-bit 母檔；週期性合成與末端 20 ms 修整讓母檔首尾 PCM 值一致。OGG 為 44.1 kHz 立體聲 Vorbis q6；此技術結果不代表已獲無縫聽感核可。
- 動作音效為 48 kHz 單聲道 PCM 24-bit 母檔、44.1 kHz 單聲道 OGG。參數、固定種子、音量與雜湊見同名 JSON／generation_manifest_take01.json；全部 OGG 完整解碼，無錯誤輸出。
- 可編輯來源 `produce_batch01_take01.py` 與母檔存於 `@/workspace/10_作品與專案/驚蟄/02_素材/音訊/母檔/BATCH01_ARRIVAL_DAILY/`。
- `game/scene_audio.rpy` 建立獨立 ambience 通道，與 sound／UI 音效共用既有 sfx mixer。環境與動作音效由設定頁「音效音量」控制；音樂仍由既有 music mixer 控制。
- 遊戲音檔為候選原檔副本；前院風量 0.45、後院水風 0.8，其餘環境為 1.0，場景切換約 1.0–1.5 秒淡化。門聲結束後留 0.12 秒，再響木鈴；場景播放不插入額外等待閱讀的 pause。
- 第一章結束、進第二章時淡出本批環境；返回主選單與重新開始也停止環境／劇情音效，避免戶外聲留在選單。第二批尚未導入。
- 已指定開發 basedir，開到序章舊道；引擎截圖與環境通道狀態確認啟動正常，完整配置見 scene_integration_take01.json。尚未替生前確認實際聽感，未重建發行包或升版。
