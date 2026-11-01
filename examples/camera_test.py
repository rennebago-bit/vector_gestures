import anki_vector
import cv2
import numpy as np
import time

print("Connecting to Vector...")
robot = anki_vector.Robot()
robot.connect()
print("Vector online!")

robot.camera.init_camera_feed()
print("Camera feed started... press ESC to quit")

while True:
    time.sleep(0.1)  # small delay to let frames come in
    
    image = robot.camera.latest_image
    
    if image is not None:
        frame = cv2.cvtColor(np.array(image.raw_image), cv2.COLOR_RGB2BGR)
        cv2.imshow("Vector's Eyes", frame)
    
    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()
robot.camera.close_camera_feed()
robot.disconnect()
print("Vector offline.")