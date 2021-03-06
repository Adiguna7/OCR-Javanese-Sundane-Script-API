from fastapi import FastAPI, File, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import Response
from random import randint
import numpy as np
import cv2
import uuid
import os
import uvicorn
import socket

from index200 import run
from AksaraSundaOCR.AksaraSundaPraser import AksaraSundaPraser

ApiVersion = "1.1.1"
SundaPraser = AksaraSundaPraser(model_path= "./AksaraSundaOCR/YoloAksara.pt")

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/image/upload")
async def analyze_route(file: UploadFile = File(...), lang: str = 'jav2'):
    try:
        contents = await file.read()
        nparr = np.fromstring(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)        
        # img_dimensions = str(img.shape)
        return_text = run(img, lang)

        return {'code': status.HTTP_200_OK, 'status': 'success', 'message': return_text}
    except Exception as e:
        return {'code': status.HTTP_500_INTERNAL_SERVER_ERROR, 'status': 'error', 'message': "Catch an error " + str(e)}


#Aksara Sunda API Endpoint

## Multi Line Array Result
@app.post("/api/sunda/lines")
async def Sunda_MultiLineList(file: UploadFile = File(...)):
    contents = await file.read()
    nparr = np.fromstring(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)[..., ::-1] 
    lst = SundaPraser.PraseImage(img)
    return {"OCR TEXT": lst}

## Single Line String Result
@app.post("/api/sunda/string")
async def Sunda_AsSingleString(file: UploadFile = File(...)):
    contents = await file.read()
    nparr = np.fromstring(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)[..., ::-1]   
    lst = SundaPraser.PraseImage(img)
    outstr = ""
    for s in lst:
        outstr += s + "\n"
    return {"OCR STRING": outstr}

@app.get("/api/version")
async def getVersion():
    return ApiVersion

# #Startup Stuff
# if __name__ == "__main__":
#     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     try:
#         s.connect(('10.255.255.255', 1)) # doesn't even have to be reachable
#         IP = s.getsockname()[0]
#     except Exception:
#         IP = '127.0.0.1'
#     finally:
#         s.close()
#     ipaddr = str(IP)
#     uvicorn.run("main:app", host=ipaddr, port=8000, log_level="info")