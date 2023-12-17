'''
Battleship Game Server

This module implements a Flask web server with a SocketIO extension to 
facilitate a multiplayer battleship game. It includes routes for player ship placement
handling attacks, and managing multiplayer game sessions. 
The server integrates an AI opponent for single-player mode.

Usage:
- Run this module to start the Flask web server.
- Access the game through the specified routes.

Endpoints:
- /placement: Handles ship placement for a single-player game.

- /attack: Processes player attacks and provides game status for both players.

- /: Renders the main game interface for single-player mode.

- /joinmultiplayer: Renders the multiplayer join interface.

- /create_game: Creates a multiplayer game session and renders the waiting interface.

- /mpplacement: Handles ship placement for a multiplayer game.

- /mpplay: Renders the main game interface for multiplayer mode.

- /mpattack: Processes player attacks in a multiplayer game and 
communicates results to both players.

Global Variables:
- BOARD_SIZE: The size of the game board.

Notes:
- The server maintains game state using global variables and communicates updates via sockets.
- For multiplayer functionality, the server supports the creation of game sessions 
and handles ship placement and attacks for two players.

Example Usage:
python
python main.py
'''


from flask import Flask, render_template,jsonify,request
from flask_socketio import SocketIO

from components import (
    create_battleships,
    initialise_board,
    place_battleship_on_board,
    place_battleships
)
from game_engine import attack,check_if_game_over

from aiClass import mainAI
app = Flask(__name__)
socket = SocketIO(app)


BOARD_SIZE = 10
AI = mainAI(BOARD_SIZE,time_allowed=2)
player_board = initialise_board()
player_ships = create_battleships()

AI_board = initialise_board()
AI_ships = create_battleships()
AI_board = place_battleships(AI_board,AI_ships,algorithm='random')

previous_attacks = [] # this is a list of coords the AI
                      #has attacked to prevent it from attacking the same square twice


def parse_front_end_board(ship_data):
    """
    Parses the ship data from the front-end and places the battleships on the board.

    Args:
        ship_data (dict): A dictionary containing the ship data from the front-end.

    Returns:
        The updated board with battleships placed.

    """
    ship_lengths = create_battleships()
    new_board = initialise_board()
    #catch if the board isnt square
    for ship in ship_data:
        orientation='horizontal' if ship_data[ship][2]=='h' else 'vertical'

        new_board = place_battleship_on_board(new_board,int(ship_data[ship][0]),
                                              int(ship_data[ship][1]),int(ship_lengths[ship]),ship,
                                              orientation=orientation)
    return new_board
@app.route('/placement',methods=['GET','POST'])
def placement_interface():
    '''This function handles a URL request and returns a response based on the request method.
    
    If the request method is 'GET', it renders the 'placement.html'
    template with the battleships and board size.

    If the request method is not 'GET', it parses the ship data 
    from the request and updates the player board.
    
    Returns:
        If the request method is 'GET', it returns the rendered template.

        If the request method is not 'GET', it returns a JSON response indicating success. 
        This JSON object can be anything, the front end just expects some response/acknowledgement.
    '''
    if request.method == 'GET':
        return render_template('placement.html', ships=create_battleships(), board_size=BOARD_SIZE)
    else:
        global player_board
        ship_data = request.get_json()


        print(ship_data)
        print(ship_data)
        player_board = parse_front_end_board(ship_data)

        return jsonify({'success': True})

