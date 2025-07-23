# 🔎 Multimodal Fact-Checker Engine

An advanced, AI-powered tool designed to verify the authenticity of information across multiple formats, including text and images. This project leverages a state-of-the-art hybrid architecture to provide nuanced and reliable fact-checking for complex, real-world scenarios.

**[➡️Fact Checker Engine Link](https://multimodal-fact-checker-wpd9txbxu9rdqrmxalo6bc.streamlit.app/)]**

---

## Key Skills Demonstrated

This project showcases a comprehensive skill set relevant for Data Scientist, Data Analyst, and Machine Learning Engineer roles.

* **Data Science & Machine Learning**
    * **End-to-End Project Lifecycle:** From problem definition and data gathering (web scraping, APIs) to model integration and deployment.
    * **Model Integration:** Applied multiple pre-trained models for various tasks, including classification, text generation, and object detection.
    * **Hybrid AI Systems:** Designed and built a sophisticated reasoning engine that combines deterministic code (signal extraction) with LLM-based synthesis for robust, reliable outputs.

* **Natural Language Processing (NLP)**
    * **Claim Extraction & Stance Detection:** Deployed models to deconstruct text and determine the stance of evidence.
    * **Text Preprocessing & Cleaning:** Implemented logic to clean and standardize text from various sources (e.g., OCR).
    * **Prompt Engineering:** Developed a multi-step "chain-of-thought" and "debate" style reasoning framework to guide LLM behavior for complex analytical tasks.

* **Computer Vision (CV)**
    * **Image Captioning:** Used the BLIP model to generate contextual descriptions of images.
    * **Optical Character Recognition (OCR):** Deployed EasyOCR to extract textual information from images.
    * **Manipulation Detection:** Applied a Vision Transformer (ViT) to classify images as authentic or AI-generated.
    * **Reverse Image Search:** Integrated with external APIs (SerpApi, ImgBB) to gather contextual data and online history for images.

* **MLOps & Tooling**
    * **Application Development:** Built and deployed a fully interactive web application using **Streamlit**.
    * **Environment Management:** Managed a complex environment with specific Python versions (`venv`) and dependencies (`requirements.txt`).
    * **API Integration:** Worked with multiple third-party APIs (Groq, SerpApi, ImgBB) and handled data securely.
    * **Version Control & Deployment:** Prepared the project for deployment with `git` and `.gitignore`, with a clear path to hosting on Streamlit Community Cloud.

## Architecture: The "Signals & Synthesis" Engine

The core of this project is a hybrid reasoning engine designed to be more reliable than a purely AI-based approach.

1.  **Evidence Gathering:** The system runs a suite of specialized modules (OCR, Reverse Image Search, Pixel Authenticity, etc.) to gather all possible evidence.
2.  **Programmatic Signal Extraction:** Crucially, it then uses reliable Python code to scan this evidence for high-priority, deterministic "signals" (e.g., keywords like "hoax," "photoshop," or explicit refutations like "didn't die").
3.  **AI-Powered Synthesis:** Finally, these reliable signals are passed, along with the raw evidence, to an LLM. The AI's job is not to *find* the contradiction, but to *synthesize* and *explain* the conclusion that the signals already point to.

This approach combines the reliability of code with the nuanced language skills of an AI, creating a system that is both intelligent and robust.

## Tech Stack

* **Backend:** Python 3.11
* **Application Framework:** Streamlit
* **AI Models & Libraries:**
    * **LLM Provider:** Groq (LLaMA-3 8B)
    * **Transformers:** Hugging Face
    * **Image Captioning:** Salesforce BLIP
    * **Manipulation Detection:** Vision Transformer (ViT)
    * **OCR:** EasyOCR
    * **NLI (Text):** DeBERTa
* **Core Tools:** Pillow, OpenCV, Requests, NumPy
* **Web APIs:** SerpApi, ImgBB

## Local Setup and Installation

**1. Clone the repository:**
```bash
git clone [https://github.com/](https://github.com/)[YOUR GITHUB USERNAME]/multimodal-fact-checker.git
cd multimodal-fact-checker
```

**2. Create and activate the virtual environment:**
*This project requires Python 3.11.*
```bash
python3.11 -m venv venv
source ven /bin/activate
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
