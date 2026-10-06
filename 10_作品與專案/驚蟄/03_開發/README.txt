# 驚蟄 / Ren'Py 專案說明

專案位置：`03_開發/JingZhe`
目前版本：`0.1.2`

現行內容：
- 短引、序章至第八章與真結局。
- 第七章包含先後兩次交卡路線，最終收束至「把卡留給自己」。
- 正式背景、角色立繪、事件圖與 CG 已導入。
- Windows 獨立版輸出至 `05_成品/`。
- `BGM01_LANTERN` seed 2802 箏版已導入主選單；`BGM02_MOON_INN_DAY` long_04 尺八版已導入日間段落；`BGM03_MOON_INN_NIGHT` seed 3003 柔鋼琴 `loop_xfade06` 版已導入月下庄夜間段落。`BGM04_BLACK_CARD_MEMORY` 的酒館 `long_03` 循環版與黑卡 `long_04` 懸疑版已接入第三章，並於 2026-10-02 經生前實機試聽確認採用。以上皆透過音樂通道循環並由設定頁「音樂音量」控制；完整規劃見 `02_素材/音訊/音訊CueSheet_rev.1.md`。

主要檔案：
- `game/script.rpy`：主劇本與分支流程。
- `game/characters.rpy`：角色名與對話樣式。
- `game/placeholders.rpy`：正式 image 定義、角色站位與演出 Transform；檔名為歷史沿用。
- `game/screens.rpy`：主選單、快速選單、存讀檔、設定與說明。
- `game/options.rpy`：標題、版本、功能開關與製作名單。
- `game/build.rpy`：正式發行包排除規則。
- `game/THIRD_PARTY_LICENSES.txt`：第三方字型授權。

固定驗證：
1. Ren'Py lint 無錯誤。
2. Windows ZIP 內必要背景、CG、立繪與字型存在，排除項目不存在。
3. 獨立版不經 SDK 啟動成功並進入序章。
4. 公開版需另外完整測試兩種首次選擇、兩條第二輪路線、存讀檔、自動播放與真結局。
