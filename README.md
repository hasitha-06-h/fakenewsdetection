# Fake News Detection System

This project is a professional, full-stack web application designed to classify news articles as **REAL** or **FAKE** using Machine Learning and Natural Language Processing. It strictly follows a standard research paper methodology for text classification.

## Project Methodology

1. **Input Collection**: Users submit text through a modern, responsive web dashboard.
2. **Text Preprocessing**: The system uses `nltk` to clean the text (lowercasing, punctuation removal, stop-word removal, and lemmatization).
3. **Feature Extraction**: Text is converted into numerical vectors using `TfidfVectorizer`.
4. **Model Training**: A `Multinomial Naive Bayes` classifier is trained on the vectorized dataset, ensuring highly dynamic and accurate probability scoring.
5. **Prediction & Results**: The Flask backend returns the classification along with a calculated confidence probability.
6. **Continuous Improvement**: The dataset can be easily expanded, and the model retrained using the provided `train_model.py` script.

## Tech Stack
- **Backend:** Python, Flask
- **Machine Learning:** Scikit-learn, Pandas, NLTK
- **Frontend:** HTML5, CSS3, Vanilla JavaScript, FontAwesome
- **UI Design:** Professional dark-theme dashboard with glassmorphism and smooth animations.

## File Structure

```text
fake_news_project/
│
├── app.py                  # Main Flask backend application
├── train_model.py          # Script to preprocess text and train the ML model
├── generate_data.py        # Script used to generate the synthetic dataset
├── dataset.csv             # The dataset containing texts and labels (REAL/FAKE)
├── model.pkl               # Saved Machine Learning Model (Naive Bayes)
├── vectorizer.pkl          # Saved TF-IDF Vectorizer
├── README.md               # Project documentation
│
├── static/                 # Frontend static assets
│   ├── style.css           # Premium dashboard styling
│   └── script.js           # Frontend logic, animations, and API communication
│
└── templates/              # HTML templates
    └── index.html          # Main dashboard interface
```

## How to Setup and Run

### Prerequisites
Make sure you have Python installed (preferably version 3.8 or higher).

### 1. Install Required Libraries
Open your terminal (in VS Code or Command Prompt) and install the dependencies:
```bash
pip install flask pandas scikit-learn nltk
```

### 2. (Optional) Retrain the Model
If you modify `dataset.csv` or want to recreate the `model.pkl` and `vectorizer.pkl` files from scratch, simply run:
```bash
python train_model.py
```

### 3. Run the Application
Start the Flask development server:
```bash
python app.py
```

### 4. Open the Dashboard
Open your preferred web browser and navigate to the address shown in your terminal, which is usually:
**http://127.0.0.1:5000**

## Features Included
- **Advanced NLP:** Uses lemmatization, TF-IDF, and stop-word removal to understand context.
- **Dynamic Probabilities:** The system gives exact confidence scores (e.g., 94.5%) rather than flat guesses.
- **Premium UI/UX:** A beautifully designed interface with animated progress bars, history logging, and real-time status updates.
- **Error Handling:** Built-in validation to handle empty inputs and server errors gracefully.
