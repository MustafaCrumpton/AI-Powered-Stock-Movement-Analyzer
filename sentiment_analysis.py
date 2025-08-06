"""
sentiment_analysis.py

This module uses the FinBERT model to analyze the sentiment of financial text, such as news headlines or article summaries.
It classifies input text into one of three categories: positive, neutral, or negative — and returns the predicted sentiment
along with a confidence score.

FinBERT is a BERT-based model fine-tuned specifically for sentiment analysis in the financial domain, making it suitable
for stock-related news and earnings reports.

"""

from transformers import AutoTokenizer, AutoModelForSequenceClassification
from torch.nn.functional import softmax
import torch

# Load model and tokenizer once
tokenizer = AutoTokenizer.from_pretrained("yiyanghkust/finbert-tone")
model = AutoModelForSequenceClassification.from_pretrained("yiyanghkust/finbert-tone")

def analyze_sentiment(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True)
    outputs = model(**inputs)
    probs = softmax(outputs.logits, dim=1)

    labels = ["negative", "neutral", "positive"]
    predicted = torch.argmax(probs)

    return {
        "label": labels[predicted],
        "confidence": round(probs[0][predicted].item(), 2)
    }

def analyze_news_sentiment(news_articles):
    """
    Apply sentiment analysis to a list of news articles.

    Args:
        news_articles (list of dict): List of articles, each with 'headline' and/or 'summary' keys.

    Returns:
        list of dict: The same list with added 'sentiment' and 'confidence' fields.
    """
    for article in news_articles:
        text = article.get("summary") or article.get("headline") or ""
        if text:
            sentiment_result = analyze_sentiment(text)
            article["sentiment"] = sentiment_result["label"]
            article["confidence"] = sentiment_result["confidence"]
        else:
            article["sentiment"] = "neutral"
            article["confidence"] = 0.0
    return news_articles

#Test Code
"""""
if __name__ == "__main__":
    test_text = "Apple stock falls by 70%"
    result = analyze_sentiment(test_text)
    print(result)
    """