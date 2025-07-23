# src/vision/captioning.py
from transformers import pipeline
from PIL import Image

MODEL_NAME = "Salesforce/blip-image-captioning-base"

try:
    # Initialize the image captioning pipeline. It will download the model on first run.
    captioner = pipeline("image-to-text", model=MODEL_NAME)
    print(f"Image captioning model '{MODEL_NAME}' loaded successfully.")
except Exception as e:
    print(f"Failed to load captioning model. Error: {e}")
    captioner = None

def generate_image_caption(image_path: str) -> str:
    """
    Generates a textual caption for a given image.

    Args:
        image_path: The file path to the image.

    Returns:
        A string containing the generated caption, or an error message.
    """
    if not captioner:
        return "Image captioning model is not available."

    try:
        # Open the image using Pillow to handle various formats
        image = Image.open(image_path).convert("RGB")
        
        # The pipeline returns a list with one dictionary: [{'generated_text': '...'}]
        result = captioner(image)
        caption = result[0].get('generated_text', 'Could not generate caption.')
        return caption
        
    except Exception as e:
        return f"An error occurred during captioning: {e}"