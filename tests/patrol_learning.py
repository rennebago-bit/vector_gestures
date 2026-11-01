# Variables
robot_name = "Vector"
battery_level = 95

# Print with variables
print(robot_name + " is online.")
print("Battery level: " + str(battery_level) + "%")

# Simple if/else
if battery_level > 20:
    print("Battery is fine, ready to patrol.")
else:
    print("Low battery, returning to charger.")

# Loop - do something multiple times
import random  # to simulate motion for now

patrol_spots = {
    "dining room": "pending",
    "living room": "pending",
    "front door": "pending",
    "hallway": "pending"
}

for spot, status in patrol_spots.items():
    print(robot_name + " is patrolling the " + spot + "...")
    
    # Randomly simulate motion detected or clear
    motion = random.choice([True, False])
    
    if motion:
        patrol_spots[spot] = "motion detected"
        print("⚠️  ALERT: Motion detected in " + spot + "!")
    else:
        patrol_spots[spot] = "clear"
        print("✅ " + spot + " is clear.")

print("\n--- Patrol Report ---")
for spot, status in patrol_spots.items():
    print(spot + ": " + status)