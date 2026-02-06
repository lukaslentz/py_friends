#
#
import tkinter as tk
from tkinter import filedialog
import os
from moviepy.editor import *
#
root = tk.Tk()
root.withdraw()
#
#
file_path1 = filedialog.askopenfilename()
file_name = os.path.basename(file_path1)
file_dir = os.path.dirname(file_path1)
#
file_path2 = filedialog.askopenfilename()
file_path3 = filedialog.askopenfilename()
#
#
#   load video 
clip1 = VideoFileClip(file_path1).subclip(0,10).margin(20)
clip2 = VideoFileClip(file_path2).subclip(0,10).margin(20)
clip3 = VideoFileClip(file_path3).subclip(0,20).margin(20)
#
combined = clips_array([[concatenate_videoclips([clip1,clip2]),clip3]])
#
combined.write_videofile(file_dir + '/combined.mp4' )