---
name: project-creator
description: Create or scaffold new project folders under the workspace's 10_作品與專案 structure (@/workspace/10_作品與專案); use when the user asks to create a project and clarify whether it is a creative/work project or a technical/development project, then create safe folders, navigation/rules files, AGENTS.md, continuation summary, shared references, archives, and consistent naming.
---

# Project Creator

Use this skill when 生前 wants to create, initialize, reorganize, or plan a new project folder.

If 生前 says only 「幫我建立一個專案」 or similar, ask one short clarification:

> 要建立哪一種？
> 1. 作品型：故事、遊戲、Live2D、角色、世界觀、AI 創作等
> 2. 開發型：程式、工具、網站、Bot、資料處理、實驗 repo 等

Prefer the labels **作品型** and **開發型**. Avoid the label 「軟體型」 unless 生前 uses it first, because some technical projects are scripts, tools, datasets, automations, or experiments rather than polished software.

Default project root (all devices):
`@/workspace/10_作品與專案`

`@/workspace` is each AI's own workspace root as defined in the root `AGENTS.md` (for 澪's current machine: `C:\Users\User\OneDrive\Workspace`). Do not assume another AI can use 澪's absolute path; resolve `@/workspace` on that AI's own machine.

If the resolved root path does not exist on the current device, do not invent a replacement. Report that the project root is unavailable on this machine and ask whether to use another path or wait for the correct device/sync state.

> 2026-07-10 update: the old root `C:\Users\User\OneDrive\Projects` no longer exists; the workspace was renamed/restructured to `Workspace` with projects under `10_作品與專案`. Never scaffold outside `@/workspace/10_作品與專案` unless 生前 explicitly asks.

## Ground rules

- Work in a 作品本位 structure: one work/project owns its own folder, rules, assets, development files, outputs, references, and archive.
- Prefer safe scaffolding: create missing folders/files; do not delete, overwrite, or move existing project content without explicit confirmation.
- Before creating, check whether a similar project folder already exists.
- If a requested project name may be ambiguous or conflicts with an existing folder, ask once.
- Keep generated placeholder files short and practical.
- For external/public actions such as creating Discord channels, ask first unless the user explicitly requested it. Assume 生前 may create/coordinate Discord channels/categories personally when needed.

## Project modes

### 作品型 scaffold

Use for stories, games, Live2D, characters, worldbuilding, image/LoRA/AI creative work, and other work where text/assets/outputs matter more than code repository conventions.

Create:

```text
<ProjectName>\
  AGENTS.md
  00_導覽與規則\
    00_接續摘要.md
    開發規則.md
    專案索引.md
  01_文本\
  02_素材\
  03_開發\
  04_共用參考\
  05_成品\
  99_封存\
```

Since 2026-07-10, every project must have its own `AGENTS.md` (entry rules for AI taking over) and `00_導覽與規則\00_接續摘要.md` (continuation summary; this exact filename is the workspace-wide convention).

Known existing convention from memory:
- Projects may already use `01_文本`, `02_素材`, `03_開發`, `05_成品`, `99_封存`.
- Newer 作品本位 projects should include `00_導覽與規則` and `04_共用參考`.
- `04_共用參考` inside a project is for that project's recurring references, not where this AgentSkill itself should live.
- Root-level shared material may live under `00_共用參考`.
- Worldbuilding/reference folders use: `00_導覽與索引`, `01_世界規則`, `02_角色與勢力`, `03_時間線`, `04_共用參考`. (Legacy `04_共用參照` was merged into `04_共用參考` on 2026-07-10.)

### 開發型 scaffold

Use for code, tools, websites, bots, local automations, data processing, experiments, and reusable technical work. Keep it generic enough that 凜 or another engineering-focused AI can adapt it to language/framework-specific conventions later.

Default structure:

```text
<ProjectName>\
  00_導覽與規則\
    開發規則.md
    專案索引.md
  01_需求與設計\
  02_參考資料\
  03_開發\
    src\
    tests\
    docs\
  04_資料與素材\
  05_輸出與發佈\
  99_封存\
```

Optional additions only when useful: `scripts`, `config`, `data`, `notebooks`, `assets`, `.github`, `deploy`, `experiments`. Do not add language-specific boilerplate unless 生前 requested the stack or an existing repo convention is obvious.

## Creation workflow

