@echo off
REM Kraftbeat Build Script
REM Builds standalone Windows executable using PyInstaller

echo ========================================
echo Kraftbeat Build Script
echo ========================================
echo.

REM Activate virtual environment
call venv312\Scripts\activate

REM Install PyInstaller if not present
echo Installing/updating PyInstaller...
pip install pyinstaller --quiet

REM Build the executable
echo.
echo Building Kraftbeat.exe...
echo This may take several minutes...
echo.

pyinstaller kraftbeat.spec --noconfirm

echo.
echo ========================================
if exist "dist\Kraftbeat.exe" (
    echo BUILD SUCCESSFUL!
    echo Output: dist\Kraftbeat.exe
) else (
    echo BUILD FAILED!
    echo Check the output above for errors.
)
echo ========================================

pause
