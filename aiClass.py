"""
AI Module

This module defines the mainAI class, which represents an AI opponent for the Battleships game. 
The AI is designed to make strategic moves based on the hits and misses recorded during the game. 
It uses various methods to determine the optimal next move, including searching around hits and 
generating placement counts for potential ship positions.

Classes:
    - `mainAI`: Represents the AI opponent with methods for generating attacks, 
                registering hits and misses, 
                and determining the next move.

Functions:
    - `check_if_in_bounds(x: int, y: int, length: int, orientation: str) -> bool`: 
        Checks if placing a ship at a given position and orientation is within 
        the bounds of the game board.

    - `create_placement_count(ship_length: int) -> dict[tuple[int, int], int]`: 
        Creates a placement count dictionary for a given ship length, indicating 
        potential ship positions on the board.

    - `add_NSEW_to_queue(coord: tuple[int, int]) -> None`: 
        Adds the North, South, East, and West coordinates of
        a hit to the queue for further exploration.

    - `generate_hit_search() -> tuple[int, int]`: 
        Generates a search coordinate based on the placement counts of ships.

    - `new_next_move(ships: dict[str, int]) -> tuple[int, int]`: 
        Determines the next move, either from the end of the queue 
        or using the optimal search coordinate.

    - `add_hit(coord: tuple[int, int]) -> None`: 
        Adds a hit coordinate to the list of hits and updates the queue with NSEW coordinates.

    - `add_miss(coord: tuple[int, int]) -> None`: 
        Adds a miss coordinate to the list of misses.

    - `register_shot(coord: tuple[int, int], hit: bool) -> None`: 
        Registers a shot, updating the hits and misses lists based on the result.

    - `check_if_offset_in_list(x: int, y: int, ship_length: int, 
                                orientation: str, data: list) -> bool`: 
        Checks if the offset of a ship position is present in a given list of data.

Usage:
    - To instantiate the mainAI class with a board size of 10 and a time limit of 5 seconds:
        ```
        ai_opponent = mainAI(size=10, time_allowed=5)
        ```

    - To generate the next move based on the current ship configuration:
        ```
        next_move = ai_opponent.new_next_move(ships={'ship1': 3, 'ship2': 2})
        ```

    - To register a hit at coordinates (3, 4):
        ```
        ai_opponent.add_hit((3, 4))
        ```

    - To check if a ship of length 3 can be placed at coordinate (0, 0) horizontally:
        ```
        is_valid = ai_opponent.check_if_in_bounds(0, 0, 3, 'horizontal')
        ```
"""


import time
from components import create_battleships



