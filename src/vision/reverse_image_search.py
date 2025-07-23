# src/vision/reverse_image_search.py
import requests
from serpapi import GoogleSearch
from src.utils.config import SERPAPI_API_KEY, IMGBB_API_KEY

def _upload_image_to_imgbb(image_path: str) -> str | None:
    """
    Uploads a local image to imgbb.com to get a public URL.

    Returns:
        The public URL of the image, or None if the upload fails.
    """
    if not IMGBB_API_KEY:
        print("Error: IMGBB_API_KEY not found.")
        return None

    url = "https://api.imgbb.com/1/upload"
    try:
        with open(image_path, "rb") as image_file:
            payload = {
                "key": IMGBB_API_KEY,
            }
            files = {"image": image_file}
            response = requests.post(url, params=payload, files=files)
            response.raise_for_status()
            
            result = response.json()
            if result.get("success"):
                # Return the direct URL of the uploaded image
                return result["data"]["url"]
            else:
                print(f"Error uploading to imgbb: {result.get('error', {}).get('message')}")
                return None
    except Exception as e:
        print(f"An exception occurred during image upload: {e}")
        return None

def find_image_source(image_path: str) -> dict:
    """
    Performs a reverse image search using Google Lens via SerpAPI.
    It first uploads the local image to get a public URL.
    """
    if not SERPAPI_API_KEY:
        return {"error": "SERPAPI_API_KEY not found."}

    # Step 1: Upload the image to get a public URL
    print("Uploading image for temporary URL...")
    public_image_url = _upload_image_to_imgbb(image_path)

    if not public_image_url:
        return {"error": "Failed to upload image to get a public URL."}
    
    print(f"Image URL: {public_image_url}")

    # Step 2: Use the public URL for the Google Lens search
    # We can now use the library wrapper as it's designed for URLs.
    params = {
        "engine": "google_lens",
        "url": public_image_url,
        "api_key": SERPAPI_API_KEY
    }

    try:
        print("Performing reverse image search...")
        search = GoogleSearch(params)
        results = search.get_dict()
        
        visual_matches = results.get("visual_matches", [])
        
        if not visual_matches:
            return {"source_results": "No visual matches found online."}

        sources = [
            {
                "title": match.get("title"),
                "link": match.get("link"),
                "source_icon": match.get("source_icon")
            }
            for match in visual_matches[:10]
        ]
        return {"source_results": sources}

    except Exception as e:
        return {"error": f"An error occurred during reverse image search: {e}"}