@app.route('/attack',methods=['GET','POST'])
def process_attack():
    """
    Process the attack made by the player and the AI and Checks if the game is over

    Returns:
        A dictionary containing the result of the attack and the AI's next move
        and wether or not the game is over and if the players attack hit or missed
    """
    variables = list(request.args.values())
    # print_board(AI_board)
    x= int(variables[0])
    y= int(variables[1])
    player_hit = attack((x,y),AI_board,AI_ships)

    ai_x, ai_y = AI.new_next_move(player_ships)
    ai_hit = attack((ai_x,ai_y),player_board,player_ships)
    AI.register_shot((ai_x,ai_y),ai_hit)
    player_win=check_if_game_over(AI_ships)
    ai_win=check_if_game_over(player_ships)
    print(ai_win)


    return_dict = {'hit':player_hit,'AI_Turn':(str(ai_x),str(ai_y))}
    if player_win is True:
        return_dict['finished']='Player Wins!'
    elif ai_win is True:
        return_dict['finished'] = 'Computer Wins!'
    return jsonify(return_dict)


@app.route('/')
def root():
    """
    This function returns the rendered template 'main.html' with the specified parameters.

    Returns:
    - The rendered template 'main.html' with the specified parameters.
    """
    return render_template('main.html', board_size=BOARD_SIZE, player_board=player_board)


# for multiplayer

mp_games = {}

@app.route('/joinmultiplayer')
def joinmultiplayer():
    '''renders the joinmp.html template'''
    return render_template('joinmp.html')
@socket.on("connect")
def connect():
    '''connects the socket, provides debug info that it works'''
    print('connected')


@app.route('/create_game')
def create_game():
    '''renders waitingmp.html template and creates a game in the mp_games dict
    with the gamecode as the key and the playerid as the value,
    otherwise renders placmentmp.html template'''


    gamecode = request.args.get('gamecode')
    playerid = request.args.get('playerid')
    if gamecode not in mp_games:
        mp_games[gamecode]={'joined':[playerid]}
        return render_template('waitingmp.html',gamecode=gamecode,playerid=playerid)
    else:
        #this is the sedcond player to join
        print('SENDING A PLAYER STRAIGHT TO MPPLACEMENT',gamecode,playerid)
        #tell the client who is waiting that the game can start now
        socket.emit('game_start',{'room':gamecode})
        mp_games[gamecode]['joined'].append(playerid)

        return render_template('placementmp.html',gamecode=gamecode,
                               playerid=playerid,ships=create_battleships(), board_size=BOARD_SIZE)
@app.route('/mpplacement',methods=['GET','POST'])
def mpplacement():
    '''renders the placementmp.html template and parses the ship data from the request
    and updates the player board'''
    if request.method == 'GET':
        gamecode = request.args.get('gamecode')
        playerid = request.args.get('playerid')
        return render_template('placementmp.html',gamecode=gamecode,
                               playerid=playerid,ships=create_battleships(), board_size=BOARD_SIZE)
    else:
        data = request.get_json()
        print(data)
        gamecode = str(data['gamecode'])
        playerid = str(data['playerid'])
        del data['gamecode']
        del data['playerid']
        ship_data = data
        print(ship_data)
        print('MP gamecode bellow')
        print(mp_games)
        print(mp_games[gamecode])

        # adds all of the relevent data to the the game associated with that gamecode, and the
        # player associated with that id
        mp_games[gamecode][playerid] = [parse_front_end_board(ship_data),create_battleships()]

        return jsonify({'success':True}) # this is because the front end expects a response

@app.route('/mpplay')
def rendermpplay():
    '''renders the mpmain.html template'''
    gamecode = request.args.get('gamecode')
    playerid = request.args.get('playerid')
    # could add a failure link page if this info doesnt checkout
    return render_template('mpmain.html',gamecode = gamecode,playerid = playerid,
                           board_size=BOARD_SIZE,player_board=mp_games[gamecode][playerid][0])


