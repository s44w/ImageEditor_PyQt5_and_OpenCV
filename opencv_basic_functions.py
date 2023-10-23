import cv2
import numpy as np
import imutils

def resize_image(image, height = 0, width = 0, coef = 0):
    res = None
    mode = cv2.INTER_LINEAR if (height > image.shape[0] or width > image.shape[1] or coef > 1) else cv2.INTER_AREA

    if height and width and coef:
        print('Incorrect input, try again')

    elif height and width:
        res = cv2.resize(image, (height, width), interpolation=mode)

    elif height:
        f = float(height)/image.shape[0]
        width = int(image.shape[1]*f)
        res = cv2.resize(image, (height, width), interpolation=mode)
    elif width:
        f = float(width)/image.shape[1]
        height = int(image.shape[0]*f)
        res = cv2.resize(image, (height, width), interpolation=mode)
    elif coef:
        res = cv2.resize(image, None, fx = coef, fy = coef, interpolation=mode)
    return res


def put_text(image, textLine, coords, textSize, color):
    #выделяю зону -> оставляю ее -> набираю текст (потом) ->

    output = image.copy()
    coef = image.shape[0]/coords[0]

    #height, width, channels = output.shape
    cv2.putText(output, textLine, coords, cv2.FONT_HERSHEY_SIMPLEX, textSize, color, 4)
    return output

def rotate_image(image, degrees):
    '''
    (h,w) = image.shape[:2]
    center = (w/2, h/2)
    prep_object = cv2.getRotationMatrix2D(center, degrees, 1.0) #матрица для поворота

    res = cv2.warpAffine(image, prep_object, (w,h))
    '''
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






