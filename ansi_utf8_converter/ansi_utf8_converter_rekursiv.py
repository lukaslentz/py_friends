import os
import tkinter as tf
from tkinter import filedialog, messagebox

def convert_tex_to_utf8():
    # GUI Fenster verstecken
    root = tf.Tk()
    root.withdraw()

    # Ordner auswählen
    folder_selected = filedialog.askdirectory(title="Ordner mit .tex Dateien auswählen")
    
    if not folder_selected:
        print("Kein Ordner ausgewählt.")
        return

    converted_count = 0
    error_count = 0

    # Alle Dateien im Ordner UND in allen Unterordnern durchlaufen
    for root_dir, _, files in os.walk(folder_selected):
        for filename in files:
            if filename.endswith(".tex"):
                file_path = os.path.join(root_dir, filename)
                
                try:
                    # Datei als ANSI (cp1252) lesen
                    with open(file_path, 'r', encoding='cp1252', errors='replace') as f:
                        content = f.read()

                    # Datei als UTF-8 speichern
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    print(f"Erfolgreich konvertiert: {file_path}")
                    converted_count += 1
                except Exception as e:
                    print(f"Fehler bei {file_path}: {e}")
                    error_count += 1

    # Abschlussmeldung
    messagebox.showinfo(
        "Fertig",
        f"Konvertierung abgeschlossen!\n\nErfolgreich: {converted_count}\nFehler: {error_count}"
    )

if __name__ == "__main__":
    convert_tex_to_utf8()
