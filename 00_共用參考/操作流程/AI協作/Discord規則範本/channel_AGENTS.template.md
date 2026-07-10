# Discord Channel Rules - <channel_id> 範本

> 這是單一 Discord 頻道規則範本。  
> 請複製到 `contexts/discord/guilds/<guild_id>/channels/<channel_id>/AGENTS.md` 後再改寫。

## 基本資訊

- 伺服器 ID：`<guild_id>`
- 頻道 ID：`<channel_id>`
- 頻道名稱：`<channel_name>`
- 頻道用途：`<channel_purpose>`
- 對應作品／專案：`<project_or_work_name>`
- 對應世界觀：`<world_setting_name_or_none>`

## 套用範圍

此檔只套用於本頻道。  
若與伺服器規則不同，以本檔作為更具體補充；但不能違反隱私、安全與身分邊界。

## 頻道定位

此頻道用來：

- `<purpose_1>`
- `<purpose_2>`
- `<purpose_3>`

不適合在此頻道處理：

- `<not_for_1>`
- `<not_for_2>`

## AI 回覆規則

- 被 tag／mention 時，根據頻道用途回覆。
- 沒有 tag／mention 時：`<silent_or_allowed>`。
- 如果只是確認、稱讚、看到了，可優先用 emoji 反應。
- 不要把其他頻道或私人 DM 的內容直接搬來這裡，除非生前明確要求且不涉及隱私。
- 回覆盡量一次整理清楚，避免連續多則拆碎。
- 若本頻道主要是收訊或收斂狀態，寧可安靜，也不要為了存在感硬回。

## 專案／作品資料入口

如果此頻道對應 workspace 內的某個作品或專案，請填：

```text
@/workspace/<PROJECT_FOLDER>
```

其中 `@/` 由每位 AI 在自己的本機規則中自行定義。

建議讀取順序：

1. `@/workspace/AGENTS.md`
2. `@/workspace/<PROJECT_FOLDER>/AGENTS.md`（如果存在）
3. `@/workspace/<PROJECT_FOLDER>/00_導覽與規則`
4. 任務需要的文本、素材、開發或成品資料

## 世界觀資料入口

如果此頻道對應某個世界觀，請填：

```text
@/workspace/00_共用參考/世界觀/<WORLD_FOLDER>
```

如果生前說「去看 `<WORLD_NAME>` 的總覽」，應先讀該世界觀總覽，再處理任務。

## 特殊規則

- `<special_rule_1>`
- `<special_rule_2>`
- `<special_rule_3>`

## 待補

- 此頻道是否允許 AI 主動提案
- 此頻道是否允許 AI 主動整理進度
- 此頻道是否有固定輸出格式
- 此頻道是否有禁忌內容