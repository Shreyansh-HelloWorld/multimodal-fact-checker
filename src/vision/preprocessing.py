# src/vision/preprocessing.py
import re

def clean_ocr_text(text: str) -> str:
    """
    Performs basic cleaning on text extracted from OCR.
    - Removes non-alphanumeric characters (keeps spaces)
    - Normalizes whitespace
    """
    # Remove special characters, but keep letters, numbers, and spaces
    cleaned_text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    # Replace multiple spaces with a single space
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
    return cleaned_text