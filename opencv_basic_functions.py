import cv2
import imutils
def save_image(image):
    print('Name the image:', end = '')
    name = input()
    name+='.jpg'
    cv2.imwrite(name, image)
    return


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

def crop_image(image):
    crop = None
    cropping = False

    return crop


def put_text(image, textLine, coords, textSize, color):
    #выделяю зону -> оставляю ее -> набираю текст (потом) ->

    output = image.copy()
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

def flip_image(image, mode):
    res = cv2.flip(image, mode)
    return res
def choose_mode(image):
    print('Input \'rot\' to rotate image,   \'res\' to resize,   \'crp\' to crop,',
          '\'flp\' to flip', sep = '')
    print('Choose modification of image:', end = '')

    mode = str(input())
    res = None
    print()
    match(mode):
        case 'rot':
            print('Input degrees:', end = '')
            degrees = int(input())

            res = rotate_image(image, degrees)

        case 'crp':
            print('Input x1, x2, y1, y2:', end = '')
            params = list(map(float, input().split()))
            res = crop_image(image, *params)

        case 'res':
            print('Input height, width and coefficient:', end = '')
            params = list(map(float, input().split()))
            res = resize_image(image, *params)

        case 'flp':
            print('Choose side of flip - \'0\' to flip horizontally, \'1\' to vertically, '
                  '\n\'-1\' to horizontally and vertically', sep = '')
            mode = int(input())
            res = flip_image(image, mode)

    return res





