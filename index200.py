import cv2
import numpy as np
from numpy.lib.type_check import imag
import pytesseract
from pytesseract import Output

def optimal_resize(img, boxes):
    # print(boxes)
    median_height = np.median(boxes["height"])
    target_height = 70
    scale_factor = target_height / median_height
    # print("Scale factor: " + str(scale_factor))
    
    #If the image is already within `skip_percentage` percent of the target size, just return the original image (it's better to skip resizing if we can)
    skip_percentage = 0.07
    if(scale_factor > 1 - skip_percentage and scale_factor < 1 + skip_percentage):
        return img
        
    if(scale_factor > 1.0):
        interpolation = cv2.INTER_CUBIC
    else:
        interpolation = cv2.INTER_AREA
    
    return cv2.resize(img, None, fx = scale_factor, fy = scale_factor, interpolation = interpolation)

def run(image, lang):    
    # print(lang)
    custom_config = r'-l ' + lang + ' --oem 1 --psm 6'
    data = pytesseract.image_to_data(image, config=custom_config, output_type=Output.DATAFRAME)

    image = optimal_resize(image, data)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    threshold_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # print(data)
    txt = pytesseract.image_to_string(threshold_img, config=custom_config)

    # cv2.imshow("image", threshold_img)
    # cv2.waitKey(0) 
    # cv2.destroyAllWindows() 
    
    return txt