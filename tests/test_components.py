from components import is_valid_placement, place_battleship_on_board, random_battleship_placement
import random
from components import is_valid_placement, random_battleship_placement, place_battleship_on_board
def test_is_valid_placement_horizontal():
    """
    Test if the is_valid_placement function correctly checks if a ship can be placed horizontally on the board.
    """
    board = [[None, None, None, None],
             [None, None, None, None],
             [None, None, None, None],
             [None, None, None, None]]
    ship_length = 3
    x = 1
    y = 1
    orientation = 'horizontal'
    assert is_valid_placement(board, x, y, ship_length, orientation) == True, "is_valid_placement function does not correctly check if ship can be placed horizontally"

def test_is_valid_placement_vertical():
    """
    Test if the is_valid_placement function correctly checks if a ship can be placed vertically on the board.
    """
    board = [[None, None, None],
             [None, None, None],
             [None, None, None],
             [None, None, None]]
    ship_length = 3
    x = 1
    y = 1
    orientation = 'vertical'
    assert is_valid_placement(board, x, y, ship_length, orientation) == True, "is_valid_placement function does not correctly check if ship can be placed vertically"

def test_is_valid_placement_out_of_bounds_horizontal():
    """
    Test if the is_valid_placement function correctly checks if a ship goes off the board.
    """
    board = [[None, None, None],
             [None, None, None],
             [None, None, None]]
    ship_length = 3
    x = 2
    y = 1
    orientation = 'horizontal'
    assert is_valid_placement(board, x, y, ship_length, orientation) == False, "is_valid_placement function does not correctly check if ship goes off the board when orientated horizontally"

def test_is_valid_placement_overlap_horizontal():
    """
    Test if the is_valid_placement function correctly checks if a ship overlaps with another ship.
    """
    board = [[None, None, None],
             [None, 'ship', None],
             [None, None, None]]
    ship_length = 3
    x = 1
    y = 1
    orientation = 'horizontal'
    assert is_valid_placement(board, x, y, ship_length, orientation) == False, "is_valid_placement function does not correctly check if ship overlaps with another ship when orientated horizontally"

def test_is_valid_placement_overlap_vertical():
    """
    Test if the is_valid_placement function correctly checks if a ship overlaps with another ship.
    """
    board = [[None, None, None],
             [None, 'ship', None],
             [None, None, None]]
    ship_length = 3
    x = 1
    y = 0
    orientation = 'vertical'
    assert is_valid_placement(board, x, y, ship_length, orientation) == False, "is_valid_placement function does not correctly check if ship overlaps with another ship when orientated vertically"

def test_random_battleship_placement():
    """
    Test if the random_battleship_placement function correctly places battleships on the board.
    """
    random.seed(0) #ensures that the random boards created are always the same

    board = [[None, None, None],
             [None, None, None],
             [None, None, None]]
    battleships = {'ship1': 3, 'ship2': 2}
    new_board = random_battleship_placement(board, battleships)
    assert new_board == board, "random_battleship_placement function does not place battleships on the board"
    assert len(new_board) == len(board), "random_battleship_placement function changes the size of the board"
    for row in new_board:
        assert len(row) == len(board[0]), "random_battleship_placement function changes the size of the board"
        for cell in row:
            assert cell is None or isinstance(cell, str), "random_battleship_placement function places invalid values on the board"
import random
from typing import List, Dict

def test_place_battleship_on_board_horizontal():
    """
    Test if the place_battleship_on_board function correctly places a battleship horizontally on the board.
    """
    board = [[None, None, None, None],
             [None, None, None, None],
             [None, None, None, None],
             [None, None, None, None]]
    x = 1
    y = 1
    ship_length = 3
    ship_name = 'ship1'
    orientation = 'horizontal'
    expected_board = [[None, None, None, None],
                      [None, 'ship1', 'ship1', 'ship1'],
                      [None, None, None, None],
                      [None, None, None, None]]
    assert place_battleship_on_board(board, x, y, ship_length, ship_name, orientation) == expected_board, "place_battleship_on_board function does not correctly place a battleship horizontally"

def test_place_battleship_on_board_vertical():
    """
    Test if the place_battleship_on_board function correctly places a battleship vertically on the board.
    """
    board = [[None, None, None],
             [None, None, None],
             [None, None, None],
             [None, None, None]]
    x = 1
    y = 1
    ship_length = 3
    ship_name = 'ship1'
    orientation = 'vertical'
    expected_board = [[None, None, None],
                      [None, 'ship1', None],
                      [None, 'ship1', None],
                      [None, 'ship1', None]]
    assert place_battleship_on_board(board, x, y, ship_length, ship_name, orientation) == expected_board, "place_battleship_on_board function does not correctly place a battleship vertically"

def test_place_battleship_on_board_invalid_orientation():
    """
    Test if the place_battleship_on_board function raises a ValueError for an invalid orientation.
    """
    board = [[None, None, None],
             [None, None, None],
             [None, None, None]]
    x = 1
    y = 1
    ship_length = {'ship1': 3}
    ship_name = 'ship1'
    orientation = 'diagonal'
    try:
        place_battleship_on_board(board, x, y, ship_length, ship_name, orientation)
        assert False, "place_battleship_on_board function should raise a ValueError for an invalid orientation"
    except ValueError:
        assert True, "place_battleship_on_board function correctly raises a ValueError for an invalid orientation"

def test_place_battleship_on_board_invalid_placement():
    """
    Test if the place_battleship_on_board function returns -1 for an invalid placement.
    """
    board = [[None, None, None],
             [None, 'ship1', None],
             [None, None, None]]
    x = 1
    y = 1
    ship_length = 3
    ship_name = 'ship1'
    orientation = 'horizontal'
    assert place_battleship_on_board(board, x, y, ship_length, ship_name, orientation) == -1, "place_battleship_on_board function does not correctly return -1 for an invalid placement"

def test_place_battleship_on_board_out_of_bounds():
    """
    Test if the place_battleship_on_board function returns -1 for a placement that goes off the board.
    """
    board = [[None, None, None],
             [None, None, None],
             [None, None, None]]
    x = 2
    y = 1
    ship_length = 3
    ship_name = 'ship1'
    orientation = 'horizontal'
    assert place_battleship_on_board(board, x, y, ship_length, ship_name, orientation) == -1, "place_battleship_on_board function does not correctly return -1 for a placement that goes off the board"

def test_place_battleship_on_board_multiple_ships():
    """
    Test if the place_battleship_on_board function correctly places multiple battleships on the board.
    """
    board = [[None, None, None],
             [None, None, None],
             [None, None, None]]
    x = 0
    y = 0
    ship_length = {'ship1': 3, 'ship2': 2}
    ship_name = 'ship1'
    orientation = 'horizontal'
    expected_board = [['ship1', 'ship1', 'ship1'],
                      [None, None, None],
                      [None, None, None]]
    assert place_battleship_on_board(board, x, y, ship_length[ship_name], ship_name, orientation) == expected_board, "place_battleship_on_board function does not correctly place multiple battleships on the board"

    x = 1
    y = 1
    ship_name = 'ship2'
    orientation = 'vertical'
    expected_board = [['ship1', 'ship1', 'ship1'],
                      [None, 'ship2', None],
                      [None, 'ship2', None]]
    assert place_battleship_on_board(board, x, y, ship_length[ship_name], ship_name, orientation) == expected_board, "place_battleship_on_board function does not correctly place multiple battleships on the board"