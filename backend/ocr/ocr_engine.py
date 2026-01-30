import pytesseract
from PIL import Image
from .preprocess import preprocess_image

import shutil
import os
import cv2
import numpy as np

# Check if Tesseract is in PATH (Debug for Render)
tesseract_cmd = shutil.which("tesseract")
print(f"DEBUG: Initial Tesseract Path: {tesseract_cmd}")

if os.name == 'nt':
    # Windows specific logic
    known_windows_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    if os.path.exists(known_windows_path):
        tesseract_cmd = known_windows_path
        print(f"DEBUG: Found Tesseract at Windows default: {tesseract_cmd}")
    elif not tesseract_cmd:
        # Check other locations
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
                print(f"DEBUG: Found Tesseract at: {tesseract_cmd}")
                break

if tesseract_cmd:
    print(f"DEBUG: Setting Tesseract CMD to: {tesseract_cmd}")
    pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
else:
    print("WARNING: Tesseract-OCR not found in PATH or common locations.")



def extract_text(image_path):
    processed = preprocess_image(image_path)
    text = pytesseract.image_to_string(processed)
    return text
