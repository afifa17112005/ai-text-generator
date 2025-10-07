# AI Text Generator — Sentiment-Based Essay Creator

## Objective
This project builds an AI-powered system that:
- Analyzes the **sentiment** of an input prompt.
- Generates text (paragraph or essay) aligned with that sentiment.

---

## Features
- Automatic sentiment detection using **Hugging Face transformers**.
- AI-generated paragraphs reflecting **positive**, **negative**, or **neutral** tones.
- Interactive **Streamlit frontend**.
- Optional manual sentiment selection.
- Adjustable text length (easily configurable in the code).

---

## Tech Stack
- **Python 3.9+**
- **Transformers (Hugging Face)**
- **Torch**
- **Streamlit**

---

## Installation & Setup

1️⃣ **Clone or Create Folder**
```bash
cd C:\Users\admin\ai-text-generator
2️⃣ Create Virtual Environment

bash
Copy code
python -m venv venv
.\venv\Scripts\Activate.ps1
3️⃣ Install Dependencies

bash
Copy code
pip install -r requirements.txt
4️⃣ Run the App

bash
Copy code
streamlit run app.py
Your browser will open at:
👉 http://localhost:8501

How It Works
User enters a prompt.

The app uses a sentiment analysis model to detect tone.

Based on sentiment, the text generation model (GPT-2) produces aligned content.

The result is displayed with detected sentiment and generated text.

Challenges & Learnings
Managing different model sizes and performance tradeoffs.

Handling bias and ensuring neutral text generation.

Optimizing inference time for large models like GPT-2.

Future Enhancements
Add adjustable essay length slider.

Support multilingual sentiment detection.

Deploy app to Streamlit Cloud or Hugging Face Spaces.

Author
Developed by Afifa A.
Saveetha Engineering College — Computer Science Engineering
AI & Data Science Enthusiast 💡

vbnet
Copy code

---

✅ Once you save this as `README.md`, you can **add, commit, and push** to GitHub cleanly.  

If you want, I can now **give you the exact commands to push everything to GitHub safely** and skip adding `venv`. Do you want me to do that next?