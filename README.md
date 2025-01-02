# TAIWAN-NO.1

## Concept Development 開發構想
- 爲了慶祝中華隊棒球奪得冠軍，所以我們做了一個小游戲來回顧我們奪冠的歷程 
模擬第九局下半 刺激的最後一局
![image](https://github.com/user-attachments/assets/c072f273-041f-4a4a-8788-8fd48b3e9920)


## Gameplay 玩法
- 鏡頭1和鏡頭2會形成一個好球帶的範圍，玩家可在鏡頭1后方投球，當球同時經過鏡頭1和鏡頭2時候會判斷為好球
 ![未命名的筆記本 (1)_page-0001 (1)](https://github.com/user-attachments/assets/34b04396-dfea-405a-bb71-7f51b25131a8)


## Implementation Resources 運用資源
- Python
- Ubuntu
- Chatgpt
- Opencv
## Hardware 硬體
- webcam*2
  
## Ubuntu Setup 虛擬機環境設定
假如是用筆電 要先去裝置管理員將鏡頭關閉 否則opencv無法處裡空置鏡頭
在虛擬機的裝置 選取兩個webcam
![image](https://github.com/user-attachments/assets/aac1ffda-40eb-4fd0-b98d-485b1dbb8871)

![image](https://github.com/user-attachments/assets/9861cdd0-405f-4f63-9809-a7ba7ebe7f18) \
最後要去找到兩個鏡頭分別的數字ex 0,2


- sudo apt install python3-opencv
- sudo apt install pillow
- sudo apt install screeninfo
- sudo apt install vlc
  
## run in ubuntu
- sudo vim <任意檔名>.py
  開啟並且將程式碼貼進去
- python3 <任意檔名>.py
  

## 游戲程式執行
<img src="https://github.com/user-attachments/assets/ce96bcaa-264d-4fe3-b014-394adedb187b" width="500">

- 設置相機的曝光程度與幀數，調整好球帶的範圍大小
- 儲存兩個攝影機捕捉的前一幀影像，作為之後逐幀差異比較的基準

<img src="https://github.com/user-attachments/assets/5a6826ff-1794-45d9-b33d-2c674337ac00" width="500">

- 記錄棒球比賽中的好球、壞球、和出局的計數
- 當達到某個條件（如 3 出局）時，進入慶祝模式並播放一段影片
- 在比賽重新開始時，重置所有的計數和播放狀態

<img src="https://github.com/user-attachments/assets/03a2519a-1350-4841-9d7e-82a7112a4652" width="500">

- 將「好球」（S）、「壞球」（B）和「出局」（O）的狀態以圖形化方式顯示，並在 3 出局達成時進入慶祝模式(播放影片)

<img src="https://github.com/user-attachments/assets/907efcf0-5f09-4e64-b180-7a715ceb002a" width="500">

- 從指定攝影機讀取一幀影像，並檢查是否成功讀取。
- 根據攝影機 ID 和偵測狀態，在影像中央繪製不同顏色的矩形框（紅色或綠色）。紅色為兩個攝影機同時偵測到目標，綠色為只有一個攝影機或未同時偵測到目標。
- 將讀取的彩色影像轉換為灰度影像，用於後續處理。


## 困難及未來展望
### 困難
- 在創新性與娛樂性發想這方面花了較多時間
- 完成程式碼後想用樹梅派運行 礙於硬體強度無法流暢偵測畫面
- 攝影機設備幀數不足準確率欠佳
- 好壞球的判斷方式
### 未來展望
- 能夠搭配match template讓他只偵測棒球
- 能夠使用高偵數camera來捕捉高速的球
- 能夠實際應用在業餘棒球比賽
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
https://www.youtube.com/watch?v=xjrykYpaBBM

## Demo 實做影片
https://www.youtube.com/watch?v=LSwQh3WOnzc

# 感謝猛哥和各位助教的幫忙
