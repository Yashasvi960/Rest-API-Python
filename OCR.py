from fastapi import FastAPI
import pytesseract
import asyncio

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Visit the endpoint: /api/v1/extract_text to perform OCR."}

async def read_image(img_pth, lang = 'eng'):
    try:
        text = pytesseract.image_to_string(img_path, lang = lang)
        await asyncio.sleep(2)
        return text
    except:
        return "[ERROR] Unable to process file: {0}".format(img_path)   