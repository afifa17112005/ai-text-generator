"""
model_utils.py
Utilities for sentiment analysis and text generation using Hugging Face transformers.
"""

from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification, AutoModelForCausalLM
import logging

logger = logging.getLogger(__name__)

class SentimentGenerator:
    def __init__(self,
                 sentiment_model_name: str = "distilbert-base-uncased-finetuned-sst-2-english",
                 gen_model_name: str = "gpt2",
                 device: int = -1):
        """device: -1 for CPU, 0 for GPU"""
        try:
            self.sentiment = pipeline("sentiment-analysis", model=sentiment_model_name, device=device)
        except Exception as e:
            logger.warning(f"Failed to load sentiment model: {e}")
            self.sentiment = pipeline("sentiment-analysis", device=device)

        try:
            self.gen_tokenizer = AutoTokenizer.from_pretrained(gen_model_name)
            if self.gen_tokenizer.pad_token is None:
                self.gen_tokenizer.pad_token = self.gen_tokenizer.eos_token
            self.gen_model = AutoModelForCausalLM.from_pretrained(gen_model_name)
            self.generator = pipeline("text-generation",
                                      model=self.gen_model,
                                      tokenizer=self.gen_tokenizer,
                                      device=device)
        except Exception as e:
            logger.warning(f"Failed to load generator model: {e}")
            self.generator = pipeline("text-generation", model="gpt2", device=device)

    def predict_sentiment(self, text: str):
        if not text.strip():
            return {"label": "neutral", "score": 1.0}

        result = self.sentiment(text, truncation=True)[0]
        label = result["label"].lower()
        score = float(result["score"])

        if label.startswith("pos"):
            norm = "positive"
        elif label.startswith("neg"):
            norm = "negative"
        else:
            norm = "neutral"

        if 0.45 < score < 0.55:
            norm = "neutral"

        return {"label": norm, "score": score}

    def generate_text(self, prompt: str, sentiment: str = None,
                      max_new_tokens: int = 100, top_k: int = 50,
                      top_p: float = 0.95, temperature: float = 0.9):
        if sentiment is None:
            sentiment = self.predict_sentiment(prompt)["label"]

        if sentiment == "positive":
            prefix = "Write an optimistic paragraph about:\n"
        elif sentiment == "negative":
            prefix = "Write a critical paragraph about:\n"
        else:
            prefix = "Write a neutral, factual paragraph about:\n"

        final_prompt = prefix + prompt.strip()

        output = self.generator(final_prompt,
                                max_new_tokens=max_new_tokens,
                                do_sample=True,
                                top_k=top_k,
                                top_p=top_p,
                                temperature=temperature,
                                num_return_sequences=1)
        return output[0]["generated_text"]
