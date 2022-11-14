"""
Course: CSE 251 
Lesson Week: 09
File: assignment09-p2.py 
Author: Marcel Pratikto

Purpose: Part 2 of assignment 09, finding the end position in the maze

Instructions:
- Do not create classes for this assignment, just functions
- Do not use any other Python modules other than the ones included
- Each thread requires a different color by calling get_color()


This code is not interested in finding a path to the end position,
However, once you have completed this program, describe how you could 
change the program to display the found path to the exit position.

What would be your strategy?  

I would add another parameter to the recursive function
that stores the coordinates that the thread has gone through.
I would also add a boolean return value for the recursive function.
If the function returns True, keep the stored coordinates.
If not, pop the coordinates.


Why would it work?

It would work because the parameter that stores the path
would only keep the coordinates that leads to the end.
It might not be in order, but that is an issue for another day.

"""
import math
import threading 
from screen import Screen
from maze import Maze
import sys
import cv2

# Include cse 251 common Python files - Dont change
from cse251 import *

SCREEN_SIZE = 800
COLOR = (0, 0, 255)
COLORS = (
    (0,0,255),
    (0,255,0),
    (255,0,0),
    (255,255,0),
    (0,255,255),
    (255,0,255),
    (128,0,0),
    (128,128,0),
    (0,128,0),
    (128,0,128),
    (0,128,128),
    (0,0,128),
    (72,61,139),
    (143,143,188),
    (226,138,43),
    (128,114,250)
)

# Globals
current_color_index = 0
thread_count = 0
stop = False

def get_color():
    """ Returns a different color when called """
    global current_color_index
    if current_color_index >= len(COLORS):
        current_color_index = 0
    color = COLORS[current_color_index]
    current_color_index += 1
    return color

# TODO
"""
When a thread comes to a fork or division in the maze, 
it will create a thread for each path except for one. 
The thread that found the fork in the path will take one of the paths. 
The other paths will be searched by the newly created threads. 
When one of the threads finds the end position, 
that thread needs to stop all other threads. 
Recursion is required for this part of the assignment.
"""
def solve_using_threads_recursion(maze, coord, color, threads):
    global stop
    
    # start maze at the coordinate given
    x,y = coord
    if maze.can_move_here(x,y):
        maze.move(x,y,color)
    else:
        return
    # When end position is found,
    # this thread needs to stop all other threads
    if maze.at_end(x,y):
        # global stop
        stop = True
        return

    # if end is not reached:
    # 1. Loop until there's a fork in the path
    found_fork = False
    possible_moves = []
    while not found_fork:
        # if another thread has already found the end, STOP
        if stop:
            return
        possible_moves = maze.get_possible_moves(x,y)
        # if there is only 1 possible move,
        # check to see if we can move there,
        # then move there
        if len(possible_moves) == 1:
            x,y = possible_moves[0]
            if maze.can_move_here(x,y):
                maze.move(x,y,color)
        # if there is no possible moves,
        # then this thread is finished, return
        elif len(possible_moves) == 0:
            return
        # if there is not 0 or 1 possible moves,
        # then a fork in the path is found
        else:
            found_fork = True
            break
    # 2. If there's a fork in the path,
    # check to see which of them is accessible.
    # Create a new thread for each accessible path,
    # one will be using the current thread,
    # the rest will be run using new threads
    if found_fork:
        run_original_thread = False
        for i in range(0,len(possible_moves)):
            next_x,next_y = possible_moves[i]
            if maze.can_move_here(next_x,next_y):
                if not run_original_thread:
                    solve_using_threads_recursion(maze,possible_moves[i],color,threads)
                    run_original_thread = True
                else:
                    new_thread = threading.Thread(target=solve_using_threads_recursion,args=(maze,possible_moves[i],get_color(),threads))
                    threads.append(new_thread)
                    new_thread.start()
        

# TODO the function to solve
def solve_find_end(maze):
    """ finds the end position using threads.  Nothing is returned """
    # everytime we run this function to solve for a maze,
    # make sure that stop is False.
    # it will turn true once a thread founds the end of the maze.
    global stop
    stop = False
    
    start_coord = maze.get_start_pos()
    threads = []

    original_thread = threading.Thread(target=solve_using_threads_recursion,args=(maze,start_coord,get_color(),threads))
    threads.append(original_thread)
    original_thread.start()
    
    # join all threads created
    for thread in threads:
        thread.join()

    # threads holds all of the thread created
    global thread_count
    thread_count = len(threads)


def find_end(log, filename, delay):
    """ Do not change this function """

    global thread_count

    # create a Screen Object that will contain all of the drawing commands
    screen = Screen(SCREEN_SIZE, SCREEN_SIZE)
    screen.background((255, 255, 0))

    maze = Maze(screen, SCREEN_SIZE, SCREEN_SIZE, filename, delay=delay)

    solve_find_end(maze)

    log.write(f'Number of drawing commands = {screen.get_command_count()}')
    log.write(f'Number of threads created  = {thread_count}')

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



def find_ends(log):
    """ Do not change this function """

    files = (
        ('verysmall.bmp', True),
        ('verysmall-loops.bmp', True),
        ('small.bmp', True),
        ('small-loops.bmp', True),
        ('small-odd.bmp', True),
        ('small-open.bmp', False),
        ('large.bmp', False),
        ('large-loops.bmp', False)
    )

    log.write('*' * 40)
    log.write('Part 2')
    for filename, delay in files:
        log.write()
        log.write(f'File: {filename}')
        find_end(log, filename, delay)
    log.write('*' * 40)


def main():
    """ Do not change this function """
    sys.setrecursionlimit(5000)
    log = Log(show_terminal=True)
    find_ends(log)



if __name__ == "__main__":
    main()