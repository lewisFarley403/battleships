# ECM1400 Battleships: 🚢💥 A Multi-Faceted Naval Warfare Experience 💣⚓

Dive into the world of naval strategy with **ECM1400 Battleships**, a versatile Battleship game implementation showcasing a range of features for both solo and multiplayer gameplay. This project, residing proudly in my software developer portfolio, boasts the following key elements:

## Features Implemented:

- **CLI Game:** 🖥️
  - Engage in a classic game of Battleships through the command line interface.

- **Web Interface with Templates:** 🌐
  - Experience an interactive web interface featuring customizable templates for an enhanced visual appeal.

- **AI Player (Using Probability Generating Functions):** 🤖🧠
  - Challenge yourself against an artificial intelligence opponent that employs probability-generating functions for strategic decision-making.

- **Multiplayer Web Interface:** 🌐🤝
  - Explore a dynamic multiplayer experience with:
    - New custom interfaces tailored for an immersive gameplay environment.
    - Novel endpoints utilizing socket connections for real-time communication.

## How to Run:

1. Ensure that Flask is installed. Run ```pip install flask```.
2. Ensure Flask-SocketIO is installed. Run ```pip install flask_socketio```.

### To Run the CLI Game:
Run ```py game_engine.py```.

### To Run Multiplayer CLI:
Run ```py mp_game_engine.py```.

### To Run the Web Interface Version:
1. Run ```py main.py```.
2. Navigate to http://127.0.0.1:8000/placement.

### To Run the Multiplayer Web Interface:
1. Run ```py main.py```.
2. Open two Chrome windows.
3. Navigate to http://127.0.0.1:8000/joinmultiplayer on both browsers.
4. Enter a numeric code for the game and press "Join Game" on both browsers.
5. Make your moves, and watch as the boards update in real-time for both players.

## Areas for Improvement in Future Versions:

- **Enhanced UI for Socket Gameplay:** 🔄
  - Implement a more intuitive user interface for socket-based gameplay. Clarify when a player can make their next attack and when they are still awaiting their turn.

- **Adjustable AI Difficulty:** 🌟
  - Introduce varying difficulty levels for the AI player. This could involve making the AI occasionally choose suboptimal moves based on the selected difficulty level.

- **Robustness for Multiplayer Web Interface:** 🛡️💪
  - Strengthen the multiplayer web interface by handling errors more gracefully. Create alert/error templates to guide users when they encounter HTTP errors due to incorrect URLs.

Embark on a strategic naval adventure with **ECM1400 Battleships**, where classic gameplay meets modern development innovation.
