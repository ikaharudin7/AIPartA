"""
COMP30024 Artificial Intelligence, Semester 1, 2022
Project Part A: Searching
This script contains the entry point to the program (the code in
`__main__.py` calls `main()`). Your solution starts here!
"""
from collections import defaultdict
from pickle import FALSE
from queue import PriorityQueue
import sys
import json


# If you want to separate your code into separate files, put them
# inside the `search` directory (like this one and `util.py`) and
# then import from them like this:
from search.util import board_dict, print_board, print_coordinate

# CONSTANTS
STEP_SIZE = 1

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

    # Dictionary contating positions of each hex
    board = board_dict(data)

    # Establish variables from the JSON file
    size = data.get("n")
    start = data.get("start")
    goal = data.get("goal")

    # A* search function
    cost = A_star(size, start, goal, board)
    print(cost)
    print_board(size, board, message="", ansi=False)




# Calculates the start and goal by taking in the coordinates as lists 
# in [r, q] format.
def calc_heuristic(start, goal):
    r1 = start[0]
    q1 = start[1]
    r2 = goal[0]
    q2 = goal[1]

    # If heading top right or bottom left direction, use Manhattan distance
    if (q2 >= q1 and r2 >= r1 or q2 <= q1 and r2 <= r1):
        prediction = abs(q2 - q1) + abs(r2 - r1)
    # If goal is to the left of the start...
    else:
        prediction = max(abs(q2 - q1), abs(r2 - r1))

    return prediction + STEP_SIZE

# Conducts A_star search (unfinished)
def A_star(size, start, goal, board):
    # Define the priority queues and list of traversed nodes
    q = []
    traversed = []
    found = False
    complete = False
    threshold = 0
    solution = []
    solution_cost = 0

    # Keep track of which hexes have been travelled to / blocked
    for key in board:
        traversed.append(key)
    
    curr = start
    cost = 1
    q.append((calc_heuristic(curr, goal), (curr, cost)))

    # Loop through traversals until optimal goal state is found 
    while not complete and len(q) > 0:
        # Sort the hexagons by fn value
        q = sorted(q, key=lambda tup: tup[0])
        
        # Get the hexagon with the minimum fn value. 
        curr_tuple = q[0]
        curr = curr_tuple[1][0]
        cost = curr_tuple[1][1]
        solution.append(curr_tuple)

        # Generate the possible branches from the current node
        neighbours = generate_branch(curr, size, traversed)

        cost += 1
        # If a path has been found, and the the heurstic + cost > the 
        # current goal's cost, get rid of it in the queue
        if found:
            if q[0][0] >= threshold:
                q.pop(q.index(curr_tuple))
            continue

        
        # Insert neighbours of current node into the queues. 
        for neighbour in neighbours:
            
            # Add which nodes have been travelled through
            traversed.append(neighbour)

            # Functin to using the heuristic (-1 as it counts the current hex's cost 2x)
            fn = cost + calc_heuristic(neighbour, goal) - STEP_SIZE
            q.append((fn, (neighbour, cost)))
            
            # If the neighbour is the goal, record the solution_cost
            if neighbour == (goal[0], goal[1]):
                threshold = fn
                found = True
                solution_cost = cost

        q.pop(q.index(curr_tuple))
        print(solution)
    return solution_cost
            


    

# Generate the possible branches from that node
def generate_branch(curr, size, traversed):
    branches = []
    max = size
    min = 0

    r1 = curr[0]
    q1 = curr[1]

    # Add possible branches into the branches list (Just brute force as there are only 6)
    if r1 - 1 >= min and (r1 - 1, q1) not in traversed:
        branches.append((r1 - 1, q1))

    if r1 + 1 < max  and (r1 + 1, q1) not in traversed:
        branches.append((r1 + 1, q1))
    
    if q1 - 1 >= min and (r1, q1 - 1) not in traversed:
        branches.append((r1, q1 - 1))
    
    if q1 + 1 < max and (r1, q1 + 1) not in traversed:
        branches.append((r1, q1 + 1))

    if q1 + 1 < max and r1 - 1 >= min and (r1 - 1, q1 + 1) not in traversed:
        branches.append((r1 - 1, q1 + 1))

    if q1 - 1 >= min and r1 + 1 < max and (r1 + 1, q1 - 1) not in traversed:
        branches.append((r1 + 1, q1 - 1))

    return branches

# Takes the data and transforms the board into a dictionary with keys
# as the tuple, and colour as the value. 
def board_dict(data):
    board = defaultdict()

    # Iterate through list and assign dictionary values
    for list in data.get("board"):
        tuple = (list[1], list[2])
        board[tuple] = list[0]
    return board