@app.route('/mpattack',methods=['POST'])
def mpattack():
    '''
    Processes a player's attack in a multiplayer battleship game. This route is 
    triggered by a POST request to '/mpattack' and receives attack 
    information through a JSON payload. 
    It updates the game state, checks for hits, and communicates the results to 
    both players via a socket connection.

    HTTP Method: POST
    Endpoint: /mpattack

    Parameters (JSON Payload):
    - gamecode (str): The unique identifier for the multiplayer game session.
    - playerid (str): The identifier for the player making the attack.
    - x (int): The x-coordinate of the attack.
    - y (int): The y-coordinate of the attack.

    Returns (JSON):
    - waiting (bool): Indicates whether the server is waiting for the second player's attack.
    - msg (str, optional): A message indicating the status of the opposition player's ship 
    placement, if applicable.
    - hit (bool, optional): Indicates whether the player's attack was a hit.
    - AI_Turn (tuple[int,int], optional): The coordinates of the AI's attack.
    - ai_hit (bool, optional): Indicates whether the AI's attack was a hit.
    - finished (str, optional): Indicates whether the game is over and who won.
'''
    gamecode = request.get_json()['gamecode']
    playerid = request.get_json()['playerid']
    x = request.get_json()['x']
    y = request.get_json()['y']

    opposition_playerid = [i for i in mp_games[gamecode]['joined'] if i!=playerid][0]
    try:
        opp_board = mp_games[gamecode][opposition_playerid][0]
        opp_ships = mp_games[gamecode][opposition_playerid][1]
    except KeyError:
        return jsonify({'waiting':False,'msg':'opposition player hasn\'t placed ships yet'})

    player_hit = attack((x,y),opp_board,opp_ships)

    return_dict_player_hit = {'hit':player_hit}
    if 'hits' not in mp_games[gamecode]:

        #handles the first attack
        mp_games[gamecode]['hits'] = {}
        mp_games[gamecode]['hits'][playerid] = [x,y,player_hit]

        return jsonify({'waiting':True}) # this is because both attacks
                                         # havent been registered with the server yet
    mp_games[gamecode]['hits'][playerid] = [x,y,player_hit]
    print(mp_games[gamecode]['hits'])
    if len(mp_games[gamecode]['hits'])==2:
        print('adding more shit to the dicts')
        #both players have attacked

        #the "ai_turn" is just the term used by the frontend for the opposition move,
        #so each player will have eachothers attack data here
        return_dict_opposition_player_hit = {}
        return_dict_opposition_player_hit['AI_Turn'] = mp_games[gamecode]['hits'][playerid][:2]
        return_dict_opposition_player_hit['ai_hit'] = mp_games[gamecode]['hits'][playerid][2]
        return_dict_opposition_player_hit['hit'] =mp_games[gamecode]['hits'][opposition_playerid][2]
        return_dict_opposition_player_hit['x'] = mp_games[gamecode]['hits'][opposition_playerid][0]
        return_dict_opposition_player_hit['y'] = mp_games[gamecode]['hits'][opposition_playerid][1]

        return_dict_player_hit['AI_Turn'] = mp_games[gamecode]['hits'][opposition_playerid][:2]
        return_dict_player_hit['ai_hit'] = mp_games[gamecode]['hits'][opposition_playerid][2]
        return_dict_player_hit['x'] = mp_games[gamecode]['hits'][playerid][0]
        return_dict_player_hit['y'] = mp_games[gamecode]['hits'][playerid][1]



    if check_if_game_over(opp_ships):
        return_dict_player_hit['finished']=f'Player {playerid} Wins!'
        return_dict_opposition_player_hit['finished']=f'Player {playerid} Wins!'
    if check_if_game_over(mp_games[gamecode][playerid][1]):
        return_dict_player_hit['finished']=f'Player {opposition_playerid} Wins!'
        return_dict_opposition_player_hit['finished']=f'Player {opposition_playerid} Wins!'
    print('emmitting socket')
    print({playerid:return_dict_player_hit})
    # emitting this socket message tells the frontend to render the new data
    socket.emit('attacksoc',{playerid:return_dict_player_hit,
                             opposition_playerid:return_dict_opposition_player_hit,'room':gamecode})
    del mp_games[gamecode]['hits'] # resets the state to no attacks registered
    return jsonify({'waiting':False})

if __name__=='__main__':
    socket.run(app,port=8000)

    app.run(port=8000)
