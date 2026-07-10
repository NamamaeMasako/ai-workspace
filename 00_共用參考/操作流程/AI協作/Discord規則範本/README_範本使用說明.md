# 範本使用說明

這個資料夾放 Discord 規則範本，目的是讓其他 AI 直接複製後改成自己的正式規則。

## 建議放置方式

- `discord_AGENTS.template.md` → 複製成 `@/workspace/contexts/discord/AGENTS.md`
- `guild_AGENTS.template.md` → 複製成 `@/workspace/contexts/discord/guilds/<guild_id>/AGENTS.md`
- `channel_AGENTS.template.md` → 複製成 `@/workspace/contexts/discord/guilds/<guild_id>/channels/<channel_id>/AGENTS.md`

## 使用原則

- 範本只放共通結構，不放單一 AI 的專屬值。
- 正式規則檔要把 `<AI_NAME>`、`<USER_CALLSIGN>`、實際路徑、是否主動回覆等補齊。
- 不要把這裡當正式規則本體；這裡是可複製的底稿。
- 若只需要最小可用版，先補全基本資訊與回覆邊界，再補特殊規則。

## 放置位置

建議這份資料放在每個 AI 共享 workspace 都能看到的位置，例如：

```text
@/workspace/00_共用參考/操作流程/AI協作/Discord規則範本
```
