ECM1400 Battleships:

Features implemented
- CLI game 
- Web interface with templates
- AI Player (Using probablity generating functions)
- Multiplayer Web Interface
    - New custom interfaces 
    - New endpoints that use socket connection for real time communication

To Run:
1- ensure that flask is installed. Run ```pip install flask```

2 - ensure flask_socketio is installed. Run ```pip install flask_socketio```

### To Run the CLI game
run ```py game_engine.py```

### To Run Multiplayer CLI
run ```py mp_game_engine.py```

### To run the web interface version
1 - run ```py main.py```

2 - navigate to http://127.0.0.1:8000/placement

### To run the web interface
1 - run ```py main.py```

2 - open 2 chrome windows

3 - navigate to http://127.0.0.1:8000/joinmultiplayer on both browers

4 - type a numeric code for the gamecode and press join game into both browsers

5 - both players make their move, and then the board for both players will update

### Improvements for next time
- Make the UI for the socket gameplay more intuitive. I'd do this by making it clearer when the player is allowed to attack again and when they are still waiting
- I would implement difficulty into the AI so that it's more beatable. I would do this by not always selecting the best move that the AI thinks, depending on the dificulty
- I'd add more robustness to the multiplayer web interface, as right now, if the user goes to a url they're not supposed to, they just get a http error. To do this I'd create alert/error templates to explain what is wrong and how to fix it