import cv2 as cv
import mediapipe.python.solutions.hands as mp_hands
import mediapipe.python.solutions.drawing_utils as drawing
import mediapipe.python.solutions.drawing_styles as drawing_styles
import math


is_tap = False

def set_tap_signal(value):
    global is_tap
    is_tap = value

def get_tap_signal():
    return is_tap


def is_tapping():
    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.5)

    # Set the desired resolution (e.g., 1280x720)
    width, height = 1280, 720
    tap_threshold = 0.06
    tap_evidence = 0
    tap_confidence = 3

    def calc_distance(p1, p2):
        return math.sqrt((p2.x - p1.x)**2 + (p2.y - p1.y)**2)

    cam = cv.VideoCapture(0)
    cam.set(3, width)  # Set the width
    cam.set(4, height)  # Set the height

    while cam.isOpened():
        success, img_rgb = cam.read()
        if not success:
            print("Camera Frame not available")
            continue

        # Convert image to RGB format
        img_rgb = cv.cvtColor(img_rgb, cv.COLOR_BGR2RGB)
        hands_detected = hands.process(img_rgb)

        # Convert image to RGB format
        img_rgb = cv.cvtColor(img_rgb, cv.COLOR_RGB2BGR)

        if hands_detected.multi_hand_landmarks:
            for hand_landmarks in hands_detected.multi_hand_landmarks:
                #drawing.draw_landmarks(
                #    img_rgb,
                #    hand_landmarks,
                #    mp_hands.HAND_CONNECTIONS,
                #    drawing_styles.get_default_hand_landmarks_style(),
                #    drawing_styles.get_default_hand_connections_style(),
                #)
                thumb = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                ind = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                if calc_distance(thumb, ind) <= tap_threshold:
                    tap_evidence += 1
                if tap_evidence >= tap_confidence:
                    print('TAP!')
                    set_tap_signal(True)
                    tap_evidence = 0
        # print(is_tap)
        # cv.imshow("Show Video", cv.flip(img_rgb, 1))

        if cv.waitKey(20) & 0xff == ord('q'):
            break

    cam.release()
