import cv2


def capturing_image(path):
    # Step 1: Load an image from file path
    image = cv2.imread(path)

    # Step 2: Check if image is loaded correctly
    if image is None:
        print("Error: Unable to load image.")
    else:
        return image




image = capturing_image(r'D:\Yr2\DSGP\Virtual Environment\DSGP\TamilDataset\TamilDataset\tsl-a\img_008.jpg')
cv2.imshow("Captured Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

