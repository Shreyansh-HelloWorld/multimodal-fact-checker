# src/text/query_generator.py
import requests
from src.utils.config import GROQ_API_KEY, QUERY_GENERATION_MODEL

def generate_search_queries(claim: str) -> list[str]:
    """
    Generates a list of search engine queries based on a single factual claim using the Groq API.

    Args:
        claim: The atomic factual claim.

    Returns:
        A list of search query strings, including the original claim.
    """
    system_prompt = (
        "You are a search query generation expert. Given a factual claim, your task is to "
        "generate 3 diverse, search-engine-optimized queries to find evidence. The queries should be "
        "varied: one as a question, one focusing on keywords, and one as a direct rephrasing. "
        "Return only the list of queries, one per line, without any extra text or numbering."
    )

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": QUERY_GENERATION_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Factual claim:\n---\n{claim}\n---"}
        ],
        "temperature": 0.5,
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()

        generated_queries = result["choices"][0]["message"]["content"].strip()
        queries = [line.strip() for line in generated_queries.split('\n') if line.strip()]

        all_queries = [claim] + queries
        unique_queries = list(dict.fromkeys(all_queries))
        return unique_queries

    except Exception as e:
        print(f"[Groq QueryGenerator] Error: {e}")
        return [claim]