class mainAI:
    '''
    this class represents the main AI opponent for the battleships game
    '''

    def __init__(self,size:int,time_allowed:int=5,hits:list[tuple[int,int]] = None,
                 misses:list[tuple[int,int]] = None):
        '''
        this function initialises the AI
        Args:
            size (int): the size of the board
            time_allowed (int): the time allowed for the AI to make a move
            hits (list): the list of hits
            misses (list): the list of misses
        '''
        self.size = size
        if hits is None:
            hits = []
        self.hits = hits

        if misses is None:
            misses = []
        self.misses = misses
        self.ships = create_battleships()
        self.start = time.time()
        self.time_allowed = time_allowed
        self.queue =[]

    def check_if_in_bounds(self,x:int,y:int,length:int,orientation:str)->bool:
        '''
        this function checks if the ship is in bounds
        Args:
            x (int): the x coordinate of the ship
            y (int): the y coordinate of the ship
            length (int): the length of the ship
            orientation (str): the orientation of the ship
        Returns:
            bool: True if the ship is in bounds, False if not
            '''
        if orientation == 'horizontal':
            if x+length > self.size:
                return False
        else:
            if y+length > self.size:
                return False
        return True

    def create_placement_count(self,ship_length:int)->dict[tuple[int,int],int]:
        '''
        places a ship on the board
        Args:
            ship_length (int): the length of the ship
        Returns:
            dict[tuple[int,int],int]: the dictionary of coordinates and their counts
        '''
        # creates a dictionary of all the coordinates,counts set to 0
        count ={(x,y):0 for x in range(self.size) for y in range(self.size)}
        for y in range(self.size):
            for x in range(self.size):
                if (x,y) in self.hits or (x,y) in self.misses:
                    #if the coordinate has been hit or missed, it cannot be a ship,
                    #so we skip it
                    continue
                for o in ['horizontal','vertical']:
                    if (self.check_if_in_bounds(x,y,ship_length,o) is False
                        or self.check_if_offset_in_list(x,y,ship_length,o,self.misses) is False
                        or self.check_if_offset_in_list(x,y,ship_length,o,self.hits) is False):
                        # if the ship is out of bounds or the offset is in the misses list,
                        # or the hits list,
                        # it cannot be a ship, so we skip it
                        continue
                    else:
                        for i in range(ship_length):
                            if o == 'horizontal':
                                count[(x+i,y)] +=1 # add 1 to the count of the coordinate

                            else:
                                count[(x,y+i)]+=1
        return count

    def add_NSEW_to_queue(self,coord:tuple[int,int]):
        '''
        this function adds the NSEW coordinates to the queue
        so that the AI can search around the hit
        Args:
            coord (tuple[int,int]): the coordinates of the hit
        Returns:
            None

        '''
        x,y = coord
        # add each north east south west of the hit to the queue, as long as it is within
        # the bounds of the board and has not been hit or missed before
        if x+1 < self.size and (x+1,y) not in self.hits and (x+1,y) not in self.misses:
            self.queue.append((x+1,y))
        if x-1 >= 0 and (x-1,y) not in self.hits and (x-1,y) not in self.misses:
            self.queue.append((x-1,y))
        if y+1 < self.size and (x,y+1) not in self.hits and (x,y+1) not in self.misses:
            self.queue.append((x,y+1))
        if y-1 >= 0 and (x,y-1) not in self.hits and (x,y-1) not in self.misses:
            self.queue.append((x,y-1))
    def generate_hit_search(self):
        '''
        this function generates a random attack that has not been used before
        Args:
            previous_attacks (list): the list of previous attacks
            size (int): the size of the board
        Returns:
            tuple[int,int]: the coordinates of the attack
        '''
        counts = []
        for ship_length in self.ships.values():
            counts.append(self.create_placement_count(ship_length))
        added_counts = {coord:0 for coord in counts[0]} #creates a dictionary of all the coordinates
                                                        #where their count is 0
        # add the counts together
        for count in counts:
            for coord in count:
                added_counts[coord]+=count[coord]
        return max(added_counts,key=added_counts.get) # finds the max value in the dictionary

    def new_next_move(self,ships)->tuple[int,int]:
        ''' 

        this function generates next attack,
        it is the end of the queue if it is not empty
        or the optimal search coordinate if it is empty
        Args:
            ships (dict): the dictionary of ships remaining
        '''
        self.ships = ships
        if len(self.queue) ==0:
            # there are no moves in the queue, so search for new leads
            return self.generate_hit_search()
        else:
            coord = self.queue.pop(0)# take from the front of the queue
        return coord
    def add_hit(self,coord:tuple[int,int]):
        '''adds coord to the list of coords hit and adds the NSEW coords to the queue to be searched
        Args:
            coord (tuple[int,int]): the coordinates of the hit'''
        self.hits.append(coord)
        self.add_NSEW_to_queue(coord)
    def add_miss(self,coord:tuple[int,int]):
        '''adds coord to the list of coords missed
        Args:
            coord (tuple[int,int]): the coordinates of the miss'''
        self.misses.append(coord)
    def register_shot(self,coord:tuple[int,int],hit:bool):
        '''registers the shot
        Args:
            coord (tuple[int,int]): the coordinates of the shot
            hit (bool): True if the shot was a hit, False if not'''

        if hit is True:
            self.add_hit(coord)
        else:
            self.add_miss(coord)
    def check_if_offset_in_list(self,x,y,ship_length,orientation,data):
        '''
        this function checks if the offset of the ship is in the list
        Args:
            x (int): the x coordinate of the ship
            y (int): the y coordinate of the ship
            ship_length (int): the length of the ship
            orientation (str): the orientation of the ship
            data (list): the list of data to check against
        Returns:
            bool: True if the offset is not in the list, False if it is
        '''
        for offset in range(ship_length+1): #this may need putting to ship_length+1
            if orientation == 'horizontal':
                if (x+offset,y) in data:
                    return False
            else:
                if (x,y+offset) in data:
                    return False
        return True
