import os
import subprocess
import tkinter as tk
from tkinter import filedialog
from collections import defaultdict

def escape_latex(s):
    """Escapes Sonderzeichen für LaTeX."""
    specials = {
        "_": r"\_",
        "&": r"\&",
        "#": r"\#",
        "%": r"\%",
        "$": r"\$",
        "{": r"\{",
        "}": r"\}",
        "^": r"\^{}",
        "~": r"\~{}",
        "\\": r"\textbackslash{}"
    }
    for char, escaped in specials.items():
        s = s.replace(char, escaped)
    return s

def find_tikz_pdfs(root):
    """
    Durchläuft rekursiv alle Unterordner von 'root' und sammelt alle PDF-Dateien,
    die in Ordnern mit dem Namen "tikz" liegen. Die Pfade werden relativ zu 'root'
    angegeben (mit Forward-Slashes).
    """
    pdf_dict = defaultdict(list)
    for dirpath, dirs, files in os.walk(root):
        if os.path.basename(dirpath).lower() == "tikz":
            for file in sorted(files):
                if file.lower().endswith(".pdf"):
                    full_path = os.path.join(dirpath, file)
                    rel_path = os.path.relpath(full_path, root).replace("\\", "/")
                    section = rel_path.split("/")[0]  # Gruppierung nach erster Unterordner-Ebene
                    pdf_dict[section].append(rel_path)
    return pdf_dict

def build_latex(pdf_dict):
    """
    Erzeugt den LaTeX-Code, in dem für jede Gruppe (Section) ein \section* gesetzt wird
    und jede PDF-Datei in einem eigenen Figure-Block (ein Bild pro Zeile) eingebunden wird.
    """
    latex = """\\documentclass[a4paper,10pt]{article}
\\usepackage{graphicx}
\\usepackage{caption}
\\usepackage{float}
\\usepackage[margin=2cm]{geometry}
\\usepackage{parskip}
\\begin{document}
"""
    for section in sorted(pdf_dict.keys()):
        latex += "\n\\clearpage\n"
        latex += "\\section*{" + escape_latex(section) + "}\n"
        files = pdf_dict[section]
        for f in files:
            latex += "\\begin{figure}[H]\n\\centering\n"
            latex += "\\includegraphics[]{" + f + "}\n"
            latex += "\\caption*{\\texttt{\\detokenize{" + f + "}}}\n"
            latex += "\\end{figure}\n\n"
    latex += "\\end{document}\n"
    return latex

def write_file(content, path):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def compile_latex(tex_file, working_dir):
    subprocess.run(["pdflatex", "-interaction=nonstopmode", os.path.basename(tex_file)], cwd=working_dir)

def cleanup_aux_files(tex_file):
    base = os.path.splitext(tex_file)[0]
    for ext in [".aux", ".log", ".out", ".toc"]:
        try:
            os.remove(base + ext)
        except FileNotFoundError:
            pass

def main():
    # Ordnerauswahl per Filedialog
    tk_root = tk.Tk()
    tk_root.withdraw()
    root_folder = filedialog.askdirectory(title="Wähle das Root-Verzeichnis (mit 'tikz'-Ordnern)")
    if not root_folder:
        print("Kein Ordner ausgewählt. Abbruch.")
        return

    pdf_dict = find_tikz_pdfs(root_folder)
    if not pdf_dict:
        print("Keine PDF-Dateien in 'tikz'-Ordnern gefunden.")
        return

    latex_code = build_latex(pdf_dict)
    tex_path = os.path.join(root_folder, "tikz_gallery.tex")
    write_file(latex_code, tex_path)
    print("LaTeX-Dokument erstellt:", tex_path)

    compile_latex(tex_path, root_folder)
    print("LaTeX-Dokument kompiliert.")

    cleanup_aux_files(tex_path)
    print("Hilfsdateien gelöscht.")
    print("PDF wurde erstellt:", os.path.join(root_folder, "tikz_gallery.pdf"))

if __name__ == "__main__":
    main()
