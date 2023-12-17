'''
AI Opponent Game Module

This module provides a simple implementation of a battleship game where the player faces 
an AI opponent. The AI opponent generates random attacks and responds to the player's attacks.
 The game loop continues until one of the players wins.

Usage:
- Run this module to start a battleship game against an AI opponent.

Functions:
- generate_attack(previous_attacks: List[tuple[int, int]], size: int) -> tuple[int, int]:
  Generates a random attack that has not been used before.
  Args:
    - previous_attacks (List[tuple[int, int]]): List of previous attacks.
    - size (int): Size of the board.
  Returns:
    - tuple[int, int]: Coordinates of the attack.

- check_if_game_over_multiplayer() -> bool:
  Checks if the game is over for multiplayer by determining if either player has won.
  Returns:
    - bool: True if the game is over, False if not.

- ai_opponent_game_loop() -> None:
  Main game loop for a battleship game against an AI opponent. 
  Alternates turns between the player and the AI, allowing the 
  player to make attacks and responding with random AI attacks.

__main__:
- Invokes the 'ai_opponent_game_loop()' function to start the game.

Notes:
- The game state is managed using global variables.
- The AI opponent generates random attacks and does not implement advanced strategies.
- For multiplayer functionality, the server maintains a dictionary 'players' with 'player' 
and 'ai' keys, each containing the respective player's board and ships.

Example Usage:

python ai_opponent_game.py
'''

import random

from components import initialise_board,create_battleships,place_battleships,print_board
from game_engine import attack,cli_coordinates_input,check_if_game_over
players = {}
def generate_attack(previous_attacks:list[list[int,int]],size:int)->tuple[int,int]:
    '''
    this function generates a random attack that has not been used before
    Args:
        previous_attacks (list): the list of previous attacks
        size (int): the size of the board
    Returns:
        tuple[int,int]: the coordinates of the attack'''
    x= random.randint(0,size-1)
    y=random.randint(0,size-1)
    while (x,y) in previous_attacks:
        x= random.randint(0,size-1)
        y=random.randint(0,size-1)
    previous_attacks.append((x,y))
    return (x,y)
def check_if_game_over_multiplayer():
    '''checks if the game is over for multiplayer,
    by checking if either player has won
    Returns:
        bool: True if the game is over, False if not
    '''
    if check_if_game_over(players['player'][1]) is True:
        # checks if the player has a ship of length 0
        print('AI Wins')
        return True
    elif check_if_game_over(players['ai'][1]) is True:
        # checks if the ai has a ship of length 0
        print('Player Wins')
        return True
    return False

def ai_opponent_game_loop()->None:
    '''
    this is the main game loop for the game
    to attack into a board generated in a random way
    and have the AI attack back
    Returns:
        None

    '''
    print('Welcome to ECM1400 Battleships - Play Against The AI')

    player_board = initialise_board()

    player_ships = create_battleships()

    player_board = place_battleships(player_board,player_ships)
    AI_ships = create_battleships()
    AI_board = initialise_board()
    AI_board = place_battleships(AI_board,AI_ships,algorithm='random')
    previous_attacks = []

    players['player'] = [player_board,player_ships]
    players['ai'] = [AI_board,AI_ships]
    players_turn = True
    while check_if_game_over_multiplayer() is False:
        if players_turn is True:
            board = players['ai'][0]
            x,y=cli_coordinates_input()
            if attack((x,y),board,players['ai'][1]) is True:
                print('Hit')
            else:
                print('Miss')
        else:
            board = players['player'][0]
            coords = generate_attack(previous_attacks,len(player_board))
            print('AI ATTACKS: ',coords)
            if attack(coords,board,players['player'][1]) is True:
                print('Hit')
            else:
                print('Miss')
            print('YOUR BOARD:')
            print_board(board)

        players_turn = not players_turn
if __name__== '__main__':
    ai_opponent_game_loop()
