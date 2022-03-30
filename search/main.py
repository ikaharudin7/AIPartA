"""
COMP30024 Artificial Intelligence, Semester 1, 2022
Project Part A: Searching

This script contains the entry point to the program (the code in
`__main__.py` calls `main()`). Your solution starts here!
"""
from collections import defaultdict
import sys
import json

# If you want to separate your code into separate files, put them
# inside the `search` directory (like this one and `util.py`) and
# then import from them like this:
from search.util import print_board, print_coordinate

def main():
    try:
        with open(sys.argv[1]) as file:
            data = json.load(file)
    except IndexError:
        print("usage: python3 -m search path/to/input.json", file=sys.stderr)
        sys.exit(1)

    # TODO:
    # Find and print a solution to the board configuration described
    # by `data`.
    # Why not start by trying to print this configuration out using the
    # `print_board` helper function? (See the `util.py` source code for
    # usage information).

    # Dictionary contating positions of each hex
    board = board_dict(data)
    size = data.get("n")

    


    print_board(size, board, message="", ansi=False)



# Takes the data and transforms the board into a dictionary with keys
# as the tuple, and colour as the value. 
def board_dict(data):
    board = defaultdict()
    for list in data.get("board"):
        tuple = (list[1], list[2])
        board[tuple] = list[0]
    return board