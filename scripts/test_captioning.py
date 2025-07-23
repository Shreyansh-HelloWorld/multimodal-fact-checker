# scripts/test_captioning.py
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.vision.captioning import generate_image_caption

# We can use the same image we used for the OCR test.
TEST_IMAGE_PATH = "data/captioning_test_image.png"

print(f"--- Generating caption for image: {TEST_IMAGE_PATH} ---")
print("Note: The model will be downloaded on the first run (~900MB).\n")

if not os.path.exists(TEST_IMAGE_PATH):
    print(f"ERROR: Test image not found at '{TEST_IMAGE_PATH}'.")
else:
    # Generate the caption
    caption = generate_image_caption(TEST_IMAGE_PATH)
    print("Generated Caption:")
    print(f'-> "{caption}"')