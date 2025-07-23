# src/text/claim_extractor.py (Groq version using LLaMA3)

import os
import requests
from src.utils.config import GROQ_API_KEY, CLAIM_EXTRACTION_MODEL

def extract_atomic_claims(text: str) -> list[str]:
    """
    Extracts atomic factual claims using Groq LLaMA3 or Mixtral LLMs.

    Args:
        text: User input text potentially containing multiple claims.

    Returns:
        A list of atomic factual claims as strings.
    """
    system_prompt = (
        "You are an expert fact-checking assistant. Your task is to extract all clear, "
        "concise, and atomic factual claims from the provided text. A factual claim is a "
        "statement that can be proven true or false. Ignore opinions, questions, or vague commentary. "
        "IMPORTANT: Your response must contain ONLY the factual claims, each on a new line. "
        "Do not include any introductory phrases, numbering, or bullet points."
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
            {"role": "user", "content": f"Text to analyze:\n---\n{text}\n---"}
        ],
        "temperature": 0.2
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        content = result["choices"][0]["message"]["content"]

        # Parse by lines
        claims = [line.strip() for line in content.split("\n") if line.strip()]
        return claims

    except Exception as e:
        print(f"[Groq ClaimExtractor] Error: {e}")
        return []
