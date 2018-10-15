import subprocess
import os


def pdf_to_svg(path):
    for file_name in os.listdir(path):
        print(file_name)
        if file_name[-3:] == "PDF":
        # if file_name == "ecg_1.PDF":
            bash_command = "Inkscape/inkscape.exe -l " + path + file_name[:-3] + "svg " + path + file_name
            # print(bash_command)
            subprocess.Popen(bash_command.split(), stdout=subprocess.PIPE)


def main():
    path = "..\ecg-samples\\"
    pdf_to_svg(path)


if __name__ == "__main__":
    main()
