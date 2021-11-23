import torch
from dataclasses import dataclass
from AksaraSundaPraser import AksaraLatin
import pandas
import torchvision.ops as ops

class DetectedCharacter:
    
    def __init__(self, datarow : pandas.DataFrame ) -> None:
        self.object_class = datarow[6]
        self.confidence = datarow.confidence
        
        self.Coord_topLeft = (datarow[1], datarow[2]) # x, y
        self.Coord_bottomRight = (datarow[3], datarow[4]) # x,y 
        
        self.center_x = (self.Coord_topLeft[0] + self.Coord_bottomRight[0]) / 2
        self.center_y = (self.Coord_topLeft[1] + self.Coord_bottomRight[1]) / 2
        
        self.width = self.Coord_bottomRight[0] - self.Coord_topLeft[0]
        self.height = self.Coord_bottomRight[1] - self.Coord_topLeft[1]
    
    def box_tensor(self, extension = 1) -> torch.Tensor:
        """
        Return box tensor
        """
        extend_x = extension * self.width
        extend_y = extension * self.height
        
        scaled_topleft_X = self.Coord_topLeft[0] - extend_x
        scaled_topleft_Y = self.Coord_topLeft[1] - extend_y
        
        scaled_bottomRight_X = self.Coord_bottomRight[0] + extend_x
        scaled_bottomRight_Y = self.Coord_bottomRight[1] + extend_y
        
        lst = [scaled_topleft_X, scaled_topleft_Y, scaled_bottomRight_X, scaled_bottomRight_Y]
        return torch.tensor([lst])
    
    def Check_IoU(self, other : 'DetectedCharacter', treshold = 0.9) -> bool:
        """
        Check if this object is inside other object
        """
        # Check if this object is inside other object
        detected_ratio = ops.box_iou(self.box_tensor(), other.box_tensor())
        if detected_ratio > treshold:
            return True
        return False
    
    def Check_Scaled_Box_IoU(self, other : 'DetectedCharacter', treshold = 0.9) -> bool:
        """
        Check if this object is inside other object
        """
        # Check if this object is inside other object
        detected_ratio = ops.box_iou(self.box_tensor(extension = 1.5), other.box_tensor())
        if detected_ratio > treshold:
            return True
        return False

class CharacterGroup():
    def __init__(self) -> None:
        self.Character = []
        pass
    
    def add(self, character : DetectedCharacter) -> None:
        self.Character.append(character)

@dataclass
class CharacterLine:
    y_center: int = 0
    char_list = []
    str_list  = []
    
    def __str__(self):
        text = ""
        for c in self.str_list:
            text += c
        return text

    def toString(self) -> str:
        return self.__str__()


class AksaraSundaPraser:
    def __init__(self, model_path = "./model/model.pth") -> None:
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path)  # default
        self.model.conf = 0.8  # NMS confidence threshold

    def pdIterate(self, pd):
        LineList = []

        for prediction in pd.itertuples():
            added = False
            for line in LineList:
                if abs(line.y_center - prediction.y_center) < 10:
                    line.char_list.append(prediction)
                    added = True
                    break
        
    
        if added == False:
            new_line = CharacterLine()
            new_line.y_center = prediction.y_center
            LineList.append(new_line)
        
        return LineList
    
    def PraseImage(self, np_image) -> list:
        
        results = self.model(np_image, size=640)  # includes NMS
        
        resultpd = results.pandas().xyxy[0]
        resultpd["height"] = (resultpd["ymax"] - resultpd["ymin"]) 
        resultpd["y_center"] = resultpd["ymin"] + (resultpd['height'] / 2)
                
        LineList = []

        for prediction in resultpd.itertuples():
            added = False
            
            for line in LineList:
                if abs(line.y_center - prediction.y_center) < 10:
                    line.char_list.append(prediction)
                    added = True
                    break
    
            if added == False:
                new_line = CharacterLine()
                new_line.char_list = []
                new_line.str_list = []
                new_line.y_center = prediction.y_center
                LineList.append(new_line)

        for line in LineList:
            line.str_list = []
            for char in line.char_list:
                line.str_list.append(AksaraLatin.get_char(int(char.name[1:])))
        
        result = [a.toString() for a in LineList]
        #print(LineList)
        #results.save()
        
        return result 
