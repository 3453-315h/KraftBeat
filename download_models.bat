@echo off
setlocal EnableDelayedExpansion
title Kraftbeat Model Downloader

:: Set project roots
set "PROJECT_ROOT=%~dp0"
set "VENV_DIR=%PROJECT_ROOT%venv"
set "MODELS_DIR=%PROJECT_ROOT%models"

:: Activate virtual environment
if exist "%VENV_DIR%\Scripts\activate.bat" (
    call "%VENV_DIR%\Scripts\activate.bat"
) else (
    echo [ERROR] Virtual environment not found at %VENV_DIR%
    echo Please run run.bat or setup.bat first.
    pause
    exit /b 1
)

:: Python script to handle the download logic
:: We write this temporary python script to reuse the Python logic we already wrote
:: This is cleaner than trying to implement complex logic in batch
set "DOWNLOADER_SCRIPT=%PROJECT_ROOT%download_models_cli.py"

echo.
echo ========================================================
echo       Kraftbeat Model Downloader (CLI)
echo ========================================================
echo.
echo Supports: MusicGen, ACE-Step, DiffRhythm
echo.
echo This tool will download models to:
echo %MODELS_DIR%
echo.

:: Check dependencies
python -c "import huggingface_hub" >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] huggingface_hub is not installed!
    echo Please check your installation.
    pause
    exit /b 1
)

:: Run the python downloader UI
python "%DOWNLOADER_SCRIPT%"

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Downloader exited with an error.
)

echo.
echo Press any key to exit...
pause >nul