1. Resolve project root.
   - Default: `@/workspace/10_作品與專案` (resolve `@/workspace` per this device's definition in the root `AGENTS.md`).
   - Verify with `Test-Path` or equivalent before writing.
2. Inspect existing folders in the root.
   - Look for exact or near-name collisions.
   - If the project already exists, offer to fill only missing scaffold pieces.
3. Choose project mode:
   - If unclear, ask whether it is **作品型** or **開發型**.
   - Creative/game/story/Live2D/AI art/worldbuilding: use 作品型.
   - Code/tool/site/bot/automation/data/research repo: use 開發型.
   - Worldbuilding/reference library: use the worldbuilding scaffold below.
   - Existing project repair: add only missing agreed folders/files.
4. Create directories with non-destructive commands.
5. Create placeholder files only if absent:
   - `AGENTS.md`
   - `00_導覽與規則\00_接續摘要.md`
   - `00_導覽與規則\開發規則.md`
   - `00_導覽與規則\專案索引.md`
6. Verify by listing the created tree.
7. Report what was created and any decisions still needing 生前.

## Placeholder file templates

Use these for 作品型. For 開發型, adapt the folder purpose list to the 開發型 scaffold and include stack/status fields only when known.

### 開發規則.md

```markdown
# 開發規則

## 專案定位
- 名稱：<ProjectName>
- 類型：<待補>
- 目前狀態：草稿

## 協作規則
- 本資料夾是此作品的主要工作區。
- 重要決策、設定變更、命名規則應記錄在本區或 MEMORY/索引中。
- 不覆蓋原始素材；需要修改時優先建立新版或放入開發區。
- 舊版本、廢案、暫停內容移入 `99_封存`，不要直接刪除。

## 資料夾用途
- `01_文本`：劇本、設定文、文案、草稿。
- `02_素材`：圖片、音訊、模型、參考素材、資料集。
- `03_開發`：工程檔、工具輸出、實驗、可重建中間檔。
- `04_共用參考`：此作品會反覆引用的共用資料與外部參照。
- `05_成品`：交付版、輸出版、可展示結果。
- `99_封存`：舊版、廢案、備份、歷史資料。
```

### 專案索引.md

```markdown
# 專案索引

## 快速入口
- 開發規則：`00_導覽與規則/開發規則.md`
- 文本：`01_文本/`
- 素材：`02_素材/`
- 開發：`03_開發/`
- 共用參考：`04_共用參考/`
- 成品：`05_成品/`
- 封存：`99_封存/`

## 目前重點
- <待補>

## 重要連結 / 相關頻道
- <待補>
```

### AGENTS.md

```markdown
# AGENTS.md - <ProjectName>

此資料夾是「<ProjectName>」的作品／專案資料。

## 接手時先讀

1. `@/workspace/AGENTS.md`
2. `@/workspace/10_作品與專案/AGENTS.md`
3. 本檔
4. `00_導覽與規則/00_接續摘要.md`
5. `00_導覽與規則/開發規則.md`

## 專案定位

<一兩句：這是什麼、目標是什麼、目前階段>

## 世界觀歸屬

本專案目前不屬於任何世界觀。若要與某世界觀連動，先與生前確認，不要自動歸類。
<若已確認歸屬，改寫本節並附世界觀入口路徑>

## 主要資料夾

<照實際結構列出，附一句用途說明>
```

### 00_接續摘要.md

```markdown
# <ProjectName> - 接續摘要

> 有實質進度時直接更新本檔；本檔是接手 AI 的第一手進度來源。

## 目前狀態

- <待補>

## 下一步建議

1. <待補>
```

Also remember to add the new project to the 目前專案 list in `@/workspace/10_作品與專案/AGENTS.md` (one line with a short description and worldview affiliation).

## Version control note

The whole workspace is a single git repo (since 2026-07-10, see root `AGENTS.md` §8). Do **not** run `git init` inside a new project; new files are covered by the workspace repo. After scaffolding, a commit of the new project folder is welcome.

## Worldbuilding/reference scaffold

For a shared worldbuilding folder, use:

```text
<WorldName>\
  00_導覽與索引\
  01_世界規則\
  02_角色與勢力\
  03_時間線\
  04_共用參考\
  99_封存\
```

Naming is normalized to `04_共用參考` (the legacy `04_共用參照` was merged on 2026-07-10 with 生前's approval). If another legacy-named folder appears, do not rename automatically; follow the existing folder unless 生前 asks to normalize it.

## Suggested PowerShell patterns

Use this kind of safe creation pattern; adapt root, name, and mode as needed.

For **作品型** projects:

```powershell
$root = 'C:\Users\User\OneDrive\Workspace\10_作品與專案'  # 澪's machine; other AIs resolve @/workspace/10_作品與專案 on their own device
$name = '<ProjectName>'
$project = Join-Path $root $name
if (-not (Test-Path $root)) { throw "Projects root not found: $root" }
if (Test-Path $project) { Write-Output "EXISTS: $project" } else { New-Item -ItemType Directory -Path $project | Out-Null }
$dirs = @('00_導覽與規則','01_文本','02_素材','03_開發','04_共用參考','05_成品','99_封存')
foreach ($d in $dirs) { New-Item -ItemType Directory -Path (Join-Path $project $d) -Force | Out-Null }
```

For **開發型** projects:

```powershell
$root = 'C:\Users\User\OneDrive\Workspace\10_作品與專案'  # 澪's machine; other AIs resolve @/workspace/10_作品與專案 on their own device
$name = '<ProjectName>'
$project = Join-Path $root $name
if (-not (Test-Path $root)) { throw "Projects root not found: $root" }
if (Test-Path $project) { Write-Output "EXISTS: $project" } else { New-Item -ItemType Directory -Path $project | Out-Null }
$dirs = @(
  '00_導覽與規則',
  '01_需求與設計',
  '02_參考資料',
  '03_開發',
  '03_開發\src',
  '03_開發\tests',
  '03_開發\docs',
  '04_資料與素材',
  '05_輸出與發佈',
  '99_封存'
)
foreach ($d in $dirs) { New-Item -ItemType Directory -Path (Join-Path $project $d) -Force | Out-Null }
```

Write placeholder files only when they are absent; never overwrite existing rules or indexes silently. For 開發型 placeholder files, adapt folder purpose lists to the 開發型 scaffold instead of copying the 作品型 wording.

## Report format

Keep the final report short:
- Created/updated path
- Folders/files added
- Existing items left untouched
- Decisions needed from 生前, if any
