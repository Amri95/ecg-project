import subprocess
import os

# bashCommand = "Inkscape/inkscape.exe -l ..\ecg-samples\MUSE_20180323_153150_73000.svg " \
#               "..\ecg-samples\MUSE_20180323_153150_73000.pdf"

path = "..\ecg-samples\\"
for file_name in os.listdir(path):
    if file_name[-3:] == "PDF":
        bashCommand = "Inkscape/inkscape.exe -l " + path + file_name[:-3] + "svg " + path + file_name
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()


