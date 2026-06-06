import anki_vector
import time

with anki_vector.Robot() as robot:
    time.sleep(5)  # give extra time to load
    
    output = []
    
    # Get behaviors
    output.append("=== BEHAVIORS ===")
    behaviors = [x for x in dir(robot.behavior) if not x.startswith('_')]
    for b in behaviors:
        output.append(b)
    
    # Get animation triggers (more reliable than anim_list)
    output.append("\n=== ANIMATION TRIGGERS ===")
    try:
        triggers = robot.anim.anim_trigger_list
        for t in triggers:
            output.append(t)
    except Exception as e:
        output.append("Could not load triggers: " + str(e))
    
    # Get animations
    output.append("\n=== ANIMATIONS ===")
    try:
        anims = robot.anim.anim_list
        for a in anims:
            output.append(a)
    except Exception as e:
        output.append("Could not load animations: " + str(e))
    
    # Save to file
    with open('vector_capabilities.txt', 'w') as f:
        f.write('\n'.join(output))
    
    print("Done! Saved to vector_capabilities.txt")