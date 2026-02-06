#
import os
import win32com.client
import time
#
def ppt2pdf(pptfile,pdffile):
    powerpoint = win32com.client.DispatchEx("Powerpoint.Application")
    powerpoint.Visible = True
    deck = powerpoint.Presentations.Open(pptfile)
    deck.SaveAs(pdffile, 32)
    deck.Close()
    powerpoint.Quit()
#
pptfile = "C:\SeafileContainer\Seafile\Meine Bibliothek\Lehre\Masele\\2023_24\Folien\Masele1_TV_Kap2_2019.pptx"
pdffile = "C:\SeafileContainer\Seafile\Meine Bibliothek\Lehre\Masele\\2023_24\Folien\Masele1_TV_Kap2_2019.pdf"
#
print(pptfile)
# ppt2pdf(pptfile,pdffile)
#
directory = os.fsencode("C:\SeafileContainer\Seafile\Meine Bibliothek\Lehre\Masele\\2023_24\Folien")
#
kapitel = 1
for filename in os.listdir(directory):
    print(filename)
    pptfilename = os.fsdecode(filename)
    if pptfilename.endswith(".pptx") or pptfilename.endswith(".ppt"):
        pptfile = os.path.join(os.fsdecode(directory),pptfilename)
        pdffile = os.path.join(os.fsdecode(directory),f"MasEle2_WiSe23_24_Kapitel_{kapitel}.pdf")
        kapitel += 1
        ppt2pdf(pptfile,pdffile)

