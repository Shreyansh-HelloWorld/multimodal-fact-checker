# src/reasoning_engine.py
import requests
import json
from src.utils.config import GROQ_API_KEY, LLM_VERIFIER_MODEL

def _call_groq_api(system_prompt: str, user_prompt: str, is_json_output: bool = False) -> str:
    """Helper function to make a call to the Groq API."""
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {"model": LLM_VERIFIER_MODEL, "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}], "temperature": 0.1, "top_p": 0.1}
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=45)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"[ReasoningEngine] API Error: {e}")
        # Return a structured error to prevent crashes
        error_json = {
            "event_truthfulness": "Uncertain",
            "image_context": "Uncertain",
            "final_verdict": "ERROR",
            "explanation": "The AI model failed to respond. Please try again."
        }
        return json.dumps(error_json)

def synthesize_image_evidence(user_query: str, analysis_report: dict) -> dict:
    """
    Uses a definitive hybrid "Signals & Synthesis" process to get a final verdict.
    """
    # --- Extract all evidence ---
    caption = analysis_report.get("image_analysis", {}).get("caption", "N/A")
    ocr_text = analysis_report.get("image_analysis", {}).get("ocr_text", "None")
    authenticity = analysis_report.get("image_analysis", {}).get("authenticity", {})
    sources = analysis_report.get("online_history", {}).get("source_results", [])
    
    # --- Step 1: PROGRAMMATIC SIGNAL EXTRACTION (Deterministic Code) ---
    programmatic_signals = []
    online_history_summary = "No significant online history found."
    if isinstance(sources, list) and len(sources) > 0:
        top_titles = [r.get("title", "").lower() for r in sources]
        online_history_summary = "The image appears on pages with these titles: " + "; ".join(top_titles)
        
        hoax_keywords = ["didn't die", "not dead", "hoax", "awareness campaign", "fake death"]
        if any(keyword in title for keyword in hoax_keywords for title in top_titles):
            programmatic_signals.append("CRITICAL: Online history contains strong evidence of a hoax or refutation.")
        
        manipulation_keywords = ["photoshop", "meme", "spam photo", "parody", "satire"]
        if any(keyword in title for keyword in manipulation_keywords for title in top_titles):
            programmatic_signals.append("NOTE: Online history suggests the image is a meme or has been photoshopped.")

    # --- Step 2: AI-POWERED SYNTHESIS (LLM Call) ---
    system_prompt = "You are a world-class multimodal fact-checking analyst. Your task is to synthesize a structured case file into a final verdict and a concise explanation. Your response MUST be a single, valid JSON object and nothing else."
    user_prompt = f"""
    **CASE FILE:**
    - **User's Question:** "{user_query}"
    - **Programmatic Signals (Most Important Evidence):** {programmatic_signals if programmatic_signals else "None"}
    - **Image Content (Caption):** "{caption}"
    - **Text in Image (OCR):** "{ocr_text}"
    - **Pixel Authenticity Analysis:** Classified as '{authenticity.get('verdict')}' with {authenticity.get('confidence')} confidence.
    - **Online History (Reverse Image Search):** {online_history_summary}

    **YOUR TASK:**
    Based on all the evidence, especially the Programmatic Signals, provide a final verdict in the following JSON format.
    {{
      "event_truthfulness": "...",
      "image_context": "...",
      "final_verdict": "...",
      "explanation": "..."
    }}
    """
    
    try:
        verdict_json_string = _call_groq_api(system_prompt, user_prompt, is_json_output=True)
        json_start = verdict_json_string.find('{')
        json_end = verdict_json_string.rfind('}') + 1
        if json_start != -1 and json_end != -1:
            clean_json_string = verdict_json_string[json_start:json_end]
            return json.loads(clean_json_string)
        else:
            raise json.JSONDecodeError("No JSON object found", verdict_json_string, 0)
    except (json.JSONDecodeError, KeyError):
        return {"final_verdict": "ERROR", "explanation": "Failed to parse the final verdict from the AI."}