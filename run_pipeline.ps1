<#
.SYNOPSIS
    Vollständige Transkriptions-Pipeline für Windows (PowerShell)

.DESCRIPTION
    Automatisiert Audio-Optimierung, Transkription und Diarisation

.PARAMETER InputDir
    Ordner mit Audio-Dateien (*.m4a, *.wav, *.mp3)

.PARAMETER Speakers
    Anzahl erwarteter Sprecher (Standard: 2)

.EXAMPLE
    .\run_pipeline.ps1 -InputDir "C:\audio" -Speakers 2
    .\run_pipeline.ps1 "C:\audio"

.NOTES
    Erfordert: Python 3.10+, FFmpeg, OpenAI API Key, HuggingFace Token
#>

param(
    [Parameter(Mandatory=$true, Position=0)]
    [string]$InputDir,

    [Parameter(Mandatory=$false, Position=1)]
    [int]$Speakers = 2
)

# Farb-Funktionen
function Write-Info {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Green
}

function Write-Warn {
    param([string]$Message)
    Write-Host "[WARN] $Message" -ForegroundColor Yellow
}

function Write-Error-Custom {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

# Fehlerbehandlung aktivieren
$ErrorActionPreference = "Stop"

# Banner
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "🎙️  InterviewForge - Audio Transkriptions-Pipeline" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""

# Prüfe ob Ordner existiert
if (-not (Test-Path $InputDir)) {
    Write-Error-Custom "Ordner existiert nicht: $InputDir"
    exit 1
}

# Zähle Audio-Dateien
$audioFiles = Get-ChildItem -Path $InputDir -Include *.m4a,*.wav,*.mp3 -File
$audioCount = $audioFiles.Count

if ($audioCount -eq 0) {
    Write-Error-Custom "Keine Audio-Dateien gefunden in: $InputDir"
    exit 1
}

Write-Info "Gefunden: $audioCount Audio-Dateien"

# Prüfe FFmpeg
try {
    $ffmpegVersion = & ffmpeg -version 2>&1 | Select-Object -First 1
    Write-Info "FFmpeg gefunden: $($ffmpegVersion -replace 'ffmpeg version ', '')"
} catch {
    Write-Error-Custom "FFmpeg nicht gefunden! Bitte installieren:"
    Write-Host "  Download: https://ffmpeg.org/download.html" -ForegroundColor Yellow
    Write-Host "  oder mit winget: winget install --id=Gyan.FFmpeg -e" -ForegroundColor Yellow
    exit 1
}

# Prüfe Python und venv
if (-not (Test-Path "venv")) {
    Write-Warn "Virtual Environment nicht gefunden. Erstelle venv..."
    python -m venv venv

    & "venv\Scripts\Activate.ps1"

    Write-Info "Installiere Dependencies..."
    pip install -r requirements.txt
} else {
    & "venv\Scripts\Activate.ps1"
}

# Prüfe Python-Version
$pythonVersion = & python --version 2>&1
Write-Info "Python: $pythonVersion"

# Prüfe API Keys
if (-not $env:OPENAI_API_KEY) {
    Write-Error-Custom "OPENAI_API_KEY nicht gesetzt!"
    Write-Host "Setze mit: `$env:OPENAI_API_KEY='your-key'" -ForegroundColor Yellow
    Write-Host "Oder erstelle .env Datei" -ForegroundColor Yellow
    exit 1
}

if (-not $env:HF_TOKEN) {
    Write-Error-Custom "HF_TOKEN nicht gesetzt!"
    Write-Host "Setze mit: `$env:HF_TOKEN='your-token'" -ForegroundColor Yellow
    Write-Host "Oder erstelle .env Datei" -ForegroundColor Yellow
    exit 1
}

Write-Info "API Keys gefunden ✓"
Write-Host ""

# ============================================
# SCHRITT 1: Audio-Optimierung
# ============================================
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Info "Schritt 1/3: Audio-Optimierung"
Write-Host "=" * 70 -ForegroundColor Cyan

$optimizedCount = 0

foreach ($file in $audioFiles) {
    $baseName = $file.BaseName
    $directory = $file.DirectoryName

    # Skip falls bereits optimiert
    if ($baseName -like "*_optimized") {
        Write-Info "Überspringe (bereits optimiert): $($file.Name)"
        continue
    }

    $outputFile = Join-Path $directory "$($baseName)_optimized.wav"

    if (Test-Path $outputFile) {
        Write-Info "Existiert bereits: $($baseName)_optimized.wav"
        $optimizedCount++
        continue
    }

    Write-Info "Optimiere: $($file.Name)"

    & ffmpeg -i "$($file.FullName)" `
        -ar 16000 `
        -ac 1 `
        -af "highpass=f=200,lowpass=f=3000,loudnorm=I=-16" `
        "$outputFile" `
        -y `
        -loglevel error

    if ($LASTEXITCODE -eq 0) {
        $optimizedCount++
    } else {
        Write-Warn "Fehler beim Optimieren von: $($file.Name)"
    }
}

Write-Info "Optimiert: $optimizedCount Dateien"
Write-Host ""

# ============================================
# SCHRITT 2: Transkription
# ============================================
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Info "Schritt 2/3: Transkription (Whisper + Pyannote)"
Write-Host "=" * 70 -ForegroundColor Cyan

& python whisper_kruse_diarization.py "$InputDir" --pattern "*_optimized.wav" --speakers $Speakers

if ($LASTEXITCODE -ne 0) {
    Write-Error-Custom "Transkription fehlgeschlagen!"
    exit 1
}

# ============================================
# SCHRITT 3: Zusammenfassung
# ============================================
Write-Host ""
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Info "Schritt 3/3: Zusammenfassung"
Write-Host "=" * 70 -ForegroundColor Cyan

$outputDir = Join-Path $InputDir "transcripts_whisper_kruse"

if (Test-Path $outputDir) {
    $transcripts = Get-ChildItem -Path $outputDir -Filter "*.txt"
    $transcriptCount = $transcripts.Count

    Write-Info "Fertig! $transcriptCount Transkripte erstellt"
    Write-Info "Output-Ordner: $outputDir"

    Write-Host ""
    Write-Host "Erstelle Transkripte:" -ForegroundColor Cyan

    $displayCount = [Math]::Min(3, $transcriptCount)
    $transcripts | Select-Object -First $displayCount | ForEach-Object {
        Write-Host "  - $($_.Name)" -ForegroundColor Gray
    }

    if ($transcriptCount -gt 3) {
        $remaining = $transcriptCount - 3
        Write-Host "  ... und $remaining weitere" -ForegroundColor Gray
    }
} else {
    Write-Error-Custom "Output-Ordner nicht gefunden: $outputDir"
    exit 1
}

Write-Host ""
Write-Host "=" * 70 -ForegroundColor Green
Write-Host "✅ Pipeline abgeschlossen!" -ForegroundColor Green
Write-Host "=" * 70 -ForegroundColor Green
