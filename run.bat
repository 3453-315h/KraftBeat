@echo off
REM Kraftbeat - Windows Launcher (DirectML)
REM Activates venv and runs the application
REM Requires Python 3.10-3.12 for DirectML support

echo ========================================
echo   Kraftbeat - AI Music Generator
echo   DirectML Backend (AMD/Intel)
echo ========================================
echo.

REM Check if venv312 exists
if not exist "venv312\Scripts\activate.bat" (
    echo Creating virtual environment with Python 3.12...
    py -3.12 -m venv venv312
    echo.
)

REM Activate venv
call venv312\Scripts\activate.bat

REM Check if dependencies are installed
python -c "import demucs" 2>nul
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    echo.
)

REM Run the application
echo Starting Kraftbeat...
venv312\Scripts\python.exe -m src.ui.main_window

pause
