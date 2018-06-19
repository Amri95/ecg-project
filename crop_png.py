import cv2


def crop_png(file_address):
    img = cv2.imread(file_address + ".png")
    crop_img = img[1376:1376+3338, 103:103+6338]
    cv2.imwrite("cropped.png", crop_img)


def main():
    crop_png("MUSE_20180323_153150_73000")


if __name__ == "__main__":
    main()