# 包子 PSD 素材流程

## 正式來源

- `parts/*.psd`：各部位的單一來源檔。修改部位時只改對應檔案。
- `包子.psd`：由部位 PSD 組合出的統合檔，也是建立 Cubism model 的來源。

不要同時手動修改部位 PSD 與統合 PSD，否則會產生同步衝突。

## 重新組合

在專案根目錄執行：

```powershell
python tools\compose_from_parts.py
```

這會先產生 `包子_rebuilt.psd` 與合成預覽，不覆蓋正式檔。確認後再執行：

```powershell
python tools\compose_from_parts.py --apply
```

套用前會自動備份現有的 `包子.psd`。

## 圖層規則

- `body_base`：透明背景上的完整包子底層；只包含固定腮紅與頭頂摺痕，不含可動五官、手、書，也不挖五官孔洞。
- `hands_book`：雙手與書。
- `left_brow` / `right_brow`：左右眉毛。
- `left_pupil` / `right_pupil`：不含睫毛的完整橢圓瞳孔，置於眼皮下方。
- `left_upper_lid` / `left_lower_lid`：左眼上下眼皮。
- `right_upper_lid` / `right_lower_lid`：右眼上下眼皮。
- `glasses`：眼鏡，置於眼睛與眼皮上方。
- `mouth_interior`：完整嘴巴內部與舌頭，可獨立移動。
- `upper_lip` / `lower_lip`：上下嘴唇，置於嘴巴內部上方。
