# InterviewForge

**Forge your qualitative interviews into scientific transcripts**

Automatisierte Audio-Transkription mit Sprecherdiarisation im wissenschaftlichen Kruse-Format

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![OpenAI Whisper](https://img.shields.io/badge/OpenAI-Whisper-green.svg)](https://openai.com/research/whisper)
[![Pyannote Audio](https://img.shields.io/badge/Pyannote-Audio-orange.svg)](https://github.com/pyannote/pyannote-audio)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## Features

- ✅ **Automatische Transkription** mit OpenAI Whisper API
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

```bash
pip install -r requirements.txt
```

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
Lade FFmpeg von [ffmpeg.org](https://ffmpeg.org/download.html) herunter

### 6. API-Keys konfigurieren

**OpenAI API Key:**
1. Erstelle einen Account bei [OpenAI](https://platform.openai.com/)
2. Generiere einen API Key unter [API Keys](https://platform.openai.com/api-keys)

**Hugging Face Token:**
1. Erstelle einen Account bei [Hugging Face](https://huggingface.co/)
2. Akzeptiere die Nutzungsbedingungen für [pyannote/speaker-diarization-3.1](https://huggingface.co/pyannote/speaker-diarization-3.1)
3. Generiere einen Token unter [Settings > Access Tokens](https://huggingface.co/settings/tokens)

**Umgebungsvariablen setzen:**

```bash
export OPENAI_API_KEY='your-openai-api-key-here'
export HF_TOKEN='your-huggingface-token-here'
```

Oder erstelle eine `.env` Datei:
```bash
OPENAI_API_KEY=your-openai-api-key-here
HF_TOKEN=your-huggingface-token-here
```

---

## Verwendung

### Basis-Verwendung

```bash
python whisper_kruse_diarization.py /path/to/audio/folder \
  --pattern '*.wav' \
  --speakers 2
```

### Audio-Optimierung (empfohlen)

Optimiere deine Audio-Dateien vor der Transkription:

```bash
# Einzelne Datei
ffmpeg -i input.m4a \
  -ar 16000 \
  -ac 1 \
  -af "highpass=f=200,lowpass=f=3000,loudnorm=I=-16" \
  output_optimized.wav -y

# Batch-Verarbeitung
for file in *.m4a; do
  ffmpeg -i "$file" \
    -ar 16000 \
    -ac 1 \
    -af "highpass=f=200,lowpass=f=3000,loudnorm=I=-16" \
    "${file%.m4a}_optimized.wav" -y
done
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
```bash
python whisper_kruse_diarization.py ./audio --pattern '*.wav' --speakers 2
```

**Optimierte Dateien verarbeiten:**
```bash
python whisper_kruse_diarization.py ./audio --pattern '*_optimized.wav' --speakers 2
```

**Eigene Config verwenden:**
```bash
python whisper_kruse_diarization.py ./audio --config my_config.yaml
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
```bash
echo $HF_TOKEN
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

- [ ] Support für mehr Transkriptionsformate (GAT2, HIAT)
- [ ] Web-Interface
- [ ] Docker-Container
- [ ] Lokales Whisper-Modell (ohne API)
- [ ] Automatische Qualitätskontrolle
- [ ] Multi-Sprach-Support

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
