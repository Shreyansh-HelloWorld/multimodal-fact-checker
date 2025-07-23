# scripts/test_pipeline.py
import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.pipeline import run_text_verification_pipeline

# A more complex input text with multiple claims
input_text = """
The Eiffel Tower is located in Berlin. This is a well-known fact.
Furthermore, the Great Wall of China is famously visible from space with the naked eye. I read it in a book.
"""

print(f"--- Running Full Pipeline for Input Text ---\n")
final_report = run_text_verification_pipeline(input_text)
print("\n--- End-to-End Verification Complete ---")

# Pretty-print the final JSON report
print("\nFinal Report:")
print(json.dumps(final_report, indent=4))