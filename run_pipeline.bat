@echo off
REM Vollständige Transkriptions-Pipeline für Windows
REM Verwendung: run_pipeline.bat C:\path\to\audio\folder [anzahl_sprecher]

setlocal enabledelayedexpansion

REM Prüfe Argumente
if "%~1"=="" (
    echo [ERROR] Kein Input-Ordner angegeben!
    echo Verwendung: run_pipeline.bat C:\path\to\audio\folder [anzahl_sprecher]
    exit /b 1
)

set INPUT_DIR=%~1
set SPEAKERS=%2
if "%SPEAKERS%"=="" set SPEAKERS=2

REM Prüfe ob Ordner existiert
if not exist "%INPUT_DIR%" (
    echo [ERROR] Ordner existiert nicht: %INPUT_DIR%
    exit /b 1
)

REM Zähle Audio-Dateien
set AUDIO_COUNT=0
for %%f in ("%INPUT_DIR%\*.m4a" "%INPUT_DIR%\*.wav" "%INPUT_DIR%\*.mp3") do (
    if exist "%%f" set /a AUDIO_COUNT+=1
)

if %AUDIO_COUNT%==0 (
    echo [ERROR] Keine Audio-Dateien gefunden in: %INPUT_DIR%
    exit /b 1
)

echo [INFO] Gefunden: %AUDIO_COUNT% Audio-Dateien

REM Prüfe FFmpeg
where ffmpeg >nul 2>nul
if errorlevel 1 (
    echo [ERROR] FFmpeg nicht gefunden! Bitte installieren:
    echo   Download von: https://ffmpeg.org/download.html
    echo   Füge FFmpeg zum PATH hinzu oder installiere mit winget:
    echo   winget install --id=Gyan.FFmpeg -e
    exit /b 1
)

REM Prüfe Python und venv
if not exist "venv" (
    echo [WARN] Virtual Environment nicht gefunden. Erstelle venv...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo [INFO] Installiere Dependencies...
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate.bat
)

REM Prüfe API Keys
if "%OPENAI_API_KEY%"=="" (
    echo [ERROR] OPENAI_API_KEY nicht gesetzt!
    echo Setze mit: set OPENAI_API_KEY=your-key
    echo Oder erstelle .env Datei
    exit /b 1
)

if "%HF_TOKEN%"=="" (
    echo [ERROR] HF_TOKEN nicht gesetzt!
    echo Setze mit: set HF_TOKEN=your-token
    echo Oder erstelle .env Datei
    exit /b 1
)

REM ============================================
REM SCHRITT 1: Audio-Optimierung
REM ============================================
echo [INFO] Schritt 1/3: Audio-Optimierung

set OPTIMIZED_COUNT=0
for %%f in ("%INPUT_DIR%\*.m4a" "%INPUT_DIR%\*.mp3" "%INPUT_DIR%\*.wav") do (
    if exist "%%f" (
        set "filename=%%~nf"
        set "filepath=%%~dpnf"

        REM Skip falls bereits optimiert
        echo !filename! | findstr /C:"_optimized" >nul
        if errorlevel 1 (
            set "output=!filepath!_optimized.wav"

            if exist "!output!" (
                echo [INFO] Existiert bereits: %%~nxf
                set /a OPTIMIZED_COUNT+=1
            ) else (
                echo [INFO] Optimiere: %%~nxf
                ffmpeg -i "%%f" -ar 16000 -ac 1 -af "highpass=f=200,lowpass=f=3000,loudnorm=I=-16" "!output!" -y -loglevel error
                set /a OPTIMIZED_COUNT+=1
            )
        ) else (
            echo [INFO] Überspringe (bereits optimiert): %%~nxf
        )
    )
)

echo [INFO] Optimiert: %OPTIMIZED_COUNT% Dateien

REM ============================================
REM SCHRITT 2: Transkription
REM ============================================
echo [INFO] Schritt 2/3: Transkription (Whisper + Pyannote)

python whisper_kruse_diarization.py "%INPUT_DIR%" --pattern "*_optimized.wav" --speakers %SPEAKERS%

REM ============================================
REM SCHRITT 3: Zusammenfassung
REM ============================================
echo [INFO] Schritt 3/3: Zusammenfassung

set OUTPUT_DIR=%INPUT_DIR%\transcripts_whisper_kruse
if exist "%OUTPUT_DIR%" (
    set TRANSCRIPT_COUNT=0
    for %%f in ("%OUTPUT_DIR%\*.txt") do set /a TRANSCRIPT_COUNT+=1

    echo [INFO] Fertig! %TRANSCRIPT_COUNT% Transkripte erstellt
    echo [INFO] Output-Ordner: %OUTPUT_DIR%

    echo.
    echo Erstelle Transkripte:
    set COUNT=0
    for %%f in ("%OUTPUT_DIR%\*.txt") do (
        if !COUNT! LSS 3 (
            echo   - %%~nxf
            set /a COUNT+=1
        )
    )

    if %TRANSCRIPT_COUNT% GTR 3 (
        set /a REMAINING=%TRANSCRIPT_COUNT%-3
        echo   ... und !REMAINING! weitere
    )
) else (
    echo [ERROR] Output-Ordner nicht gefunden: %OUTPUT_DIR%
    exit /b 1
)

echo.
echo [INFO] Pipeline abgeschlossen!

endlocal
