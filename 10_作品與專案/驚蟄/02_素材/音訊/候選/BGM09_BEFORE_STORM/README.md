# BGM09 交卡與出發短版候選與鋼琴修訂

2026-10-13：BGM08 靜路輕箏 long_03 於序章實機確認後，接續製作本曲。第一輪四首短版完成（前三首 take01，第 4 首 take02）。2026-10-16 生前認為第 2 方向稍近，但要求更快、更不安；take02 的節奏獲認可，但情緒被指出偏悲傷；take03「警戒懸念版」已選為長版方向，60 秒 long_01 已製作循環副本、接入第七章交卡與出發段，開發版場景試用中；正式核可待確認。詳見[長版製作紀錄](longform/README.md)。

## 使用場景與情緒

第七章交出黑卡、同行選擇、離開月下庄、前往林道與交戰前的準備。兩輪、四條分支共用同一個方向；真正出手交戰時切換已核可 BGM06。

情緒為「風雨前的寧靜」：危險尚未發生，但心中已有戒備；相對緊張、聲音克制、節奏慢於戰鬥，不做吵雜鼓擊、快速推進、歡樂或恐怖片驚嚇，也不加入風雨等環境聲。

## 四個方向

1. 低弦沉息：低弦連續樂句與緩慢底層脈動，表現沉住氣的戒備。
2. 鋼琴暗潮：柔鋼琴與低弦，透過自然共鳴與未解和聲表現安靜的不安。
3. 箏影待雨：低音輕箏、長尾音與弦樂，保持克制與警覺。
4. 低管預兆：低音單簧管與弦樂，探索隱約陰影與壓住的緊張。

名稱、配器與情緒是製作意圖；實際生成的聽感及適配由生前試聽判斷。

| 方向 | 時長 | Seed | LUFS | dBTP | OGG |
| --- | --- | --- | --- | --- | --- |
| 01 低弦沉息 | 20 秒 | 3601 | -15.95 | -2.44 | `candidate_01_low_strings_seed3601_take01.ogg` |
| 02 鋼琴暗潮 | 20 秒 | 3602 | -16.17 | -2.25 | `candidate_02_felt_piano_seed3602_take01.ogg` |
| 03 箏影待雨 | 20 秒 | 3603 | -16.21 | -2.26 | `candidate_03_muted_guzheng_seed3603_take01.ogg` |
| 04 低管預兆 | 20 秒 | 3614 | -15.98 | -2.40 | `candidate_04_bass_clarinet_seed3614_take02.ogg` |

## 來源與處理

- 本機 ACE-Step 1.5 Turbo text2music、thinking=false、8 steps、固定 seed 3601／3602／3603／3614，未引用其他曲目的 reference_audio／src_audio。
- E minor、4/4、60／62／64／58 BPM 是模型提示，未宣稱實測節奏或調性。
- 原始 25 秒 WAV、48 kHz 立體聲浮點 PCM 存於 `../../母檔/BGM09_BEFORE_STORM/`；保留未淡出的完整來源，供後續長版樂句與尾音參考。
- 原始試聽取前 20 秒，淡入 0.03 秒／淡出 0.5 秒並初步 loudnorm；再作固定增益、-2.5 dBFS limiter（5 ms attack／50 ms release、延遲補償與時間戳重建），OGG 為 Vorbis q5、44.1 kHz 立體聲。
- 原始 WAV、OGG、premaster OGG、完整請求／回傳、處理參數與 SHA-256 保存於同名 JSON 和 generation_manifest_take01.json。
- 解碼結果、實測 LUFS／峰值與近靜音事件見 technical_check_take01.json；格式處理紀錄不代表聽感已核可。

第 4 方向首次 seed 3604 的尾端留白較長，因此交付前改製 take02／seed 3614，強化連續樂句與弦樂底層；首次來源／候選及 generation_manifest_initial_take01.json 留存為歷程，未曾由生前審聽否決。第 2 方向有約 0.80 秒的近靜音間隔，實測事件保留於紀錄；是否符合閱讀氣氛由生前試聽判斷。

## 下一步

