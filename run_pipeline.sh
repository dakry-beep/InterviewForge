#!/bin/bash
# Vollständige Transkriptions-Pipeline
# Verwendung: ./run_pipeline.sh /path/to/audio/folder

set -e  # Exit bei Fehler

# Farben für Output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Funktion für farbigen Output
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Prüfe Argumente
if [ $# -eq 0 ]; then
    log_error "Kein Input-Ordner angegeben!"
    echo "Verwendung: ./run_pipeline.sh /path/to/audio/folder"
    exit 1
fi

INPUT_DIR="$1"
SPEAKERS="${2:-2}"  # Default: 2 Sprecher

# Prüfe ob Ordner existiert
if [ ! -d "$INPUT_DIR" ]; then
    log_error "Ordner existiert nicht: $INPUT_DIR"
    exit 1
fi

# Prüfe ob Audio-Dateien vorhanden sind
AUDIO_COUNT=$(find "$INPUT_DIR" -maxdepth 1 -type f \( -name "*.m4a" -o -name "*.wav" -o -name "*.mp3" \) | wc -l)
if [ "$AUDIO_COUNT" -eq 0 ]; then
    log_error "Keine Audio-Dateien gefunden in: $INPUT_DIR"
    exit 1
fi

log_info "Gefunden: $AUDIO_COUNT Audio-Dateien"

# Prüfe FFmpeg
if ! command -v ffmpeg &> /dev/null; then
    log_error "FFmpeg nicht gefunden! Bitte installieren:"
    echo "  Ubuntu/Debian: sudo apt install ffmpeg"
    echo "  macOS: brew install ffmpeg"
    exit 1
fi

# Prüfe Python und venv
if [ ! -d "venv" ]; then
    log_warn "Virtual Environment nicht gefunden. Erstelle venv..."
    python3 -m venv venv
    source venv/bin/activate
    log_info "Installiere Dependencies..."
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Prüfe API Keys
if [ -z "$OPENAI_API_KEY" ]; then
    log_error "OPENAI_API_KEY nicht gesetzt!"
    echo "Setze mit: export OPENAI_API_KEY='your-key'"
    echo "Oder erstelle .env Datei basierend auf .env.example"
    exit 1
fi

if [ -z "$HF_TOKEN" ]; then
    log_error "HF_TOKEN nicht gesetzt!"
    echo "Setze mit: export HF_TOKEN='your-token'"
    echo "Oder erstelle .env Datei basierend auf .env.example"
    exit 1
fi

# ============================================
# SCHRITT 1: Audio-Optimierung
# ============================================
log_info "Schritt 1/3: Audio-Optimierung"

OPTIMIZED_COUNT=0
for file in "$INPUT_DIR"/*.{m4a,mp3,wav}; do
    # Skip falls Glob nicht matched
    [ -e "$file" ] || continue

    # Skip falls bereits optimiert
    basename=$(basename "$file")
    if [[ $basename == *"_optimized.wav" ]]; then
        log_info "Überspringe (bereits optimiert): $basename"
        continue
    fi

    # Generiere Output-Namen
    filename="${file%.*}"
    output="${filename}_optimized.wav"

    if [ -f "$output" ]; then
        log_info "Existiert bereits: $(basename "$output")"
        OPTIMIZED_COUNT=$((OPTIMIZED_COUNT + 1))
        continue
    fi

    log_info "Optimiere: $(basename "$file")"
    ffmpeg -i "$file" \
        -ar 16000 \
        -ac 1 \
        -af "highpass=f=200,lowpass=f=3000,loudnorm=I=-16" \
        "$output" \
        -y \
        -loglevel error

    OPTIMIZED_COUNT=$((OPTIMIZED_COUNT + 1))
done

log_info "Optimiert: $OPTIMIZED_COUNT Dateien"

# ============================================
# SCHRITT 2: Transkription
# ============================================
log_info "Schritt 2/3: Transkription (Whisper + Pyannote)"

python3 whisper_kruse_diarization.py "$INPUT_DIR" \
    --pattern '*_optimized.wav' \
    --speakers "$SPEAKERS"

# ============================================
# SCHRITT 3: Zusammenfassung
# ============================================
log_info "Schritt 3/3: Zusammenfassung"

OUTPUT_DIR="$INPUT_DIR/transcripts_whisper_kruse"
if [ -d "$OUTPUT_DIR" ]; then
    TRANSCRIPT_COUNT=$(find "$OUTPUT_DIR" -name "*.txt" | wc -l)
    log_info "Fertig! $TRANSCRIPT_COUNT Transkripte erstellt"
    log_info "Output-Ordner: $OUTPUT_DIR"

    # Zeige erste 3 Dateien
    echo ""
    echo "Erstelle Transkripte:"
    find "$OUTPUT_DIR" -name "*.txt" | head -3 | while read -r file; do
        echo "  - $(basename "$file")"
    done

    if [ "$TRANSCRIPT_COUNT" -gt 3 ]; then
        echo "  ... und $((TRANSCRIPT_COUNT - 3)) weitere"
    fi
else
    log_error "Output-Ordner nicht gefunden: $OUTPUT_DIR"
    exit 1
fi

echo ""
log_info "Pipeline abgeschlossen! 🎉"
