import pandas as pd
import re
import string
import pickle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, precision_score, recall_score
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download NLTK resources
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

def preprocess_text(text):
    """
    Cleans and preprocesses the input text.
    - Converts to lowercase
    - Removes punctuation
    - Removes stop words
    - Lemmatizes tokens
    """
    # 1. Lowercasing
    text = text.lower()
    
    # 2. Removing punctuation and special characters
    text = re.sub(f"[{re.escape(string.punctuation)}]", " ", text)
    
    # 3. Tokenization & Stopword removal & Lemmatization
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    
    tokens = text.split()
    processed_tokens = [
        lemmatizer.lemmatize(word) 
        for word in tokens 
        if word not in stop_words
    ]
    
    return " ".join(processed_tokens)

def train_and_save_model():
    print("Loading dataset...")
    try:
        df = pd.read_csv('dataset.csv')
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return

    print("Preprocessing text data...")
    df['clean_text'] = df['text'].apply(preprocess_text)
    
    # Map labels to binary values (FAKE: 0, REAL: 1)
    # Using 1 for REAL and 0 for FAKE is a common convention
    df['label_num'] = df['label'].map({'FAKE': 0, 'REAL': 1})
    
    X = df['clean_text']
    y = df['label_num']
    
    print("Splitting dataset...")
    # Due to small sample dataset, we might have very few samples for test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Extracting features using TF-IDF...")
    vectorizer = TfidfVectorizer(max_features=5000)
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)
    
    print("Training Naive Bayes model...")
    model = MultinomialNB()
    model.fit(X_train_tfidf, y_train)
    
    print("Evaluating model...")
    y_pred = model.predict(X_test_tfidf)
    accuracy = accuracy_score(y_test, y_pred)
    # Zero_division=0 handles cases with very small test sets
    precision = precision_score(y_test, y_pred, zero_division=0)
    recall = recall_score(y_test, y_pred, zero_division=0)
    
    print(f"Model Accuracy:  {accuracy:.2f}")
    print(f"Model Precision: {precision:.2f}")
    print(f"Model Recall:    {recall:.2f}")
    
    print("Saving model and vectorizer...")
    with open('vectorizer.pkl', 'wb') as f:
        pickle.dump(vectorizer, f)
    with open('model.pkl', 'wb') as f:
        pickle.dump(model, f)
        
    print("Training complete! model.pkl and vectorizer.pkl generated successfully.")

if __name__ == "__main__":
    train_and_save_model()
