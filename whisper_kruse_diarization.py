#!/usr/bin/env python3
"""
OpenAI Whisper + Pyannote Speaker Diarization + Kruse Format
Kombiniert beste Textqualität (OpenAI) mit Speaker-Trennung (Pyannote) und Kruse-Notation
"""

import os
import sys
import argparse
import yaml
import time
from pathlib import Path
from datetime import datetime
from openai import OpenAI
from typing import Optional, Dict, List

# Farben
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_colored(text: str, color: str):
    print(f"{color}{text}{Colors.ENDC}")

def load_kruse_config(config_path: Path) -> dict:
    """Lädt Kruse-Konfiguration"""
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def map_speaker(speaker: str, config: dict) -> str:
    """Mapped Speaker-ID zu Kruse-Label"""
    speakers = config.get('speakers', {})
    return speakers.get(speaker, speakers.get('default', 'P') + speaker.split('_')[-1])

def detect_pause(prev_end: float, curr_start: float, config: dict) -> Optional[str]:
    """Erkennt Pausen zwischen Segmenten"""
    thresholds = config.get('thresholds', {})
    pause_duration = curr_start - prev_end

    if pause_duration >= thresholds.get('long_pause_min_s', 3.0):
        return f"({int(pause_duration)}s)"
    elif pause_duration >= thresholds.get('medium_pause_s', 2.0):
        return config['symbols'].get('medium_pause', "(..)")
    elif pause_duration >= thresholds.get('short_pause_s', 1.0):
        return config['symbols'].get('short_pause', "(.)")

    return None

def format_time_kruse(seconds: float, format_type: str = "MM:SS") -> str:
    """Formatiert Zeit nach Kruse-Standard"""
    if format_type == "MM:SS":
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{mins:02d}:{secs:02d}"
    else:
        hours = int(seconds // 3600)
        mins = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours:02d}:{mins:02d}:{secs:02d}"

def transcribe_with_openai(client: OpenAI, audio_file: Path, language: str = "de", prompt: str = None) -> dict:
    """Transkribiert mit OpenAI Whisper"""
    print_colored(f"📤 OpenAI Whisper: {audio_file.name}", Colors.OKCYAN)

    file_size_mb = audio_file.stat().st_size / (1024 * 1024)

    if file_size_mb > 25:
        print_colored(f"❌ Datei zu groß: {file_size_mb:.1f} MB (Limit: 25 MB)", Colors.FAIL)
        return None

    start = time.time()

    # Default-Prompt für deutsche Street-Interviews
    if prompt is None:
        prompt = "Interview, Straßeninterview, Hamburg, Reeperbahn, Anna, Obdachlosigkeit, Drogenkonsum"

    with open(audio_file, 'rb') as f:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
            language=language,
            prompt=prompt,  # Kontext für bessere Erkennung
            response_format="verbose_json",
            timestamp_granularities=["segment"],
            temperature=0.0  # Deterministische Ausgabe für Konsistenz
        )

    elapsed = time.time() - start
    print_colored(f"⏱️  OpenAI: {elapsed:.1f}s", Colors.OKGREEN)

    return transcript

