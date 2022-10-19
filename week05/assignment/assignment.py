"""
Course: CSE 251
Lesson Week: 05
File: assignment.py
Author: Marcel Pratikto

Purpose: Assignment 05 - Factories and Dealers

Instructions:

- Read the comments in the following code.  
- Implement your code where the TODO comments are found.
- No global variables, all data must be passed to the objects.
- Only the included/imported packages are allowed.  
- Thread/process pools are not allowed
- You are not allowed to use the normal Python Queue object.  You must use Queue251.
- the shared queue between the threads that are used to hold the Car objects
  can not be greater than MAX_QUEUE_SIZE

"""

from datetime import datetime, timedelta
from multiprocessing import Semaphore
import multiprocessing
import time
import threading
import random

# Include cse 251 common Python files
from cse251 import *

# Global Consts
MAX_QUEUE_SIZE = 10
SLEEP_REDUCE_FACTOR = 50
#CARS_TO_CREATE_PER_FACTORY = 500 # based on week04 assignment, not needed?
FACTORY_FINISHED_MESSAGE = "!done!"

# NO GLOBAL VARIABLES!

class Car():
    """ This is the Car class that will be created by the factories """

    # Class Variables
    car_makes = ('Ford', 'Chevrolet', 'Dodge', 'Fiat', 'Volvo', 'Infiniti', 'Jeep', 'Subaru', 
                'Buick', 'Volkswagen', 'Chrysler', 'Smart', 'Nissan', 'Toyota', 'Lexus', 
                'Mitsubishi', 'Mazda', 'Hyundai', 'Kia', 'Acura', 'Honda')

    car_models = ('A1', 'M1', 'XOX', 'XL', 'XLS', 'XLE' ,'Super' ,'Tall' ,'Flat', 'Middle', 'Round',
                'A2', 'M1X', 'SE', 'SXE', 'MM', 'Charger', 'Grand', 'Viper', 'F150', 'Town', 'Ranger',
                'G35', 'Titan', 'M5', 'GX', 'Sport', 'RX')

    car_years = [i for i in range(1990, datetime.now().year)]

    def __init__(self):
        # Make a random car
        self.model = random.choice(Car.car_models)
        self.make = random.choice(Car.car_makes)
        self.year = random.choice(Car.car_years)

        # Sleep a little.  Last statement in this for loop - don't change
        time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))

        # Display the car that has was just created in the terminal
        #self.display()
           
    def display(self):
        print(f'{self.make} {self.model}, {self.year}')


class Queue251():
    """ This is the queue object to use for this assignment. Do not modify!! """

    def __init__(self):
        self.items = []
        self.max_size = 0

    def get_max_size(self):
        return self.max_size

    def put(self, item):
        self.items.append(item)
        if len(self.items) > self.max_size:
            self.max_size = len(self.items)

    def get(self):
        return self.items.pop(0)


class Factory(threading.Thread):
    """ This is a factory.  It will create cars and place them on the car queue """

    def __init__(self, car_queue, sem_available_slots, barrier_factory, num_dealers):
        super().__init__()
        self.cars_to_produce = random.randint(200, 300)     # Don't change
        self.sem_available_slots = sem_available_slots        
        self.car_queue = car_queue
        self.barrier = barrier_factory
        self.num_dealers = num_dealers

    def run(self):
        # TODO produce the cars, then send them to the dealerships
        print(f"PRODUCING {self.cars_to_produce} CARS")
        for i in range(self.cars_to_produce):
            self.car_queue.put(Car())
            self.sem_available_slots.release()
        #print(self.car_queue)
        # TODO wait until all of the factories are finished producing cars
        self.barrier.wait()
        # TODO "Wake up/signal" the dealerships one more time.  Select one factory to do this
        print("FINISHED MAKING CARS!!!")
        for _ in range(self.num_dealers):
            self.car_queue.put(FACTORY_FINISHED_MESSAGE)
            self.sem_available_slots.release()
            self.num_dealers -= 1



