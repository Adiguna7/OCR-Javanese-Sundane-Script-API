## Instalation and Run Javanese-Sundanese OCR (For linux)

---

First of all clone this project and install python>=3.6:

`` git clone https://github.com/Adiguna7/OCR-Javanese-Sundane-Script-API.git``


Instal Tesseract5.0
1. ``sudo add-apt-repository -y ppa:alex-p/tesseract-ocr-devel``
2. ``sudo apt install tesseract-ocr``

Install Python Depedency
1. ``sudo pip install -r requirements.txt``

Run Server
1. ``uvicorn server:app --reload``
