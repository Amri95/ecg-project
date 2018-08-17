from wand.image import Image
from wand.color import Color
from PyPDF2 import PdfFileWriter, PdfFileReader


def pdf_to_png(file_address):
    with Image(filename=file_address, resolution=600) as img:
        with Image(width=img.width, height=img.height, background=Color("white")) as bg:
            bg.composite(img, 0, 0)
            bg.save(filename=file_address[3:-4] + ".png")


def crop_pdf(file_address):
    with open(file_address, 'rb') as in_f:
        input = PdfFileReader(in_f)
        output = PdfFileWriter()

        page = input.getPage(0)
        # print(page.mediaBox.getUpperRight_x(), page.mediaBox.getUpperRight_y())

        page.cropBox.lowerLeft = (88, 0)
        page.cropBox.upperRight = (612, 792)
        output.addPage(page)

        with open("../ecg-samples/out.pdf", "wb") as out_f:
            output.write(out_f)


def main():
    # pdf_to_png("../MUSE_20180323_153150_73000.pdf")
    crop_pdf("../ecg-samples/MUSE_20180323_153150_73000.pdf")


if __name__ == "__main__":
    main()
