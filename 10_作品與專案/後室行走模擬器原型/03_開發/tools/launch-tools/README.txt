Launch files整理：

根目錄唯一平常啟動入口：
- START_GAME.bat：直接啟動遊戲。

工具檔案：
- run_game_check.bat：Godot headless 快速檢查專案能不能載入，不開遊戲視窗，跑完就退出。
- run_game_debug.bat：console/verbose 模式啟動遊戲，適合抓錯、看 log、找閃退或互動異常原因。
- run_game_legacy.bat：舊入口備份，不建議使用。

連續空間物理驗證（2026-09-08）：
- 在 03_開發 目錄執行：
  <Godot executable> --headless --path . --script res://tools/launch-tools/check_continuous_walk.gd
- 不開遊戲視窗，使用真實角色碰撞檢查鎖門／解鎖、動畫、兩段走廊往返、視角、鑰匙與音訊混合。
- 成功輸出 CONTINUOUS_WALK_FAILURES=0，exit code 0。
- 此測試不代表美術、聽感或所有角度已由人類驗收。
