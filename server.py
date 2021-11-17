from index import run
from fastapi import FastAPI, File, UploadFile, status
from pydantic import BaseModel
from fastapi.responses import Response
import os
from random import randint
import uuid
import numpy as np
import cv2

app = FastAPI()

@app.post("/image/upload")
async def analyze_route(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        nparr = np.fromstring(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)        
        # img_dimensions = str(img.shape)
        return_text = run(img)

        return {'code': status.HTTP_200_OK, 'status': 'success', 'message': return_text}
    except Exception as e:
        return {'code': status.HTTP_500_INTERNAL_SERVER_ERROR, 'status': 'error', 'message': "Catch an error " + str(e)}

