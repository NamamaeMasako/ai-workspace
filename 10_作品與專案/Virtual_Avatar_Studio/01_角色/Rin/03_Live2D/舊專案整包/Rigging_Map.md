# Rin Live2D Rigging Strategy (Hiyori Reference)

## 1. 頭部 (Head)
- **Angle X/Y/Z**: 
  - 透過變形器層級 (Head > Face > Hair) 實現。
  - 瀏海 (Hair_Front) 增加 3 個物理點位，對應頭部擺動。
- **Eyes**:
  - **EyeOpen L/R**: 標準 0~1 區間。
  - **EyeSmile**: 當眼睛閉合時觸發 Loading 圖標微光效果。
  - **瞳孔 (Pupil)**: 設定 2D 物理，增加跟隨晃動感。

## 2. 核心組件 (The Ahoge)
- **科技呆毛 (Cowlick_Technology)**:
  - 獨立參數 `ParamAhogeMove`。
  - 設定高頻低幅的物理模擬，模擬「數據接收中」的微顫。

## 3. 下半身 (Legs & Boots)
- **數據長襪 (Stocking_DataBlue_R)**:
  - 貼圖滾動設定：利用 UV 偏移或分層透明度切換。
  - 參數 `ParamDataLoad`：0~1 代表 0~100% 系統負載。
- **透明短靴 (Boots_Window_A)**:
  - 遮罩設定：靴子視窗區域為 Alpha 遮罩，透出內部的長襪數據層。

## 4. 裝飾細節 (Details)
- **領口飾邊 (Collar_GlacierWhite)**: 固定層。
- **數位護甲 (Shoulder_Armor)**: 增加獨立的 Z 軸晃動。

---
*Status: Initial Map Completed. Ready for Cubism Import.*
