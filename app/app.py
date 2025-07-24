# app/app.py (Definitive Final Version)
import streamlit as st
import sys, os, tempfile
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.pipeline import run_text_verification_pipeline, run_image_verification_pipeline

st.set_page_config(page_title="Fact-Checker AI", page_icon="🔎", layout="wide")
st.title("🔎 Multimodal Fact-Checker Engine")
st.write("This tool leverages a sophisticated pipeline of AI models to verify factual claims. Select a verification mode below to begin.")
text_tab, image_tab = st.tabs(["📝 Text-based Fact-Checker", "🖼️ Image-based Fact-Checker"])

# --- Text Verification Tab ---
with text_tab:
    st.header("Verify a Text Claim")
    with st.form("text_form"):
        text_input = st.text_area("Enter the text you want to verify:", height=150)
        submitted_text = st.form_submit_button("Verify Text")
    if submitted_text:
        if text_input:
            with st.spinner("Analyzing text..."):
                text_report = run_text_verification_pipeline(text_input)
            st.subheader("Text Verification Report")
            if not text_report:
                st.warning("No factual claims were found.")
            else:
                for result in text_report:
                    st.markdown(f"#### Claim: \"{result.get('claim', 'N/A')}\"")
                    verdict = result.get("verdict", "UNCERTAIN")
                    if verdict == "REFUTED": st.error(f"**Verdict: {verdict}**")
                    elif verdict == "SUPPORTED": st.success(f"**Verdict: {verdict}**")
                    else: st.warning(f"**Verdict: {verdict}**")
                    st.info(f"**Explanation:** {result.get('explanation')}")
                    st.divider()
        else:
            st.error("Please enter some text to verify.")

# --- Image Verification Tab (Polished UI) ---
with image_tab:
    st.header("Verify an Image")
    with st.form("image_form"):
        image_file = st.file_uploader("Upload an image", type=['png', 'jpg', 'jpeg'])
        user_query = st.text_input("What specific claim do you want to check?", placeholder="e.g., Is this photo real?")
        submitted_image = st.form_submit_button("Verify Image")
    
    if submitted_image:
        if image_file and user_query:
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(image_file.name)[1]) as tmp_file:
                tmp_file.write(image_file.getbuffer())
                image_path = tmp_file.name
            with st.spinner("Performing deep analysis... This is the final version."):
                image_report = run_image_verification_pipeline(image_path, user_query)
            os.unlink(image_path)

            st.subheader("Image Verification Report")
            final_verdict_data = image_report.get("final_verdict", {})
            st.markdown(f"#### Your Question: \"{image_report.get('user_query')}\"")

            verdict_map = {"SUPPORTED": st.success, "REFUTED": st.error, "MISLEADING": st.error, "UNCERTAIN": st.warning, "ERROR": st.error}
            overall_verdict = final_verdict_data.get("final_verdict", "UNCERTAIN").upper()
            display_function = verdict_map.get(overall_verdict, st.warning)
            display_function(f"**Overall Conclusion: {overall_verdict}**")

            # --- ✅ Polished side-by-side display ---
            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="Event Truthfulness", value=final_verdict_data.get("event_truthfulness", "N/A"))
            with col2:
                st.metric(label="Image Context", value=final_verdict_data.get("image_context", "N/A"))
            
            st.info(f"**Analyst's Explanation:**\n\n{final_verdict_data.get('explanation')}")
            st.divider()

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### Raw Image Analysis")
                analysis = image_report.get("image_analysis", {})
                auth = analysis.get('authenticity', {})
                st.write(f"**Caption:** *{analysis.get('caption')}*")
                st.write(f"**Text in image (OCR):** *\"{analysis.get('ocr_text') if analysis.get('ocr_text') else 'None'}\"*")
                st.write(f"**Authenticity Check:** {auth.get('verdict')} (Confidence: {auth.get('confidence')})")
            with col2:
                st.markdown("#### Raw Online History")
                history = image_report.get("online_history", {})
                sources = history.get("source_results", [])
                if isinstance(sources, list) and len(sources) > 0:
                    for source in sources[:5]:
                        title = source.get("title")
                        link = source.get("link")
                        if title and link: st.markdown(f"- [{title}]({link})")
                        elif title: st.write(f"- {title}")
                else:
                    st.write("No online history found.")
        else:
            st.error("Please upload an image and provide a question to verify.")