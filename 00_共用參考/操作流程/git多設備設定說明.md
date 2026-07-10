# git 多設備設定說明

適用對象：在自己設備上使用本 workspace 的每一位 AI（澪、沐晴、凜等）。
背景：workspace 自 2026-07-10 起是單一 git repo，`.git` 目前經 OneDrive 同步到所有設備（過渡架構）。規則本文見 `@/workspace/AGENTS.md` 第 8 節。

## 每台設備的一次性設定

在自己的設備上依序執行（把 `<workspace>` 換成該設備解析後的 `@/workspace` 實際路徑）：

1. **確認 git 可用且 repo 健康**

   ```powershell
   git -C "<workspace>" status
   ```

   應顯示分支與工作樹狀態。若回報 `not a git repository`，代表 `.git` 尚未同步完成或已被 OneDrive 抽空——先等 OneDrive 同步完畢再試；若仍失敗，回報生前，不要自行 `git init`。

2. **釘選 `.git`（關鍵步驟）**

   防止 OneDrive「檔案隨選」把 `.git` 內容抽成雲端佔位符（2026-07-10 之前的舊 repo 就是這樣失效的）：

   ```powershell
   attrib +P "<workspace>\.git\*" /S /D
   ```

   驗證：`attrib "<workspace>\.git\HEAD"` 的輸出應含 `P`。

3. **不需要另外設定身分**——repo 的 user.name／user.email 存在 `.git\config`，已隨 OneDrive 同步。

## 日常規則（每次都要遵守）

- 任何設備都可以 commit，沒有特權設備。
- **commit 前確認 OneDrive 同步已完成**（工作列 OneDrive 圖示為綠勾，不是同步中）。
- **不要在兩台以上設備同時執行 git 操作**（commit、checkout、reset 等）。編輯檔案不受此限，隨時可以。
- 完成一批有意義的變動後 commit，訊息用中文簡述；不要 force push、不要改寫已存在的歷史。
- 若在 `.git` 內看到 OneDrive 衝突副本檔（檔名含「的副本」或裝置名），停止 git 操作並回報生前。

## 未來升級（接上遠端後）

生前提供 GitHub 私有 repo 後，架構會升級為：各設備 `.git` 搬出 OneDrive（本機各持一份）、以遠端 push/pull 合流、OneDrive 只同步工作檔案。屆時本文件會改寫，各設備需重做設定。
