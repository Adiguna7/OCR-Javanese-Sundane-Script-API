import torch
from dataclasses import dataclass
import pandas
import cv2 as cv
import numpy as np
import torchvision.ops as ops
from AksaraSundaOCR.data_processor import *
from AksaraSundaOCR.AksaraLatin import *

class AksaraSundaPraser:
    def __init__(self, model_path = "./model/model.pth") -> None:
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path)  # default
        self.model.conf = 0.3  # NMS confidence threshold

    def rescale(self, np_image):
        """
        Rescale image to fit model input size
        """
        img_gray = cv.cvtColor(np_image, cv.COLOR_RGB2GRAY)
        edged = cv.Canny(img_gray, 30, 200)
        contours, _ = cv.findContours(edged, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
        listof_rect = []
        for c in contours:
            x, y, w, h = cv.boundingRect(c)
            tup = (w, h, (w*h) )
            listof_rect.append(tup)
        sortfun = lambda x: x[2]
        listof_rect.sort(key=sortfun, reverse=True)
        mid_offseted = int(len(listof_rect)/2)
              
        avg_width = np.mean([x[0] for x in listof_rect[:mid_offseted]])
        avg_height = np.mean([x[1] for x in listof_rect[:mid_offseted]])
        
        scaled_factor_widht = float( avg_width / 60)
        scaled_factor_height = float( avg_height / 60)
        #print(scaled_factor_widht, scaled_factor_height)
        img_width, img_height, _ = np_image.shape
        
        scaled_width = int(img_width * scaled_factor_widht)
        scaled_hight = int(img_height * scaled_factor_height)
        print(scaled_width, scaled_hight)
        
        resized_img = cv.resize(np_image, (scaled_width, scaled_hight) )
        
        return resized_img
        
        #img = torch.from_numpy(img).float().unsqueeze(0)
        #img = ops.Resize.apply(img, size=640)
        #return img
    
    def PraseImage(self, np_image) -> list:
        
        results = self.model(np_image, size=640)  # includes NMS
        results.save()
        
        resultpd = results.pandas().xyxy[0]
        resultpd["height"] = (resultpd["ymax"] - resultpd["ymin"]) 
        resultpd["y_center"] = resultpd["ymin"] + (resultpd['height'] / 2)

        line_data = PraseDataframe(resultpd)
        
        for l in line_data:
            for detected in l.Detected_Objects:
                id = detected.Glyph.object_class
                c = get_char(id)
                l.PrasedString_list.append(c)
        
        result = [a.toString() for a in line_data]

        return result 
