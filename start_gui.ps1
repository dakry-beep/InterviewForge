<#
.SYNOPSIS
    InterviewForge GUI Launcher (Windows PowerShell)

.DESCRIPTION
    Startet die grafische Benutzeroberfläche für InterviewForge

.EXAMPLE
    .\start_gui.ps1
#>

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  🎙️  InterviewForge GUI" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Prüfe Python
try {
    $pythonVersion = & python --version 2>&1
    Write-Host "[INFO] Python gefunden: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Python nicht gefunden!" -ForegroundColor Red
    Write-Host "Bitte installiere Python 3.10 oder höher von python.org" -ForegroundColor Yellow
    Read-Host "Drücke Enter zum Beenden"
    exit 1
}

# Aktiviere venv falls vorhanden
if (Test-Path "venv\Scripts\Activate.ps1") {
    Write-Host "[INFO] Aktiviere Virtual Environment..." -ForegroundColor Green
    & "venv\Scripts\Activate.ps1"
}

# Starte GUI
Write-Host "[INFO] Starte GUI..." -ForegroundColor Green
Write-Host ""

& python interviewforge_gui.py

# Warte auf Benutzer-Eingabe wenn Fehler auftritt
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "[ERROR] GUI wurde mit Fehler beendet (Code: $LASTEXITCODE)" -ForegroundColor Red
    Read-Host "Drücke Enter zum Beenden"
}
