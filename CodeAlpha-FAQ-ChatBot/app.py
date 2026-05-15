import json
import string
import nltk
from flask import Flask, render_template, request, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Initialize Flask app
app = Flask(__name__)

# Download necessary NLTK data (safe to call multiple times)
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

# Load FAQ Data
with open('faq_data.json', 'r', encoding='utf-8') as f:
    faq_data = json.load(f)

# Extract questions and answers
questions = [item['question'] for item in faq_data]
answers = [item['answer'] for item in faq_data]

# Preprocessing function
def preprocess_text(text):
    """
    Preprocess the text by:
    1. Converting to lowercase
    2. Tokenizing
    3. Removing punctuation
    4. Removing stopwords
    """
    # 1. Lowercase conversion
    text = text.lower()
    
    # 2. Tokenization
    tokens = word_tokenize(text)
    
    # 3. Remove punctuation
    tokens = [word for word in tokens if word not in string.punctuation]
    
    # 4. Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    
    # Join back to a single string for vectorizer
    return " ".join(tokens)

# Preprocess all FAQ questions
preprocessed_questions = [preprocess_text(q) for q in questions]

# Initialize TF-IDF Vectorizer
vectorizer = TfidfVectorizer()
# Fit and transform the preprocessed FAQ questions to a matrix of TF-IDF features
tfidf_matrix = vectorizer.fit_transform(preprocessed_questions)

def get_best_response(user_input):
    """
    Given a user input, return the best matching answer using TF-IDF and Cosine Similarity.
    """
    # Preprocess the user query
    processed_query = preprocess_text(user_input)
    
    # Vectorize the query
    query_vector = vectorizer.transform([processed_query])
    
    # Calculate cosine similarity between the query and all FAQ questions
    similarities = cosine_similarity(query_vector, tfidf_matrix)
    
    # Find the index of the highest similarity score
    best_index = similarities.argmax()
    best_score = similarities[0, best_index]
    
    # Confidence threshold to ensure chatbot doesn't answer irrelevant questions
    CONFIDENCE_THRESHOLD = 0.2
    
    if best_score < CONFIDENCE_THRESHOLD:
        return "Sorry, I could not understand your question."
    else:
        return answers[best_index]

@app.route('/')
def home():
    """Render the front-end UI."""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """API endpoint to handle chatbot messages."""
    data = request.get_json()
    
    if not data or 'message' not in data:
        return jsonify({"error": "Invalid request"}), 400
        
    user_message = data['message']
    bot_response = get_best_response(user_message)
    
    return jsonify({"response": bot_response})

if __name__ == '__main__':
    app.run(debug=True)
