@echo off
setlocal enabledelayedexpansion

:: Switch to the directory where this script is located
cd /d "%~dp0"

title ExtractDesign Studio — Reverse-Engineering Engine

cls
echo ========================================================================
echo   ExtractDesign Studio v2.0.0
echo   Reverse-engineer design systems, UI components ^& website intelligence
echo   Author: Karthikeyan T (@carthworks) ^| License: Apache-2.0
echo ========================================================================
echo.

:: 1. Locate Python executable
set "PY_CMD="
where python >nul 2>&1
if !errorlevel! equ 0 (
    set "PY_CMD=python"
) else (
    where py >nul 2>&1
    if !errorlevel! equ 0 (
        set "PY_CMD=py"
    )
)

if not defined PY_CMD (
    echo [ERROR] Python is not installed or not in your system PATH.
    echo Please install Python 3.10 or higher from https://www.python.org/
    echo.
    pause
    exit /b 1
)

for /f "tokens=*" %%v in ('!PY_CMD! --version 2^>^&1') do echo [*] Using: %%v

:: 2. Check and free port 8000 if occupied
echo [*] Checking port 8000 availability...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":8000" ^| findstr "LISTENING"') do (
    echo [*] Port 8000 is occupied by PID %%a. Releasing port...
    taskkill /f /pid %%a >nul 2>&1
)

:: 3. Verify core dependencies
echo [*] Checking Python dependencies...
!PY_CMD! -c "import requests, bs4, tinycss2, flask, flask_cors" >nul 2>&1
if !errorlevel! neq 0 (
    echo [*] Missing dependencies detected. Installing from requirements.txt...
    !PY_CMD! -m pip install -r requirements.txt
    if !errorlevel! neq 0 (
        echo [ERROR] Failed to install dependencies. Please run 'pip install -r requirements.txt' manually.
        pause
        exit /b 1
    )
) else (
    echo [OK] All dependencies verified.
)

:: 4. Auto-launch browser after brief delay in background
echo [*] Starting web application at http://localhost:8000/ ...
start "" cmd /c "timeout /t 2 /nobreak >nul & start http://localhost:8000/"

:: 5. Start unbuffered server
echo.
echo ========================================================================
echo   Server is active! Press Ctrl+C in this window to stop the server.
echo ========================================================================
echo.

:server_loop
!PY_CMD! -u server.py
echo.
echo [*] Server process ended. Auto-restarting in 1s... (Press Ctrl+C in terminal to abort)
timeout /t 1 /nobreak >nul
goto server_loop
