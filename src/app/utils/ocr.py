# src/app/utils/ocr.py
# Placeholder: OCR utilities if required. Requires tesseract installed in environment.
from typing import Optional
try:
    import pytesseract
    from PIL import Image
except Exception:
    pytesseract = None

def ocr_image_bytes(image_bytes: bytes) -> Optional[str]:
    if pytesseract is None:
        return None
    img = Image.open(io.BytesIO(image_bytes))
    return pytesseract.image_to_string(img)
