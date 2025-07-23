# scripts/test_image_pipeline.py
import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.pipeline import run_image_verification_pipeline

# We will test the fake Bill Gates image
TEST_IMAGE_PATH = "data/ai_image.png"

# The user's specific question about the image
USER_QUERY = "Is this a real photo of Bill Gates giving away $5,000?"

# Run the full image pipeline
report = run_image_verification_pipeline(TEST_IMAGE_PATH, USER_QUERY)

# Pretty-print the final JSON report
print("\n--- FINAL IMAGE REPORT ---")
print(json.dumps(report, indent=4))