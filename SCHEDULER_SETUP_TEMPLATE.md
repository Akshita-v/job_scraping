# Automation Setup Guide

## Schedule Daily Job Scraping

This guide explains how to set up the job scraper to run automatically at 8:00 AM daily using Windows Task Scheduler.

## Prerequisites

- Python installed and accessible from command line
- Project folder path (you'll need this)
- Windows OS

## Step 1: Find Your Python Path

Open PowerShell and run:
```powershell
where python
```

Copy this path - you'll need it for Task Scheduler. Example: `C:\Users\YourUsername\AppData\Local\Programs\Python\Python313\python.exe`

## Step 2: Find Your Project Path

Example: `C:\Users\YourUsername\Downloads\swelist`

## Step 3: Create Scheduler Scripts

Create these two files in your project folder:

### File 1: `schedule_runner.py`
```python
import subprocess
import os
from datetime import datetime

os.chdir(r"<YOUR_PROJECT_PATH>")  # Replace with your project path

log_file = "scheduler.log"

try:
    result = subprocess.run(["python", "main.py"], capture_output=True, text=True, timeout=300)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a") as f:
        f.write(f"\n[{timestamp}] Job Scraper Executed\n")
        f.write(f"Return Code: {result.returncode}\n")
        if result.stdout:
            f.write(f"Output:\n{result.stdout}\n")
        if result.stderr:
            f.write(f"Errors:\n{result.stderr}\n")
        f.write("-" * 50 + "\n")
    
    print(f"[{timestamp}] Job scraper completed successfully")
    
except subprocess.TimeoutExpired:
    with open(log_file, "a") as f:
        f.write(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ERROR: Job scraper timed out\n")
    print("ERROR: Job scraper timed out")
    
except Exception as e:
    with open(log_file, "a") as f:
        f.write(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ERROR: {str(e)}\n")
    print(f"ERROR: {str(e)}")
```

**Replace `<YOUR_PROJECT_PATH>` with your actual project path**

### File 2: `run_daily.bat` (Alternative)
```batch
@echo off
cd /d <YOUR_PROJECT_PATH>
call .venv\Scripts\activate.bat
python main.py
pause
```

**Replace `<YOUR_PROJECT_PATH>` with your actual project path**

## Step 4: Open Task Scheduler

- Press `Win + R`
- Type `taskschd.msc`
- Press Enter

## Step 5: Create Basic Task

1. Click "Create Basic Task" (right panel)
2. Name: `SWE Job Scraper Daily`
3. Description: `Automated daily job scraping and email notifications`
4. Click "Next"

## Step 6: Set Trigger

1. Select "Daily"
2. Start date: Today's date
3. Recur every: 1 day
4. Start time: `08:00` (8:00 AM)
5. Click "Next"

## Step 7: Set Action

1. Select "Start a program"
2. Program/script: `<YOUR_PYTHON_PATH>` (from Step 1)
3. Add arguments: `<YOUR_PROJECT_PATH>\schedule_runner.py`
   - Example: `C:\Users\akshi\Downloads\swelist\schedule_runner.py`
4. Start in: `<YOUR_PROJECT_PATH>`
   - Example: `C:\Users\akshi\Downloads\swelist`
5. Click "Next"

## Step 8: Set Conditions & Settings

1. Uncheck "Start the task only if the computer is on AC power"
2. Check "Run task as soon as possible after a scheduled start is missed"
3. Check "Allow task to be run on demand"
4. Click "Next"

## Step 9: Finish

Click "Finish"

## Verify Setup

1. Check `scheduler.log` in your project folder
2. Monitor `opportunities.csv` for new jobs
3. Manually run to test: `python schedule_runner.py`

## Troubleshooting

### Task not running?
- Open Event Viewer: `Win + R` → `eventvwr.msc`
- Check Windows Logs → System for errors
- Verify Python path is correct

### Python not found?
- Make sure Python is in PATH
- Use full path to python executable
- Test: `python --version` in PowerShell

### Check Task Status
- Open Task Scheduler
- Find "SWE Job Scraper Daily"
- Check "Last Run Result" column

### Disable/Edit Task
- Right-click task in Task Scheduler
- Select "Disable", "Edit", or "Delete"

## Alternative: Using Batch File

If you prefer using the batch file instead of Python script:
- In Step 7, use `<YOUR_PROJECT_PATH>\run_daily.bat` as the Program/script
- Leave "Add arguments" empty

## Support

Check `scheduler.log` for detailed execution logs and error messages.
