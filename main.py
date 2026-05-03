import math
import time

import cv2
import mediapipe as mp
import pyautogui

# Optional brightness control
try:
    import screen_brightness_control as sbc
    BRIGHTNESS_AVAILABLE = True
except:
    BRIGHTNESS_AVAILABLE = False


class AdvancedGestureController:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            model_complexity=1,
            min_detection_confidence=0.75,
            min_tracking_confidence=0.75
        )
        self.mp_draw = mp.solutions.drawing_utils

        self.prev_time = 0
        self.cooldown = 1.2
        self.last_action_time = 0
        self.prev_y = None

    def distance(self, p1, p2):
        return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

    def get_landmarks(self, hand_landmarks, frame_shape):
        h, w, _ = frame_shape
        lm_list = []
        for lm in hand_landmarks.landmark:
            lm_list.append((int(lm.x * w), int(lm.y * h)))
        return lm_list

    def detect_gesture(self, lm):
        thumb_tip = lm[4]
        thumb_ip = lm[3]
        index_tip = lm[8]
        middle_tip = lm[12]
        ring_tip = lm[16]
        pinky_tip = lm[20]

        # 👍 Volume Up
        if thumb_tip[1] < thumb_ip[1] and index_tip[1] > thumb_tip[1]:
            return "VOLUME_UP"

        # 👎 Volume Down
        if thumb_tip[1] > thumb_ip[1] and index_tip[1] < thumb_tip[1]:
            return "VOLUME_DOWN"

        # 🤏 Screenshot (Pinch)
        if self.distance(thumb_tip, index_tip) < 40:
            return "SCREENSHOT"

        # ✌️ Peace
        if (index_tip[1] < lm[6][1] and
            middle_tip[1] < lm[10][1] and
            ring_tip[1] > lm[14][1] and
            pinky_tip[1] > lm[18][1]):
            return "PEACE"

        # ✋ Open Palm → Brightness
        fingers_open = (
            index_tip[1] < lm[6][1] and
            middle_tip[1] < lm[10][1] and
            ring_tip[1] < lm[14][1]
        )

        if fingers_open:
            return "BRIGHTNESS"

        return "NONE"

    def perform_action(self, gesture, lm):
        current_time = time.time()

        if gesture != "BRIGHTNESS" and (current_time - self.last_action_time < self.cooldown):
            return

        if gesture == "VOLUME_UP":
            pyautogui.press("volumeup")

        elif gesture == "VOLUME_DOWN":
            pyautogui.press("volumedown")

        elif gesture == "SCREENSHOT":
            pyautogui.screenshot(f"screenshot_{int(time.time())}.png")

        elif gesture == "PEACE":
            pyautogui.press("playpause")

        elif gesture == "BRIGHTNESS":
            y = lm[8][1]

            if self.prev_y is not None:
                diff = self.prev_y - y

                if abs(diff) > 5:
                    if BRIGHTNESS_AVAILABLE:
                        try:
                            current = sbc.get_brightness()[0]
                            new = max(0, min(100, current + diff // 5))
                            sbc.set_brightness(new)
                        except:
                            pass
                    else:
                        if diff > 0:
                            pyautogui.press("brightnessup")
                        else:
                            pyautogui.press("brightnessdown")

            self.prev_y = y
            return

        self.last_action_time = current_time

    def run(self):
        cap = cv2.VideoCapture(0)

        while True:
            success, frame = cap.read()
            if not success:
                break

            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = self.hands.process(rgb)

            gesture_text = "NONE"

            if result.multi_hand_landmarks:
                for hand_landmarks in result.multi_hand_landmarks:
                    lm = self.get_landmarks(hand_landmarks, frame.shape)

                    gesture = self.detect_gesture(lm)
                    gesture_text = gesture

                    self.perform_action(gesture, lm)

                    self.mp_draw.draw_landmarks(
                        frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                    )

            # FPS
            curr_time = time.time()
            fps = 1 / (curr_time - self.prev_time) if self.prev_time else 0
            self.prev_time = curr_time

            # UI
            cv2.putText(frame, f'Gesture: {gesture_text}', (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            cv2.putText(frame, f'FPS: {int(fps)}', (10, 90),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            cv2.imshow("Advanced Gesture System", frame)

            if cv2.waitKey(1) & 0xFF == 27:
                break

        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    AdvancedGestureController().run()