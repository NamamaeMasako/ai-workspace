# 包子（Baozi）

包子是 Virtual_Avatar_Studio 的角色，與凜（Rin）分開管理。Codex 角色對話名稱為 `v-skin｜包子（Baozi）`。

2026-10-06 依使用者指示，從 OpenClaw 本機工作區的外包 Live2D 資料整併至本專案。原資料曾依外包流程分類，此次整理不變更素材的來源、使用權或交付關係；不與其他角色素材混用。

## 現行工作入口

以 `03_Live2D/既有專案整包/` 為既有 Live2D 專案根目錄，完整保留原內部結構：

- Cubism 工作檔：`03_Live2D/既有專案整包/work/包子.cmo3`。
- PSD 部位來源：`03_Live2D/既有專案整包/source/parts/`。
- 統合 PSD：`03_Live2D/既有專案整包/source/包子.psd`。
- 素材流程：`03_Live2D/既有專案整包/source/README.md`。
- 既有 VTube Studio 匯出：`03_Live2D/既有專案整包/export_vts/包子/包子.model3.json`。
- 既有預覽：`03_Live2D/既有專案整包/preview/`。

PSD 部位檔與統合檔的關係、工具執行方式依素材流程文件。`tools/` 依相對位置定位 `source/` 等資料夾，不要單獨搬動其中一個資料夾。

## 歷史與草稿

- `99_封存/OpenClaw舊工作歷史/`：原 `media/bao_live2d`，含早期素材、工程版本與操作截圖。
- `99_封存/OpenClaw修復草稿/`：原 `tmp/bao_live2d_repair`，含修復素材、工程與預覽。
- 整包內的 `archive/`、各 `*_backup_*` 與 `tmp_*` 保留原分類，用於回溯，不自動當作現行正式版本。

## 搬遷記錄與多設備

- 搬遷前後已核對 300 個檔案的 SHA-256；此次沒有重新生成模型或修改 PSD／Cubism／匯出內容。
- `00_角色設定/2026-10-06_搬遷清單.json` 記錄搬遷前檔案雜湊與來源／目的地；其中絕對路徑只描述此次搬遷設備，其他設備應以自己的 `@/workspace` 定位本專案。
- 此次設備的三個舊 OpenClaw 路徑保留目錄連結（Junction），指向本角色資料。它們不是另一份專案，不應另行編輯成獨立版本。
- 其他設備直接使用共用 Workspace 下的本角色資料夾，不依賴本機 `.openclaw` 路徑。

## 下一步

- 從上述現行入口接續工作，先確認任務要修改的版本與角色。
- 本次僅整理資料，尚未在 Cubism／VTube Studio 重新開啟或檢查匯出效果。
