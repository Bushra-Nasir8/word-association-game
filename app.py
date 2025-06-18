import os
import json
import random
import time
from flask import Flask, render_template, request, jsonify, session, redirect, url_for

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session

# Load word lists
WORDS = [
    "apple", "book", "car", "dog", "elephant", "flower", "guitar", "house", 
    "island", "jacket", "kitchen", "lamp", "mountain", "notebook", "ocean", 
    "piano", "queen", "river", "sun", "tree", "umbrella", "violin", "water", 
    "xylophone", "yellow", "zebra", "airplane", "banana", "computer", "diamond",
    "earth", "forest", "garden", "honey", "ice", "jungle", "kite", "lemon",
    "moon", "night", "orange", "pencil", "quiet", "rain", "star", "time",
    "universe", "vacation", "window", "x-ray", "yogurt", "zoo"
]

TABOO_WORDS = [
    "the", "and", "but", "or", "not", "very", "really", "just", "like", "so"
]

# High scores storage
HIGH_SCORES_FILE = "high_scores.json"

def load_high_scores():
    try:
        if os.path.exists(HIGH_SCORES_FILE):
            with open(HIGH_SCORES_FILE, 'r') as f:
                return json.load(f)
        return []
    except Exception:
        return []

def save_high_score(name, score):
    scores = load_high_scores()
    scores.append({"name": name, "score": score, "date": time.strftime("%Y-%m-%d")})
    scores.sort(key=lambda x: x["score"], reverse=True)
    scores = scores[:10]  # Keep only top 10
    with open(HIGH_SCORES_FILE, 'w') as f:
        json.dump(scores, f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game')
def game():
    # Initialize game state
    session['score'] = 0
    session['strikes'] = 0
    session['current_word'] = random.choice(WORDS)
    session['used_words'] = [session['current_word']]
    return render_template('game.html', word=session['current_word'])

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    player_word = data.get('word', '').lower().strip()
    time_taken = data.get('time', 0)
    
    # Get current game state
    score = session.get('score', 0)
    strikes = session.get('strikes', 0)
    current_word = session.get('current_word', '')
    used_words = session.get('used_words', [])
    
    # Check if time is up
    if time_taken >= 5:
        strikes += 1
        result = {
            'valid': False,
            'message': "Time's up!",
            'score': score,
            'strikes': strikes,
            'game_over': strikes >= 3
        }
    # Check if word is empty
    elif not player_word:
        result = {
            'valid': False,
            'message': 'Please enter a word',
            'score': score,
            'strikes': strikes,
            'game_over': False
        }
    # Check if word is a taboo word
    elif player_word in TABOO_WORDS:
        strikes += 1
        result = {
            'valid': False,
            'message': f'"{player_word}" is a taboo word!',
            'score': score,
            'strikes': strikes,
            'game_over': strikes >= 3
        }
    # Check if word was already used
    elif player_word in used_words:
        result = {
            'valid': False,
            'message': 'Word already used!',
            'score': score,
            'strikes': strikes,
            'game_over': False
        }
    # For simplicity, we'll accept any non-taboo word as valid
    else:
        score += 1
        used_words.append(player_word)
        
        # Get a new word that hasn't been used yet
        available_words = [w for w in WORDS if w not in used_words]
        if not available_words:
            # If all words have been used, reset the used words list except for the current submission
            used_words = [player_word]
            available_words = [w for w in WORDS if w not in used_words]
        
        next_word = random.choice(available_words)
        used_words.append(next_word)
        
        result = {
            'valid': True,
            'message': 'Good association!',
            'score': score,
            'strikes': strikes,
            'next_word': next_word,
            'game_over': False
        }
    
    # Update session
    session['score'] = score
    session['strikes'] = strikes
    session['current_word'] = result.get('next_word', current_word)
    session['used_words'] = used_words
    
    return jsonify(result)

@app.route('/end', methods=['GET', 'POST'])
def end():
    if request.method == 'POST':
        name = request.form.get('name', 'Anonymous')
        score = session.get('score', 0)
        save_high_score(name, score)
        return redirect(url_for('high_scores'))
    
    return render_template('end.html', score=session.get('score', 0))

@app.route('/high_scores')
def high_scores():
    scores = load_high_scores()
    return render_template('high_scores.html', scores=scores)

if __name__ == '__main__':
    app.run(debug=True)
