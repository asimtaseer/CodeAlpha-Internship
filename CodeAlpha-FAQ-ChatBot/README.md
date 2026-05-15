# CodeAlpha FAQ Chatbot

A beginner-friendly NLP-based chatbot built with Python, Flask, NLTK, and Scikit-Learn that answers common questions about the CodeAlpha internship platform. The UI features a very attractive, modern dark theme.

## Features

- **Natural Language Processing**: Uses `nltk` for tokenization and stopword removal.
- **Machine Learning**: Uses `TfidfVectorizer` and `cosine_similarity` to find the most accurate answer among the FAQs based on the user's input.
- **Flask Backend**: Easy-to-understand backend API.
- **Modern Dark UI**: Features chat bubbles, scrolling, typing animations, and font-awesome icons.
- **Confidence Threshold**: Ensures the bot acknowledges when it doesn't understand a question.

## Project Structure

```
project/
│
├── app.py                # Main Flask application and NLP logic
├── faq_data.json         # JSON file containing all the Q&A pairs
├── requirements.txt      # Project dependencies
├── templates/
│   └── index.html        # Main HTML layout
├── static/
│   ├── style.css         # Dark modern theme and responsive styles
│   └── script.js         # Vanilla JavaScript to handle Fetch API and UI effects
└── README.md             # Project documentation
```

## Setup Instructions

### 1. Requirements

Make sure you have Python installed on your system.

### 2. Install Dependencies

Open a terminal or command prompt in the project directory and run the following command to install the required libraries:

```bash
pip install -r requirements.txt
```

### 3. Running the Chatbot

Start the Flask server by running:

```bash
python app.py
```

### 4. Viewing the Chatbot

Wait for the terminal to display `Running on http://127.0.0.1:5000/`. Then open a web browser and go to `http://127.0.0.1:5000/` or `http://localhost:5000/`. Let the bot help you!

## Notes

- First run might take a brief second to download necessary NLTK corpora like `punkt` and `stopwords`. It will happen automatically.
- Ensure that the console window stays open while you are using the app in your browser!
