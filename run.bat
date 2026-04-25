@echo off

REM Step 1: Create venv if not exists
IF NOT EXIST .venv (
    echo Creating virtual environment...
    python -m venv .venv
)

REM Step 2: Activate venv
call .venv\Scripts\activate

REM Step 3: Install dependencies only if missing
python -c "import cv2, mediapipe, numpy" 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo Installing requirements...
    pip install -r requirements.txt
)

REM Step 4: Run app
echo Starting application...
python my_face_app.py

pause