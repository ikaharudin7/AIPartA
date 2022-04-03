"""
COMP30024 Artificial Intelligence, Semester 1, 2022
Project Part A: Searching

This script contains the entry point to the program (the code in
`__main__.py` calls `main()`). Your solution starts here!
"""
from collections import defaultdict
from pickle import FALSE
from queue import PriorityQueue
from re import I
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
    start = (data.get("start")[0], data.get("start")[1])
    goal = (data.get("goal")[0], data.get("goal")[1])

    # Create a list for storing all nodes in various branches, from the start
    # first index is the node itself as a tuple coordinate
    # second index is whether it has been traversed(1) or not(0)
    # third index is the value of f(n)
    branch_nodes = [[start, 0, calc_heuristic(start, goal)]] 

    # create a list to hold the shortest path found
    shortest_path = []

    curr = start 
    # perform find_shortest_path(size, board, start, goal, curr, branch_nodes, shortest_path)
    print(find_shortest_path(size, board, start, goal, curr, branch_nodes, shortest_path))
    print(branch_nodes)
    print_board(size, board, message="", ansi=False)


# Checks if the given node is found in the branch_nodes list, returning the index if found, else -1
def check_in_branch_nodes(node, branch_nodes): 
    in_or_not = -1
    i = 0
    for elem in branch_nodes:
        if (elem[0] == node):
            in_or_not = i 
            break
        i = i + 1
    return in_or_not

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

    return prediction


# Takes the data and transforms the board into a dictionary with keys
# as the tuple, and colour as the value. 
def board_dict(data):
    board = defaultdict()

    # Iterate through list and assign dictionary values
    for list in data.get("board"):
        coordinate = (list[1], list[2])
        board[coordinate] = list[0]
    return board

# returns a node's neighbours, on the grid 
def neighbours_on_grid(node, size):
    r1 = node[0]
    q1 = node[1]
    min = 0 
    max = size - 1

    # there are at most 6 neighbours of any given node 
    all_neighbours = [(r1,q1-1), (r1,q1+1), (r1-1,q1), (r1-1,q1+1), (r1+1,q1), (r1+1,q1-1)]
    on_grid = [] # the neighbours which are on the grid
    for neighbour in all_neighbours:
        if (neighbour[0] > max or neighbour[0] < min or neighbour[1] > max or neighbour[1] < min):
            continue
        on_grid.append(neighbour)
    return on_grid

# checks to see if this node is blocked
def node_is_blocked(node, board):
    blocked_nodes = [] 
    is_blocked = 0
    for elem in board:
        blocked_nodes.append(elem)

    for coordinate in blocked_nodes:
        if (coordinate == node):
            is_blocked = 1

    return is_blocked

# Returns a list containing the shortest path 
def find_shortest_path(size, board, start, goal, curr, branch_nodes, shortest_path):
    new_curr = () 
    if (curr == goal): # we have reached the end of the path 
        shortest_path.append(curr)
        j = check_in_branch_nodes(curr, branch_nodes)
        branch_nodes[j][1] = 1 # mark this node as traversed
        return shortest_path 

    else: 
        # these are the neighbours on the grid
        on_grid = neighbours_on_grid(curr, size)
        # set a list of the feasible neighbours of the current node
        possible_neighbours = []

        for neighbour in on_grid:
            if (check_in_branch_nodes(neighbour,branch_nodes) != -1):
                continue 
            if (node_is_blocked(neighbour, board) == 1):
                continue
            else:
                possible_neighbours.append(neighbour)

        # if no neighbours feasible...
        if (len(possible_neighbours) == 0):
            i = check_in_branch_nodes(curr, branch_nodes)
            branch_nodes.pop(i)
            if (len(branch_nodes) >= i + 1): 
                new_curr = branch_nodes[i][0]
            else: 
                new_curr = branch_nodes[i-1][0]

        else: 
            shortest_path.append(curr)
            j = check_in_branch_nodes(curr, branch_nodes)
            branch_nodes[j][1] = 1 # mark this node as traversed 
            g_n = len(shortest_path) # the path cost to get from the start node to these neighbours
            priority_queue = []

            for neighbour in possible_neighbours: 
                priority_queue.append((g_n+calc_heuristic(neighbour, goal), neighbour))
            priority_queue.sort()

            # append this onto branch_nodes in order of priority
            for elem in priority_queue:
                node = [elem[1], 0, elem[0]]
                branch_nodes.append(node)
            new_curr = priority_queue[0][1]
    
    return find_shortest_path(size, board, start, goal, new_curr, branch_nodes, shortest_path)
    