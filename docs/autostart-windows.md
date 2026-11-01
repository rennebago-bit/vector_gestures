# Start Gesture Control Automatically on Windows

This setup starts `vector_gestures.py` whenever you sign in to Windows, using Task Scheduler.

## Requirements

Before setting up automatic startup:

- Wire Pod is running and Vector is reachable on the network.
- Gesture dependencies are installed from the repository root:

  ```powershell
  py -m pip install -r requirements.txt
  ```

- Camera access is allowed for Python in **Windows Settings → Privacy & security → Camera**.
- Test the gesture controller manually first:

  ```powershell
  cd C:\Users\YOUR_NAME\Desktop\ORGS\Vector
  py vector_gestures.py
  ```

## Create a startup script

Create `start_vector_gestures.bat` in the repository root:

```bat
@echo off
cd /d "C:\Users\YOUR_NAME\Desktop\ORGS\Vector"
py vector_gestures.py
```

Find the Python executable if the command above does not work:

```powershell
py -0p
where.exe py
```

Replace `py` in the batch file with the full Python executable path if necessary, for example:

```bat
"C:\Users\YOUR_NAME\AppData\Local\Programs\Python\Python311\python.exe" vector_gestures.py
```

Replace the example project path with the actual path to the repository.

## Option 1: Use Task Scheduler manually

1. Open **Task Scheduler**.
2. Select **Create Task** from the right-hand menu.
3. On the **General** tab:
   - Name the task `Vector Gesture Control`.
   - Select **Run only when user is logged on**.
   - Enable **Run with highest privileges** only if required by your webcam or Python setup.
4. On the **Triggers** tab, select **New**.
   - Begin the task: **At log on**.
   - Choose your Windows user account if prompted.
5. On the **Actions** tab, select **New**.
   - Action: **Start a program**.
   - Program/script: the full path to `start_vector_gestures.bat`.
   - Start in: the Vector repository folder.
6. On the **Settings** tab, enable **If the task fails, restart every: 1 minute** if you want automatic retries.
7. Select **OK**, then use **Run** in Task Scheduler to test it.

## Option 2: Create the task with PowerShell

Run PowerShell as your normal Windows user and replace the paths below as needed:

```powershell
$Project = "C:\Users\YOUR_NAME\Desktop\ORGS\Vector"
$Bat = Join-Path $Project "start_vector_gestures.bat"

$action = New-ScheduledTaskAction `
  -Execute $Bat `
  -WorkingDirectory $Project

$trigger = New-ScheduledTaskTrigger -AtLogOn

$settings = New-ScheduledTaskSettingsSet `
  -RestartCount 3 `
  -RestartInterval (New-TimeSpan -Minutes 1)

Register-ScheduledTask `
  -TaskName "Vector Gesture Control" `
  -Action $action `
  -Trigger $trigger `
  -Settings $settings
```

Test the task without signing out:

```powershell
Start-ScheduledTask -TaskName "Vector Gesture Control"
```

## Logs

The batch file can send output to a log without changing the Python script. Update its contents to include:

```bat
@echo off
cd /d "C:\Users\YOUR_NAME\Desktop\ORGS\Vector"
py vector_gestures.py >> vector_gestures.log 2>&1
```

View recent log lines with:

```powershell
Get-Content .\vector_gestures.log -Tail 50
```

## Stop or remove the task

Stop a running task:

```powershell
Stop-ScheduledTask -TaskName "Vector Gesture Control"
```

Disable it:

```powershell
Disable-ScheduledTask -TaskName "Vector Gesture Control"
```

Remove it completely:

```powershell
Unregister-ScheduledTask -TaskName "Vector Gesture Control" -Confirm:$false
```

## Notes

- Task Scheduler starts the task when you sign in, not before Windows reaches the Windows sign-in screen.
- Keep the PC awake and signed in for gesture control to continue running.
- Start Wire Pod before the gesture task, or allow enough startup delay if both run from scheduled tasks. Opening Wire Pod first avoids a startup race.
- The gesture script opens an OpenCV window, so it should run in a normal interactive Windows user session rather than as a background system account.
- If automatic startup exits immediately, open the task log and run `start_vector_gestures.bat` manually to identify Python, project-path, camera, or Vector connection errors.