def diarize_with_pyannote(audio_file: Path, num_speakers: Optional[int] = None) -> dict:
    """Speaker Diarization mit pyannote.audio"""
    try:
        from pyannote.audio import Pipeline
        import torch
    except ImportError:
        print_colored("❌ pyannote.audio nicht installiert!", Colors.FAIL)
        print_colored("   Installiere mit: ./venv/bin/pip install pyannote.audio", Colors.WARNING)
        return None

    print_colored(f"🎙️ Pyannote Diarization...", Colors.OKCYAN)

    # Lade Pipeline
    hf_token = os.getenv("HF_TOKEN")
    if hf_token:
        pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization-3.1",
            token=hf_token
        )
    else:
        # Versuche ohne Token (falls lokal gecacht)
        pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization-3.1"
        )

    # GPU-Unterstützung aktivieren
    if torch.cuda.is_available():
        device = torch.device("cuda")
        pipeline.to(device)
        print_colored(f"🚀 GPU aktiviert: {torch.cuda.get_device_name(0)}", Colors.OKGREEN)
    else:
        print_colored("⚠️  Keine GPU verfügbar, nutze CPU", Colors.WARNING)

    # Diarization durchführen
    start = time.time()

    if num_speakers:
        diarization_output = pipeline(str(audio_file), num_speakers=num_speakers)
    else:
        diarization_output = pipeline(str(audio_file))

    elapsed = time.time() - start
    print_colored(f"⏱️  Diarization: {elapsed:.1f}s", Colors.OKGREEN)

    # Konvertiere zu Dict-Format
    segments = []
    # Pyannote 4.x gibt DiarizeOutput zurück, speaker_diarization enthält die Daten
    if hasattr(diarization_output, 'speaker_diarization'):
        diarization = diarization_output.speaker_diarization
    else:
        diarization = diarization_output

    for segment, _, speaker in diarization.itertracks(yield_label=True):
        segments.append({
            'start': segment.start,
            'end': segment.end,
            'speaker': f"SPEAKER_{str(speaker).split('_')[-1] if '_' in str(speaker) else speaker}"
        })

    return {'segments': segments}

def merge_transcription_and_diarization(transcript, diarization) -> List[dict]:
    """Kombiniert Whisper-Text mit Pyannote-Sprechern"""
    # Whisper Segmente
    whisper_segments = []
    if hasattr(transcript, 'segments'):
        for seg in transcript.segments:
            whisper_segments.append({
                'start': seg.start,
                'end': seg.end,
                'text': seg.text.strip()
            })

    # Diarization Segmente
    diar_segments = diarization.get('segments', [])

    # Merge: Für jedes Whisper-Segment finde den passenden Speaker
    merged = []
    last_known_speaker = None

    for wseg in whisper_segments:
        speaker = None
        best_overlap = 0

        # Finde Speaker mit größter Überlappung
        for dseg in diar_segments:
            overlap_start = max(wseg['start'], dseg['start'])
            overlap_end = min(wseg['end'], dseg['end'])
            overlap = max(0, overlap_end - overlap_start)

            if overlap > best_overlap:
                best_overlap = overlap
                speaker = dseg['speaker']

        # Wenn keine Überlappung gefunden: verwende letzten bekannten Speaker
        if speaker is None and best_overlap == 0:
            # Prüfe ob Speaker zur Mitte passt (fallback)
            mid_time = (wseg['start'] + wseg['end']) / 2
            for dseg in diar_segments:
                if dseg['start'] <= mid_time <= dseg['end']:
                    speaker = dseg['speaker']
                    break

            # Wenn immer noch kein Speaker: verwende letzten bekannten
            if speaker is None and last_known_speaker is not None:
                speaker = last_known_speaker
            elif speaker is None:
                speaker = "UNKNOWN"

        if speaker != "UNKNOWN":
            last_known_speaker = speaker

        merged.append({
            'start': wseg['start'],
            'end': wseg['end'],
            'text': wseg['text'],
            'speaker': speaker
        })

    return merged

