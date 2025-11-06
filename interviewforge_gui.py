#!/usr/bin/env python3
"""
InterviewForge GUI
Benutzerfreundliche grafische Oberfläche für Audio-Transkription
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
from pathlib import Path
import threading
import subprocess
import queue
from datetime import datetime

class InterviewForgeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("InterviewForge - Audio Transkription")
        self.root.geometry("900x700")

        # Queue für Thread-Kommunikation
        self.output_queue = queue.Queue()
        self.process = None
        self.is_running = False

        # Farben
        self.bg_color = "#f0f0f0"
        self.accent_color = "#4a90e2"

        self.root.configure(bg=self.bg_color)

        self.create_widgets()
        self.load_config()

        # Prüfe regelmäßig die Output-Queue
        self.root.after(100, self.check_output_queue)

    def create_widgets(self):
        """Erstelle alle GUI-Elemente"""

        # Header
        header_frame = tk.Frame(self.root, bg=self.accent_color, height=80)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)

        title_label = tk.Label(
            header_frame,
            text="🎙️ InterviewForge",
            font=("Helvetica", 24, "bold"),
            bg=self.accent_color,
            fg="white"
        )
        title_label.pack(pady=20)

        # Main Container
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # === EINGABE-BEREICH ===
        input_frame = ttk.LabelFrame(main_frame, text="📁 Eingabe", padding=15)
        input_frame.pack(fill=tk.X, pady=(0, 10))

        # Audio-Ordner
        tk.Label(input_frame, text="Audio-Ordner:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.folder_var = tk.StringVar()
        folder_entry = ttk.Entry(input_frame, textvariable=self.folder_var, width=60)
        folder_entry.grid(row=0, column=1, padx=10, pady=5)
        ttk.Button(input_frame, text="Durchsuchen...", command=self.browse_folder).grid(row=0, column=2, pady=5)

        # === EINSTELLUNGEN ===
        settings_frame = ttk.LabelFrame(main_frame, text="⚙️ Einstellungen", padding=15)
        settings_frame.pack(fill=tk.X, pady=(0, 10))

        # Whisper-Modus
        tk.Label(settings_frame, text="Whisper-Modus:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.mode_var = tk.StringVar(value="auto")
        mode_combo = ttk.Combobox(
            settings_frame,
            textvariable=self.mode_var,
            values=["auto", "api", "local"],
            state="readonly",
            width=20
        )
        mode_combo.grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)
        mode_combo.bind("<<ComboboxSelected>>", self.on_mode_change)

        # Info-Label für Modus
        self.mode_info_var = tk.StringVar(value="Automatisch (API wenn verfügbar)")
        tk.Label(settings_frame, textvariable=self.mode_info_var, font=("Helvetica", 9), fg="gray").grid(
            row=0, column=2, sticky=tk.W, pady=5
        )

        # Sprecheranzahl
        tk.Label(settings_frame, text="Anzahl Sprecher:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.speakers_var = tk.IntVar(value=2)
        speakers_spin = ttk.Spinbox(
            settings_frame,
            from_=1,
            to=10,
            textvariable=self.speakers_var,
            width=20
        )
        speakers_spin.grid(row=1, column=1, sticky=tk.W, padx=10, pady=5)

        # Modellgröße (nur für lokalen Modus)
        tk.Label(settings_frame, text="Modellgröße (lokal):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.model_size_var = tk.StringVar(value="medium")
        self.model_size_combo = ttk.Combobox(
            settings_frame,
            textvariable=self.model_size_var,
            values=["tiny", "base", "small", "medium", "large", "large-v2", "large-v3"],
            state="readonly",
            width=20
        )
        self.model_size_combo.grid(row=2, column=1, sticky=tk.W, padx=10, pady=5)

        # Model Info
        model_info_text = "tiny=75MB, base=150MB, small=500MB, medium=1.5GB (empfohlen), large=3GB"
        tk.Label(settings_frame, text=model_info_text, font=("Helvetica", 8), fg="gray").grid(
            row=2, column=2, columnspan=2, sticky=tk.W, pady=5
        )

        # === OUTPUT-FORMATE ===
        formats_frame = ttk.LabelFrame(main_frame, text="📄 Ausgabeformate", padding=15)
        formats_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(formats_frame, text="Wähle Formate:").grid(row=0, column=0, sticky=tk.W, pady=5)

        # Checkboxen für Formate
        self.format_txt_var = tk.BooleanVar(value=True)
        self.format_md_var = tk.BooleanVar(value=False)
        self.format_csv_var = tk.BooleanVar(value=False)
        self.format_html_var = tk.BooleanVar(value=False)

        format_checks_frame = tk.Frame(formats_frame)
        format_checks_frame.grid(row=0, column=1, sticky=tk.W, padx=10, pady=5, columnspan=3)

        ttk.Checkbutton(
            format_checks_frame,
            text="TXT (Kruse)",
            variable=self.format_txt_var
        ).pack(side=tk.LEFT, padx=5)

        ttk.Checkbutton(
            format_checks_frame,
            text="Markdown",
            variable=self.format_md_var
        ).pack(side=tk.LEFT, padx=5)

        ttk.Checkbutton(
            format_checks_frame,
            text="CSV",
            variable=self.format_csv_var
        ).pack(side=tk.LEFT, padx=5)

        ttk.Checkbutton(
            format_checks_frame,
            text="HTML",
            variable=self.format_html_var
        ).pack(side=tk.LEFT, padx=5)

        # Info
        tk.Label(formats_frame, text="Mindestens ein Format auswählen", font=("Helvetica", 8), fg="gray").grid(
            row=1, column=1, sticky=tk.W, padx=10, pady=(0,5)
        )

        # === API-KEYS ===
        api_frame = ttk.LabelFrame(main_frame, text="🔑 API-Keys", padding=15)
        api_frame.pack(fill=tk.X, pady=(0, 10))

        # OpenAI API Key
        tk.Label(api_frame, text="OpenAI API Key:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.openai_key_var = tk.StringVar()
        openai_entry = ttk.Entry(api_frame, textvariable=self.openai_key_var, width=50, show="*")
        openai_entry.grid(row=0, column=1, padx=10, pady=5)
        ttk.Button(api_frame, text="Anzeigen", command=lambda: self.toggle_password(openai_entry)).grid(
            row=0, column=2, pady=5
        )
        tk.Label(api_frame, text="(nur für API-Modus)", font=("Helvetica", 9), fg="gray").grid(
            row=0, column=3, sticky=tk.W, pady=5
        )

        # HuggingFace Token
        tk.Label(api_frame, text="HuggingFace Token:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.hf_token_var = tk.StringVar()
        hf_entry = ttk.Entry(api_frame, textvariable=self.hf_token_var, width=50, show="*")
        hf_entry.grid(row=1, column=1, padx=10, pady=5)
        ttk.Button(api_frame, text="Anzeigen", command=lambda: self.toggle_password(hf_entry)).grid(
            row=1, column=2, pady=5
        )
        tk.Label(api_frame, text="(für Pyannote)", font=("Helvetica", 9), fg="gray").grid(
            row=1, column=3, sticky=tk.W, pady=5
        )

        # === FORTSCHRITT ===
        progress_frame = ttk.LabelFrame(main_frame, text="📊 Fortschritt", padding=15)
        progress_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Log-Ausgabe
        self.log_text = scrolledtext.ScrolledText(
            progress_frame,
            height=15,
            font=("Courier", 9),
            bg="#1e1e1e",
            fg="#00ff00",
            insertbackground="white"
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # Fortschrittsbalken
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            mode='indeterminate'
        )
        self.progress_bar.pack(fill=tk.X, pady=(10, 0))

        # === BUTTONS ===
        button_frame = tk.Frame(main_frame, bg=self.bg_color)
        button_frame.pack(fill=tk.X, pady=(0, 0))

        self.start_button = ttk.Button(
            button_frame,
            text="▶️ Transkription starten",
            command=self.start_transcription,
            style="Accent.TButton"
        )
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = ttk.Button(
            button_frame,
            text="⏹️ Stoppen",
            command=self.stop_transcription,
            state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame,
            text="🗑️ Log löschen",
            command=self.clear_log
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame,
            text="📁 Output öffnen",
            command=self.open_output_folder
        ).pack(side=tk.RIGHT, padx=5)

        # Statusbar
        self.status_var = tk.StringVar(value="Bereit")
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W,
            bg="#e0e0e0"
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Style
        style = ttk.Style()
        style.configure("Accent.TButton", foreground="blue", font=("Helvetica", 11, "bold"))

    def on_mode_change(self, event=None):
        """Aktualisiere Info-Text basierend auf gewähltem Modus"""
        mode = self.mode_var.get()
        info_texts = {
            "auto": "Automatisch (API wenn verfügbar, sonst lokal)",
            "api": "OpenAI Whisper API (beste Qualität)",
            "local": "Lokales Whisper (Datenschutz, kostenlos)"
        }
        self.mode_info_var.set(info_texts.get(mode, ""))

    def toggle_password(self, entry):
        """Zeige/Verstecke Passwort"""
        if entry.cget('show') == '*':
            entry.config(show='')
        else:
            entry.config(show='*')

    def browse_folder(self):
        """Ordner auswählen"""
        folder = filedialog.askdirectory(title="Audio-Ordner auswählen")
        if folder:
            self.folder_var.set(folder)

    def load_config(self):
        """Lade gespeicherte Einstellungen"""
        # Lade API-Keys aus Umgebungsvariablen
        openai_key = os.getenv('OPENAI_API_KEY', '')
        hf_token = os.getenv('HF_TOKEN', '')

        if openai_key:
            self.openai_key_var.set(openai_key)
        if hf_token:
            self.hf_token_var.set(hf_token)

    def log(self, message):
        """Schreibe in Log-Ausgabe"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()

    def clear_log(self):
        """Lösche Log"""
        self.log_text.delete(1.0, tk.END)

    def open_output_folder(self):
        """Öffne Output-Ordner"""
        folder = self.folder_var.get()
        if not folder:
            messagebox.showwarning("Warnung", "Bitte wähle zuerst einen Audio-Ordner aus!")
            return

        output_folder = Path(folder) / "transcripts_whisper_kruse"

        if not output_folder.exists():
            messagebox.showinfo("Info", f"Output-Ordner existiert noch nicht:\n{output_folder}")
            return

        # Öffne Ordner im Datei-Explorer
        if sys.platform == 'win32':
            os.startfile(output_folder)
        elif sys.platform == 'darwin':
            subprocess.run(['open', output_folder])
        else:
            subprocess.run(['xdg-open', output_folder])

    def validate_inputs(self):
        """Validiere Eingaben"""
        if not self.folder_var.get():
            messagebox.showerror("Fehler", "Bitte wähle einen Audio-Ordner aus!")
            return False

        if not Path(self.folder_var.get()).exists():
            messagebox.showerror("Fehler", "Der ausgewählte Ordner existiert nicht!")
            return False

        # Prüfe ob mindestens ein Format gewählt wurde
        if not any([self.format_txt_var.get(), self.format_md_var.get(),
                   self.format_csv_var.get(), self.format_html_var.get()]):
            messagebox.showerror("Fehler", "Bitte wähle mindestens ein Ausgabeformat!")
            return False

        mode = self.mode_var.get()

        # Prüfe API-Key für API-Modus
        if mode == 'api' and not self.openai_key_var.get():
            messagebox.showerror(
                "Fehler",
                "API-Modus gewählt, aber kein OpenAI API Key angegeben!\n\n"
                "Bitte gib einen API Key ein oder wähle 'auto' oder 'local' Modus."
            )
            return False

        return True

    def start_transcription(self):
        """Starte Transkription in separatem Thread"""
        if not self.validate_inputs():
            return

        self.is_running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.progress_bar.start()
        self.status_var.set("Läuft...")

        self.log("=" * 70)
        self.log("🎙️ InterviewForge - Transkription gestartet")
        self.log("=" * 70)

        # Starte in separatem Thread
        thread = threading.Thread(target=self.run_transcription, daemon=True)
        thread.start()

    def run_transcription(self):
        """Führe Transkription aus (in separatem Thread)"""
        try:
            # Setze Umgebungsvariablen
            env = os.environ.copy()
            if self.openai_key_var.get():
                env['OPENAI_API_KEY'] = self.openai_key_var.get()
            if self.hf_token_var.get():
                env['HF_TOKEN'] = self.hf_token_var.get()

            # Baue Kommando
            script_path = Path(__file__).parent / "whisper_kruse_diarization.py"

            # Sammle gewählte Formate
            formats = []
            if self.format_txt_var.get():
                formats.append('txt')
            if self.format_md_var.get():
                formats.append('md')
            if self.format_csv_var.get():
                formats.append('csv')
            if self.format_html_var.get():
                formats.append('html')

            cmd = [
                sys.executable,
                str(script_path),
                self.folder_var.get(),
                '--pattern', '*_optimized.wav',
                '--speakers', str(self.speakers_var.get()),
                '--mode', self.mode_var.get(),
                '--model-size', self.model_size_var.get(),
                '--formats'
            ] + formats

            self.log(f"Befehl: {' '.join(cmd)}")
            self.log(f"Formate: {', '.join(formats)}")
            self.log("")

            # Führe aus
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                env=env
            )

            # Lese Output
            for line in self.process.stdout:
                if not self.is_running:
                    break
                self.output_queue.put(line.strip())

            self.process.wait()

            if self.process.returncode == 0:
                self.output_queue.put("SUCCESS")
            else:
                self.output_queue.put(f"ERROR: Exit code {self.process.returncode}")

        except Exception as e:
            self.output_queue.put(f"EXCEPTION: {str(e)}")

    def check_output_queue(self):
        """Prüfe Output-Queue und aktualisiere GUI"""
        try:
            while True:
                message = self.output_queue.get_nowait()

                if message == "SUCCESS":
                    self.log("")
                    self.log("=" * 70)
                    self.log("✅ Transkription erfolgreich abgeschlossen!")
                    self.log("=" * 70)
                    self.status_var.set("Erfolgreich abgeschlossen")
                    self.finish_transcription()
                    messagebox.showinfo("Erfolg", "Transkription erfolgreich abgeschlossen!")

                elif message.startswith("ERROR:"):
                    self.log("")
                    self.log("=" * 70)
                    self.log(f"❌ {message}")
                    self.log("=" * 70)
                    self.status_var.set("Fehler aufgetreten")
                    self.finish_transcription()
                    messagebox.showerror("Fehler", message)

                elif message.startswith("EXCEPTION:"):
                    self.log("")
                    self.log(f"💥 Exception: {message[11:]}")
                    self.status_var.set("Fehler aufgetreten")
                    self.finish_transcription()
                    messagebox.showerror("Fehler", f"Ein Fehler ist aufgetreten:\n{message[11:]}")

                else:
                    self.log(message)

        except queue.Empty:
            pass

        # Rufe diese Funktion wieder auf
        if self.is_running or not self.output_queue.empty():
            self.root.after(100, self.check_output_queue)

    def stop_transcription(self):
        """Stoppe Transkription"""
        if messagebox.askyesno("Bestätigen", "Möchtest du die Transkription wirklich abbrechen?"):
            self.is_running = False
            if self.process:
                self.process.terminate()
            self.log("")
            self.log("⏹️ Transkription abgebrochen")
            self.status_var.set("Abgebrochen")
            self.finish_transcription()

    def finish_transcription(self):
        """Aufräumen nach Transkription"""
        self.is_running = False
        self.progress_bar.stop()
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)


def main():
    root = tk.Tk()
    app = InterviewForgeGUI(root)

    # Zentriere Fenster
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

    root.mainloop()


if __name__ == '__main__':
    main()
