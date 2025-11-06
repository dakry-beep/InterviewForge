# 🚀 InterviewForge GUI - Schnellstart

Eine 3-Minuten-Anleitung zum Starten der grafischen Oberfläche.

---

## ⚡ Schnellstart (3 Schritte)

### Schritt 1: Voraussetzungen prüfen

**Python installiert?**
```bash
python --version
# Sollte Python 3.10 oder höher anzeigen
```

**FFmpeg installiert?**
```bash
ffmpeg -version
# Falls nicht: siehe Installation unten
```

### Schritt 2: Dependencies installieren

```bash
# Virtual Environment erstellen (optional, empfohlen)
python -m venv venv

# Aktivieren
source venv/bin/activate          # Linux/macOS
venv\Scripts\activate             # Windows

# Abhängigkeiten installieren
pip install -r requirements.txt    # Für API-Modus
# ODER
pip install -r requirements-local.txt  # Für lokalen Modus
```

### Schritt 3: GUI starten

**Linux/macOS:**
```bash
./start_gui.sh
```

**Windows:**
Doppelklick auf `start_gui.bat`

Oder:
```bash
python interviewforge_gui.py
```

---

## 🎯 Erste Transkription (GUI)

1. **📁 Audio-Ordner auswählen**
   - Klicke auf "Durchsuchen..."
   - Wähle Ordner mit deinen Audio-Dateien (*.wav, *.mp3, *.m4a)

2. **⚙️ Einstellungen**
   - **Whisper-Modus:** `auto` (empfohlen)
     - Nutzt API wenn Key vorhanden, sonst lokal
   - **Anzahl Sprecher:** `2` (Standard)
   - **Modellgröße:** `medium` (für lokalen Modus)

3. **🔑 API-Keys eingeben** (optional)
   - **OpenAI API Key:** Nur für API-Modus
   - **HuggingFace Token:** Für Pyannote (immer erforderlich)
   - Klicke "Anzeigen" um Keys sichtbar zu machen

4. **▶️ Start**
   - Klicke "Transkription starten"
   - Beobachte Fortschritt im Log
   - Warte bis "Erfolgreich abgeschlossen" erscheint

5. **📂 Ergebnisse öffnen**
   - Klicke "Output öffnen"
   - Transkripte befinden sich in: `[dein-ordner]/transcripts_whisper_kruse/`

---

## 🔧 FFmpeg Installation

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
```powershell
# Mit winget
winget install --id=Gyan.FFmpeg -e

# Oder manuell von https://ffmpeg.org/download.html
```

---

## 🔑 API-Keys erhalten

### OpenAI API Key (für API-Modus)
1. Gehe zu https://platform.openai.com/
2. Registriere/Login
3. Gehe zu https://platform.openai.com/api-keys
4. Klicke "Create new secret key"
5. Kopiere den Key (beginnt mit `sk-...`)

### HuggingFace Token (immer erforderlich)
1. Gehe zu https://huggingface.co/
2. Registriere/Login
3. Akzeptiere Nutzungsbedingungen: https://huggingface.co/pyannote/speaker-diarization-3.1
4. Gehe zu https://huggingface.co/settings/tokens
5. Erstelle "New token" (Read-Zugriff reicht)
6. Kopiere den Token

---

## 💡 Tipps

### Für beste Qualität (API-Modus)
- Setze OpenAI API Key
- Wähle Modus: `api`
- ⚠️ Kostet Geld (~$0.006/Minute Audio)

### Für Datenschutz (Lokal-Modus)
- **Kein** OpenAI API Key nötig
- Wähle Modus: `local`
- Wähle Modell: `medium` oder `large`
- ✅ Komplett offline, kostenlos
- ⚠️ Benötigt mehr RAM/GPU

### Audio-Optimierung
Die Pipeline optimiert Audio automatisch:
- 16 kHz Mono
- Hoch-/Tiefpassfilter
- Lautstärke-Normalisierung

### GPU-Beschleunigung
Für **viel** schnellere lokale Transkription:

**NVIDIA GPU?**
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Prüfen:
python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}')"
```

---

## ❓ Probleme?

### GUI startet nicht
**Linux:**
```bash
sudo apt install python3-tk
```

**macOS:**
```bash
brew install python-tk
```

### "No module named..."
```bash
pip install -r requirements.txt
```

### Weitere Hilfe
- Siehe vollständige README.md
- Issues: https://github.com/yourusername/InterviewForge/issues

---

## 📊 Modi-Vergleich

| Feature | API-Modus | Lokal-Modus |
|---------|-----------|-------------|
| **Qualität** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Kosten** | ~$0.006/Min | Kostenlos |
| **Datenschutz** | ⚠️ Daten → OpenAI | ✅ Lokal |
| **Internet** | Erforderlich | Optional |
| **Hardware** | Minimal | GPU empfohlen |
| **Geschwindigkeit** | Schnell | Variabel |

---

**Viel Erfolg mit InterviewForge! 🎙️**

Bei Fragen: Siehe README.md oder erstelle ein Issue.
