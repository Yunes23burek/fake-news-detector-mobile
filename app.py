
from flask import Flask, render_template, request, jsonify
import pickle
import re
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import nltk
from nltk.corpus import stopwords
import numpy as np

app = Flask(__name__)

# Download required NLTK data
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# Simple preprocessing function
def clean_text(text):
    """Nettoyer le texte"""
    text = text.lower()
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    words = text.split()
    words = [w for w in words if w not in stop_words and len(w) > 2]
    return ' '.join(words)

# Simple model - we'll use a pre-trained approach with sample data
class FakeNewsDetector:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
        self.model = LogisticRegression(max_iter=1000)
        self.is_trained = False
        self._train_with_sample_data()

    def _train_with_sample_data(self):
        """Entraîner avec des données d'exemple"""
        # Sample fake news
        fake_news = [
            "shocking revelation government hiding aliens area secret documents leaked",
            "miracle cure cancer discovered pharmaceutical companies dont want know",
            "celebrity dies tragic accident details emerge",
            "breaking world ending tomorrow scientists confirm",
            "vaccines cause autism new study proves",
            "elvis presley spotted alive local grocery store",
            "moon landing faked nasa admits finally",
            "5g towers spreading coronavirus experts warn",
            "bill gates microchipping everyone through vaccines",
            "flat earth society gains millions new members",
        ]

        # Sample real news
        real_news = [
            "congress passes new infrastructure bill bipartisan support",
            "stock market closes higher strong earnings reports",
            "local school district announces new education programs",
            "scientists discover new species deep ocean expedition",
            "unemployment rate drops lowest level decade",
            "new renewable energy project launched state",
            "researchers publish findings climate change study",
            "city council approves budget fiscal year",
            "medical breakthrough helps patients rare disease",
            "international summit addresses global trade policies",
        ]

        texts = fake_news + real_news
        labels = [1] * len(fake_news) + [0] * len(real_news)

        X = self.vectorizer.fit_transform(texts)
        self.model.fit(X, labels)
        self.is_trained = True

    def predict(self, text):
        """Prédire si une news est fausse ou vraie"""
        cleaned = clean_text(text)
        if not cleaned:
            return {"prediction": "unknown", "confidence": 0, "cleaned_text": ""}

        X = self.vectorizer.transform([cleaned])
        proba = self.model.predict_proba(X)[0]
        pred = self.model.predict(X)[0]

        return {
            "prediction": "fake" if pred == 1 else "real",
            "confidence": float(max(proba)),
            "fake_probability": float(proba[1]),
            "real_probability": float(proba[0]),
            "cleaned_text": cleaned
        }

detector = FakeNewsDetector()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    text = data.get('text', '')

    if not text or len(text.strip()) < 10:
        return jsonify({
            "error": "Veuillez entrer un texte plus long (minimum 10 caractères).",
            "prediction": None
        })

    result = detector.predict(text)
    return jsonify(result)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
