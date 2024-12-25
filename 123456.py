import cv2
import time
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from screeninfo import get_monitors
import threading
import vlc

# 初始化 pygame 音訊系統
# pygame.init()
# pygame.mixer.init()

# 打開內建攝影頭（攝像頭0）和外接攝影頭（攝像頭1）
cap1 = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(2)

if not cap1.isOpened():
    print("無法開啟攝影頭 1")
if not cap2.isOpened():
    print("無法開啟攝影頭 2")

# 設置攝影頭幀率和曝光
cap1.set(cv2.CAP_PROP_FPS, 60)
cap2.set(cv2.CAP_PROP_FPS, 60)
cap1.set(cv2.CAP_PROP_EXPOSURE, -6)
cap2.set(cv2.CAP_PROP_EXPOSURE, -5)

# 矩形框的寬度和高度
rect_width_cam1 = 400  # 改為較寬
rect_height_cam1 = 200
rect_width_cam2 = 300
rect_height_cam2 = 450

# 初始化前一幀
ret1, frame1 = cap1.read()
ret2, frame2 = cap2.read()
prev_frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
prev_frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

# 棒球計數器初始化
class BaseballCounter:
    def __init__(self):
        self.strike_count = 0
        self.ball_count = 0
        self.out_count = 0
        self.celebration_mode = False
        self.video_started = False
        self.video_player = None
        self.vlc_instance = None
        # 獲取螢幕解析度
        monitor = get_monitors()[0]  # 獲取主螢幕
        self.screen_width = monitor.width
        self.screen_height = monitor.height

    def reset_counts(self):
        self.strike_count = 0
        self.ball_count = 0
        self.out_count = 0
        self.celebration_mode = False
        self.video_started = False
        if self.video_player is not None:
            self.video_player.stop()
            self.video_player = None
        if self.vlc_instance is not None:
            self.vlc_instance.release()
            self.vlc_instance = None

    def update_counts(self, detected_both):
        if detected_both and not self.celebration_mode:
            if self.strike_count < 2:
                self.strike_count += 1
            elif self.strike_count == 2:
                self.strike_count = 0
                self.out_count += 1
                if self.out_count == 3:
                    self.celebration_mode = True
                    try:
                        # 初始化 VLC 實例
                        if self.vlc_instance is None:
                            self.vlc_instance = vlc.Instance('--no-xlib')
                        
                        # 創建媒體播放器
                        if self.video_player is None:
                            self.video_player = self.vlc_instance.media_player_new()
                            
                            # 設置播放器參數
                            self.video_player.set_rate(1.0)
                            self.video_player.audio_set_volume(100)
                            
                            # 載入媒體
                            video_path = '/home/123456/celebration.mp4'
                            media = self.vlc_instance.media_new(video_path)
                            media.get_mrl()
                            self.video_player.set_media(media)
                            
                            # 設置全螢幕
                            self.video_player.set_fullscreen(True)
                            
                            # 開始播放
                            self.video_player.play()
                            time.sleep(0.1)  # 給予一點時間初始化
                            print("開始播放影片")
                    except Exception as e:
                        print(f"載入影片時發生錯誤: {e}")
                        if self.video_player is not None:
                            self.video_player.stop()
                            self.video_player = None
                        if self.vlc_instance is not None:
                            self.vlc_instance.release()
                            self.vlc_instance = None
            else:
                if self.ball_count < 3:
                    self.ball_count += 1
                else:
                    self.ball_count = 0

    def draw(self, frame):
        """在畫面左上角繪製棒球計數器"""
        # 如果有影片在播放，檢查播放狀態
        if self.video_player is not None and self.celebration_mode:
            state = self.video_player.get_state()
            if state == vlc.State.Ended:
                # 影片播放完畢，重新開始
                self.video_player.set_position(0)
                self.video_player.play()
            elif state == vlc.State.Error:
                print("影片播放發生錯誤")
                self.video_player.stop()
                self.video_player = None

        x, y, w, h = 10, 10, 20, 150
        cv2.rectangle(frame, (x, y), (x + w, y + h), (200, 200, 200), -1)  # 灰色背景

        # 使用 FONT_HERSHEY_SIMPLEX 字體
        font = cv2.FONT_HERSHEY_SIMPLEX
        spacing = 50

        # S (好球 - 黃色)
        cv2.putText(frame, 'S', (x , y + 40), font, 1, (0, 0, 0), 2)
        for i in range(3):
            color = (0, 255, 255) if i < self.strike_count else (200, 200, 200)
            cv2.circle(frame, (x + 40 + i * spacing, y + 30), 15, color, -1)

        # B (壞球 - 綠色)
        cv2.putText(frame, 'B', (x , y + 90), font, 1, (0, 0, 0), 2)
        for i in range(4):
            color = (0, 255, 0) if i < self.ball_count else (200, 200, 200)
            cv2.circle(frame, (x + 40 + i * spacing, y + 80), 15, color, -1)

        # O (出局 - 紅色)
        cv2.putText(frame, 'O', (x , y + 140), font, 1, (0, 0, 0), 2)
        for i in range(3):
            color = (0, 0, 255) if i < self.out_count else (200, 200, 200)
            cv2.circle(frame, (x + 40 + i * spacing, y + 130), 15, color, -1)

        # 如果達到 3 個出局，顯示慶祝畫面
        if self.celebration_mode:
            # 在畫面中央顯示大字
            center_text = "慶祝中華隊奪冠"
            # 使用更大的字體大小
            font_scale = 0.5  # 增加字體大小
            thickness = 12  # 增加文字粗細

            # 使用 PIL 創建一個空白圖片來繪製中文
            from PIL import Image, ImageDraw, ImageFont
            img_pil = Image.fromarray(frame)
            draw = ImageDraw.Draw(img_pil)
            
            # 使用系統字體（支援 Ubuntu 和 Windows）
            try:
                # 嘗試使用 Ubuntu 常見字體
                font = ImageFont.truetype("/usr/share/fonts/truetype/wqy/wqy-microhei.ttc", 80)
            except:
                try:
                    # 嘗試使用 Windows 字體
                    font = ImageFont.truetype("msjh.ttc", 80)
                except:
                    try:
                        # 備用 Windows 字體
                        font = ImageFont.truetype("simsun.ttc", 80)
                    except:
                        # 如果都失敗了，使用默認字體
                        print("無法載入中文字體，使用默認字體")
                        font = ImageFont.load_default()

            # 獲取文字大小
            text_bbox = draw.textbbox((0, 0), center_text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            
            # 計算文字位置，確保完全置中
            text_x = (frame.shape[1] - text_width) // 2
            text_y = (frame.shape[0] - text_height) // 2

            # 繪製彩色邊框
            cv2.rectangle(frame, (0, 0), (frame.shape[1], frame.shape[0]), (0, 255, 255), 20)
            
            # 繪製文字
            draw.text((text_x, text_y), center_text, font=font, fill=(255, 255, 0))
            
            # 將 PIL 圖片轉回 OpenCV 格式
            frame = cv2.cvtColor(np.asarray(img_pil), cv2.COLOR_RGB2BGR)

            # 顯示按 Enter 重新開始的提示
            hint_text = "按 Enter 鍵重新開始"
            try:
                # 嘗試使用 Ubuntu 常見字體
                font_small = ImageFont.truetype("/usr/share/fonts/truetype/wqy/wqy-microhei.ttc", 32)
            except:
                try:
                    # 嘗試使用 Windows 字體
                    font_small = ImageFont.truetype("msjh.ttc", 32)
                except:
                    try:
                        # 備用 Windows 字體
                        font_small = ImageFont.truetype("simsun.ttc", 32)
                    except:
                        # 如果都失敗了，使用默認字體
                        print("無法載入中文字體，使用默認字體")
                        font_small = ImageFont.load_default()

            # 重新創建 PIL 圖片（因為前面已經轉換回 OpenCV 格式）
            img_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            draw = ImageDraw.Draw(img_pil)
            
            # 計算提示文字位置
            hint_bbox = draw.textbbox((0, 0), hint_text, font=font_small)
            hint_width = hint_bbox[2] - hint_bbox[0]
            hint_x = (frame.shape[1] - hint_width) // 2
            hint_y = text_y + text_height + 50

            # 繪製提示文字
            draw.text((hint_x, hint_y), hint_text, font=font_small, fill=(255, 255, 255))
            
            # 再次將 PIL 圖片轉回 OpenCV 格式
            frame = cv2.cvtColor(np.asarray(img_pil), cv2.COLOR_RGB2BGR)

counter = BaseballCounter()

def process_frame(cap, prev_frame, camera_id, detected_both):
    ret, frame = cap.read()
    if not ret:
        print(f"無法從攝影頭 {camera_id} 讀取影像")
        return None, prev_frame, False

    frame_height, frame_width = frame.shape[:2]
    if camera_id == 1:
        rect_width, rect_height = rect_width_cam1, rect_height_cam1
    else:
        rect_width, rect_height = rect_width_cam2, rect_height_cam2

    top_left = ((frame_width - rect_width) // 2, (frame_height - rect_height) // 2)
    bottom_right = ((frame_width + rect_width) // 2, (frame_height + rect_height) // 2)

    rectangle_color = (0, 0, 255) if detected_both else (0, 255, 0)  # 紅色如果兩個框都有偵測到，否則綠色
    cv2.rectangle(frame, top_left, bottom_right, rectangle_color, 2)

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 逐幀差異
    frame_diff = cv2.absdiff(prev_frame, gray_frame)

    # 邊緣檢測與膨脹操作
    edges = cv2.Canny(frame_diff, 50, 150)
    dilated = cv2.dilate(edges, None, iterations=2)

    # 找出輪廓
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    detected = False
    for contour in contours:
        if cv2.contourArea(contour) > 100:  # 面積閾值
            (x, y, w, h) = cv2.boundingRect(contour)
            if (top_left[0] <= x <= bottom_right[0] and top_left[1] <= y <= bottom_right[1]):
                detected = True
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)  # 繪製紅色框標記目標
                break

    return frame, gray_frame, detected

while True:
    frame1, prev_frame1, detected1 = process_frame(cap1, prev_frame1, 1, False)
    frame2, prev_frame2, detected2 = process_frame(cap2, prev_frame2, 2, False)

    if frame1 is None or frame2 is None:
        break

    detected_both = detected1 and detected2
    frame1, prev_frame1, _ = process_frame(cap1, prev_frame1, 1, detected_both)
    frame2, prev_frame2, _ = process_frame(cap2, prev_frame2, 2, detected_both)

    counter.update_counts(detected_both)

    counter.draw(frame1)
    counter.draw(frame2)

    cv2.imshow('Camera 1', frame1)
    cv2.imshow('Camera 2', frame2)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == 13:  # Enter 鍵的 ASCII 碼是 13
        counter.reset_counts()  # 重置所有計數

cap1.release()
cap2.release()
cv2.destroyAllWindows()
