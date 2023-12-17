"""
Component Module

This module provides functions for initializing a game board, creating battleships from a file,
and placing battleships on the board using different placement algorithms.

Functions:
    - `initialise_board(size: int = 10) -> List[List]`: 
        Creates an empty 2D square board with the specified size.

    - `create_battleships(filename: str = 'battleships.txt') -> Dict[str, int]`: 
        Creates a dictionary of battleships from a file.

    - `place_battleships(board: List[List], ships: Dict[str, int], 
                                algorithm: str = 'simple') -> List[List]`: 
        Places battleships on a board using specified algorithms.

    - `random_battleship_placement(board: List[List], battleships: Dict[str, int]) -> List[List]`: 
        Places ships with random coordinates and orientation on a board.

    - `simple_battleship_placement(board: List[List], battleships: Dict[str, int]) -> List[List]`: 
        Places ships one on each line from the top left of the board.

    - `is_valid_placement(board: List[List], x: int, y: int, 
                            ship_length: Dict[str, int], orientation: str = 'horizontal') -> bool`: 
        Checks if a ship can be placed on a board at a given coordinate and orientation.

    - `place_battleship_on_board(board: List[List], x: int, y: int, ship_length: int,
                                    ship_name: str,orientation: str = 'horizontal') -> List[List]`: 
        Places a battleship on the game board.

    - `print_board(board: List[List]) -> None`: 
        Prints a board to the console.

Usage:
    - To create a board of size 5 and place two battleships
    on it using the random placement algorithm:
        ```
        current_board = initialise_board(size=5)
        current_board = place_battleships(current_board, 
        {'ship 1': 3, 'ship 2': 2}, algorithm='random')
        ```
    - To read battleships from a file called `battleships.txt` and place them on a board
    of size 10 using the simple placement algorithm:
        ```
        current_board = initialise_board(size=10)
        ship_data = create_battleships(filename='battleships.txt')
        current_board = place_battleships(current_board, ship_data, algorithm='simple')
        ```
    - To check if a ship of length 3 can be placed on a board at coordinate (0, 0) horizontally:
        ```
        current_board = initialise_board(size=10)
        is_valid_placement(current_board, 0, 0, 3, 'horizontal')
        ```
"""

import random
from typing import List,Dict

def initialise_board(size = 10)->List[List]:
    '''Creates an empty 2D square board with width and height of size.

    Creates a 2D list of size x that containing all None values to signify 
    that this board is empty

    Args:
        size(int) : the width and height of the board (default 10)
    
    Returns:
        board(list): a 2D list of size x size containing all None values
    '''
    empty_board = [[None for _ in range(size)] for _ in range(size)]
    return empty_board

def create_battleships(filename = 'battleships.txt')->Dict[str,int]:
    '''Creates a dictionary of battleships from a file

    Creates a dictionary of battleships from a file, with the name of the 
    ship as the key and the length of the ship as the value
    by splitting each line on : to extract the name and length of the ship

    Args:
        filename : the directory of the text file to read ship data from 
        (default 'battleships.txt'), which has the name of the battle 
        ships and their lengths separated by a colon on each line
        
    
    Returns:
        A dictionary of battleships with the name of the ship as the key
        and the length of the ship as the value
    '''
    with open(filename,'r', encoding='utf-8') as f:
        battleships = {}
        for line in f.readlines():
            line = line.strip()
            name, length = line.split(':')
            battleships[name] = int(length)
        return battleships


def place_battleships(board:List[List],ships:Dict[str,int],algorithm:str = 'simple')->List[List]:
    '''Places battleships on a board, using algorithms that depend on the algorithm parameter

    Places battleships on a board, using algorithms that depend on the algorithm parameter 
    and the ships to be placed
    
    if the algorithm parameter is: 
        -'simple', the ships will be placed one on each line from the top left
        -'random', the ships will be placed randomly on the board

    Args:
        board : the board to place the battleships on
        battleships : the dictionary of battleships to place on the board
        algorithm : the algorithm to use to place the battleships (default 'simple')
    
    Returns:
        The board with the battleships placed on it
    '''
    if algorithm == 'simple':
        return simple_battleship_placement(board, ships)
    elif algorithm == 'random':
        return random_battleship_placement(board, ships)
