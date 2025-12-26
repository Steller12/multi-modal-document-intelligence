# ingestion/ocr.py
import pytesseract
from PIL import Image
import io

def run_ocr(image_bytes):
    try:
        image = Image.open(io.BytesIO(image_bytes))
        return pytesseract.image_to_string(image).strip()
    except Exception:
        return ""
