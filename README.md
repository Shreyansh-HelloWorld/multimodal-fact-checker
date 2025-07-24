# 🔎 Multimodal Fact-Checker Engine

An advanced, AI-powered tool designed to verify the authenticity of information across multiple formats, including text and images. This project leverages a state-of-the-art hybrid architecture to provide nuanced and reliable fact-checking for complex, real-world scenarios.

**[➡️ Live Demo](https://multimodal-fact-checker-wpd9txbxu9rdqrmxalo6bc.streamlit.app/)**

---

## Key Skills Demonstrated

This project showcases a comprehensive skill set relevant for Data Scientist, Data Analyst, and Machine Learning Engineer roles.

* **Data Science & Machine Learning**
    * **End-to-End Project Lifecycle:** From problem definition and data gathering (web scraping, APIs) to model integration and deployment of a live application.
    * **Model Integration:** Applied multiple pre-trained models for various tasks, including classification, text generation, and computer vision.
    * **Hybrid AI Systems:** Designed and built a sophisticated **"Hierarchical Reasoning Engine"** that combines deterministic code (for high-confidence signal extraction) with advanced LLM synthesis for robust, reliable outputs.

* **Natural Language Processing (NLP)**
    * **Claim Extraction & Stance Detection:** Deployed models to deconstruct text and determine the stance of evidence.
    * **Prompt Engineering:** Engineered a complex, intent-driven, "chain-of-thought" prompt to guide the LLM's reasoning process for multimodal evidence synthesis.

* **Computer Vision (CV)**
    * **Image Captioning:** Used the BLIP model to generate contextual descriptions of images.
    * **Optical Character Recognition (OCR):** Deployed EasyOCR to extract textual information from images.
    * **Manipulation Detection:** Applied a Vision Transformer (ViT) to classify images as authentic or AI-generated.
    * **Reverse Image Search:** Integrated with external APIs (SerpApi, ImgBB) to gather contextual data and online history.

* **MLOps & Tooling**
    * **Application Development:** Built and deployed a fully interactive web application using **Streamlit** and **Streamlit Community Cloud**.
    * **Environment Management:** Managed a complex environment with specific Python versions (`venv`) and dependencies (`requirements.txt`).
    * **Version Control:** Used **Git** and **GitHub** for version control and continuous deployment.
    * **Secure API Management:** Handled secret API keys securely using `.env` files locally and Streamlit's secrets management in production.

## Final Architecture: The "Hierarchical Reasoning Engine"

The core of the project is a hybrid, hierarchical reasoning engine designed for maximum reliability.

1.  **Deterministic Checks First:** The system first uses reliable Python code to check for undeniable "red flags" in the evidence (e.g., keywords like "hoax" or "photoshop"). If found, it makes an immediate, high-confidence decision.
2.  **Targeted AI Analysis:** If the case is ambiguous, it proceeds to a targeted AI call to determine the "Web Consensus" based on news headlines.
3.  **Final AI Synthesis:** The results of the first two stages are then fed as powerful, pre-processed signals to a final, advanced AI reasoner, which synthesizes all the information into a nuanced, multi-axis verdict and a human-readable explanation.

This architecture is robust because it uses deterministic code for simple cases and saves the most powerful AI reasoning for the truly complex and nuanced scenarios.

## Tech Stack

* **Backend:** Python 3.11
* **Application Framework:** Streamlit
* **AI Models & Libraries:**
    * **LLM Provider:** Groq (**LLaMA-3 70B**)
    * **Transformers:** Hugging Face
    * **Image Captioning:** Salesforce BLIP
    * **Manipulation Detection:** Vision Transformer (ViT)
    * **OCR:** EasyOCR
* **Core Tools:** Pillow, OpenCV, Requests, NumPy
* **Web APIs:** SerpApi, ImgBB

## Local Setup and Installation

**1. Clone the repository:**
```bash
git clone [https://github.com/Shreyansh-HelloWorld/multimodal-fact-checker.git](https://github.com/Shreyansh-HelloWorld/multimodal-fact-checker.git)
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

Launch the Streamlit application using the following command:

```bash
python -m streamlit run app/app.py
```
