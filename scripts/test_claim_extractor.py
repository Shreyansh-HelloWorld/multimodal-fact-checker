import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.text.claim_extractor import extract_atomic_claims

text = (
    "The US economy grew by 2.3% last quarter. "
    "I think this shows strong recovery, although some people disagree. "
    "Also, there was a volcanic eruption in Iceland recently."
)

claims = extract_atomic_claims(text)
print("Extracted Claims:")
for i, claim in enumerate(claims, 1):
    print(f"{i}. {claim}")
