@echo off
REM InterviewForge GUI Launcher (Windows)

title InterviewForge GUI

echo ========================================
echo    InterviewForge GUI
echo ========================================
echo.

REM Prüfe Python
where python >nul 2>nul
if errorlevel 1 (
    echo [ERROR] Python nicht gefunden!
    echo Bitte installiere Python 3.10 oder hoeher von python.org
    pause
    exit /b 1
)

REM Aktiviere venv falls vorhanden
if exist "venv\Scripts\activate.bat" (
    echo [INFO] Aktiviere Virtual Environment...
    call venv\Scripts\activate.bat
)

REM Starte GUI
echo [INFO] Starte GUI...
echo.
python interviewforge_gui.py

REM Deaktiviere venv
if exist "venv\Scripts\deactivate.bat" (
    call venv\Scripts\deactivate.bat
)

pause