def generate_kruse_txt(segments: List[dict], audio_file: Path, output_file: Path, config: dict):
    """Generiert Kruse-Format TXT"""

    txt_lines = []
    txt_lines.append("=" * 80)
    txt_lines.append(f"Transkript: {audio_file.name}")
    txt_lines.append(f"Datum: {datetime.now().strftime('%d.%m.%Y')}")
    txt_lines.append(f"Format: Kruse-Notation (OpenAI Whisper + Pyannote)")
    txt_lines.append("=" * 80)
    txt_lines.append("")

    # Legende
    txt_lines.append("LEGENDE:")
    for speaker_id, label in config['speakers'].items():
        if speaker_id != 'default':
            txt_lines.append(f"  {label}: {speaker_id}")
    txt_lines.append("")
    txt_lines.append("SYMBOLE:")
    for symbol_name, symbol in config['symbols'].items():
        txt_lines.append(f"  {symbol}: {symbol_name.replace('_', ' ').title()}")
    txt_lines.append("")
    txt_lines.append("=" * 80)
    txt_lines.append("")

    # Transkript
    line_number = 1
    prev_end = 0
    current_block = []
    current_speaker = None
    current_start = None

    for segment in segments:
        start = segment.get('start', 0)
        end = segment.get('end', 0)
        text = segment.get('text', '').strip()
        speaker = segment.get('speaker', 'UNKNOWN')

        speaker_label = map_speaker(speaker, config)

        # Pause erkennen
        pause = detect_pause(prev_end, start, config)

        # Neuer Sprecher oder neue Zeile
        if speaker != current_speaker:
            # Vorherigen Block schreiben
            if current_block:
                timestamp = format_time_kruse(current_start, config['format'].get('timestamp_format', 'MM:SS'))
                block_text = ' '.join(current_block)

                # Zeilen umbrechen bei max_line_length
                max_len = config['format'].get('max_line_length', 80)
                words = block_text.split()
                lines = []
                current_line = []
                current_length = 0

                for word in words:
                    if current_length + len(word) + 1 <= max_len:
                        current_line.append(word)
                        current_length += len(word) + 1
                    else:
                        lines.append(' '.join(current_line))
                        current_line = [word]
                        current_length = len(word)

                if current_line:
                    lines.append(' '.join(current_line))

                # Schreibe Block
                for i, line in enumerate(lines):
                    if i == 0:
                        if config['format'].get('timestamps_each_block', True):
                            txt_lines.append(f"{line_number:3d} [{timestamp}] {map_speaker(current_speaker, config)}: {line}")
                        else:
                            txt_lines.append(f"{line_number:3d} {map_speaker(current_speaker, config)}: {line}")
                    else:
                        txt_lines.append(f"{line_number:3d}     {line}")
                    line_number += 1

                txt_lines.append("")

            # Pause vor neuem Sprecher
            if pause:
                txt_lines.append(f"{line_number:3d}     {pause}")
                line_number += 1
                txt_lines.append("")

            # Neuen Block starten
            current_speaker = speaker
            current_start = start
            current_block = [text]
        else:
            # Pause im gleichen Sprecher
            if pause:
                current_block.append(pause)
            current_block.append(text)

        prev_end = end

    # Letzten Block schreiben
    if current_block:
        timestamp = format_time_kruse(current_start, config['format'].get('timestamp_format', 'MM:SS'))
        block_text = ' '.join(current_block)

        max_len = config['format'].get('max_line_length', 80)
        words = block_text.split()
        lines = []
        current_line = []
        current_length = 0

        for word in words:
            if current_length + len(word) + 1 <= max_len:
                current_line.append(word)
                current_length += len(word) + 1
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
                current_length = len(word)

        if current_line:
            lines.append(' '.join(current_line))

        for i, line in enumerate(lines):
            if i == 0:
                if config['format'].get('timestamps_each_block', True):
                    txt_lines.append(f"{line_number:3d} [{timestamp}] {map_speaker(current_speaker, config)}: {line}")
                else:
                    txt_lines.append(f"{line_number:3d} {map_speaker(current_speaker, config)}: {line}")
            else:
                txt_lines.append(f"{line_number:3d}     {line}")
            line_number += 1

    # In Datei schreiben
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(txt_lines))

    print_colored(f"💾 Kruse-TXT gespeichert: {output_file}", Colors.OKGREEN)

