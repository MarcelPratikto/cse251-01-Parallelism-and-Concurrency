"""
Course: CSE 251 
Lesson Week: 09
File: assignment09-p1.py 
Author: Marcel Pratikto

Purpose: Part 1 of assignment 09, finding a path to the end position in a maze

Instructions:
- Do not create classes for this assignment, just functions
- Do not use any other Python modules other than the ones included

"""
import math
from screen import Screen
from maze import Maze
import cv2
import sys

# Include cse 251 common Python files - Dont change
from cse251 import *

SCREEN_SIZE = 800
COLOR = (0, 0, 255)


# TODO add any functions
def using_recursion(maze, path, coord):
    # When given new coordinate, move there.
    # Append new coordinates to path.
    # If it's the right path that leads to the end, it will stay
    # otherwise it will be removed by this function.
    x = coord[0]
    y = coord[1]
    maze.move(x,y,COLOR)
    #print(f"moved to ({x},{y})")
    path.append((x,y))
    if maze.at_end(x, y):
        #print("CONGRATS, YOU'VE REACHED THE END!!!")
        return True
    
    # If there are no possible moves:
    # maze.restore, pop from path, return False
    # If there are possible moves, call this function again with the new coordinates
    # Store the result from the recursive calls
    # If end is not found:
    # maze.restore, pop from path, return False
    # If end is found:
    # break out of the loop going through all the possible moves
    # simply return True
    possible_moves = maze.get_possible_moves(x,y)
    if len(possible_moves) == 0:
        maze.restore(x, y)
        path.pop()
        return False
    for coordinate in possible_moves:
        new_x = coordinate[0]
        new_y = coordinate[1]
        if maze.can_move_here(new_x,new_y):
            end_found = using_recursion(maze, path, (new_x, new_y))
            if end_found:
                break
            #print(f"end = {end}")
    if not end_found:
        maze.restore(x, y)
        path.pop()
        return False
    else:
        return True
            
    

def solve_path(maze):
    """ Solve the maze and return the path found between the start and end positions.  
        The path is a list of positions, (x, y) """
    # TODO start add code here
    path = []

    coord_start = maze.get_start_pos()
    #print(f"coord_start: {coord_start}")
    using_recursion(maze, path, coord_start)
    #print(f"path: {path}")

    return path


def get_path(log, filename):
    """ Do not change this function """

    # create a Screen Object that will contain all of the drawing commands
    screen = Screen(SCREEN_SIZE, SCREEN_SIZE)
    screen.background((255, 255, 0))

    maze = Maze(screen, SCREEN_SIZE, SCREEN_SIZE, filename)

    path = solve_path(maze)

    log.write(f'Number of drawing commands for = {screen.get_command_count()}')

    done = False
    speed = 1
    while not done:
        if screen.play_commands(speed): 
            key = cv2.waitKey(0)
            if key == ord('+'):
                speed = max(0, speed - 1)
            elif key == ord('-'):
                speed += 1
            elif key != ord('p'):
                done = True
        else:
            done = True

    return path


def find_paths(log):
    """ Do not change this function """

    files = ('verysmall.bmp', 'verysmall-loops.bmp', 
            'small.bmp', 'small-loops.bmp', 
            'small-odd.bmp', 'small-open.bmp', 'large.bmp', 'large-loops.bmp')

    log.write('*' * 40)
    log.write('Part 1')
    for filename in files:
        log.write()
        log.write(f'File: {filename}')
        path = get_path(log, filename)
        log.write(f'Found path has length          = {len(path)}')
    log.write('*' * 40)


def main():
    """ Do not change this function """
    sys.setrecursionlimit(5000)
    log = Log(show_terminal=True)
    find_paths(log)


if __name__ == "__main__":
    main()