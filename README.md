# 🔎 Multimodal Fact-Checker Engine

A sophisticated, AI-powered tool designed to verify the authenticity of information across multiple formats, including text and images. This project leverages a state-of-the-art hybrid architecture to provide nuanced and reliable fact-checking for real-world scenarios.

**[➡️ Live Demo Link Here]** *(You will get this link after deploying to Streamlit Community Cloud)*

---

## Key Features

* **Multimodal Input:** Analyze claims from both plain text and images.
* **Text Analysis Pipeline:**
    * **Claim Extraction:** Automatically identifies and separates individual, verifiable claims from a block of text.
    * **Evidence-Based Verification:** Searches the web for real-time evidence to support or refute each claim.
    * **Dual-Engine Verification:** Uses a combination of a fine-tuned NLI model (DeBERTa) and an LLM (LLaMA-3 via Groq) for robust analysis.
* **Image Analysis Pipeline:**
    * **Image Captioning:** Generates a textual description of the image's content using the BLIP model.
    * **Optical Character Recognition (OCR):** Extracts and analyzes any text present within an image using EasyOCR.
    * **Manipulation Detection:** Classifies images as "Real," "Fake," or "Uncertain" using a Vision Transformer model.
    * **Reverse Image Search:** Scours the internet to find the image's online history, context, and origin.
* **Advanced AI Reasoning:**
    * Employs a final **"Signals & Synthesis"** architecture. This hybrid model uses deterministic Python code to find critical "signals" (like contradictions or evidence of a hoax) and feeds them to a powerful LLM to synthesize a final, nuanced, multi-axis verdict.

## Architecture Overview

The project's core is the **"Signals & Synthesis"** reasoning engine. This advanced, hybrid architecture was developed to overcome the limitations of purely AI-based analysis.

1.  **Evidence Gathering:** The system first runs a suite of specialized modules to gather all possible evidence (OCR, Reverse Image Search, Pixel Authenticity, etc.).
2.  **Programmatic Signal Extraction:** Crucially, it then uses reliable, deterministic Python code to scan this evidence for high-priority signals (e.g., keywords like "hoax," "photoshop," or explicit refutations like "didn't die").
3.  **AI-Powered Synthesis:** Finally, these reliable signals are passed, along with the raw evidence, to an LLM. The AI's job is not to find the truth, but to synthesize the pre-processed signals and evidence into a high-quality, human-readable explanation and a structured verdict.

This approach combines the reliability of code with the nuanced language skills of an AI, creating a system that is both intelligent and robust.

## Tech Stack

* **Backend:** Python 3.11
* **Frontend:** Streamlit
* **AI Models & Libraries:**
    * **LLM Provider:** Groq (LLaMA-3 8B)
    * **Transformers:** Hugging Face
    * **Image Captioning:** Salesforce BLIP
    * **Manipulation Detection:** Vision Transformer (ViT)
    * **OCR:** EasyOCR
    * **NLI (Text):** DeBERTa
* **Core Tools:** Pillow, OpenCV, Requests
* **Web Search:** SerpApi, ImgBB

## Setup and Installation

**1. Clone the repository:**
```bash
git clone [https://github.com/](https://github.com/)[YOUR GITHUB USERNAME]/multimodal-fact-checker.git
cd multimodal-fact-checker
```

**2. Create and activate the virtual environment:**
*This project requires Python 3.11.*
```bash
python3.11 -m venv venv
source venv/bin/activate
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. Set up API Keys:**
Create a file named `.env` in the root of the project folder and add your API keys:
```
GROQ_API_KEY="your_groq_api_key_here"
SERPAPI_API_KEY="your_serpapi_api_key_here"
IMGBB_API_KEY="your_imgbb_api_key_here"
```

## How to Run

Launch the Streamlit application using the following command from the project's root directory:

```bash
python -m streamlit run app/app.py
```
The application will open in your web browser.