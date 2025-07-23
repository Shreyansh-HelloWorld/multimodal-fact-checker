# scripts/test_ml_verifier.py
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.text.ml_verifier import classify_evidence_stance

claim = "The Eiffel Tower is located in Paris, France."
evidence = [
    "The Eiffel Tower, a wrought-iron lattice tower, is a famous landmark in Paris.", # Should support
    "France's capital city, Paris, is home to the iconic Eiffel Tower.", # Should support
    "The Statue of Liberty is located in New York City.", # Should be neutral
    "Some people claim the Eiffel Tower is actually in Las Vegas.", # Should refute
]

print("This test will download the NLI model (~1.6GB) if you're running it for the first time.\n")
print(f"Claim:\n\"{claim}\"\n")

results = classify_evidence_stance(claim, evidence)

print("ML Verifier Stance Classification:")
for res in results:
    print(f"- Evidence: \"{res['evidence']}\"")
    print(f"  Stance: {res['stance']} (Score: {res['score']})")
    print("-" * 20)