"""
app.py
Streamlit frontend for Sentiment-Aligned Text Generator.
Run: streamlit run app.py
"""

import streamlit as st
from model_utils import SentimentGenerator
import torch

st.set_page_config(page_title="Sentiment-Aligned AI Text Generator")

st.title("🧠 Sentiment-Aligned AI Text Generator")
st.write("Enter a prompt. The system detects its sentiment and generates a paragraph aligned with that tone.")

# Sidebar
st.sidebar.header("⚙️ Settings")
gen_model = st.sidebar.selectbox("Text model", ["gpt2", "distilgpt2"], index=0)
sent_model = st.sidebar.selectbox("Sentiment model", ["distilbert-base-uncased-finetuned-sst-2-english"])
use_gpu = st.sidebar.checkbox("Use GPU (if available)", value=False)
device = 0 if (use_gpu and torch.cuda.is_available()) else -1

max_tokens = st.sidebar.slider("Length (tokens)", 50, 300, 120, 10)
temperature = st.sidebar.slider("Creativity (temperature)", 0.2, 1.5, 0.9, 0.1)
top_p = st.sidebar.slider("Top-p", 0.1, 1.0, 0.95, 0.05)
top_k = st.sidebar.slider("Top-k", 10, 200, 50, 10)

@st.cache_resource
def load_models(gen_model, sent_model, device):
    return SentimentGenerator(sentiment_model_name=sent_model,
                              gen_model_name=gen_model,
                              device=device)

with st.spinner("Loading models..."):
    sg = load_models(gen_model, sent_model, device)

prompt = st.text_area("Enter your prompt:", height=150,
                      placeholder="e.g., 'The importance of small-town businesses in local economies'")
manual_sent = st.selectbox("Manual sentiment override (optional)",
                           ["(auto detect)", "positive", "negative", "neutral"])

if st.button("Generate"):
    if not prompt.strip():
        st.error("Please enter a prompt first.")
    else:
        detected = sg.predict_sentiment(prompt)
        sentiment_used = None if manual_sent == "(auto detect)" else manual_sent

        st.info(f"Detected sentiment: **{detected['label']}** (confidence {detected['score']:.2f})")
        if sentiment_used:
            st.warning(f"Manual override: {sentiment_used}")

        with st.spinner("Generating text..."):
            result = sg.generate_text(prompt,
                                      sentiment=sentiment_used or detected["label"],
                                      max_new_tokens=max_tokens,
                                      top_k=top_k,
                                      top_p=top_p,
                                      temperature=temperature)
        st.subheader("Generated Text:")
        st.write(result)
