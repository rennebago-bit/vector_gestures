import anki_vector
import time

with anki_vector.Robot() as robot:
    time.sleep(2)
    print(dir(robot.status))