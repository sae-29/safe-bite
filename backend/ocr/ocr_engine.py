import pytesseract
from PIL import Image
from .preprocess import preprocess_image

import shutil
import os

# Try to find tesseract in common locations or use PATH
tesseract_cmd = shutil.which("tesseract")

# Check common Windows paths if not found in PATH
if not tesseract_cmd:
    # We prioritize the one we just installed
    known_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    if os.path.exists(known_path):
        tesseract_cmd = known_path
    else:
        # Fallback to other potential locations
        possible_paths = [
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
            r"C:\Users\HP\AppData\Local\Programs\Tesseract-OCR\tesseract.exe",
            r"D:\Program Files\Tesseract-OCR\tesseract.exe",
            r"D:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
            r"D:\Tesseract-OCR\tesseract.exe"
        ]
        for p in possible_paths:
            if os.path.exists(p):
                tesseract_cmd = p
                break

# Fallback to the user's path (but it looks like an installer, so we warn)
# user_provided_path = r"D:\Downloads\tesseract-ocr-w64-setup-5.5.0.20241111.exe"

if tesseract_cmd:
    print(f"DEBUG: Found Tesseract at {tesseract_cmd}")
    pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
else:
    print("WARNING: Tesseract-OCR not found in any common locations.")
    print("Checked paths:", possible_paths)



def extract_text(image_path):
    processed = preprocess_image(image_path)
    text = pytesseract.image_to_string(processed)
    return text
