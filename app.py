from flask import Flask, request, jsonify, render_template
import pickle
import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import os

app = Flask(__name__)

# Ensure NLTK resources are available
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')
    nltk.download('omw-1.4')

# Load the trained model and vectorizer
MODEL_PATH = 'model.pkl'
VECTORIZER_PATH = 'vectorizer.pkl'

model = None
vectorizer = None

if os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH):
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    with open(VECTORIZER_PATH, 'rb') as f:
        vectorizer = pickle.load(f)
else:
    print("Warning: Model or vectorizer not found. Please run train_model.py first.")

# In-memory history of last 5 predictions
prediction_history = []

def preprocess_text(text):
    """Same preprocessing function used during training."""
    text = text.lower()
    text = re.sub(f"[{re.escape(string.punctuation)}]", " ", text)
    
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    
    tokens = text.split()
    processed_tokens = [
        lemmatizer.lemmatize(word) 
        for word in tokens 
        if word not in stop_words
    ]
    return " ".join(processed_tokens)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if not model or not vectorizer:
        return jsonify({'error': 'Model is not trained. Please contact administrator.'}), 500

    data = request.json
    text = data.get('text', '').strip()
    
    if not text:
        return jsonify({'error': 'Input text cannot be empty.'}), 400
        
    try:
        # Preprocess
        cleaned_text = preprocess_text(text)
        
        # Feature Extraction
        vectorized_text = vectorizer.transform([cleaned_text])
        
        # Predict
        prediction = model.predict(vectorized_text)[0]
        probabilities = model.predict_proba(vectorized_text)[0]
        
        # In our mapping: 0 = FAKE, 1 = REAL
        if prediction == 1:
            result = "Real News"
            confidence = probabilities[1] * 100
        else:
            result = "Fake News"
            confidence = probabilities[0] * 100
            
        # Format confidence
        confidence_str = f"{confidence:.2f}%"
        
        # Save to history
        history_entry = {
            'text': text[:50] + "..." if len(text) > 50 else text,
            'result': result,
            'confidence': confidence_str
        }
        prediction_history.insert(0, history_entry)
        
        # Keep only the last 5
        if len(prediction_history) > 5:
            prediction_history.pop()
            
        return jsonify({
            'result': result,
            'confidence': confidence_str,
            'history': prediction_history
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
