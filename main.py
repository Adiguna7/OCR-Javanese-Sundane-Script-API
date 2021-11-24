from fastapi import FastAPI
from fastapi import FastAPI, File, UploadFile
import numpy as np
import cv2 as cv
#import AksaraSundaPraser as asp
from AksaraSundaPraser import AksaraSundaPraser as asp
from AksaraSundaPraser import *
from fastapi.middleware.cors import CORSMiddleware

SundePraser = asp.AksaraSundaPraser(model_path= "./AksaraSundaPraser/YoloAksara.pt")

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

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/file/")
async def create_file(file: UploadFile = File(...)):
    contents = await file.read()
    nparr = np.fromstring(contents, np.uint8)
    img = cv.imdecode(nparr, cv.IMREAD_COLOR)[..., ::-1]
    #print(img.shape)
    
    lst = SundePraser.PraseImage(img)

    return {"OCR TEXT": lst}

@app.post("/file/string/")
async def create_file(file: UploadFile = File(...)):
    contents = await file.read()
    nparr = np.fromstring(contents, np.uint8)
    img = cv.imdecode(nparr, cv.IMREAD_COLOR)[..., ::-1]
    #print(img.shape)
    
    lst = SundePraser.PraseImage(img)

    outstr = ""
    for s in lst:
        outstr += s + "\n"
    return {"OCR STRING": outstr}