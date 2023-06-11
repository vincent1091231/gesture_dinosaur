from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import cv2
import mediapipe as mp
import math
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

file_path = os.path.dirname(os.path.abspath(__file__))
# edge的webdriver所在位址
path = os.path.join(file_path,'driver/chromedriver.exe')
s = Service(path)
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.maximize_window()

driver.get('https://fivesjs.skipser.com/trex-game/')



#影像偵測
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode = True,
                      max_num_hands = 2,
                      min_detection_confidence = 0.75,
                      min_tracking_confidence = 0.5)

def vector_2d_angle(v1, v2):
    v1_x = v1[0]
    v1_y = v1[1]
    v2_x = v2[0]
    v2_y = v2[1]
    try:
        angle_ = math.degrees(math.acos((v1_x*v2_x+v1_y*v2_y)/(((v1_x**2+v1_y**2)**0.5)*((v2_x**2+v2_y**2)**0.5))))
    except:
        angle_ = 65535.
    if angle_ > 180.:
        angle_ = 65535.
    return angle_

def hand_angle(hand_):
    angle_list = []
    
    angle_ = vector_2d_angle(
    ((int(hand_[0][0]) - int(hand_[2][0])),(int(hand_[0][1]) - int(hand_[2][1]))),
    ((int(hand_[3][0]) - int(hand_[4][0])),(int(hand_[3][1]) - int(hand_[4][1])))
    )    
    angle_list.append(angle_)
    
    angle_ = vector_2d_angle(
    ((int(hand_[0][0]) - int(hand_[6][0])),(int(hand_[0][1]) - int(hand_[6][1]))),
    ((int(hand_[7][0]) - int(hand_[8][0])),(int(hand_[7][1]) - int(hand_[8][1])))
    )    
    angle_list.append(angle_)
    
    angle_ = vector_2d_angle(
    ((int(hand_[0][0]) - int(hand_[10][0])),(int(hand_[0][1]) - int(hand_[10][1]))),
    ((int(hand_[11][0]) - int(hand_[12][0])),(int(hand_[11][1]) - int(hand_[12][1])))
    )    
    angle_list.append(angle_)
    
    angle_ = vector_2d_angle(
    ((int(hand_[0][0]) - int(hand_[14][0])),(int(hand_[0][1]) - int(hand_[14][1]))),
    ((int(hand_[15][0]) - int(hand_[16][0])),(int(hand_[15][1]) - int(hand_[16][1])))
    )    
    angle_list.append(angle_)
    
    angle_ = vector_2d_angle(
    ((int(hand_[0][0]) - int(hand_[18][0])),(int(hand_[0][1]) - int(hand_[18][1]))),
    ((int(hand_[19][0]) - int(hand_[20][0])),(int(hand_[19][1]) - int(hand_[20][1])))
    )    
    angle_list.append(angle_)
    
    return angle_list

def h_gesture(angle_list):
    thr_angle = 65.
    thr_angle_thumb = 53.
    thr_angle_s = 49.
    gesture_str = None
    if 65535. not in angle_list:
        '''if(angle_list[0] < thr_angle_s) and (angle_list[1] < thr_angle_s) and (angle_list[2] > thr_angle) and (angle_list[3] < thr_angle_s) and (angle_list[4] < thr_angle_s):
            gesture_str = "love forever"'''
        if(angle_list[0] < thr_angle_s) and (angle_list[1] > thr_angle) and (angle_list[2] > thr_angle) and (angle_list[3] > thr_angle) and (angle_list[4] > thr_angle):
            gesture_str = "Jump"
        if(angle_list[0] > thr_angle_thumb) and (angle_list[1] > thr_angle) and (angle_list[2] < thr_angle_s) and (angle_list[3] > thr_angle) and (angle_list[4] > thr_angle):
            gesture_str = "fuck you"
    return gesture_str

def detect():
    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode = False,
                           max_num_hands = 2,
                           min_detection_confidence = 0.8,
                           min_tracking_confidence = 0.75
                          )
   
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        frame = cv2.flip(frame,1)
        results = hands.process(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                hand_local = []
                for i in range(21):
                    x = hand_landmarks.landmark[i].x*frame.shape[1]
                    y = hand_landmarks.landmark[i].y*frame.shape[0]
                    hand_local.append((x,y))
                if hand_local:
                    angle_list = hand_angle(hand_local)
                    gesture_str = h_gesture(angle_list)
                    cv2.putText(frame,gesture_str,(0,100),0,1.3,(0,0,255),3)
                    if gesture_str == 'Jump':
                        driver.find_element_by_tag_name('body').send_keys(Keys.ARROW_UP)
        cv2.imshow("MediaPipe Hands", frame)
        if cv2.waitKey(1) == ord("q"):
            cv2.destroyAllWindows()
            break
    cap.release()

if __name__ == "__main__":
    detect()

driver.quit()