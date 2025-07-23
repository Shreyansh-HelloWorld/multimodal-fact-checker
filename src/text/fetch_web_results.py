# src/text/fetch_web_results.py
from serpapi import GoogleSearch
from src.utils.config import SERPAPI_API_KEY

def get_evidence_snippets(queries: list[str], num_results_per_query: int = 3) -> list[str]:
    """
    Fetches evidence snippets from the web using SerpAPI for a list of queries.

    Args:
        queries: A list of search query strings.
        num_results_per_query: The number of search results to process for each query.

    Returns:
        A list of unique evidence snippets found from the web search.
    """
    if not SERPAPI_API_KEY:
        print("SERPAPI_API_KEY not found in environment variables.")
        return []

    all_snippets = []
    for query in queries:
        params = {
            "engine": "google",
            "q": query,
            "api_key": SERPAPI_API_KEY,
            "num": num_results_per_query # How many results to fetch
        }
        
        try:
            search = GoogleSearch(params)
            results = search.get_dict()
            
            # Extract snippets from the organic search results
            organic_results = results.get("organic_results", [])
            for result in organic_results:
                snippet = result.get("snippet")
                if snippet:
                    all_snippets.append(snippet)
                    
        except Exception as e:
            print(f"[SerpAPI] An error occurred for query '{query}': {e}")
            continue # Move to the next query if one fails

    # Return a list of unique snippets to avoid redundancy
    return list(dict.fromkeys(all_snippets))