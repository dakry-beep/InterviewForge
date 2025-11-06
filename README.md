# InterviewForge

**Forge your qualitative interviews into scientific transcripts**

Automatisierte Audio-Transkription mit Sprecherdiarisation im wissenschaftlichen Kruse-Format

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![OpenAI Whisper](https://img.shields.io/badge/OpenAI-Whisper-green.svg)](https://openai.com/research/whisper)
[![Pyannote Audio](https://img.shields.io/badge/Pyannote-Audio-orange.svg)](https://github.com/pyannote/pyannote-audio)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## Features

- ✅ **Grafische Benutzeroberfläche (GUI)** - einfach zu bedienen
- ✅ **Automatische Transkription** mit OpenAI Whisper (API oder lokal)
- ✅ **Datenschutz-Modus** mit lokalem Whisper (kein API-Key nötig)
- ✅ **Sprecherdiarisation** mit Pyannote Audio 3.1
- ✅ **Wissenschaftliches Format** (Kruse-Notation)
- ✅ **Audio-Optimierung** (FFmpeg)
- ✅ **GPU-beschleunigt** (CUDA-Support)
- ✅ **Batch-Verarbeitung** mehrerer Dateien
- ✅ **Konfigurierbar** via YAML

---

## Beispiel-Output

```
================================================================================
Transkript: interview_01.wav
Datum: 04.11.2025
Format: Kruse-Notation (OpenAI Whisper + Pyannote)
================================================================================

LEGENDE:
  I: SPEAKER_00 (Interviewer)
  P1: SPEAKER_01 (Person 1)

SYMBOLE:
  (.): Kurze Pause
  (..): Mittlere Pause
  (3s): Lange Pause
  ((lacht)): Lachen
  (unv.): Unverständlich

================================================================================

  1 [00:01] I: Wie würden Sie Ihre Erfahrungen beschreiben?
  2
  3 [00:05] P1: Also (..) ich kann sagen, dass es _sehr_ interessant war.
  4     Besonders die ersten Wochen (.) waren herausfordernd.
  5
  6 [00:15] I: Können Sie das genauer erläutern?
```

---

## Installation

### 1. Voraussetzungen

- Python 3.10 oder höher
- FFmpeg
- OpenAI API Key
- Hugging Face Account + Token
- (Optional) NVIDIA GPU mit CUDA für beschleunigte Diarisation

### 2. Repository klonen

```bash
git clone https://github.com/yourusername/InterviewForge.git
cd InterviewForge
```

### 3. Virtual Environment erstellen

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# oder
venv\Scripts\activate  # Windows
```

### 4. Dependencies installieren

**Für API-Modus (empfohlen für beste Qualität):**
```bash
pip install -r requirements.txt
```

**Für Lokal-Modus (Datenschutz, ohne OpenAI API):**
```bash
pip install -r requirements-local.txt
```

**Für GUI (grafische Oberfläche):**

Die GUI nutzt `tkinter`, das bei den meisten Python-Installationen bereits enthalten ist.

**Falls tkinter fehlt:**

**Ubuntu/Debian:**
```bash
sudo apt install python3-tk
```

**Fedora/RHEL:**
```bash
sudo dnf install python3-tkinter
```

**macOS:**
```bash
brew install python-tk
```

**Windows:**
tkinter ist bereits in der Standard-Python-Installation enthalten.

### 5. FFmpeg installieren

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
# Mit winget (empfohlen)
winget install --id=Gyan.FFmpeg -e

# Oder manueller Download
# Lade FFmpeg von https://ffmpeg.org/download.html herunter
# Füge FFmpeg zum PATH hinzu
```

### 6. API-Keys konfigurieren

#### Für API-Modus:

**OpenAI API Key (erforderlich):**
1. Erstelle einen Account bei [OpenAI](https://platform.openai.com/)
2. Generiere einen API Key unter [API Keys](https://platform.openai.com/api-keys)

**Hugging Face Token (erforderlich):**
1. Erstelle einen Account bei [Hugging Face](https://huggingface.co/)
2. Akzeptiere die Nutzungsbedingungen für [pyannote/speaker-diarization-3.1](https://huggingface.co/pyannote/speaker-diarization-3.1)
3. Generiere einen Token unter [Settings > Access Tokens](https://huggingface.co/settings/tokens)

#### Für Lokal-Modus:

**Hugging Face Token (erforderlich):**
- Nur für Pyannote Speaker Diarization erforderlich
- Kein OpenAI API Key nötig!

**Umgebungsvariablen setzen:**

**Linux/macOS:**
```bash
export OPENAI_API_KEY='your-openai-api-key-here'
export HF_TOKEN='your-huggingface-token-here'
```

**Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY='your-openai-api-key-here'
$env:HF_TOKEN='your-huggingface-token-here'
```

**Windows (CMD):**
```cmd
set OPENAI_API_KEY=your-openai-api-key-here
set HF_TOKEN=your-huggingface-token-here
```

Oder erstelle eine `.env` Datei:
```bash
OPENAI_API_KEY=your-openai-api-key-here
HF_TOKEN=your-huggingface-token-here
```

---

## Whisper Modi: API vs. Lokal

InterviewForge unterstützt zwei Transkriptions-Modi:

### 🌐 API-Modus (empfohlen für beste Qualität)
- **Vorteile:**
  - ✅ Beste Transkriptionsqualität
  - ✅ Bessere Performance bei Hintergrundmusik
  - ✅ Geringere Hardware-Anforderungen
  - ✅ Keine Modell-Downloads erforderlich
- **Nachteile:**
  - ❌ OpenAI API Key erforderlich (kostenpflichtig)
  - ❌ Audio-Daten werden an OpenAI gesendet
  - ❌ Internet-Verbindung erforderlich
  - ❌ Dateilimit: 25 MB

### 💻 Lokal-Modus (Datenschutz)
- **Vorteile:**
  - ✅ **Volle Datenschutz-Kontrolle** (keine Daten verlassen deinen Computer)
  - ✅ Kein OpenAI API Key erforderlich (kostenlos)
  - ✅ Offline-Nutzung möglich
  - ✅ Keine Dateigrößen-Limits
- **Nachteile:**
  - ❌ Höhere Hardware-Anforderungen (GPU empfohlen)
  - ❌ Längere Verarbeitungszeit
  - ❌ Modell-Download erforderlich (~3GB für large)
  - ❌ Evtl. niedrigere Qualität bei komplexen Audios

### 🔄 Auto-Modus (Standard)
- Nutzt API-Modus wenn `OPENAI_API_KEY` gesetzt ist
- Fällt automatisch auf Lokal-Modus zurück wenn kein API-Key vorhanden

**Empfehlung:**
- **Wissenschaftliche Interviews mit sensiblen Daten:** Lokal-Modus
- **Öffentliche Daten / beste Qualität:** API-Modus

---

## Verwendung

### 🖥️ Grafische Benutzeroberfläche (GUI) - Empfohlen für Einsteiger

InterviewForge verfügt über eine benutzerfreundliche grafische Oberfläche für einfache Bedienung!

**Start der GUI:**

**Linux/macOS:**
```bash
./start_gui.sh
```

**Windows (Doppelklick):**
- `start_gui.bat` (CMD)
- `start_gui.ps1` (PowerShell)

**Oder direkt mit Python:**
```bash
python interviewforge_gui.py
```

**GUI Features:**
- 📁 Einfache Ordnerauswahl per Durchsuchen-Button
- ⚙️ Alle Einstellungen an einem Ort:
  - Whisper-Modus (Auto/API/Lokal)
  - Sprecheranzahl
  - Modellgröße für lokalen Modus
- 📄 **Ausgabeformate wählbar:**
  - TXT (Kruse-Notation)
  - Markdown (.md)
  - CSV (für Excel/Analyse)
  - HTML (für Browser/Präsentation)
- 🔑 API-Keys direkt eingeben (mit Anzeigen/Verstecken)
- 📊 Live-Fortschrittsanzeige mit farbigem Log
- 🎯 Start/Stop-Buttons
- 📂 Direkter Zugriff auf Output-Ordner

**Screenshot-Übersicht:**
```
┌─────────────────────────────────────────────┐
│        🎙️ InterviewForge                    │
├─────────────────────────────────────────────┤
│ 📁 Eingabe                                   │
│   Audio-Ordner: [C:\audio] [Durchsuchen]   │
├─────────────────────────────────────────────┤
│ ⚙️ Einstellungen                             │
│   Whisper-Modus:    [auto ▼]                │
│   Anzahl Sprecher:  [2]                     │
│   Modellgröße:      [medium ▼]              │
├─────────────────────────────────────────────┤
│ 📄 Ausgabeformate                            │
│   [x] TXT  [x] Markdown  [ ] CSV  [x] HTML  │
├─────────────────────────────────────────────┤
│ 🔑 API-Keys                                  │
│   OpenAI:     [***********] [Anzeigen]      │
│   HuggingFace:[***********] [Anzeigen]      │
├─────────────────────────────────────────────┤
│ 📊 Fortschritt                               │
│ ┌─────────────────────────────────────────┐ │
│ │ [00:12] ✅ Optimierung abgeschlossen    │ │
│ │ [00:13] 🎤 Transkribiere Datei 1/5...  │ │
│ └─────────────────────────────────────────┘ │
│ [████████████░░░░░░░░░░░] 60%              │
├─────────────────────────────────────────────┤
│ [▶️ Starten] [⏹️ Stoppen] [📁 Output öffnen]│
└─────────────────────────────────────────────┘
```

**Vorteile der GUI:**
- ✅ Keine Kommandozeilen-Kenntnisse erforderlich
- ✅ Alle Optionen übersichtlich an einem Ort
- ✅ Direkte visuelle Rückmeldung
- ✅ API-Keys sicher eingeben (mit Passwort-Schutz)
- ✅ Einfacher Zugriff auf Ergebnisse

---

### 💻 Kommandozeile / Terminal

#### Automatische Pipeline

**Linux/macOS:**
```bash
# Auto-Modus (empfohlen)
./run_pipeline.sh /path/to/audio/folder 2 auto

# API-Modus
./run_pipeline.sh /path/to/audio/folder 2 api

# Lokal-Modus (Datenschutz)
./run_pipeline.sh /path/to/audio/folder 2 local
```

**Windows (PowerShell):**
```powershell
# Auto-Modus (empfohlen)
.\run_pipeline.ps1 -InputDir "C:\audio" -Speakers 2 -Mode auto

# Lokal-Modus (Datenschutz)
.\run_pipeline.ps1 -InputDir "C:\audio" -Speakers 2 -Mode local
```

**Windows (CMD):**
```cmd
REM Auto-Modus
run_pipeline.bat "C:\audio" 2 auto

REM Lokal-Modus
run_pipeline.bat "C:\audio" 2 local
```

Die Pipeline führt automatisch durch:
1. ✅ Audio-Optimierung (FFmpeg)
2. ✅ Transkription mit Whisper
3. ✅ Speaker Diarization
4. ✅ Kruse-Format Export

### Manuelle Verwendung

**Linux/macOS:**
```bash
# API-Modus
python whisper_kruse_diarization.py /path/to/audio/folder \
  --pattern '*.wav' \
  --speakers 2 \
  --mode api

# Lokal-Modus (Datenschutz)
python whisper_kruse_diarization.py /path/to/audio/folder \
  --pattern '*.wav' \
  --speakers 2 \
  --mode local \
  --model-size medium
```

**Windows:**
```powershell
# API-Modus
python whisper_kruse_diarization.py "C:\audio" --pattern "*.wav" --speakers 2 --mode api

# Lokal-Modus
python whisper_kruse_diarization.py "C:\audio" --pattern "*.wav" --speakers 2 --mode local --model-size medium
```

**Verfügbare Modellgrößen (lokal):**
- `tiny` - Schnellstes Modell (~1 GB RAM, niedrige Qualität)
- `base` - Standard (~1 GB RAM, gute Balance)
- `small` - Bessere Qualität (~2 GB RAM)
- `medium` - Hohe Qualität (~5 GB RAM, empfohlen)
- `large-v3` - Beste Qualität (~10 GB RAM)

### 📄 Ausgabeformate

InterviewForge kann Transkripte in **4 verschiedenen Formaten** exportieren:

```bash
# Nur TXT (Standard)
python whisper_kruse_diarization.py ./audio --formats txt

# Mehrere Formate gleichzeitig
python whisper_kruse_diarization.py ./audio --formats txt md html

# Alle Formate
python whisper_kruse_diarization.py ./audio --formats all
```

**Format-Übersicht:**

| Format | Datei | Verwendung | Vorteile |
|--------|-------|------------|----------|
| **TXT** | `.txt` | Wissenschaft | Kruse-Notation mit Zeilennummern |
| **Markdown** | `.md` | Dokumentation | GitHub, Obsidian, Notion |
| **CSV** | `.csv` | Datenanalyse | Excel, SPSS, R, Python, Pandas |
| **HTML** | `.html` | Präsentation | Browser, responsive, farbcodiert |

**Format-Beispiele:**

**TXT (Kruse-Notation):**
```
  1 [00:01] I: Wie würden Sie Ihre Erfahrungen beschreiben?
  2
  3 [00:05] P1: Also (..) ich kann sagen, dass es _sehr_
  4     interessant war. Besonders die ersten Wochen (.)
  5     waren herausfordernd.
```

**Markdown (.md):**
```markdown
## Transkript

**[00:01] I:** Wie würden Sie Ihre Erfahrungen beschreiben?

**[00:05] P1:** Also (..) ich kann sagen, dass es _sehr_ interessant war.
Besonders die ersten Wochen (.) waren herausfordernd.
```

**CSV:**
```csv
Zeile,Zeitstempel,Start (s),Ende (s),Dauer (s),Sprecher ID,Sprecher Label,Text
1,00:01,1.00,4.50,3.50,SPEAKER_00,I,"Wie würden Sie Ihre Erfahrungen beschreiben?"
2,00:05,5.20,9.80,4.60,SPEAKER_01,P1,"Also ich kann sagen, dass es sehr interessant war."
```
- ✅ Perfekt für statistische Analyse
- ✅ Import in Excel, SPSS, R
- ✅ Zeitstempel in Sekunden für Berechnungen

**HTML:**
- 🎨 Professionelles Design mit CSS
- 🌈 Farbcodierte Sprecher
- 📱 Responsive Layout (Desktop & Mobile)
- 🖨️ Druckoptimiert
- 🎯 Direkt im Browser öffnen
- ⚡ Keine Software erforderlich

### Audio-Optimierung (empfohlen)

Optimiere deine Audio-Dateien vor der Transkription:

**Einzelne Datei (alle Systeme):**
```bash
ffmpeg -i input.m4a -ar 16000 -ac 1 -af "highpass=f=200,lowpass=f=3000,loudnorm=I=-16" output_optimized.wav -y
```

**Batch-Verarbeitung (Linux/macOS):**
```bash
for file in *.m4a; do
  ffmpeg -i "$file" \
    -ar 16000 \
    -ac 1 \
    -af "highpass=f=200,lowpass=f=3000,loudnorm=I=-16" \
    "${file%.m4a}_optimized.wav" -y
done
```

**Batch-Verarbeitung (Windows PowerShell):**
```powershell
Get-ChildItem *.m4a | ForEach-Object {
  ffmpeg -i $_.FullName `
    -ar 16000 `
    -ac 1 `
    -af "highpass=f=200,lowpass=f=3000,loudnorm=I=-16" `
    "$($_.BaseName)_optimized.wav" -y
}
```

**Batch-Verarbeitung (Windows CMD):**
```cmd
for %%f in (*.m4a) do ffmpeg -i "%%f" -ar 16000 -ac 1 -af "highpass=f=200,lowpass=f=3000,loudnorm=I=-16" "%%~nf_optimized.wav" -y
```

**Optimierungs-Parameter:**
- `-ar 16000`: Resampling auf 16 kHz
- `-ac 1`: Mono (Stereo → Mono)
- `highpass=f=200`: Entfernt tieffrequente Störgeräusche
- `lowpass=f=3000`: Entfernt hochfrequente Störgeräusche
- `loudnorm=I=-16`: Lautstärke-Normalisierung (ITU-R BS.1770-4)

### Parameter

| Parameter | Beschreibung | Standard |
|-----------|--------------|----------|
| `input_dir` | Ordner mit Audio-Dateien | `.` (aktueller Ordner) |
| `--pattern` | Glob-Pattern für Dateien | `*.wav` |
| `--speakers` | Anzahl erwarteter Sprecher | `2` |
| `--config` | Pfad zur Config-Datei | `kruse_config.yaml` |
| `--output` | Output-Ordner | `transcripts_whisper_kruse` |

### Beispiele

**Alle WAV-Dateien transkribieren:**

Linux/macOS:
```bash
python whisper_kruse_diarization.py ./audio --pattern '*.wav' --speakers 2
```

Windows:
```powershell
python whisper_kruse_diarization.py .\audio --pattern "*.wav" --speakers 2
```

**Optimierte Dateien verarbeiten:**

Linux/macOS:
```bash
python whisper_kruse_diarization.py ./audio --pattern '*_optimized.wav' --speakers 2
```

Windows:
```powershell
python whisper_kruse_diarization.py .\audio --pattern "*_optimized.wav" --speakers 2
```

**Eigene Config verwenden:**

Linux/macOS:
```bash
python whisper_kruse_diarization.py ./audio --config my_config.yaml
```

Windows:
```powershell
python whisper_kruse_diarization.py .\audio --config my_config.yaml
```

---

## Konfiguration

Die Sprecherzuordnung kann in `kruse_config.yaml` angepasst werden:

```yaml
speakers:
  SPEAKER_00: "I"    # Interviewer
  SPEAKER_01: "P1"   # Person 1
  SPEAKER_02: "P2"   # Person 2
  SPEAKER_03: "P3"   # Person 3
  SPEAKER_04: "P4"   # Person 4
  SPEAKER_05: "P5"   # Person 5

pause_thresholds:
  short: 0.5    # (.) kurze Pause
  medium: 1.0   # (..) mittlere Pause
  long: 2.0     # (3s) lange Pause
```

---

## Kruse-Notationsformat

Die Pipeline generiert Transkripte im wissenschaftlichen **Kruse-Format**:

### Notationssymbole

| Symbol | Bedeutung | Beispiel |
|--------|-----------|----------|
| `(.)` | Kurze Pause (<1s) | "Ja (.) genau" |
| `(..)` | Mittlere Pause (1-2s) | "Hmm (..) ich denke" |
| `(3s)` | Lange Pause (>2s) | "Warte mal (5s) ja" |
| `((lacht))` | Paraverbale Äußerung | "Das ist lustig ((lacht))" |
| `((seufzt))` | Seufzen | "Ach ((seufzt)) das war schwer" |
| `(unv.)` | Unverständlich | "Ich war (unv.) gestern" |
| `(?)` | Unsicher | "War das gestern(?)" |
| `/` | Abbruch/Unterbrechung | "Ich wollte noch/ nein" |
| `_wort_` | Betonung | "Das ist _sehr_ wichtig" |
| `wo::rt` | Dehnung | "Ja::a genau" |

### Zeitstempel

Format: `[MM:SS]` am Beginn jedes Sprecherwechsels

### Zeilennummerierung

Fortlaufende Nummerierung für wissenschaftliche Zitation (Zeile 1→, 2→, etc.)

**Zitat-Beispiel:**
> "Das war eine wichtige Erfahrung" (Interview_01, Z. 15)

---

## Workflow

```
┌─────────────────┐
│  Audio-Dateien  │
│  (M4A, WAV)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ FFmpeg          │
│ Optimierung     │◄─── 16kHz Mono, Filter, Normalisierung
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ OpenAI Whisper  │
│ API             │◄─── Spracherkennung
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Pyannote Audio  │
│ Diarization     │◄─── Sprecherzuordnung (GPU)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Kruse-Format    │
│ Kombination     │◄─── Zeitstempel, Pausen, Nummerierung
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  TXT-Output     │
│  (Kruse)        │
└─────────────────┘
```

---

## Hardware-Anforderungen

### Minimal
- CPU: x86_64 (Intel/AMD)
- RAM: 8GB
- Festplatte: 5GB frei
- Internet: Stabile Verbindung für API-Calls

### Empfohlen
- CPU: Mehrkern (4+ Kerne)
- RAM: 16GB+
- GPU: NVIDIA mit 8GB+ VRAM (für schnelle Diarisation)
- Festplatte: SSD mit 10GB+ frei
- Internet: Schnelle Verbindung (für große Audio-Dateien)

---

## Troubleshooting

### GUI startet nicht: "ModuleNotFoundError: No module named 'tkinter'"

**Linux:**
```bash
# Ubuntu/Debian
sudo apt install python3-tk

# Fedora/RHEL
sudo dnf install python3-tkinter
```

**macOS:**
```bash
brew install python-tk
```

**Windows:**
tkinter sollte bereits installiert sein. Falls nicht, installiere Python neu von python.org

### "ModuleNotFoundError: No module named 'openai'"
```bash
pip install -r requirements.txt
```

### "CUDA out of memory"
Reduziere die Batch-Größe oder nutze CPU:
```python
# In whisper_kruse_diarization.py
pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.1",
    use_auth_token=hf_token
)  # Nutzt automatisch GPU wenn verfügbar
```

### "OpenAI API Error: Invalid API Key"
Prüfe deinen API Key:
```bash
echo $OPENAI_API_KEY
# Sollte mit "sk-" beginnen
```

### "pyannote model not found"
1. Akzeptiere die Nutzungsbedingungen: https://huggingface.co/pyannote/speaker-diarization-3.1
2. Prüfe deinen HF Token:

Linux/macOS:
```bash
echo $HF_TOKEN
```

Windows (PowerShell):
```powershell
echo $env:HF_TOKEN
```

Windows (CMD):
```cmd
echo %HF_TOKEN%
```

### Windows: "Execution Policy" Fehler bei PowerShell
Wenn du den Fehler "cannot be loaded because running scripts is disabled" erhältst:

```powershell
# Execution Policy temporär für diese Sitzung ändern
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process

# Oder dauerhaft für den aktuellen User
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Windows: FFmpeg nicht im PATH
Wenn FFmpeg nicht gefunden wird:

1. Installiere mit winget:
```powershell
winget install --id=Gyan.FFmpeg -e
```

2. Oder füge FFmpeg manuell zum PATH hinzu:
   - Lade FFmpeg von https://ffmpeg.org/download.html
   - Entpacke nach `C:\ffmpeg`
   - Füge `C:\ffmpeg\bin` zum System PATH hinzu
   - Starte PowerShell/CMD neu

### Lokales Whisper: Modell-Download
Beim ersten Mal nutzen des lokalen Modus werden Modelle heruntergeladen:

**Modellgrößen:**
- `tiny`: ~75 MB
- `base`: ~150 MB
- `small`: ~500 MB
- `medium`: ~1.5 GB
- `large-v3`: ~3 GB

Die Modelle werden in `~/.cache/whisper/` gespeichert (Linux/macOS) oder `%USERPROFILE%\.cache\whisper\` (Windows).

### Lokales Whisper: GPU-Unterstützung
Für schnellere lokale Transkription mit NVIDIA GPU:

**Linux:**
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

**Windows:**
```powershell
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

Prüfe GPU-Support:
```python
python -c "import torch; print(f'CUDA verfügbar: {torch.cuda.is_available()}')"
```

---

## Wissenschaftliche Verwendung

### Methodenbeschreibung (Kopiervorlage)

> Die Transkription erfolgte mittels OpenAI Whisper API (Radford et al., 2022)
> und Pyannote Audio 3.1 (Bredin, 2023) im Kruse-Format (Kruse, 2015).
> Die Audio-Dateien wurden zunächst auf 16 kHz Mono resampled und durch
> Hoch- (200 Hz) und Tiefpassfilter (3000 Hz) bereinigt sowie auf -16 LUFS
> normalisiert (ITU-R BS.1770-4).

### Zitationen

**OpenAI Whisper:**
```
Radford, A., Kim, J. W., Xu, T., Brockman, G., McLeavey, C., & Sutskever, I. (2022).
Robust Speech Recognition via Large-Scale Weak Supervision.
arXiv preprint arXiv:2212.04356.
```

**Pyannote Audio:**
```
Bredin, H. (2023).
pyannote.audio 2.1 speaker diarization pipeline: principle, benchmark, and recipe.
Proceedings of Interspeech 2023.
```

**Kruse-Notation:**
```
Kruse, J. (2015).
Qualitative Interviewforschung: Ein integrativer Ansatz (2. Auflage).
Weinheim: Beltz Juventa.
```

---

## Lizenz

MIT License - siehe [LICENSE](LICENSE) Datei

---

## Beitragen

Contributions sind willkommen! Bitte erstelle einen Pull Request oder öffne ein Issue.

1. Fork das Repository
2. Erstelle einen Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Committe deine Änderungen (`git commit -m 'Add some AmazingFeature'`)
4. Push zum Branch (`git push origin feature/AmazingFeature`)
5. Öffne einen Pull Request

---

## Roadmap

- [x] ~~Lokales Whisper-Modell (ohne API)~~ ✅ Implementiert
- [x] ~~GUI (Grafische Benutzeroberfläche)~~ ✅ Implementiert
- [ ] Support für mehr Transkriptionsformate (GAT2, HIAT)
- [ ] Web-Interface (Browser-basiert)
- [ ] Docker-Container
- [ ] Automatische Qualitätskontrolle
- [ ] Multi-Sprach-Support
- [ ] Audio-Recorder Integration

---

## Methodische Grundlagen

Die Entwicklung der InterviewForge-Pipeline wurde durch das Open-Source-Projekt [noScribe](https://github.com/kaixxx/noScribe) (Dröge, 2024) inspiriert, welches automatisierte Transkription mit Whisper und Speaker Diarization kombiniert.

**InterviewForge stellt jedoch eine eigenständige Implementierung dar**, die statt lokaler Modelle die **OpenAI Whisper API** nutzt und eine **spezialisierte Kruse-Notation** für qualitative Forschung implementiert.

### Designentscheidungen

Die Verwendung der OpenAI Whisper API anstelle lokaler Modelle wurde aus folgenden Gründen gewählt:

- **Bessere Ergebnisse bei Hintergrundmusik**: Die OpenAI API zeigt robustere Performance bei komplexen Audio-Szenarien mit Musik oder Umgebungsgeräuschen
- **Datenschutz-Kontext**: Für die Transkription öffentlicher Fernsehsendungen spielen Datenschutzbedenken eine untergeordnete Rolle
- **Keine lokale Infrastruktur**: Keine Notwendigkeit für leistungsstarke lokale Hardware mit GPU

### Literaturverweis

```
Dröge, K. (2024). noScribe. AI-powered Audio Transcription
(Version 0.6) [Computer software]. https://github.com/kaixxx/noScribe
```

---

## Danksagungen

- **[noScribe](https://github.com/kaixxx/noScribe)** von Kai Dröge für die Inspiration und das Konzept der Kombination von Whisper + Diarization
- [OpenAI Whisper](https://github.com/openai/whisper) für das Spracherkennungs-Modell
- [Pyannote Audio](https://github.com/pyannote/pyannote-audio) für die Sprecherdiarisation
- [FFmpeg](https://ffmpeg.org/) für die Audio-Verarbeitung
- Jan Kruse für die Kruse-Notation in der qualitativen Interviewforschung

---

## Kontakt

**Issues:** [GitHub Issues](https://github.com/yourusername/InterviewForge/issues)
**Discussions:** [GitHub Discussions](https://github.com/yourusername/InterviewForge/discussions)

---

**Entwickelt mit ❤️ für wissenschaftliche Transkription**
