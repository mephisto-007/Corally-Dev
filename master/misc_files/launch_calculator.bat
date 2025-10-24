@echo off
echo 🚀 Launching Calculator Suite GUI...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

REM Launch the GUI
python gui_launcher.py

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo ❌ An error occurred. Press any key to exit.
    pause >nul
)
