import os
import subprocess
from moviepy.config import get_setting

# Pfad zum aktuell ausgeführten Skript
script_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_path)

# ffmpeg-Pfad von MoviePy holen
ffmpeg_exe = get_setting("FFMPEG_BINARY")
print("Verwende ffmpeg:", ffmpeg_exe)

# concat-Datei schreiben
with open("concat.txt", "w", encoding="utf-8") as f:
    f.write("file 'Screen_Recording_20251201_132034_Notewise.mp4'\n")
    f.write("file 'Screen_Recording_20251201_134730_Notewise.mp4'\n")

# ffmpeg mit vollem Pfad aufrufen
result = subprocess.run([
    ffmpeg_exe,
    "-f", "concat",
    "-safe", "0",
    "-i", "concat.txt",
    "-c", "copy",
    "combined.mp4"
], capture_output=True, text=True)

print("Returncode:", result.returncode)
if result.returncode != 0:
    print("Fehler bei ffmpeg:")
    print(result.stderr)
else:
    print("Fertig: combined.mp4 erzeugt.")
