"""
Course: CSE 251
Lesson Week: 06
File: assignment.py
Author: Marcel Pratikto
Purpose: Processing Plant
Instructions:
- Implement the classes to allow gifts to be created.
"""

import random
import multiprocessing as mp
import os.path
import time
import datetime

# Include cse 251 common Python files - Don't change
from cse251 import *

CONTROL_FILENAME = 'settings.txt'
BOXES_FILENAME   = 'boxes.txt'

# Settings consts
MARBLE_COUNT = 'marble-count'
CREATOR_DELAY = 'creator-delay'
BAG_COUNT = 'bag-count'
BAGGER_DELAY = 'bagger-delay'
ASSEMBLER_DELAY = 'assembler-delay'
WRAPPER_DELAY = 'wrapper-delay'
END_MESSAGE = "!!!NO MORE!!!"

# No Global variables

class Bag():
    """ bag of marbles - Don't change """

    def __init__(self):
        self.items = []

    def add(self, marble):
        self.items.append(marble)

    def get_size(self):
        return len(self.items)

    def __str__(self):
        return str(self.items)


class Gift():
    """ Gift of a large marble and a bag of marbles - Don't change """

    def __init__(self, large_marble, marbles):
        self.large_marble = large_marble
        self.marbles = marbles

    def __str__(self):
        marbles = str(self.marbles)
        marbles = marbles.replace("'", "")
        return f'Large marble: {self.large_marble}, marbles: {marbles[1:-1]}'


class Marble_Creator(mp.Process):
    """ This class "creates" marbles and sends them to the bagger """

    colors = ('Gold', 'Orange Peel', 'Purple Plum', 'Blue', 'Neon Silver', 
        'Tuscan Brown', 'La Salle Green', 'Spanish Orange', 'Pale Goldenrod', 'Orange Soda', 
        'Maximum Purple', 'Neon Pink', 'Light Orchid', 'Russian Violet', 'Sheen Green', 
        'Isabelline', 'Ruby', 'Emerald', 'Middle Red Purple', 'Royal Orange', 'Big Dip O’ruby', 
        'Dark Fuchsia', 'Slate Blue', 'Neon Dark Green', 'Sage', 'Pale Taupe', 'Silver Pink', 
        'Stop Red', 'Eerie Black', 'Indigo', 'Ivory', 'Granny Smith Apple', 
        'Maximum Blue', 'Pale Cerulean', 'Vegas Gold', 'Mulberry', 'Mango Tango', 
        'Fiery Rose', 'Mode Beige', 'Platinum', 'Lilac Luster', 'Duke Blue', 'Candy Pink', 
        'Maximum Violet', 'Spanish Carmine', 'Antique Brass', 'Pale Plum', 'Dark Moss Green', 
        'Mint Cream', 'Shandy', 'Cotton Candy', 'Beaver', 'Rose Quartz', 'Purple', 
        'Almond', 'Zomp', 'Middle Green Yellow', 'Auburn', 'Chinese Red', 'Cobalt Blue', 
        'Lumber', 'Honeydew', 'Icterine', 'Golden Yellow', 'Silver Chalice', 'Lavender Blue', 
        'Outrageous Orange', 'Spanish Pink', 'Liver Chestnut', 'Mimi Pink', 'Royal Red', 'Arylide Yellow', 
        'Rose Dust', 'Terra Cotta', 'Lemon Lime', 'Bistre Brown', 'Venetian Red', 'Brink Pink', 
        'Russian Green', 'Blue Bell', 'Green', 'Black Coral', 'Thulian Pink', 
        'Safety Yellow', 'White Smoke', 'Pastel Gray', 'Orange Soda', 'Lavender Purple',
        'Brown', 'Gold', 'Blue-Green', 'Antique Bronze', 'Mint Green', 'Royal Blue', 
        'Light Orange', 'Pastel Blue', 'Middle Green')

    def __init__(self, creator_parent, marble_count, creator_delay):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.creator_parent = creator_parent
        self.marble_count = marble_count
        self.creator_delay = creator_delay

    def run(self):
        '''
        for each marble:
            send the marble (one at a time) to the bagger
              - A marble is a random name from the colors list above
            sleep the required amount
        Let the bagger know there are no more marbles
        '''
        for _ in range(self.marble_count):
            marble = random.choice(Marble_Creator.colors)
            #send to bagger
            self.creator_parent.send(marble)
            time.sleep(self.creator_delay)
        #let bagger know there are no more marbles
        self.creator_parent.send(END_MESSAGE)
        self.creator_parent.close()


class Bagger(mp.Process):
    """ Receives marbles from the marble creator, then there are enough
        marbles, the bag of marbles are sent to the assembler """
    def __init__(self, creator_child, bagger_parent, bag_count, bagger_delay):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.creator_child = creator_child
        self.bagger_parent = bagger_parent
        self.bag_count = bag_count
        self.bagger_delay = bagger_delay

    def run(self):
        '''
        while there are marbles to process
            collect enough marbles for a bag
            send the bag to the assembler
            sleep the required amount
        tell the assembler that there are no more bags
        '''
        bag_of_marbles = []
        marble = self.creator_child.recv()
        while marble != END_MESSAGE:
            if len(bag_of_marbles) < self.bag_count:
                bag_of_marbles.append(marble)
            marble = self.creator_child.recv()
        # send bag to assembler
        self.bagger_parent.send(bag_of_marbles)
        time.sleep(self.bagger_delay)
        self.bagger_parent.send(END_MESSAGE)
        self.bagger_parent.close()


