AksaraMap = {}

## glyph

# Vocal
AksaraMap[1] = "A"
AksaraMap[2] = "I"
AksaraMap[3] = "U"
AksaraMap[4] = "É"
AksaraMap[5] = "O"
AksaraMap[6] = "E"
AksaraMap[7] = "EU"

# Consonants (Native)
AksaraMap[8]  = "KA"
AksaraMap[9]  = "GA"
AksaraMap[10] = "NGA"
AksaraMap[11] = "CA"
AksaraMap[12] = "JA"
AksaraMap[13] = "NYA"
AksaraMap[14] = "TA"
AksaraMap[15] = "DA"
AksaraMap[16] = "NA"
AksaraMap[17] = "PA"
AksaraMap[18] = "BA"
AksaraMap[19] = "MA"
AksaraMap[20] = "YA"
AksaraMap[21] = "RA"
AksaraMap[22] = "LA"
AksaraMap[23] = "WA"
AksaraMap[24] = "SA"
AksaraMap[25] = "HA"

#Consonants (foreign)
AksaraMap[26] = "FA"
AksaraMap[27] = "QA"
AksaraMap[28] = "VA"    
AksaraMap[29] = "XA"
AksaraMap[30] = "ZA"
AksaraMap[31] = "KHA"
AksaraMap[32] = "SYA"

## Diacritics

#Above Diacritics
AksaraMap[33] = "I"
AksaraMap[34] = "E"
AksaraMap[35] = "EU"
AksaraMap[36] = "R"
AksaraMap[37] = "NG"

#Below Diacritics
AksaraMap[38] = "É"
AksaraMap[39] = "R"
AksaraMap[40] = "L"

#Inline Diacritics
AksaraMap[41] = "O"
AksaraMap[42] = "EU"
AksaraMap[43] = "Y"
AksaraMap[44] = "H"
AksaraMap[45] = ""


def get_char(id):
    return AksaraMap[id]

