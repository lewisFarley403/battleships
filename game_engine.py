'''
Game Engine Module

This module provides a simple implementation of a battleship game,
including functions for processing player attacks, checking game status, and a main game loop.

Usage:
- Run the module to start a single-player game loop.
- To integrate an AI opponent, uncomment the 'ai_opponent_game_loop()' line in the '__main__' block.

Functions:
- attack(coords: list[int, int], board: list[list], battleships: dict[str, int]) -> bool:
  Processes an attack on the board and updates the board and battleships dictionary accordingly.
  Args:
    - coords (list[int, int]): The coordinates of the attack.
    - board (list[list]): The board to attack.
    - battleships (dict[str, int]): The dictionary of battleships.
  Returns:
    - bool: True if the attack was successful, False if not.

- cli_coordinates_input() -> list[int, int]:
  Gets the coordinates of an attack from the user.
  Returns:
    - list[int, int]: The coordinates of the attack.

- check_if_game_over(battleships: dict[str, int]) -> bool:
  Checks if the game is over by verifying if all battleship lengths are 0.
  Args:
    - battleships (dict[str, int]): The dictionary of battleships.
  Returns:
    - bool: True if the game is over, False if not.

- simple_game_loop():
  Main game loop for a single-player game. Initializes the board,
  places battleships, and allows the player to make attacks until the game is over.

__main__:
- Invokes the 'simple_game_loop()' function to start a single-player game loop.
'''

from components import place_battleships,initialise_board,create_battleships

players = {}
def attack(coords:list[int,int],board:list[list],battleships:dict[str,int])->bool:
    '''
    this processes an attack on the board and updates the board 
    and battleships dictionary accordingly
    Args:
        coords (list[int,int]): the coordinates of the attack
        board (list[list]): the board to attack
        battleships (dict[str,int]): the dictionary of battleships
    Returns:
        bool: True if the attack was successful, False if not
    '''
    content_of_square = board[coords[1]][coords[0]]
    if content_of_square is not None:
        battleships[content_of_square]-=1
        board[coords[1]][coords[0]] = None
        return True
    return False

def cli_coordinates_input():
    '''
    this function gets the coordinates from the user
    Returns:
        list[int,int]: the coordinates of the attack
    '''
    x = int(input('Enter an x coordinate to attack: ')) -1# -1 because i count from 0,
    # but users will count from 1
    y=int(input('Enter a y coordinate to attack: '))-1
    return (x,y)
def check_if_game_over(battleships):
    '''
    this function checks if the game is over
    by checking if all battleship lengths are 0

    Args:
        battleships (dict[str,int]): the dictionary of battleships
    Returns:
        bool: True if the game is over, False if not
    '''
    for ship in battleships:
        if battleships[ship]>0:
            return False
    return True
def simple_game_loop():
    '''
    this is the main game loop for the game
    to attack into a board generated in a simple way
    Returns:
        None
    '''
    print('Welcome to ECM1400 Battleships - single player')
    board = initialise_board()
    ships = create_battleships()
    board = place_battleships(board,ships)
    print(ships)
    print(check_if_game_over(ships))
    while check_if_game_over(ships) is False:
        coords = cli_coordinates_input()
        if attack(coords,board,ships) is True:
            print('Hit')
        else:
            print('Miss')






if __name__=='__main__':
    simple_game_loop()
    # ai_opponent_game_loop()
