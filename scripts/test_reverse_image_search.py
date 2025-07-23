# scripts/test_reverse_image_search.py
import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.vision.reverse_image_search import find_image_source

TEST_IMAGE_PATH = "data/mona_lisa.jpg"

print(f"--- Performing reverse image search for: {TEST_IMAGE_PATH} ---\n")

if not os.path.exists(TEST_IMAGE_PATH):
    print(f"ERROR: Test image not found at '{TEST_IMAGE_PATH}'.")
else:
    results = find_image_source(TEST_IMAGE_PATH)
    
    # Pretty-print the JSON results
    print(json.dumps(results, indent=4))