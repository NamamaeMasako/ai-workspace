# OpenClaw 升版步驟

這份是給生前、澪、沐晴、凜共用的升版參考。升版前先確認「是哪一台設備／哪一位 AI 的本地環境」，不要假設兩台機器狀態相同。

## 0. 先確認目前狀態

```powershell
openclaw status
openclaw update status
```

如果只是想預覽會做什麼，不要真的升版：

```powershell
openclaw update --dry-run
```

## 1. 建議升版流程（一般情況）

```powershell
openclaw update
```

`openclaw update` 會依安裝方式處理升版，通常會：

- 檢查目前 channel / 版本
- 更新 OpenClaw
- 同步 plugins
- 執行 doctor
- 重啟 Gateway（除非加 `--no-restart`）

## 2. 升版後驗證

```powershell
openclaw doctor
openclaw gateway status
openclaw health
```

確認重點：

- Gateway 有正常 running
- Discord / 其他 channel 還能收發
- `doctor` 沒有新的致命錯誤
- 重要插件或節點沒有失效

## 3. 切換版本線

穩定版：

```powershell
openclaw update --channel stable
```

Beta：

```powershell
openclaw update --channel beta
```

開發版 / main：

```powershell
openclaw update --channel dev
```

單次指定 tag / version：

```powershell
openclaw update --tag <version-or-tag>
```

建議切 channel 前先 dry-run：

```powershell
openclaw update --channel beta --dry-run
```

## 4. 如果不想讓它自動重啟

```powershell
openclaw update --no-restart
```

之後手動重啟：

```powershell
openclaw gateway restart
```

注意：`--no-restart` 後，正在跑的 Gateway 可能還是舊 code，直到重啟才會吃到新版。

## 5. 如果升版失敗

先不要亂刪資料。OpenClaw 的設定、憑證、workspace 通常在 `~/.openclaw`，升版主要動的是 OpenClaw 程式本體。

依序試：

```powershell
openclaw doctor
openclaw update --dry-run
openclaw update
```

如果 npm/package 安裝階段壞掉，可用安裝器修復（官方文件建議）：

```bash
curl -fsSL https://openclaw.ai/install.sh | bash -s -- --install-method npm
```

Windows 若沒有 bash/curl 環境，先用目前平台可用的官方安裝方式，或請其中一位 AI 查當前官方文件後再動。

## 6. Rollback / 降版

npm 全域安裝可指定版本：

```powershell
npm i -g openclaw@<version>
openclaw doctor
openclaw gateway restart
```

查目前 npm 最新版：

```powershell
npm view openclaw version
```

如果是 source/git checkout，要用 git checkout 到指定 commit/tag，再 install/build，這種情況先不要憑記憶操作，先查 local docs 或 repo 狀態。

## 7. 生前這台目前常用指令備忘

```powershell
openclaw status
openclaw update status
openclaw update --dry-run
openclaw update
openclaw doctor
openclaw gateway status
openclaw gateway restart
openclaw health
```

## 8. 注意事項

- 升版前先確認是在澪、沐晴還是凜的機器上。
- 有外部服務、Discord bot、節點連線時，升版後要實測收發，不只看 service running。
- 不要用 `openclaw gateway stop` + `start` 假裝 restart；要重啟就用 `openclaw gateway restart`。
- 看到 downgrade、破壞性操作、或需要刪檔時，先停下來問生前。
- 參考官方 local docs：
  - `docs/install/updating.md`
  - `docs/cli/update.md`
