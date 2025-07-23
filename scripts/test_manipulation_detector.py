# scripts/test_manipulation_detector.py
import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.vision.manipulation_detector import classify_image_authenticity

# --- Define paths for your test images ---
REAL_IMAGE1_PATH = "data/real_photo1.jpg"
REAL_IMAGE2_PATH = "data/real_photo2.jpg"
AI_IMAGE_PATH = "data/ai_image.png"

def run_test(image_path: str):
    """Helper function to run the test and print results."""
    print(f"--- Analyzing Image: {image_path} ---")
    if not os.path.exists(image_path):
        print(f"ERROR: Test image not found at '{image_path}'. Please add it to the 'data' folder.")
        return
    
    result = classify_image_authenticity(image_path)
    print(json.dumps(result, indent=4))
    print("-" * 30)

# --- Run the tests ---
print("Note: The detector model will be downloaded on the first run.\n")
run_test(REAL_IMAGE1_PATH)
run_test(REAL_IMAGE2_PATH)
run_test(AI_IMAGE_PATH)

