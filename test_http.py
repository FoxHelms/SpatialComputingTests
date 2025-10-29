from dotenv import load_dotenv
import os
import requests
import cv2 as cv
import numpy as np

import mediapipe.python.solutions.hands as mp_hands
import mediapipe.python.solutions.drawing_utils as drawing
import mediapipe.python.solutions.drawing_styles as drawing_styles
import math

load_dotenv()

# set win size to 96x96 val=0
# set win size to 128x128 val=2

cam_ip = os.getenv('ESP_URL')
cam_port = os.getenv('ESP_PORT')
bound_str = os.getenv('BOUNDARY')
config_cam = f'http://{cam_ip}/control?var=framesize&val=2'
requests.get(config_cam)


hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.05)


url = 'http://{cam_ip}:{cam_port}/stream'
boundary = b'\r\n' + b'bound_str' + b'\r\n'
resp = requests.get(url, stream=True)
buffer = b''


#hands tap config
tap_threshold = 0.05
tap_evidence = 0
tap_confidence = 1

def calc_distance(p1, p2):
    return math.sqrt((p2.x - p1.x)**2 + (p2.y - p1.y)**2)

for chunk in resp.iter_content(chunk_size=1024):
    if chunk:
        buffer += chunk
        while True:
            boundary_index = buffer.find(boundary)
            if boundary_index == -1:
                break

            # Extract one frame (everything before the boundary)
            part = buffer[:boundary_index]
            buffer = buffer[boundary_index + len(boundary):]
            # print(buffer)
            # Split headers and content
            if b"\r\n\r\n" in part:
                header, content = part.split(b"\r\n\r\n", 1)
                #print('\n\n\n')
                img = cv.imdecode(np.frombuffer(content, np.uint8), cv.IMREAD_COLOR)
                if img is None:
                    print(f"Error: Could not decode image")
                else:
                    hands_detected = hands.process(img)
                    if hands_detected.multi_hand_landmarks:
                        for hand_landmarks in hands_detected.multi_hand_landmarks:
                            #drawing.draw_landmarks(
                            #img,
                            #hand_landmarks,
                            #mp_hands.HAND_CONNECTIONS,
                            #drawing_styles.get_default_hand_landmarks_style(),
                            #drawing_styles.get_default_hand_connections_style(),
                            #)
                            thumb = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                            ind = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            
                            # calculate tap
                            if calc_distance(thumb, ind) <= tap_threshold:
                                tap_evidence += 1
                            if tap_evidence >= tap_confidence:
                                print('TAP!')
                                tap_evidence = 0

                    
                    # Display the image (optional)
                    cv.imshow('JPEG Image', img)
                    if cv.waitKey(1) & 0xFF == ord('q'):
                        break
cv.destroyAllWindows() # Closes all OpenCV windows