def main():
    parser = argparse.ArgumentParser(
        description="OpenAI Whisper + Pyannote Diarization + Kruse Format"
    )
    parser.add_argument('input_folder', type=str, help='Ordner mit Audio-Dateien')
    parser.add_argument('-o', '--output', type=str, default=None,
                       help='Output-Ordner (Standard: input_folder/transcripts_whisper_kruse)')
    parser.add_argument('--config', type=str, default='kruse_config.yaml',
                       help='Kruse-Konfigurations-Datei')
    parser.add_argument('--pattern', type=str, default=None,
                       help='Datei-Pattern (z.B. "*_optimized.wav")')
    parser.add_argument('-s', '--speakers', type=int, default=None,
                       help='Anzahl Sprecher (für Diarization)')
    parser.add_argument('-l', '--language', type=str, default='de',
                       help='Sprache (Standard: de)')
    parser.add_argument('--api-key', type=str, default=None,
                       help='OpenAI API Key (oder OPENAI_API_KEY env)')
    parser.add_argument('--hf-token', type=str, default=None,
                       help='HuggingFace Token (oder HF_TOKEN env)')

    args = parser.parse_args()

    # Paths
    input_folder = Path(args.input_folder)
    script_dir = Path(__file__).parent
    config_path = script_dir / args.config

    if not input_folder.exists():
        print_colored(f"❌ Ordner nicht gefunden: {input_folder}", Colors.FAIL)
        sys.exit(1)

    if not config_path.exists():
        print_colored(f"❌ Kruse-Config nicht gefunden: {config_path}", Colors.FAIL)
        sys.exit(1)

    # Load config
    kruse_config = load_kruse_config(config_path)

    # Output folder
    if args.output:
        output_folder = Path(args.output)
    else:
        output_folder = input_folder / "transcripts_whisper_kruse"

    output_folder.mkdir(parents=True, exist_ok=True)

    # API Keys
    api_key = args.api_key or os.getenv('OPENAI_API_KEY')
    if not api_key:
        print_colored("❌ Kein OpenAI API Key!", Colors.FAIL)
        sys.exit(1)

    hf_token = args.hf_token or os.getenv('HF_TOKEN')
    if not hf_token:
        print_colored("⚠️  Kein HuggingFace Token - Pyannote braucht evtl. einen", Colors.WARNING)

    # OpenAI Client
    client = OpenAI(api_key=api_key)

    # Find files
    if args.pattern:
        audio_files = sorted(input_folder.glob(args.pattern))
    else:
        audio_files = []
        for ext in ['.wav', '.mp3', '.m4a', '.flac']:
            audio_files.extend(input_folder.glob(f"*{ext}"))
        audio_files = sorted(set(audio_files))

    if not audio_files:
        print_colored(f"❌ Keine Audio-Dateien gefunden!", Colors.FAIL)
        sys.exit(1)

    # Header
    print_colored(f"\n{'='*70}", Colors.HEADER)
    print_colored(f"🎙️ OpenAI Whisper + Pyannote + Kruse", Colors.HEADER)
    print_colored(f"{'='*70}", Colors.HEADER)
    print_colored(f"📁 Input:  {input_folder}", Colors.OKBLUE)
    print_colored(f"📁 Output: {output_folder}", Colors.OKBLUE)
    print_colored(f"📊 Dateien: {len(audio_files)}", Colors.OKBLUE)
    print_colored(f"{'='*70}\n", Colors.HEADER)

    # Process files
    success = 0
    failed = 0

    for i, audio_file in enumerate(audio_files, 1):
        print_colored(f"\n[{i}/{len(audio_files)}] {audio_file.name}", Colors.BOLD)

        output_txt = output_folder / f"{audio_file.stem}_whisper_kruse.txt"
        if output_txt.exists():
            print_colored(f"⏭️  Bereits vorhanden", Colors.WARNING)
            continue

        try:
            # 1. OpenAI Whisper Transkription
            transcript = transcribe_with_openai(client, audio_file, args.language)
            if not transcript:
                failed += 1
                continue

            # 2. Pyannote Diarization
            diarization = diarize_with_pyannote(audio_file, args.speakers)
            if not diarization:
                failed += 1
                continue

            # 3. Merge
            segments = merge_transcription_and_diarization(transcript, diarization)
            print_colored(f"📊 {len(segments)} Segmente kombiniert", Colors.OKGREEN)

            # 4. Kruse-Format generieren
            generate_kruse_txt(segments, audio_file, output_txt, kruse_config)

            success += 1

        except Exception as e:
            print_colored(f"❌ Fehler: {e}", Colors.FAIL)
            failed += 1

    # Summary
    print_colored(f"\n{'='*70}", Colors.HEADER)
    print_colored(f"✅ Fertig!", Colors.HEADER)
    print_colored(f"{'='*70}", Colors.HEADER)
    print(f"   Gesamt:  {len(audio_files)}")
    print_colored(f"   ✅ Erfolg: {success}", Colors.OKGREEN)
    print_colored(f"   ❌ Fehler: {failed}", Colors.FAIL)
    print()

if __name__ == '__main__':
    main()