選中短版實際以 reference_audio 引導約 60 秒長版。來源模板應保留自然樂句尾音，參照未淡出的 25 秒原母檔，避免直接以 19 秒間隔反覆拼接帶淡出的 20 秒短版而複製短收音。長版經生前確認後，才處理循環與開發版完整場景試聽。

完整場景配置見[音訊 Cue Sheet](../../音訊CueSheet_rev.1.md)。

## 鋼琴暗潮 take02：加快脈動與加深不安（2026-10-16）

- 生前回饋：「2版方向稍微比較對，但節奏感應該再快一些，並帶有更多的不安感。」這是方向修訂，尚未選定長版或正式採用。
- 新短版 `candidate_02_felt_piano_seed3622_take02.ogg`，20 秒。鋼琴保留為主體，增加重複低中音脈動與較短樂句間隔，透過半音摩擦、懸留和聲與不安定低音加深緊張；維持交卡／出發前的克制，不加入吵雜戰鼓或環境音。
- 原第 2 版 `candidate_02_felt_piano_seed3602_take01.ogg` 已實際作 multipart reference_audio 上傳，SHA-256 `71005648a7fd6d6e6507f9b1727bdc32877cb7923ddd2c8e81cf6a0ea2f8dafc`。以音訊參考保留鋼琴／室內樂方向，重新生成節奏與樂句，未把原檔直接加速或聲稱逐段保留。
- 本機 ACE-Step 1.5 Turbo text2music、thinking=false、8 steps、seed 3622；沒有 src_audio 或固定時間樂句模板。
- E minor／4拍與 80 BPM 為提示（原稿提示 62 BPM），不宣稱量測了實際節奏、調性或緊張程度；聽感由生前比較。
- 保留原始 25 秒 WAV；20 秒試聽作淡入淡出、音量匹配、限制峰值及時間戳重建，OGG 為 44.1 kHz 立體聲。實測 -16.06 LUFS／-2.33 dBTP；完整解碼無錯誤輸出，近靜音事件見 technical_check_piano_revision_take02.json。
- 原始 WAV、premaster OGG、原第 2 版、原始請求／回傳及雜湊均保留；generation_manifest_piano_revision_take02.json 保存本次來源與處理紀錄。待短版確認後才做長版，遊戲仍未導入 BGM09。

## 鋼琴 take03：緊張戒備、減少悲傷（2026-10-16）

- 生前回饋 take02「節奏可以，但聽起來比較悲傷；需要緊張的不安感」。take02 的節奏方向獲認可，情緒尚未採用。
- 新 20 秒短版 `candidate_02_felt_piano_seed3632_take03.ogg`，沿用 80 BPM 提示，目標是察覺威脅、繃緊神經與等待危險。減少抒情主旋律、下降樂句、悲戚長音與哀傷大提琴，改以非抒情的鋼琴短音型、持續低音、短弦音與未解決音程營造懸念。
- 原始 take01 第 2 版實際上傳為 reference_audio，僅作鋼琴音色方向參考；未用偏悲傷的 take02 作整體風格參考，沒有 src_audio／固定樂句模板，沒有直接加速舊檔。
- 本機 ACE-Step 1.5 Turbo text2music、thinking=false、8 steps、seed 3632；80 BPM／E minor／4拍為提示，未量測實際速度，也不宣稱生成後已達到主觀情緒目標。
- 原始 25 秒 WAV、20 秒 OGG、premaster、參考來源與 SHA-256／完整請求保存；實測 -16.35 LUFS／-2.21 dBTP，44.1 kHz 立體聲 OGG，完整解碼無錯誤輸出，近靜音紀錄見 technical_check_piano_revision_take03.json。
- 使用場景仍為第七章交卡、同行選擇與出發前，實際交戰才切 BGM06。新版待生前比較緊張／悲傷的感受差異，尚未製作長版、循環或導入。

## take03 長版試作（2026-10-16）

生前回覆「這版好像還行，做成長版試試」，已以選中短版實際作 reference_audio、未淡出的原始母檔作自然樂句來源，完成 60 秒 long_01。待確認情緒、節奏與銜接後再做循環／導入，詳見[長版紀錄](longform/README.md)。
