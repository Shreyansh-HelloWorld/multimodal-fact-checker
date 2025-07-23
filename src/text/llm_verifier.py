# src/text/llm_verifier.py
import requests
from src.utils.config import GROQ_API_KEY, CLAIM_EXTRACTION_MODEL

def verify_claim_with_llm(claim: str, evidence_snippets: list[str]) -> dict:
    """
    Uses a Groq-hosted LLaMA 3 model to verify the claim against the provided evidence snippets.

    Args:
        claim: The factual claim to verify.
        evidence_snippets: A list of evidence texts retrieved from the web.

    Returns:
        A dictionary with 'verdict' and 'explanation'.
    """
    system_prompt = (
        "You are a fact-checking assistant. Your job is to verify a factual claim using provided evidence. "
        "Always respond with a clear VERDICT and concise EXPLANATION.\n\n"
        "Respond only in this format:\n"
        "VERDICT: [SUPPORTED/REFUTED/NOT ENOUGH INFO]\n"
        "EXPLANATION: <reasoning>"
    )

    user_prompt = (
        f"Claim:\n{claim}\n\n"
        f"Evidence:\n" +
        "\n\n".join([f"- {e}" for e in evidence_snippets])
    )

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": CLAIM_EXTRACTION_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.3,
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        reply = result["choices"][0]["message"]["content"]

        # Parse VERDICT and EXPLANATION
        verdict_line = next((line for line in reply.splitlines() if line.startswith("VERDICT:")), None)
        explanation_line = next((line for line in reply.splitlines() if line.startswith("EXPLANATION:")), None)

        verdict = verdict_line.replace("VERDICT:", "").strip().upper() if verdict_line else "NOT ENOUGH INFO"
        explanation = explanation_line.replace("EXPLANATION:", "").strip() if explanation_line else reply.strip()

        return {
            "verdict": verdict,
            "explanation": explanation
        }

    except Exception as e:
        print(f"[Groq LLMVerifier] Error: {e}")
        return {
            "verdict": "NOT ENOUGH INFO",
            "explanation": "LLM verification failed due to an API error."
        }
