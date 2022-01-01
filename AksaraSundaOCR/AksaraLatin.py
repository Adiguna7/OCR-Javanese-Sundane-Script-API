
from typing import Callable


class AksaraSundaCharacter:
    def __init__(self, id : int, char : str, fun : Callable) -> None:
        self.id = id
        self.char = char
        self.praseFunc = fun
    
    def str_builder(self, text : str) -> str:
        return self.praseFunc(text)
    

AksaraMap = {}

## glyph

# Vocal
AksaraMap[1] = AksaraSundaCharacter(1, 'a', lambda text : text + 'A')
AksaraMap[2] = AksaraSundaCharacter(2, 'i', lambda text : text + 'I')
AksaraMap[3] = AksaraSundaCharacter(3, 'u', lambda text : text + 'U')
AksaraMap[4] = AksaraSundaCharacter(4, 'e', lambda text : text + 'É')
AksaraMap[5] = AksaraSundaCharacter(5, 'o', lambda text : text + 'O')
AksaraMap[6] = AksaraSundaCharacter(6, 'a', lambda text : text + 'E')
AksaraMap[7] = AksaraSundaCharacter(7, 'a', lambda text : text + 'EU')

# Consonants (Native)
AksaraMap[9]  = AksaraSundaCharacter(9, 'g', lambda text : text + 'GA')
AksaraMap[8]  = AksaraSundaCharacter(8, 'k', lambda text : text + 'KA')
AksaraMap[10] = AksaraSundaCharacter(10, 'ng', lambda text : text + 'NGA')
AksaraMap[11] = AksaraSundaCharacter(11, 'c', lambda text : text + 'CA')
AksaraMap[12] = AksaraSundaCharacter(12, 'j', lambda text : text + 'JA')
AksaraMap[13] = AksaraSundaCharacter(13, 'ny', lambda text : text + 'NYA')
AksaraMap[14] = AksaraSundaCharacter(14, 't', lambda text : text + 'TA')
AksaraMap[15] = AksaraSundaCharacter(15, 'd', lambda text : text + 'DA')
AksaraMap[16] = AksaraSundaCharacter(16, 'n', lambda text : text + 'NA')
AksaraMap[17] = AksaraSundaCharacter(17, 'p', lambda text : text + 'PA')
AksaraMap[18] = AksaraSundaCharacter(18, 'b', lambda text : text + 'BA')
AksaraMap[19] = AksaraSundaCharacter(19, 'm', lambda text : text + 'MA')
AksaraMap[20] = AksaraSundaCharacter(20, 'y', lambda text : text + 'YA')
AksaraMap[21] = AksaraSundaCharacter(21, 'r', lambda text : text + 'RA')
AksaraMap[22] = AksaraSundaCharacter(22, 'l', lambda text : text + 'LA')
AksaraMap[23] = AksaraSundaCharacter(23, 'w', lambda text : text + 'WA')
AksaraMap[24] = AksaraSundaCharacter(24, 's', lambda text : text + 'SA')
AksaraMap[25] = AksaraSundaCharacter(25, 'h', lambda text : text + 'HA')

#Consonants (foreign)
AksaraMap[26] = AksaraSundaCharacter(26, 'f', lambda text : text + 'FA')
AksaraMap[27] = AksaraSundaCharacter(27, 'q', lambda text : text + 'QA')
AksaraMap[28] = AksaraSundaCharacter(28, 'v', lambda text : text + 'VA')
AksaraMap[29] = AksaraSundaCharacter(29, 'x', lambda text : text + 'XA')
AksaraMap[30] = AksaraSundaCharacter(30, 'z', lambda text : text + 'ZA')
AksaraMap[31] = AksaraSundaCharacter(31, 'kh', lambda text : text + 'KHA')
AksaraMap[32] = AksaraSundaCharacter(32, 'sy', lambda text : text + 'SYA')

## Diacritics

#Above Diacritics
AksaraMap[33] = AksaraSundaCharacter(33, 'i', lambda text : text.replace('A', 'I'))
AksaraMap[34] = AksaraSundaCharacter(34, 'E', lambda text : text.replace('A', 'E'))
AksaraMap[35] = AksaraSundaCharacter(35, 'EU', lambda text : text.replace('A', 'EU'))
AksaraMap[36] = AksaraSundaCharacter(36, 'R', lambda text : text + "R")
AksaraMap[37] = AksaraSundaCharacter(37, 'NG', lambda text : text + "NG")

#Below Diacritics
AksaraMap[38] = AksaraSundaCharacter(38, 'É', lambda text : text.replace('A', 'É'))
AksaraMap[39] = AksaraSundaCharacter(39, 'r', lambda text : text[0] + 'R' + text[1])
AksaraMap[40] = AksaraSundaCharacter(40, 'l', lambda text : text[0] + 'L' + text[1])

#Inline Diacritics
AksaraMap[41] = AksaraSundaCharacter(41, 'O', lambda text : text.replace('A', 'O'))
AksaraMap[42] = AksaraSundaCharacter(42, 'EU', lambda text : text.replace('A', 'EU'))
AksaraMap[43] = AksaraSundaCharacter(43, 'y', lambda text : text[0] + 'Y' + text[1])
AksaraMap[44] = AksaraSundaCharacter(44, 'H', lambda text : text + "H")
AksaraMap[45] = AksaraSundaCharacter(45, 'a', lambda text : text.replace('A', ''))


def get_char(id : int) -> AksaraSundaCharacter:
    return AksaraMap[id]

