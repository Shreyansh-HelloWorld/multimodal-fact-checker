# src/vision/manipulation_detector.py
from transformers import pipeline
from PIL import Image

MODEL_NAME = "umm-maybe/AI-image-detector"

try:
    detector = pipeline("image-classification", model=MODEL_NAME)
    print(f"Manipulation detector model '{MODEL_NAME}' loaded successfully.")
except Exception as e:
    print(f"Failed to load manipulation detector model. Error: {e}")
    detector = None

def classify_image_authenticity(image_path: str) -> dict:
    """
    Classifies an image as Real, Fake, or Uncertain based on a confidence threshold.
    """
    if not detector:
        return {"error": "Manipulation detector is not available."}

    try:
        image = Image.open(image_path)
        results = detector(image)
        
        scores = {item['label']: item['score'] for item in results}
        
        # Determine the verdict based on the label with the highest score
        best_label = max(scores, key=scores.get)
        confidence = round(scores[best_label], 2)
        
        CONFIDENCE_THRESHOLD = 0.75 

        if confidence < CONFIDENCE_THRESHOLD:
            verdict = "Uncertain"
        else:
            # --- THE FIX IS HERE ---
            # Use the model's actual labels: 'human' and 'artificial'
            verdict = "Real" if best_label == 'human' else "Fake"
        
        return {
            "verdict": verdict,
            "confidence": confidence,
            # --- THE FIX IS HERE ---
            # Get the scores using the correct labels
            "raw_score_real": round(scores.get('human', 0), 2),
            "raw_score_fake": round(scores.get('artificial', 0), 2)
        }

    except Exception as e:
        return {"error": f"An error occurred during image authenticity classification: {e}"}