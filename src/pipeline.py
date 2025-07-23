# src/pipeline.py


# --- Imports for Text Pipeline ---
from src.text.claim_extractor import extract_atomic_claims
from src.text.query_generator import generate_search_queries
from src.text.fetch_web_results import get_evidence_snippets
from src.text.ml_verifier import classify_evidence_stance
from src.text.llm_verifier import verify_claim_with_llm
from src.reasoning_engine import synthesize_image_evidence

# --- Imports for Image Pipeline ---
from src.vision.preprocessing import clean_ocr_text
from src.vision.captioning import generate_image_caption
from src.vision.ocr import extract_text_from_image
from src.vision.reverse_image_search import find_image_source
from src.vision.manipulation_detector import classify_image_authenticity

def calculate_credibility_score(stance_results: list[dict]) -> float:
    """
    Calculates a simple credibility score based on the NLI results.
    Score = (#Supports - #Refutes) / #Total
    """
    supports = sum(1 for r in stance_results if r['stance'] == 'SUPPORTS')
    refutes = sum(1 for r in stance_results if r['stance'] == 'REFUTES')
    total_relevant = supports + refutes
    
    if total_relevant == 0:
        return 0.0
        
    return (supports - refutes) / total_relevant


def run_text_verification_pipeline(raw_text: str) -> list[dict]:
    """
    Runs the full end-to-end pipeline for verifying claims in a raw text.
    """
    final_results = []
    
    print("Step 1: Extracting claims...")
    atomic_claims = extract_atomic_claims(raw_text)
    if not atomic_claims:
        print("No factual claims were extracted.")
        return []
    print(f"Found {len(atomic_claims)} claims.")

    for claim in atomic_claims:
        print(f"\n--- Verifying Claim: \"{claim}\" ---")
        
        print("Step 2: Generating search queries...")
        queries = generate_search_queries(claim)
        
        print("Step 3: Fetching web evidence...")
        evidence_snippets = get_evidence_snippets(queries)
        
        if not evidence_snippets:
            print("Could not find evidence. Concluding as NOT ENOUGH INFO.")
            result = {
                "claim": claim,
                "verdict": "NOT ENOUGH INFO",
                "explanation": "No relevant evidence was found online to verify this claim.",
                "credibility_score": 0.0,
                "evidence": []
            }
            final_results.append(result)
            continue

        print("Step 4: Classifying evidence stance with ML model...")
        stance_results = classify_evidence_stance(claim, evidence_snippets)
        
        print("Step 5: Generating final verdict with LLM...")
        llm_result = verify_claim_with_llm(claim, evidence_snippets)
        
        final_verdict = {
            "claim": claim,
            "verdict": llm_result["verdict"],
            "explanation": llm_result["explanation"],
            "credibility_score": calculate_credibility_score(stance_results),
            "evidence": stance_results
        }
        final_results.append(final_verdict)
        
    return final_results


# --- NEW: Image Verification Pipeline Function (Correctly Indented) ---

# In src/pipeline.py, replace the existing image pipeline function
def run_image_verification_pipeline(image_path: str, user_query: str) -> dict:
    """
    Runs the full end-to-end pipeline for verifying an image.
    This final version passes all evidence to a central reasoning engine.
    """
    print("\n--- Starting Image Verification Pipeline ---")

    # Step 1: Run all analysis modules
    print("Step 1: Running all image analysis modules...")
    caption = generate_image_caption(image_path)
    ocr_text = extract_text_from_image(image_path)
    ocr_text = clean_ocr_text(ocr_text) # ✅ New line
    authenticity_report = classify_image_authenticity(image_path)
    reverse_search_results = find_image_source(image_path)

    # Assemble a complete report of all raw data
    full_analysis_report = {
        "user_query": user_query,
        "image_analysis": {
            "caption": caption, "ocr_text": ocr_text, "authenticity": authenticity_report
        },
        "online_history": reverse_search_results
    }
    
    # Step 2: Call the central reasoning engine to get the final verdict
    print("Step 2: Synthesizing all data with the Reasoning Engine...")
    final_verdict = synthesize_image_evidence(user_query, full_analysis_report)
    
    # Add the final verdict to our full report
    full_analysis_report["final_verdict"] = final_verdict
    
    print("--- Image Verification Pipeline Complete ---")
    return full_analysis_report