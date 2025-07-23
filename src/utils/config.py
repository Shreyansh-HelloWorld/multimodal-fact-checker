# src/utils/config.py
import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")
IMGBB_API_KEY = os.getenv("IMGBB_API_KEY")

# LLM Model Configurations (Groq)
CLAIM_EXTRACTION_MODEL = "llama3-8b-8192"
QUERY_GENERATION_MODEL = "llama3-8b-8192"
LLM_VERIFIER_MODEL = "llama3-8b-8192" # Let's add this for clarity

# Local ML Model Configurations (Hugging Face)
NLI_MODEL = "MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli"