#!/usr/bin/env python3
import os
import tkinter as tk
from tkinter import filedialog
from pdf2image import convert_from_path

def main():
    # Verstecke das Hauptfenster
    root = tk.Tk()
    root.withdraw()

    # Öffne Dialog zur Auswahl mehrerer PDF-Dateien
    pdf_paths = filedialog.askopenfilenames(
        title="Wähle eine oder mehrere PDF-Dateien",
        filetypes=[("PDF-Dateien", "*.pdf")],
    )
    if not pdf_paths:
        print("Keine PDF-Dateien ausgewählt. Beende Programm.")
        return

    # Öffne Dialog zur Auswahl des Zielordners für die PNG-Dateien
    output_dir = filedialog.askdirectory(
        title="Wähle den Zielordner für die PNG-Dateien"
    )
    if not output_dir:
        print("Kein Zielordner ausgewählt. Beende Programm.")
        return

    # Für jede ausgewählte PDF-Datei eine PNG erzeugen und im gewählten Ordner speichern
    for pdf_path in pdf_paths:
        try:
            # Konvertiere nur die erste Seite der PDF in ein PIL-Image
            images = convert_from_path(pdf_path, first_page=1, last_page=1)
            if not images:
                print(f"Fehler: Konnte Seiten in '{pdf_path}' nicht konvertieren.")
                continue

            img = images[0]
            # Basename der PDF (ohne Verzeichnispfad und ohne Erweiterung)
            base_name = os.path.splitext(os.path.basename(pdf_path))[0]
            # Erzeuge den Pfad für die PNG-Datei im Ausgabeverzeichnis
            png_path = os.path.join(output_dir, base_name + ".png")

            # Speichere das Bild als PNG
            img.save(png_path, "PNG")
            print(f"Erzeugt: {png_path}")

        except Exception as e:
            print(f"Fehler bei '{pdf_path}': {e}")

if __name__ == "__main__":
    main()
