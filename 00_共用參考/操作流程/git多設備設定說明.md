# git 多設備設定說明

適用對象：在自己設備上使用本 workspace 的每一位 AI（澪、沐晴、凜等）。
規則本文見 `@/workspace/AGENTS.md` 第 8 節；本檔是實際操作步驟。

## 架構（2026-07-10 定案）

- **OneDrive**：負責工作檔案的即時同步（日常編輯照舊，不需理會 git）。
- **GitHub**：負責版本歷史的合流。遠端：`https://github.com/NamamaeMasako/ai-workspace.git`（私有）。
- **各設備的 git 資料庫**：放在 OneDrive 之外的本機路徑 `C:\GitRepos\ai-workspace.git`，每台設備自己一份。
- workspace 根目錄的 `.git` 是一個單行指標檔（內容 `gitdir: C:/GitRepos/ai-workspace.git`），經 OneDrive 同步、所有設備共用同一內容——所以**每台設備都必須用同一個本機路徑** `C:\GitRepos\ai-workspace.git`。

## 一次性設定（每台新設備做一次）

澪的設備（首建 repo 的那台）已完成，其他設備依序執行；`<workspace>` 換成該設備解析後的 `@/workspace` 實際路徑：

1. **確認 git 已安裝**：`git --version`。

2. **把歷史從 GitHub 抓到本機**（第一次需要 GitHub 登入，會跳出瀏覽器視窗請生前完成）：

   ```powershell
   New-Item -ItemType Directory -Force C:\GitRepos | Out-Null
   git clone --bare https://github.com/NamamaeMasako/ai-workspace.git C:\GitRepos\ai-workspace.git
   git -C C:\GitRepos\ai-workspace.git config core.bare false
   git -C C:\GitRepos\ai-workspace.git config core.logallrefupdates true
   git -C C:\GitRepos\ai-workspace.git config core.worktree "<workspace>"
   git -C C:\GitRepos\ai-workspace.git config remote.origin.fetch "+refs/heads/*:refs/remotes/origin/*"
   ```

3. **確認指標檔存在**：`<workspace>\.git` 應是內容為 `gitdir: C:/GitRepos/ai-workspace.git` 的單行文字檔（會由 OneDrive 從其他設備同步過來；若沒有就自己建一個）。

4. **對齊帳本**（把索引對到目前歷史；不會動到任何工作檔案）：

   ```powershell
   git -C "<workspace>" fetch origin
   git -C "<workspace>" reset origin/main
   ```

5. **釘選指標檔**，防止 OneDrive 把它抽成雲端佔位符：

   ```powershell
   attrib +P "<workspace>\.git"
   ```

6. **驗證**：`git -C "<workspace>" status` 應能正常顯示；若有未 commit 的變動屬正常（那是 OneDrive 同步進來、還沒被任何設備 commit 的內容）。

## 日常規則

- 日常編輯檔案完全不受 git 影響，照舊即可。
- 做任何 git 操作前，先對齊帳本：`git fetch origin` → `git reset origin/main`。
- 完成一批有意義的變動後 commit（中文訊息）並**隨即 push**。
- push 被拒絕＝另一台先推了：`git fetch origin` → `git reset origin/main` → 重新 commit → push。這個流程不會弄壞任何東西，工作檔案永遠以 OneDrive 的現況為準。
- 不要 force push、不要改寫已存在的歷史、不要在專案資料夾內另外 `git init`。

## 疑難排解

- `git status` 回報 `not a git repository`：檢查指標檔是否存在、內容是否正確、`C:\GitRepos\ai-workspace.git` 是否存在（若無，重跑一次性設定第 2 步）。
- 出現大量「已刪除」狀態：多半是帳本沒對齊，跑第 4 步的對齊指令。
- 任何看不懂的 git 錯誤：停手回報生前，不要嘗試 force 類指令。歷史在 GitHub 上有完整副本，本機 git 資料庫壞了大不了重做一次性設定。
