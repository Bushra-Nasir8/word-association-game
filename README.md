<<<<<<< HEAD
# word-association-game
=======
# Word Association Game

A web-based Word Association Game built with Flask and JavaScript.

## Features

- Start screen with game instructions
- Random word generation
- 5-second timer for each word
- Score tracking
- Strike system (3 strikes and you're out)
- Taboo words that trigger instant strikes
- High score tracking
- Responsive design for mobile and desktop

## Setup Instructions

1. Make sure you have Python installed (Python 3.6 or higher recommended)

2. Install Flask:
   ```
   pip install flask
   ```

3. Run the application:
   ```
   python app.py
   ```

4. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

## How to Play

1. Click "Start Game" on the home screen
2. You'll be shown a random word
3. Type a related word in the input box and submit within 5 seconds
4. Get 1 point for each valid association
5. Game ends after 3 strikes or timeouts
6. Avoid using taboo words!

## Project Structure

- `app.py` - Flask application with game logic
- `/templates/` - HTML templates
  - `base.html` - Base template with common elements
  - `index.html` - Home/start screen
  - `game.html` - Main game screen
  - `end.html` - Game over screen
  - `high_scores.html` - High scores display
- `/static/css/` - CSS stylesheets
  - `style.css` - Main stylesheet

## Game Logic

For simplicity, this version accepts any non-taboo word as a valid association. In a more advanced version, you could implement:

1. A dictionary API to validate words
2. A word association API to check if words are related
3. More sophisticated scoring based on association strength

## License

This project is open source and available for personal and educational use.
>>>>>>> fbed3ef (first commit)
