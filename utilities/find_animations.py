import anki_vector
import time

with anki_vector.Robot() as robot:
    time.sleep(3)  # wait for anim list to load
    excited = [a for a in robot.anim.anim_list if 'excited' in a.lower()]
    happy = [a for a in robot.anim.anim_list if 'happy' in a.lower()]
    print("EXCITED animations:")
    for a in excited:
        print(a)
    print("\nHAPPY animations:")
    for a in happy:
        print(a)