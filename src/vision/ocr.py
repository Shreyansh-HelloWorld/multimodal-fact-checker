# src/vision/ocr.py
import easyocr
import warnings
from PIL import Image
import numpy as np

# This is the single, final version of this file.

try:
    # Initialize the OCR reader ONCE, forcing CPU for maximum stability.
    reader = easyocr.Reader(['en'], gpu=False)
    print("EasyOCR reader loaded successfully.")
except Exception as e:
    print(f"Failed to load EasyOCR reader. Error: {e}")
    reader = None

def extract_text_from_image(image_path: str) -> str:
    """
    Extracts text from an image using a stable CPU-based method.
    """
    if not reader:
        return "OCR reader is not available."
    try:
        # Pass the image path directly to the reader, which can handle it.
        detections = reader.readtext(image_path)
        
        if not detections:
            return "" # Return empty string if no text is found
            
        all_text = " ".join([text for bbox, text, score in detections])
        return all_text
    except Exception as e:
        return f"An error occurred during OCR processing: {e}"