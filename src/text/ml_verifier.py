# src/text/ml_verifier.py
from transformers import pipeline
from src.utils.config import NLI_MODEL

# Initialize the NLI pipeline from Hugging Face.
try:
    # Using device=0 will try to use the GPU (M-series Mac, CUDA) if available.
    # It will fall back to CPU if no compatible GPU is found.
    nli_pipeline = pipeline("text-classification", model=NLI_MODEL)
    print(f"NLI model '{NLI_MODEL}' loaded successfully on device: {nli_pipeline.device}")
except Exception as e:
    print(f"Failed to load NLI model. Please check model name and internet connection. Error: {e}")
    nli_pipeline = None

def classify_evidence_stance(claim: str, evidence_snippets: list[str]) -> list[dict]:
    """
    Classifies the stance of each evidence snippet relative to the claim using an NLI model.
    """
    if not nli_pipeline:
        print("NLI pipeline not available. Returning empty results.")
        return []

    results = []
    for snippet in evidence_snippets:
        # Pass the text pair to the pipeline
        raw_result = nli_pipeline({"text": snippet, "text_pair": claim})
        
        # The labels from this model are 'entailment', 'contradiction', 'neutral'.
        stance_map = {
            "entailment": "SUPPORTS",
            "contradiction": "REFUTES",
            "neutral": "NEUTRAL"
        }
        
        # --- FIX IS HERE ---
        # Access 'label' and 'score' directly from the result dictionary.
        stance = stance_map.get(raw_result['label'], "NEUTRAL")
        score = round(raw_result['score'], 2)

        results.append({
            "evidence": snippet,
            "stance": stance,
            "score": score
        })
        
    return results