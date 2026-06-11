import cv2
import mediapipe as mp
from mediapipe.tasks.python.vision import GestureRecognizer, GestureRecognizerOptions
from mediapipe.tasks.python.vision.core.vision_task_running_mode import VisionTaskRunningMode
import anki_vector
import os
from anki_vector.util import degrees
import time
import numpy as np

model_path = "gesture_recognizer.task"

# Setup gesture recognizer
base_options = mp.tasks.BaseOptions(model_asset_path=model_path)
options = GestureRecognizerOptions(
    base_options=base_options,
    running_mode=VisionTaskRunningMode.IMAGE
)

# Connect to Vector
print("Connecting to Vector...")
robot = anki_vector.Robot()
robot.connect()
print("Vector online!")

robot.camera.init_camera_feed()
print("Gesture control online... press ESC to quit")

last_gesture = ""

with GestureRecognizer.create_from_options(options) as recognizer:
    while True:
        image = robot.camera.latest_image
        if image is None:
            continue
        frame = cv2.cvtColor(np.array(image.raw_image), cv2.COLOR_RGB2BGR)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        result = recognizer.recognize(mp_image)

        if result.gestures:
            gesture = result.gestures[0][0].category_name

            # Only trigger when gesture changes
            if gesture != last_gesture:
                last_gesture = gesture
                print("Gesture: " + gesture)
                cv2.putText(frame, gesture, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                # Vector responses
                if gesture == "Thumb_Up":
                    robot.anim.play_animation('anim_pounce_success_02')
                    robot.behavior.say_text("Cool beans!")
                elif gesture == "Victory":
                    robot.behavior.say_text("you cool")
                elif gesture == "Open_Palm":
                    robot.behavior.say_text("Hello!")
                    robot.anim.play_animation('anim_greeting_hello_01')
                    time.sleep(4)
                elif gesture == "Closed_Fist":
                    robot.behavior.drive_off_charger()
                    robot.behavior.set_head_angle(degrees(20.0))
                    robot.behavior.set_lift_height(0.0)
                    robot.behavior.say_text("Fist bump!")
                    time.sleep(0.5)
                    robot.behavior.set_lift_height(0.8)
                    time.sleep(0.5)
                    robot.behavior.set_lift_height(0.3)
                    time.sleep(0.3)
                    robot.behavior.set_lift_height(0.8)
                    time.sleep(0.3)
                    robot.behavior.set_lift_height(0.0)
                    robot.anim.play_animation('anim_pounce_success_02')
                elif gesture == "ILoveYou":
                    robot.behavior.say_text("Hi human! I love you too!")

        if hasattr(result, "hand_landmarks") and result.hand_landmarks:
            for hand_landmarks in result.hand_landmarks:
                for landmark in hand_landmarks:
                    h, w, _ = frame.shape
                    x = int(landmark.x * w)
                    y = int(landmark.y * h)
                    cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

                connections = [
                    (0,1),(1,2),(2,3),(3,4),
                    (0,5),(5,6),(6,7),(7,8),
                    (0,9),(9,10),(10,11),(11,12),
                    (0,13),(13,14),(14,15),(15,16),
                    (0,17),(17,18),(18,19),(19,20)
                ]
                for start, end in connections:
                    h, w, _ = frame.shape
                    x1 = int(hand_landmarks[start].x * w)
                    y1 = int(hand_landmarks[start].y * h)
                    x2 = int(hand_landmarks[end].x * w)
                    y2 = int(hand_landmarks[end].y * h)
                    cv2.line(frame, (x1,y1), (x2,y2), (255, 255, 0), 2)

        cv2.imshow("Vector Eyes", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

robot.camera.close_camera_feed()
cv2.destroyAllWindows()
robot.disconnect()
print("Vector offline.")