def random_battleship_placement(board: List[List], battleships: Dict[str,int])->List[List]:
    '''places ships with random coordinates and orientation on a board

    Places ships with random coordinates and orientation on a board, checking if the placement is 
    valid before placing the ship

    Args:
        board : the board to place the battleships on
        battleships : the dictionary of battleships names and lengths to place on the board
    Returns:
        The board with the battleships placed on it
    '''

    for ship in battleships:
        placed = False
        while not placed:

            x = random.randint(0,len(board)-1)
            y = random.randint(0,len(board)-1)
            orientation = random.choice(['horizontal','vertical'])
            if is_valid_placement(board,x,y,battleships[ship],orientation=orientation) is True:
                board = place_battleship_on_board(board,x,y,battleships[ship],
                                                    ship,orientation=orientation)
                placed = True
    return board


def simple_battleship_placement(board:List[List], battleships:Dict[str,int])->List[List]:
    '''places ships one on each line from the top left of the board

    Places ships one on each line from the top left of the board,
    checking if the placement is valid before placing the ship
    Args:
        board : the board to place the battleships on
        battleships : the dictionary of battleships names and lengths to place on the board
    Returns:
        The board (2D Array) with the battleships placed on it
    '''
    for i,ship in enumerate(battleships):
        size = len(board)
         #creates the name, for example "ship 2" for the length of ship 2
         # then adds Nones to pad it to the correct size
        none_padding = [None for _ in range(size-battleships[ship])]
        new_row = [ship for _ in range(battleships[ship])]+ none_padding
        board[i] = new_row
    return board

def is_valid_placement(board: List[List], x: int, y: int, ship_length: Dict[str, int],
                        orientation: str = 'horizontal') -> bool:
    '''
    Checks if a ship can be placed on a board at a given coordinate and orientation.

    This function checks if a ship can be placed on a board at a given 
    coordinate and orientation by checking if the ship will 
    go off the board and if there are any other ships in the way.

    Args:
        board: The board to place the battleships on.
        x: The x coordinate to place the ship at.
        y: The y coordinate to place the ship at.
        ship_length: The length of the ship to place.
        orientation: The orientation of the ship to place (default 'horizontal').

    Returns:
        True if the ship can be placed, False if it cannot.
    '''
    if orientation == 'horizontal':
        if x + ship_length > len(board):
            # the ship will go off the board
            return False
        for i in range(ship_length):
            if board[y][x + i] is not None:
                # there is already a ship in the way
                return False
        return True
    elif orientation == 'vertical':
        # this adds to the row not col, but otherwise the same as above
        if y + ship_length > len(board):
            return False
        for i in range(ship_length):
            if board[y + i][x] is not None:
                return False
        return True
    else:
        raise ValueError('orientation must be "horizontal" or "vertical"')


def place_battleship_on_board(board:List[List],x:int,y:int,ship_length:int,
                              ship_name:str, orientation:str='horizontal')-> List[List]:

    '''
    Place a battleship on the game board.

    Args:
    - board (list): The game board represented as a 2D list.
    - x (int): The x-coordinate of the top-left corner of the battleship.
    - y (int): The y-coordinate of the top-left corner of the battleship.
    - ship_length (int): The length of the battleship.
    - ship_name (str): The name of the battleship.
    - orientation (str, optional): The orientation of the battleship. Defaults to 'horizontal'.

    Returns:
    - board (list): The updated game board with the battleship placed.

    Raises:
    - ValueError: If the orientation is neither 'horizontal' nor 'vertical'.

    '''
    if is_valid_placement(board,x,y,ship_length,orientation=orientation): #might need ==True
        if orientation == 'horizontal':
            for i in range(ship_length):
                board[y][x+i] = ship_name
        elif orientation == 'vertical':
            for i in range(ship_length):
                board[y+i][x] = ship_name
        else:
            raise ValueError('orientation must be "horizontal" or "vertical"')
        return board
    else:
        return -1
def print_board(board:List[List])->None:
    '''Prints a board to the console
    
    Prints a board to the console, with the longest item in the board being the width of each cell

    Args:
        board : the board to print
    Returns:
        None
    '''
    longest = -1
    for row in board:
        for item in row:
            if item is not None:
                if len(item)>longest:
                    longest = len(item)
    for row in board:
        print("-" * (len(row)*(longest+3)) + "+")
        print("| " + " | ".join(str(cell)+' '*(longest-len(cell))
        if cell is not None else ' '*longest for cell in row) + " |")
    print("+---" * len(board[0]) + "+")
if __name__=='__main__':
    current_board =initialise_board(size=3)
    random.seed(0)
    current_board = place_battleships(current_board, {'ship 1':3,'ship 2':2},algorithm='random')
    print(current_board)
