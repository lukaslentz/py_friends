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

    # Alle Dateien im Ordner durchlaufen
    for filename in os.listdir(folder_selected):
        if filename.endswith(".tex"):
            file_path = os.path.join(folder_selected, filename)
            
            try:
                # Datei als ANSI (cp1252) lesen
                # 'replace' bei errors verhindert den Absturz, falls Zeichen unbekannt sind
                with open(file_path, 'r', encoding='cp1252', errors='replace') as f:
                    content = f.read()

                # Datei als UTF-8 speichern
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"Erfolgreich konvertiert: {filename}")
                converted_count += 1
            except Exception as e:
                print(f"Fehler bei {filename}: {e}")
                error_count += 1

    # Abschlussmeldung
    messagebox.showinfo("Fertig", f"Konvertierung abgeschlossen!\n\nErfolgreich: {converted_count}\nFehler: {error_count}")

if __name__ == "__main__":
    convert_tex_to_utf8()