class Dealer(threading.Thread):
    """ This is a dealer that receives cars """

    def __init__(self, car_queue, sem_available_slots):
        super().__init__()
        self.cars_recv = 0
        self.car_queue = car_queue
        self.sem_available_slots = sem_available_slots

    def run(self):
        while True:
            # TODO handle a car            
            if self.sem_available_slots.acquire():                
                car = self.car_queue.get()                
                #print(f"{car}")
                if car == FACTORY_FINISHED_MESSAGE:
                    print("FINISHED GETTING CARS!!!") 
                    return                   
                self.cars_recv += 1
            # else:
            #     car = self.car_queue.get()                
            #     print(f"{car}")
            #     if car == FACTORY_FINISHED_MESSAGE:
            #         print("FINISHED GETTING CARS!!!")
            #         return
            # Sleep a little - don't change.  This is the last line of the loop
            time.sleep(random.random() / (SLEEP_REDUCE_FACTOR + 0))



def run_production(factory_count, dealer_count):
    """ This function will do a production run with the number of
        factories and dealerships passed in as arguments.
    """
    # TODO Create semaphore(s)
    sem_available_slots = Semaphore(0)
    # TODO Create queue
    car_queue = Queue251()
    # Create lock(s)
    lock = threading.Lock()
    # Create barrier(s)
    barrier_factory = multiprocessing.Barrier(factory_count)
    barrier_dealer = multiprocessing.Barrier(dealer_count)

    # This is used to track the number of cars receives by each dealer
    dealer_stats = list([0] * dealer_count)
    # This is used to track the number of cars each factory produces
    factory_stats = list([0] * factory_count)

    # TODO create your factories, each factory will create CARS_TO_CREATE_PER_FACTORY
    # It will actually create a random amount of cars, 200-300    
    factories = [Factory(car_queue, sem_available_slots, barrier_factory, dealer_count) for x in range(factory_count)]

    # TODO create your dealerships
    dealers = [Dealer(car_queue, sem_available_slots) for x in range(dealer_count)]

    log.start_timer()

    # TODO Start all factories
    for factory in factories:
        factory.start()

    # TODO Start all dealerships
    for dealer in dealers:
        dealer.start()

    time.sleep(1)   # make sure all dealers have time to start

    

    # TODO Wait for factories and dealerships to complete
    for dealer in dealers:
        dealer.join()
    for factory in factories:
        factory.join()

    dealer_index = 0
    for dealer in dealers:
        dealer_stats[dealer_index] = dealer.cars_recv
        dealer_index += 1
    run_time = log.stop_timer(f'{sum(dealer_stats)} cars have been created')
    
    factory_index = 0
    for factory in factories:
        factory_stats[factory_index] = factory.cars_to_produce
        factory_index += 1

    # This function must return the following - Don't change!
    # factory_stats: is a list of the number of cars produced by each factory.
    #                collect this information after the factories are finished. 
    return (run_time, car_queue.get_max_size(), dealer_stats, factory_stats)


def main(log):
    """ Main function - DO NOT CHANGE! """

    runs = [(1, 1), (1, 2), (2, 1), (2, 2), (2, 5), (5, 2), (10, 10)]
    for factories, dealerships in runs:
        run_time, max_queue_size, dealer_stats, factory_stats = run_production(factories, dealerships)

        log.write(f'Factories      : {factories}')
        log.write(f'Dealerships    : {dealerships}')
        log.write(f'Run Time       : {run_time:.4f}')
        log.write(f'Max queue size : {max_queue_size}')
        log.write(f'Factor Stats   : {factory_stats}')
        log.write(f'Dealer Stats   : {dealer_stats}')
        log.write('')

        # The number of cars produces needs to match the cars sold
        assert sum(dealer_stats) == sum(factory_stats)


if __name__ == '__main__':

    log = Log(show_terminal=True)
    main(log)


