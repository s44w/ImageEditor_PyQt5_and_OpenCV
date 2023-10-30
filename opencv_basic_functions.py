import cv2
import numpy as np
import imutils

def put_text(image, textLine, coords, textSize, color):
    output = image.copy()
    cv2.putText(output, textLine, coords, cv2.FONT_HERSHEY_SIMPLEX, textSize, color, 4)
    return output

def rotate_image(image, degrees):
    res = imutils.rotate(image, degrees)
    return res

# -----------------------------COLOR FILTERS------------------------

def filterSepia(image):
    sepiaImage = np.array(image, dtype=np.float64)
    sepiaImage = cv2.transform(sepiaImage, np.matrix([[0.272, 0.543, 0.131],
                                                      [0.349, 0.686, 0.168],
                                                      [0.393, 0.769, 0.189]]))
    sepiaImage[np.where(sepiaImage>255)] = 255
    sepiaImage = np.array(sepiaImage, dtype=np.uint8)

    return sepiaImage

def filterInvert(image):
    invertedImage = cv2.bitwise_not(image)

    return invertedImage


def filterGray(image):
    grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img = cv2.cvtColor(grayImage, cv2.COLOR_GRAY2BGR)
    return img

def filterSharpen(image):
    kernel = np.array([[-1, -1, -1],
                       [-1, 9.5, -1],
                       [-1, -1, -1]])
    sharpenedImage = cv2.filter2D(image, -1, kernel)
    return sharpenedImage

# ---------------------------------------------------------------------

def flip_image(image, mode):
    res = cv2.flip(image, mode)
    return res

def increase_brightness(img, value):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    v = cv2.add(v, value)
    v[v>255] = 255
    v[v<0] = 0

    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img






