# 🤖 Vector Gesture Bot — Setup Guide

A Python-based gesture control system for the Anki Vector robot using Wire Pod, OpenCV, and MediaPipe. Control your Vector with hand gestures — no cloud required.

Built and documented by a first-time Python learner in a single day.

---

## What this does

- Detects your hand gestures in real time using your webcam
- Maps gestures to Vector behaviors (speech, movement, animations)
- Runs fully locally via Wire Pod — no Anki/Digital Dream Labs account needed
- Draws a live hand skeleton so you can see what the camera sees

---

## What you need

- An Anki Vector robot
- [Wire Pod](https://github.com/kercre123/wire-pod) running on your local network
- A Mac or PC with a webcam
- Python 3.9+
- VS Code (recommended)

---

## Part 1 — Install Python

**Check if Python is already installed:**
```bash
python3 --version
```

If you get `command not found`, install it via Homebrew (Mac):

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

After Homebrew installs, add it to your PATH (follow the instructions it prints), then:

```bash
brew install python
```

---

## Part 2 — Set up VS Code

1. Download [VS Code](https://code.visualstudio.com)
2. Install the **Python** extension (by Microsoft)
3. Install the **Pylance** extension
4. Create a project folder — e.g. `~/Desktop/Vector`
5. Open that folder in VS Code

---

## Part 3 — Install required libraries

Open your terminal (VS Code's built-in terminal works great) and run:

```bash
pip3 install wirepod_vector_sdk --break-system-packages
pip3 install opencv-python --break-system-packages
pip3 install mediapipe --break-system-packages
pip3 install protobuf==3.20.3 --break-system-packages
```

> **Note:** If you get a protobuf conflict warning, ignore it — it still works.

---

## Part 4 — Connect Vector via Wire Pod

Make sure Wire Pod is running on your network. Find your Wire Pod's IP address (e.g. `192.168.1.66`) and Vector's IP address (pick him up — his eyes show his IP).

Run the SDK configurator:

```bash
python3 -m anki_vector.configure
```

When prompted:
- **Wire Pod IP:** enter your Wire Pod IP with port, e.g. `192.168.1.66:8080`
- Follow the remaining prompts

If successful you'll see a cert file saved to `~/.anki_vector/`.

---

## Part 5 — Test the connection

Create a file called `hello_vector.py`:

```python
import anki_vector

with anki_vector.Robot() as robot:
    robot.behavior.say_text("Hello! I am online.")
```

Run it:

```bash
cd ~/Desktop/Vector
python3 hello_vector.py
```

Vector should speak. If she does, you're fully connected! 🎉

---

## Part 6 — Run the gesture controller

Download `vector_gestures.py` from this repo and place it in your Vector folder alongside the `gesture_recognizer.task` model file.

The first time you run it, the model will download automatically:

```bash
python3 vector_gestures.py
```

A webcam window will open showing your hand skeleton and detected gesture name. Vector will respond to your gestures in real time.

---

## Default gesture mappings

| Gesture | Vector response |
|---|---|
| 👍 Thumbs up | "Thank you!" |
| ✋ Open palm | "Stopping!" |
| ☝️ Pointing up | "I see you!" |
| ✊ Closed fist | "Starting patrol!" |
| ✌️ Victory | "Woohoo!" |
| 🤟 I love you | "Hello! Nice to see you!" |

You can customize these by editing the gesture mapping section in `vector_gestures.py`.

---

## Troubleshooting

**`protobuf` error on configure:**
```bash
pip3 install protobuf==3.20.3 --break-system-packages
```

**`mediapipe` has no attribute `solutions`:**
Your MediaPipe version is 0.10.30+. Use the `GestureRecognizer` API as shown in `vector_gestures.py` — the old `solutions` API was removed.

**`ListAnimations request timed out`:**
Wire Pod doesn't support the animation list API. Use known animation names directly via `robot.anim.play_animation('anim_name_here')`. See `vector_reference.html` for a full searchable list.

**Vector not responding:**
- Make sure Vector and your computer are on the same WiFi network
- Confirm Wire Pod is running at its IP address
- Check that the cert file exists at `~/.anki_vector/`

---

## Resources

- [Wire Pod](https://github.com/kercre123/wire-pod) — local Vector server
- [wirepod_vector_sdk](https://pypi.org/project/wirepod-vector-sdk/) — Python SDK for Wire Pod
- [MediaPipe](https://mediapipe.readthedocs.io) — hand gesture detection
- [OpenCV](https://opencv.org) — computer vision
- [r/AnkiVector](https://www.reddit.com/r/AnkiVector/) — community

---

## Contributing

Have a gesture mapping you love? Submit a pull request! This repo is meant to grow into a community gesture library for Vector owners.

---

*Built with Python 3.9, Wire Pod, MediaPipe, and a lot of love for vector.*
