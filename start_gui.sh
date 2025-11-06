#!/bin/bash
# InterviewForge GUI Launcher (Linux/macOS)

# Farben
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}🎙️ InterviewForge GUI${NC}"
echo ""

# Prüfe Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 nicht gefunden!${NC}"
    echo "Bitte installiere Python 3.10 oder höher"
    exit 1
fi

# Aktiviere venv falls vorhanden
if [ -d "venv" ]; then
    echo -e "${GREEN}📦 Aktiviere Virtual Environment...${NC}"
    source venv/bin/activate
fi

# Prüfe tkinter
python3 -c "import tkinter" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}⚠️  tkinter nicht gefunden!${NC}"
    echo "Installiere mit:"
    echo "  Ubuntu/Debian: sudo apt install python3-tk"
    echo "  macOS: brew install python-tk"
    exit 1
fi

# Starte GUI
echo -e "${GREEN}🚀 Starte GUI...${NC}"
python3 interviewforge_gui.py

# Deaktiviere venv
if [ -d "venv" ]; then
    deactivate 2>/dev/null || true
fi
