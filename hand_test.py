import cv2
import mediapipe as mp
from mediapipe.tasks.python.vision import GestureRecognizer, GestureRecognizerOptions
from mediapipe.tasks.python.vision.core.vision_task_running_mode import VisionTaskRunningMode
import urllib.request
import os

# Download the gesture model if we don't have it
model_path = "gesture_recognizer.task"
if not os.path.exists(model_path):
    print("Downloading gesture model...")
    urllib.request.urlretrieve(
        "https://storage.googleapis.com/mediapipe-models/gesture_recognizer/gesture_recognizer/float16/1/gesture_recognizer.task",
        model_path
    )
    print("Model downloaded!")

# Setup
base_options = mp.tasks.BaseOptions(model_asset_path=model_path)
options = GestureRecognizerOptions(
    base_options=base_options,
    running_mode=VisionTaskRunningMode.IMAGE
)

camera = cv2.VideoCapture(0)
print("Hand detector online... press ESC to quit")

with GestureRecognizer.create_from_options(options) as recognizer:
    while True:
        ret, frame = camera.read()
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
        result = recognizer.recognize(mp_image)

        if result.gestures:
            gesture = result.gestures[0][0].category_name
            print("Gesture: " + gesture)
            cv2.putText(frame, gesture, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Draw hand landmarks
        if result.hand_landmarks:
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

camera.release()
cv2.destroyAllWindows()