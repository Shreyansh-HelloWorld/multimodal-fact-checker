# scripts/test_ocr.py
import sys
import os

# This is the single, final version of this file.

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.vision.ocr import extract_text_from_image

# This line specifies the image to test.
TEST_IMAGE_PATH = "data/ocr_test_image.png"

print(f"--- Extracting text from image: {TEST_IMAGE_PATH} ---")

# Check if the test image exists before running.
if not os.path.exists(TEST_IMAGE_PATH):
    print(f"\nERROR: Test image not found at '{TEST_IMAGE_PATH}'.")
    print("Please add an image with text to the 'data' folder to run this test.")
else:
    # Run the OCR function from our module
    extracted_text = extract_text_from_image(TEST_IMAGE_PATH)
    
    if extracted_text:
        print("\nSuccessfully Extracted Text:")
        print(f'-> "{extracted_text}"')
    else:
        print("\nNo text was found in the image, or an error occurred.")