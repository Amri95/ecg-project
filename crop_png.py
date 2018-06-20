import cv2


def crop_png(file_address):
    img = cv2.imread(file_address)

    # 1376:1376+3338, 103:103+6338 was manually fitted
    crop_img = img[1376:1376+3338, 103:103+6338]
    cv2.imwrite(file_address[:-4] + "_cropped.png", crop_img)


def main():
    crop_png("MUSE_20180323_153150_73000.png")


if __name__ == "__main__":
    main()
