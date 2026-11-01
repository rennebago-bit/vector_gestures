# Start Gesture Control Automatically on macOS

This setup starts `vector_gestures.py` automatically when you log in. It uses a macOS LaunchAgent.

## Requirements

Before setting up automatic startup:

- Wire Pod is running.
- Vector is connected to Wire Pod and reachable on the network.
- Gesture dependencies are installed from the repository root:

  ```bash
  python3 -m pip install -r requirements.txt
  ```

- Camera access is allowed for Terminal or the Python executable in **System Settings → Privacy & Security → Camera**.
- Test the gesture controller manually first:

  ```bash
  cd /Users/rennjarrett/Desktop/ORGS/Vector
  python3 vector_gestures.py
  ```

## Create the LaunchAgent

Create the LaunchAgent folder if it does not already exist:

```bash
mkdir -p ~/Library/LaunchAgents
nano ~/Library/LaunchAgents/com.vector.gestures.plist
```

Paste the following configuration:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
"http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.vector.gestures</string>

    <key>ProgramArguments</key>
    <array>
        <string>/opt/homebrew/bin/python3</string>
        <string>/Users/rennjarrett/Desktop/ORGS/Vector/vector_gestures.py</string>
    </array>

    <key>WorkingDirectory</key>
    <string>/Users/rennjarrett/Desktop/ORGS/Vector</string>

    <key>RunAtLoad</key>
    <true/>

    <key>KeepAlive</key>
    <true/>

    <key>StandardOutPath</key>
    <string>/Users/rennjarrett/Desktop/ORGS/Vector/vector_gestures.log</string>

    <key>StandardErrorPath</key>
    <string>/Users/rennjarrett/Desktop/ORGS/Vector/vector_gestures.log</string>
</dict>
</plist>
```

The Python executable and project paths may differ on another Mac. Find the Python executable used by the project with:

```bash
which python3
```

Replace `/opt/homebrew/bin/python3` and `/Users/rennjarrett/Desktop/ORGS/Vector` above if needed.

## Enable it

Load the LaunchAgent:

```bash
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.vector.gestures.plist
```

It will start when you log in. `KeepAlive` also restarts the script if it exits unexpectedly. To apply changes after editing the file, unload it and load it again:

```bash
launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/com.vector.gestures.plist
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.vector.gestures.plist
```

## Check the status and logs

View the script's output:

```bash
tail -n 50 /Users/rennjarrett/Desktop/ORGS/Vector/vector_gestures.log
```

Check whether launchd is managing the job:

```bash
launchctl print gui/$(id -u)/com.vector.gestures
```

## Stop automatic startup

Stop the service while keeping the configuration file:

```bash
launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/com.vector.gestures.plist
```

Start it again without rebooting:

```bash
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.vector.gestures.plist
```

Remove automatic startup completely:

```bash
rm ~/Library/LaunchAgents/com.vector.gestures.plist
```

## Notes

- A LaunchAgent starts at login, not before macOS has finished loading your user session.
- The gesture script must keep running, so leave your Mac awake and logged in.
- Wire Pod may need to be running before the gesture controller starts. If startup races ahead of Wire Pod, wait for it to become available or add startup delays/retries to the script.
- `vector_gestures.py` opens a live OpenCV camera window and runs in the user session so that the camera and Vector display can be used correctly.
