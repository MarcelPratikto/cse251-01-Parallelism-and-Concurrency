"""
Course: CSE 251
Lesson Week: 04
File: assignment.py
Author: Marcel Pratikto

Purpose: Assignment 04 - Factory and Dealership

Instructions:

- See I-Learn
https://github.com/byui-cse/cse251-course/blob/master/week04/prove.md

"""

import time
import threading
import random

# Include cse 251 common Python files
from cse251 import *

# Global Consts - Do not change
CARS_TO_PRODUCE = 500
MAX_QUEUE_SIZE = 10
SLEEP_REDUCE_FACTOR = 50

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

        # Display the car that has just be created in the terminal
        self.display()
           
    def display(self):
        print(f'{self.make} {self.model}, {self.year}')


class Queue251():
    """ This is the queue object to use for this assignment. Do not modify!! """

    def __init__(self):
        self.items = []

    def size(self):
        return len(self.items)

    def put(self, item):
        self.items.append(item)

    def get(self):
        return self.items.pop(0)


class Factory(threading.Thread):
    """ This is a factory.  It will create cars and place them on the car queue """

    def __init__(self, queue, sem_factory, sem_dealer, queue_stats):
        # you need to add arguments that will pass all of data that 1 factory needs to create cars and to place them in a queue.
        super().__init__()
        self.queue = queue
        self.sem_factory = sem_factory
        self.sem_dealer = sem_dealer
        # self.thread = threading.Thread(target=self.run, args=())
        self.queue_stats = queue_stats

    def run(self):
        for i in range(CARS_TO_PRODUCE):            
            """
            create a car
            place the car on the queue
            signal the dealer that there is a car on the queue
            """
            self.sem_factory.acquire()                       
            car = Car()            
            self.queue.put(car)
            self.sem_dealer.release()      
        # signal the dealer that there there are not more cars
        print("There are no more cars!")
        self.queue.put("nocars")


class Dealer(threading.Thread):
    """ This is a dealer that receives cars """

    def __init__(self, queue, sem_factory, sem_dealer, queue_stats):
        # you need to add arguments that pass all of data that 1 Dealer needs to sell a car
        super().__init__()
        self.queue = queue
        self.sem_factory = sem_factory
        self.sem_dealer = sem_dealer
        # self.thread = threading.Thread(target=self.run, args=())
        self.queue_stats = queue_stats

    def run(self):
        while True:
            """
            take the car from the queue
            signal the factory that there is an empty slot in the queue
            """
            size = self.queue.size()
            self.queue_stats[size-1] += 1
            if size > 0:                
                self.sem_factory.release()
                car = self.queue.get()
                if car == "nocars":
                    pass
                print(f"car: {car.make} {car.model} {car.year}")
                self.sem_dealer.acquire()

            # Sleep a little after selling a car
            # Last statement in this for loop - don't change
            time.sleep(random.random() / (SLEEP_REDUCE_FACTOR))



def main():
    log = Log(show_terminal=True)

    # Create semaphore(s)
    sem_factory = threading.Semaphore(MAX_QUEUE_SIZE)
    sem_dealer = threading.Semaphore(0)

    # Create queue251 
    q251 = Queue251()

    # Create lock(s)?
    lock = threading.Lock()

    # This tracks the length of the car queue during receiving cars by the dealership
    # i.e., update this list each time the dealer receives a car
    queue_stats = [0] * MAX_QUEUE_SIZE

    # create your one factory
    factory = Factory(q251, sem_factory, sem_dealer, queue_stats)

    # create your one dealership
    dealer = Dealer(q251, sem_factory, sem_dealer, queue_stats)

    # keep track of time?
    log.start_timer()

    # Start factory and dealership
    # factory.run()
    # dealer.run()
    # factory.thread.start()
    # dealer.thread.start()
    factory.start()
    dealer.start()

    # Wait for factory and dealership to complete
    factory.join()
    dealer.join()

    log.stop_timer(f'All {sum(queue_stats)} have been created')

    xaxis = [i for i in range(1, MAX_QUEUE_SIZE + 1)]
    plot = Plots()
    plot.bar(xaxis, queue_stats, title=f'{sum(queue_stats)} Produced: Count VS Queue Size', x_label='Queue Size', y_label='Count')



if __name__ == '__main__':
    main()
