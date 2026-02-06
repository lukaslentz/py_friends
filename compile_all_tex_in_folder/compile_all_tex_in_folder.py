import subprocess
import os
from pathlib import Path
from tkinter import Tk, filedialog

# Erweiterungen, die behalten werden sollen
keep_extensions = {".tex", ".pdf", ".jpeg", ".jpg", ".png", ".py", ".tcp"}

def compile_tex_files(root_dir):
    root_path = Path(root_dir)

    for tex_file in root_path.rglob("*.tex"):
        print(f"🔧 Kompiliere: {tex_file}")
        try:
            subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", str(tex_file)],
                cwd=tex_file.parent,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True
            )
        except subprocess.CalledProcessError:
            print(f"⚠️ Fehler beim Kompilieren: {tex_file}")

    # Hilfsdateien löschen
    for file in root_path.rglob("*.*"):
        if file.suffix.lower() not in keep_extensions:
            try:
                file.unlink()
                print(f"🗑️  Entfernt: {file}")
            except Exception as e:
                print(f"⚠️ Fehler beim Löschen von {file}: {e}")

if __name__ == "__main__":
    # Tkinter GUI initialisieren
    root = Tk()
    root.withdraw()  # Hauptfenster ausblenden

    selected_folder = filedialog.askdirectory(title="Ordner mit .tex-Dateien auswählen")

    if selected_folder:
        compile_tex_files(selected_folder)
    else:
        print("🚫 Kein Ordner ausgewählt. Vorgang abgebrochen.")
