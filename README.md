# TAIWAN-NO.1

## Concept Development 開發構想
- 爲了慶祝中華隊棒球奪得冠軍，所以我們做了一個小游戲來回顧我們奪冠的歷程

## Gameplay 玩法
- 鏡頭1和鏡頭2會形成一個好球帶的範圍，玩家可在鏡頭1后方投球，當球經過鏡頭1和鏡頭2時候會判斷為好球

## Implementation Resources 運用資源
- Python
- Ubuntu
- Chatgpt
- Opencv

## Ubuntu Setup 虛擬機設定
- sudo apt install python3-opencv

## 游戲程式執行
![image](https://github.com/user-attachments/assets/ce96bcaa-264d-4fe3-b014-394adedb187b)
- 設置相機的曝光程度與幀數，調整好球帶的範圍大小
- 儲存兩個攝影機捕捉的前一幀影像，作為之後逐幀差異比較的基準

![image](https://github.com/user-attachments/assets/5a6826ff-1794-45d9-b33d-2c674337ac00)
- 記錄棒球比賽中的好球、壞球、和出局的計數
- 當達到某個條件（如 3 出局）時，進入慶祝模式並播放一段影片
- 在比賽重新開始時，重置所有的計數和播放狀態

![image](https://github.com/user-attachments/assets/03a2519a-1350-4841-9d7e-82a7112a4652)
- 將「好球」（S）、「壞球」（B）和「出局」（O）的狀態以圖形化方式顯示，並在 3 出局達成時進入慶祝模式(播放影片)

![image](https://github.com/user-attachments/assets/907efcf0-5f09-4e64-b180-7a715ceb002a)
- 從指定攝影機讀取一幀影像，並檢查是否成功讀取。
- 根據攝影機 ID 和偵測狀態，在影像中央繪製不同顏色的矩形框（紅色或綠色）。紅色為兩個攝影機同時偵測到目標，綠色為只有一個攝影機或未同時偵測到目標。
- 將讀取的彩色影像轉換為灰度影像，用於後續處理。








## 困難及未來展望
### 困難
- 在創新性與娛樂性發想這方面花了較多時間
- 完成程式碼後想用樹梅派運行 礙於硬體強度無法流暢偵測畫面
- 攝影機設備幀數不足準確率欠佳
- 好球帶的判斷方式
### 未來展望
- 希望能夠搭配match template讓他只偵測棒球
- 
## Job Assignment 工作分配
- 陳冠霖 111213016
  - readme撰寫
  - 創意發想
  - 資料整合
- 張平治 111213007
  - 程式撰寫
  - 創意發想
- 賴詩璿 111213004
  - 程式撰寫
  - 樹莓派測試
- 李晉偉 111213060
  - 影片剪輯
  - 樹莓派測試
- 呂秉衡 111213048
  - 程式撰寫
  - readme撰寫

## References 參考資料

## Demo 實做影片
https://www.youtube.com/watch?v=LSwQh3WOnzc
