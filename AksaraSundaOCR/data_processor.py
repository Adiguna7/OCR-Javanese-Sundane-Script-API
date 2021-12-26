import pandas
import torch
import torchvision.ops as ops

class DetectedCharacter:
    def __init__(self, datarow : pandas.DataFrame ) -> None:
        self.object_class = int(datarow[6])
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
    
class AksaraCompound:
    def __init__(self, glyp : 'DetectedCharacter') -> None:
        self.Glyph = glyp
        self.Diacritics = None
    
    def Check_Diacratics(self, diacratics : 'DetectedCharacter') -> bool:
        if self.Glyph.Check_IoU(diacratics):
            self.Diacritics = diacratics
            return True
        return False
    
    def center_y(self) -> float:
        return self.Glyph.center_y

class ApproximateLine:
    def __init__(self, y : int) -> None:
        self.y_center = y
        self.Detected_Objects = []
        self.PrasedString_list = []
    
    def within_limit(self, compund : 'AksaraCompound', limit : int = 10) -> bool:
        if (self.y_center - limit) <= compund.center_y() <= (self.y_center + limit):
            return True
        return False
    
    def append(self, obj : 'DetectedCharacter') -> None:
        self.Detected_Objects.append(obj)
    
    def __str__(self) -> str:
        strr = ''
        for s in self.PrasedString_list:
            strr += s
        return strr

    def toString(self) -> str:
        return self.__str__()
    


def PraseDataframe(df : pandas.DataFrame) -> list:
    """
    Prase dataframe to list of DetectedCharacter
    """
    df['object_class'] = df['class']
    df = df.drop(df[(df.object_class < 33) & (df.confidence < 0.8)].index) #remove all non great Main Aksara pediction
    
    detected = []
    for row in df.itertuples():
        detected.append( DetectedCharacter(row) )
    
    #remove duplicates for classes over 33
    cleaned_detected = []
    for obj in detected:
        for other in detected:
            if obj == other:
                pass
            if obj.Check_IoU(other):
                if obj.confidence < other.confidence:
                    cleaned_detected.append(other)
                else:
                    cleaned_detected.append(obj)
                break
        else:
            cleaned_detected.append(obj)
        
    
    Detected_Glyphs = []
    Detected_Diacritics = []
    for det in cleaned_detected:
        if det.object_class < 33:
            Detected_Glyphs.append(det)
        else:
            Detected_Diacritics.append(det)
    
    Detected_AksaraGroup = []
    for det in Detected_Glyphs:
        compund = AksaraCompound(det)
        for diac in Detected_Diacritics:
            if compund.Check_Diacratics(diac):
                break        
        Detected_AksaraGroup.append(compund)
    
    DetectedLines = []
    for det in Detected_AksaraGroup:
        for lines in DetectedLines:
            if lines.within_limit(det):
                lines.append(det)
                break
        else:
            l = ApproximateLine(det.center_y())
            DetectedLines.append(l)    
    
    return DetectedLines