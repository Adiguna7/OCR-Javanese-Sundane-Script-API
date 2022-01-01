import pandas
import torch
from torch.types import Number
from AksaraSundaOCR.AksaraLatin import *
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
    
    def box_tensor(self, extension = 0) -> torch.Tensor:
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
    
    def Scaled_IoU_Box(self, other : 'DetectedCharacter', treshold = 0.9) -> Number:
        """
        Check if this object is inside other object
        """
        # Check if this object is inside other object
        box = self.box_tensor(extension = 0.5)
        other = other.box_tensor(extension = 0)
        detected_ratio = ops.box_iou(other, box)
        return detected_ratio.item()
    
    def Check_Scaled_Box_IoU(self, other : 'DetectedCharacter', treshold = 0.9) -> bool:
        """
        Check if this object is inside other object
        """
        # Check if this object is inside other object
        box = self.box_tensor(extension = 1.5)
        other = other.box_tensor(extension = 0)
        detected_ratio = ops.box_iou(box, other)
        print(box, other, detected_ratio.item())
        if detected_ratio > treshold:
            return True
        return False
    
class AksaraCompound:
    def __init__(self, glyp : 'DetectedCharacter') -> None:
        self.Glyph = glyp
        self.Diacritics = None
    
    def Check_Diacratics(self, diacratics : 'DetectedCharacter') -> bool:
        if self.Glyph.Check_Scaled_Box_IoU(diacratics):
            #self.Diacritics = diacratics
            return True
        return False
    
    def Scaled_IoU_Box(self, diacratics : 'DetectedCharacter') -> Number:
        return self.Glyph.Scaled_IoU_Box(diacratics)
    
    def Set_Diacratics(self, diacratics : 'DetectedCharacter') -> None:
        self.Diacritics = diacratics
    
    def center_y(self) -> float:
        return self.Glyph.center_y

    def center_x(self) -> float:
        return self.Glyph.center_x
    
    def __str__(self) -> str:
        out_str = ""
        glyp = get_char(self.Glyph.object_class)
        glyp.str_builder(out_str)
        
        if self.Diacritics is not None:
            diac = get_char(self.Diacritics.object_class)
            diac.str_builder(out_str)
        return out_str

    def praser(self) -> str:
        out_str = ""
        glyp = get_char(self.Glyph.object_class)
        out_str = glyp.str_builder(out_str)
        #print(out_str)
        if self.Diacritics is not None:
            diac = get_char(self.Diacritics.object_class)
            out_str = diac.str_builder(out_str)
        return out_str

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
    
    def sort(self) -> None:
        self.Detected_Objects.sort(key = lambda x : x.Glyph.center_x )
    
    
    def __str__(self) -> str:
        strr = ''
        for s in self.PrasedString_list:
            strr += s + ' '
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
    #cleaned_detected = []
    #for obj in detected:
    #    for other in detected:
    #        if obj == other:
    #            pass
    #        if obj.Check_IoU(other):
    #            if obj.confidence < other.confidence:
    #                cleaned_detected.append(other)
    #            else:
    #                cleaned_detected.append(obj)
    #            break
    #    else:
    #        cleaned_detected.append(obj)
        
    
    Detected_Glyphs = []
    Detected_Diacritics = []
    for det in detected:
        if det.object_class < 33:
            Detected_Glyphs.append(det)
            #print('glyph', det.object_class)
        else:
            Detected_Diacritics.append(det)
    
    Detected_AksaraGroup = []
    for det in Detected_Glyphs:
        compund = AksaraCompound(det)
        possible_diacratics = [d for d in Detected_Diacritics] #if compund.Check_Diacratics(d)]
        possible_diacratics.sort(key = lambda x : compund.Scaled_IoU_Box(x))
        clean_diacratics = [d for d in possible_diacratics if compund.Scaled_IoU_Box(d) > 0]
        clean_diacratics.sort(key = lambda x : x.confidence, reverse = False)
        if len(clean_diacratics) > 0:
            compund.Set_Diacratics(clean_diacratics[0])
            #print(clean_diacratics[0].object_class)
        #for d in possible_diacratics:
        #    print()
        #    if compund.Check_Diacratics(d):
        #        compund.Set_Diacratics(d)
        #        #print(compund.Glyph.object_class, compund.Diacritics.object_class)
        #        break
            
        #if len(possible_diacratics) > 0:
        #    compund.Set_Diacratics(possible_diacratics[0])     
        Detected_AksaraGroup.append(compund)
    
    #print('Aksara Group Count :',len(Detected_AksaraGroup))
    
    DetectedLines = []
    for det in Detected_AksaraGroup:
        for lines in DetectedLines:
            if lines.within_limit(det):
                lines.append(det)
                break
        else:
            l = ApproximateLine(det.center_y())
            l.append(det)
            DetectedLines.append(l)    
    
    
    for det in DetectedLines:
        det.sort()
    
    DetectedLines.sort(key = lambda x : x.y_center)
    
    return DetectedLines