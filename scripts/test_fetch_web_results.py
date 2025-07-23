# scripts/test_fetch_web_results.py
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.text.query_generator import generate_search_queries
from src.text.fetch_web_results import get_evidence_snippets

# 1. Start with a sample claim
claim = "The Great Wall of China is visible from space with the naked eye."

print(f"Claim: \"{claim}\"\n")

# 2. Generate queries for this claim
queries = generate_search_queries(claim)
print("Generated Queries:")
for q in queries:
    print(f"- {q}")
print("\n" + "="*30 + "\n")

# 3. Fetch evidence snippets using these queries
print("Fetching evidence from the web...")
evidence = get_evidence_snippets(queries)

if evidence:
    print("\nSuccessfully retrieved evidence snippets:")
    for i, snippet in enumerate(evidence, 1):
        print(f"{i}. {snippet}")
else:
    print("\nCould not retrieve any evidence. Please check your SerpAPI key and network connection.")