class Assembler(mp.Process):
    """ Take the set of marbles and create a gift from them.
        Sends the completed gift to the wrapper """
    marble_names = ('Lucky', 'Spinner', 'Sure Shot', 'The Boss', 'Winner', '5-Star', 'Hercules', 'Apollo', 'Zeus')

    def __init__(self, bagger_child, assembler_parent, assembler_delay):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.bagger_child = bagger_child
        self.assembler_parent = assembler_parent
        self.assembler_delay = assembler_delay

    def run(self):
        '''
        while there are bags to process
            create a gift with a large marble (random from the name list) and the bag of marbles
            send the gift to the wrapper
            sleep the required amount
        tell the wrapper that there are no more gifts
        '''
        bag_marbles = self.bagger_child.recv()
        while bag_marbles != END_MESSAGE:
            gift = Gift(random.choice(Assembler.marble_names), bag_marbles)
            self.assembler_parent.send(gift)
            time.sleep(self.assembler_delay)
            bag_marbles = self.bagger_child.recv()
        self.assembler_parent.send(END_MESSAGE)
        self.assembler_parent.close()
        

class Wrapper(mp.Process):
    """ Takes created gifts and wraps them by placing them in the boxes file """
    def __init__(self, assembler_child, num_gifts, wrapper_delay):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.assembler_child = assembler_child
        self.num_gifts = num_gifts
        self.wrapper_delay = wrapper_delay

    def run(self):
        '''
        open file for writing
        while there are gifts to process
            save gift to the file with the current time
            sleep the required amount
        '''
        with open(BOXES_FILENAME, "w") as boxes_file:
            gift = self.assembler_child.recv()
            while gift != END_MESSAGE:
                boxes_file.write(
                    f"Created - {datetime.now().time()}: Large marble: {gift.large_marble}, marbles: {gift.marbles}"
                )
                self.num_gifts += 1
                time.sleep(self.wrapper_delay)
                gift = self.assembler_child.recv()


def display_final_boxes(filename, log):
    """ Display the final boxes file to the log file -  Don't change """
    if os.path.exists(filename):
        log.write(f'Contents of {filename}')
        with open(filename) as boxes_file:
            for line in boxes_file:
                log.write(line.strip())
    else:
        log.write_error(f'The file {filename} doesn\'t exist.  No boxes were created.')



def main():
    """ Main function """

    log = Log(show_terminal=True)

    log.start_timer()

    # Load settings file
    settings = load_json_file(CONTROL_FILENAME)
    if settings == {}:
        log.write_error(f'Problem reading in settings file: {CONTROL_FILENAME}')
        return
    marble_count = settings[MARBLE_COUNT]
    creator_delay = settings[CREATOR_DELAY]
    bag_count = settings[BAG_COUNT]
    bagger_delay = settings[BAGGER_DELAY]
    assembler_delay = settings[ASSEMBLER_DELAY]
    wrapper_delay = settings[WRAPPER_DELAY]

    log.write(f'Marble count                = {settings[MARBLE_COUNT]}')
    log.write(f'settings["creator-delay"]   = {settings[CREATOR_DELAY]}')
    log.write(f'settings["bag-count"]       = {settings[BAG_COUNT]}') 
    log.write(f'settings["bagger-delay"]    = {settings[BAGGER_DELAY]}')
    log.write(f'settings["assembler-delay"] = {settings[ASSEMBLER_DELAY]}')
    log.write(f'settings["wrapper-delay"]   = {settings[WRAPPER_DELAY]}')

    # TODO: create Pipes between creator -> bagger -> assembler -> wrapper
    creator_parent, creator_child = mp.Pipe()
    bagger_parent, bagger_child = mp.Pipe()
    assembler_parent, assembler_child = mp.Pipe()
    #wrapper_parent, wrapper_child = mp.Pipe()

    # TODO create variable to be used to count the number of gifts
    num_gifts = 0

    # delete final boxes file
    if os.path.exists(BOXES_FILENAME):
        os.remove(BOXES_FILENAME)

    log.write('Create the processes')
    # TODO Create the processes (ie., classes above)
    marble_creator = Marble_Creator(creator_parent, marble_count, creator_delay)
    bagger = Bagger(creator_child, bagger_parent, bag_count, bagger_delay)
    assembler = Assembler(bagger_child, assembler_parent, assembler_delay)
    wrapper = Wrapper(assembler_child, num_gifts, wrapper_delay)

    log.write('Starting the processes')
    # TODO add code here
    marble_creator.start()
    bagger.start()
    assembler.start()
    wrapper.start()

    log.write('Waiting for processes to finish')
    # TODO add code here
    marble_creator.join()
    bagger.join()
    assembler.join()
    wrapper.join()

    display_final_boxes(BOXES_FILENAME, log)

    # TODO Log the number of gifts created.
    log.write(f"number of gifts created:    = {num_gifts}")


if __name__ == '__main__':
    main()

