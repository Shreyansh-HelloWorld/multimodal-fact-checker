# src/reasoning_engine.py (Definitive Final Version)
import requests
import json
import re
from src.utils.config import GROQ_API_KEY, LLM_VERIFIER_MODEL

def _call_groq_api(system_prompt: str, user_prompt: str) -> str:
    """Helper function to make a call to the Groq API."""
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {"model": LLM_VERIFIER_MODEL, "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}], "temperature": 0.0, "top_p": 0.1}
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"[ReasoningEngine] API Error: {e}")
        return "ERROR: The AI model failed to respond."

def _parse_final_report(report_text: str) -> dict:
    """
    Parses the structured text report from the LLM into a dictionary using robust regex.
    """
    verdict_data = {
        "explanation": report_text, # Default to the full text
        "event_truthfulness": "Uncertain",
        "image_context": "Uncertain",
        "final_verdict": "UNCERTAIN"
    }
    try:
        # Use regex to find the verdicts, ignoring whitespace and case
        et_match = re.search(r"EVENT TRUTHFULNESS:\s*(.*)", report_text, re.IGNORECASE)
        if et_match: verdict_data["event_truthfulness"] = et_match.group(1).strip()

        ic_match = re.search(r"IMAGE CONTEXT:\s*(.*)", report_text, re.IGNORECASE)
        if ic_match: verdict_data["image_context"] = ic_match.group(1).strip()

        ov_match = re.search(r"OVERALL CONCLUSION:\s*(.*)", report_text, re.IGNORECASE)
        if ov_match: verdict_data["final_verdict"] = ov_match.group(1).strip().upper()
        
        # Clean up the explanation
        explanation = re.sub(r"EVENT TRUTHFULNESS:.*", "", report_text, flags=re.IGNORECASE)
        explanation = re.sub(r"IMAGE CONTEXT:.*", "", explanation, flags=re.IGNORECASE)
        explanation = re.sub(r"OVERALL CONCLUSION:.*", "", explanation, flags=re.IGNORECASE)
        verdict_data["explanation"] = explanation.strip()

        return verdict_data
    except Exception as e:
        print(f"Error parsing final response: {e}")
        return {"final_verdict": "ERROR", "explanation": "Failed to parse the AI's report."}

def synthesize_image_evidence(user_query: str, analysis_report: dict) -> dict:
    """
    Uses a definitive "Deterministic-Guided Synthesis" architecture for maximum reliability.
    """
    # --- Extract all evidence ---
    caption = analysis_report.get("image_analysis", {}).get("caption", "N/A")
    ocr_text = analysis_report.get("image_analysis", {}).get("ocr_text", "None")
    authenticity = analysis_report.get("image_analysis", {}).get("authenticity", {})
    sources = analysis_report.get("online_history", {}).get("source_results", [])
    thematic_search = analysis_report.get("thematic_search", [])

    online_history_summary = "No significant online history found."
    if isinstance(sources, list) and len(sources) > 0:
        online_history_summary = "\n- ".join([f"'{r.get('title', '')}'" for r in sources])

    thematic_search_summary = "No thematic search results found for the text in the image."
    if isinstance(thematic_search, list) and len(thematic_search) > 0:
        thematic_search_summary = "\n- ".join(thematic_search)
    
    # --- STAGE 1: INTENT RECOGNITION (DETERMINISTIC) ---
    intent = "NEWS_CONTENT"
    authenticity_keywords = ["photo", "image", "real", "ai", "fake", "photoshop", "generated", "doctored", "is this photo real"]
    if any(keyword in user_query.lower() for keyword in authenticity_keywords):
        intent = "IMAGE_AUTHENTICITY"
    
    # --- STAGE 2: GUIDED REASONING (SINGLE, POWERFUL PROMPT) ---
    system_prompt = "You are a world-class multimodal fact-checking analyst. You must follow all instructions and the output format precisely."
    
    user_prompt = f"""
    **CASE FILE:**
    - **User's Question:** "{user_query}"
    - **Detected User Intent:** {intent}
    - **Online History (from Reverse Image Search):**{online_history_summary}
    - **Thematic Web Search (from OCR text):**{thematic_search_summary}
    - **Pixel Authenticity Analysis:** Classified as '{authenticity.get('verdict')}' with {authenticity.get('confidence')} confidence.
    - **Text in Image (OCR):** "{ocr_text}"

    **CRITICAL THINKING FRAMEWORK:**
    1.  **State Your Goal:** Begin by stating your primary goal based on the Detected User Intent.
    2.  **Weigh the Evidence:** Analyze the Online History and Thematic Search. Is there a consensus? Are there refutations? State how this web evidence relates to your goal.
    3.  **Synthesize:** Combine your web evidence analysis with the Pixel Authenticity analysis to form a final, holistic conclusion that directly answers the User's Question.
    4.  **Report:** Write out your final report below, following the format exactly.

    **FINAL REPORT FORMAT (DO NOT add any other text):**
    EVENT TRUTHFULNESS: [One of: Event is Real, Event is Fake, Uncertain, N/A]
    IMAGE CONTEXT: [One of: Accurate Context, Misleading Context, Fabricated Image, Contextual Graphic, N/A]
    
    [Your full, step-by-step reasoning and explanation for your conclusion.]
    
    OVERALL CONCLUSION: [One of: SUPPORTED, REFUTED, UNCERTAIN, MISLEADING]
    """
    
    response_text = _call_groq_api(system_prompt, user_prompt)
    
    if "ERROR:" in response_text:
        return {"final_verdict": "ERROR", "explanation": response_text}
        
    return _parse_final_report(response_text)