# src/utils/config.py
import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")
IMGBB_API_KEY = os.getenv("IMGBB_API_KEY")

# LLM Model Configurations (Groq) - UPDATED TO NEW MODEL NAMES
CLAIM_EXTRACTION_MODEL = "llama-3.1-8b-instant"  # was "llama3-8b-8192"
QUERY_GENERATION_MODEL = "llama-3.1-8b-instant"  # was "llama3-8b-8192"
LLM_VERIFIER_MODEL = "llama-3.1-8b-instant"      # was "llama3-8b-8192"

# Optional: If you want to use the more powerful 70B model for verification
# LLM_VERIFIER_MODEL = "llama-3.3-70b-versatile"  # More powerful but slower

# Local ML Model Configurations (Hugging Face)
NLI_MODEL = "MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli"