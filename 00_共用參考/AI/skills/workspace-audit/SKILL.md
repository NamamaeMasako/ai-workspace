---
name: workspace-audit
description: Run a health check on the creative workspace (@/workspace) - detect drift between AGENTS.md rules and actual folder structure, broken path references, absolute paths that should be abstract, duplicate/bilingual folder pairs, stale 00_ToSort items, missing per-project entry files, generated caches leaking into git, and git repo health; use when 生前 asks for a workspace 健檢/體檢/audit, before or after any large reorganization, or periodically.
---

# Workspace Audit（工作區健檢）

對 `@/workspace` 做一輪健康檢查，找出「規則寫的」與「資料夾實際長的」之間的漂移。
**本 skill 原則上只報告、不動手**；除非生前明確核可，才執行修正（workspace 規則：大量搬移／改名前先列計畫確認）。

起源：2026-07-10 的一次全面健檢。當時發現的問題（失效的空 .git、重複資料夾、過時索引路徑、缺接續摘要）全部屬於下列檢查類型。

## 執行時機

- 生前說「健檢」「體檢」「audit」「檢查工作區」。
- 大規模整理、搬移、改名之前（建基準）與之後（驗證引用）。
- 平時建議每 1–2 個月跑一次。

## 檢查清單

依序執行，逐項記錄結果。路徑以該設備解析後的 `@/workspace` 為根。

### 1. git 健康（最優先）

- `git -C <workspace> status` 應正常運作；若回報 not a repository，表示 `.git` 又被 OneDrive 抽空（歷史事故），立即回報為高優先。
- 抽查 `.git` 內檔案是否帶 Pinned 屬性（`attrib <workspace>\.git\HEAD` 應含 `P`）；若遺失，重跑 `attrib +P "<workspace>\.git\*" /S /D`。
- 檢查是否有未 commit 的變更堆積（`git status --short`）；有意義的變動應已 commit（根 AGENTS.md 第 7 節第 13 條）。
- 檢查遠端狀態：`git remote -v`。若已有遠端，檢查最後 push 時間；若尚無遠端，提醒異地備份缺口（根 AGENTS.md 第 8 節）。

### 2. 生成快取入庫檢查

- `git status --ignored --short` 抽查：新出現的快取類型（新引擎、新工具的自動生成物）是否已被 `.gitignore` 涵蓋。
- 常見漏網：`.godot/`、`game/cache/`、`*.rpyc`、tensorboard 事件檔、`node_modules/`、`__pycache__/`。
- 發現新類型 → 建議同步更新 `.gitignore` 與根 AGENTS.md 第 8 節清單。

### 3. 規則 vs 實際結構

- 根目錄實際資料夾 vs 根 AGENTS.md 第 1 節描述。
- `00_共用參考` 實際子資料夾 vs 根 AGENTS.md 的「目前實際子分類」。
- `10_作品與專案` 實際專案 vs 其 AGENTS.md 的「目前專案」清單。
- 任何一邊多出或少掉，都算漂移。

### 4. 每專案必備檔

每個 `10_作品與專案\<專案>` 應有：

- `AGENTS.md`（2026-07-10 起必備）
- `00_導覽與規則\00_接續摘要.md`（統一檔名，不接受其他命名）
- `00_導覽與規則\開發規則.md`

使用自訂編號的專案，其 AGENTS.md 內應有與全域模板的編號對照（例：Virtual_Avatar_Studio）。

### 5. 斷鏈引用

- Grep 所有 `.md`／`.txt` 中的 `@/workspace/...` 路徑，逐一驗證目標存在。
- 特別注意 AGENTS、索引、導覽、接續摘要類文件——這些是接手入口，斷了最傷。
- 斷鏈不直接判定失敗：先在對應資料夾找同用途新檔（根 AGENTS.md 第 7 節第 9 條），再回報「引用需更新」。

### 6. 絕對路徑洩漏

- Grep `C:\Users`（或該設備的本機根）出現在 `.md`／`.txt` 中的位置。
- 允許出現的地方：根 AGENTS.md 的 `@/` 定義示範、`99_封存` 內、本機工具／服務／debug 紀錄（如 OpenClaw、skill 內的本機示例，但需標明是某台設備的路徑）。
- 其他位置一律建議改為 `@/workspace` 寫法。

### 7. 重複與中英並存資料夾

- 同層出現同用途兩資料夾（歷史案例：`04_共用參照`/`04_共用參考`、`audio`/`音效`、`launch-tools`/`啟動工具`）。
- 同層出現語意衝突的相同編號（例：某專案 `04_` 不是共用參考卻用了 04）。
- 內容幾乎相同、檔名相似的成對索引檔。

### 8. 封存紀律

- `03_開發` 內不應有 `99_` 開頭資料夾、散落的 `.bak`、舊 log、crash log（Ren'Py 的 errors.txt/traceback.txt 等）——應在專案層 `99_封存`。
- `99_封存` 內的資料夾應附日期與原因（資料夾名或說明檔）。

### 9. 00_ToSort 超期

- 列出存放超過 14 天的項目，向生前提出歸檔建議（根 AGENTS.md 第 7 節第 12 條）。
- 不要未經確認就自行歸檔。

### 10. 記憶文件同步

- 黑貓：`00_接續摘要.md`（主檔）與 `MEMORY.md`（頻道快照）的「最後整理」日期與最新進度段落應一致；快照不得超前主檔。
- 各專案接續摘要的「目前狀態」是否明顯落後實際資料（例如 03_開發 有大量新檔案但摘要未提）。
- 世界觀 `03_時間線` 進度索引是否落後作品接續摘要。

## 報告格式

依嚴重度分級輸出：

- **高**：資料安全或接手入口直接受影響（git 失效、主檔斷鏈、必備檔缺失）。
- **中**：會誤導 AI 判斷（規則漂移、重複資料夾、過時索引、快取入庫）。
- **低**：紀律與一致性（絕對路徑、封存位置、超期 ToSort）。

每項附：位置、證據、建議做法、預估工作量。修正需生前核可後才執行；核可後的修正完成時，記得依根 AGENTS.md 第 7 節第 8 條同步更新所有受影響的規則與索引，並 commit。
