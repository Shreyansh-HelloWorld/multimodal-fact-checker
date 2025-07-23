# scripts/test_llm_verifier.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.text.llm_verifier import verify_claim_with_llm

claim = "The US economy grew by 2.3% last quarter."
evidence = [
    "According to the Bureau of Economic Analysis, the US GDP increased by 2.3% in Q2 2023.",
    "News reports confirm the growth, citing strong consumer spending.",
]

result = verify_claim_with_llm(claim, evidence)

print("Verdict:", result["verdict"])
print("Explanation:", result["explanation"])
