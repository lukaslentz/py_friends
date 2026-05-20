from pathlib import Path
import subprocess
import sys
import tkinter as tk
from tkinter import filedialog, messagebox


def select_input_file() -> Path | None:
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        title="Videodatei auswählen",
        filetypes=[
            ("Videodateien", "*.mp4 *.mov *.mkv *.avi *.webm"),
            ("MP4-Dateien", "*.mp4"),
            ("Alle Dateien", "*.*"),
        ],
    )

    root.destroy()

    if not file_path:
        return None

    return Path(file_path)


def select_output_file(input_path: Path) -> Path | None:
    root = tk.Tk()
    root.withdraw()

    default_name = input_path.stem + "_panopto.mp4"

    file_path = filedialog.asksaveasfilename(
        title="Zieldatei speichern unter",
        defaultextension=".mp4",
        initialfile=default_name,
        filetypes=[
            ("MP4-Datei", "*.mp4"),
            ("Alle Dateien", "*.*"),
        ],
    )

    root.destroy()

    if not file_path:
        return None

    return Path(file_path)


def convert_for_panopto(input_path: Path, output_path: Path, fps: int = 10):
    if not input_path.exists():
        messagebox.showerror("Fehler", f"Datei nicht gefunden:\n{input_path}")
        sys.exit(1)

    cmd = [
        "ffmpeg",
        "-y",

        # Fehlerhafte oder fehlende Zeitstempel möglichst neu erzeugen
        "-fflags", "+genpts+discardcorrupt",
        "-err_detect", "ignore_err",

        # Eingabedatei
        "-i", str(input_path),

        # Video neu codieren
        "-vf", f"fps={fps},format=yuv420p",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "23",

        # Audio neu codieren
        "-c:a", "aac",
        "-b:a", "160k",
        "-ar", "48000",
        "-ac", "2",

        # Für Upload/Streaming günstiger
        "-movflags", "+faststart",

        # Ausgabedatei
        str(output_path),
    ]

    print("Starte Umwandlung...")
    print("Eingabe :", input_path)
    print("Ausgabe :", output_path)
    print()

    try:
        subprocess.run(cmd, check=True)
    except FileNotFoundError:
        messagebox.showerror(
            "ffmpeg nicht gefunden",
            "ffmpeg wurde nicht gefunden.\n\n"
            "Bitte ffmpeg installieren und sicherstellen, dass es im PATH liegt."
        )
        sys.exit(1)
    except subprocess.CalledProcessError:
        messagebox.showerror(
            "Fehler",
            "Die Umwandlung ist fehlgeschlagen."
        )
        sys.exit(1)

    print()
    print("Fertig.")
    print(f"Neue Datei: {output_path}")

    messagebox.showinfo(
        "Fertig",
        f"Die Datei wurde erfolgreich umgewandelt:\n\n{output_path}"
    )


def main():
    input_path = select_input_file()

    if input_path is None:
        print("Keine Eingabedatei ausgewählt.")
        return

    output_path = select_output_file(input_path)

    if output_path is None:
        print("Keine Ausgabedatei ausgewählt.")
        return

    convert_for_panopto(input_path, output_path, fps=10)


if __name__ == "__main__":
    main()