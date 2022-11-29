"""
Course: CSE 251
Lesson Week: 11
File: Assignment.py
Author: Marcel Pratikto
"""

import time
import random
import multiprocessing as mp

# number of cleaning staff and hotel guests
CLEANING_STAFF = 2
HOTEL_GUESTS = 5

# number of people in the room
_count = 0

# Run program for this number of seconds
TIME = 60

STARTING_PARTY_MESSAGE =  'Turning on the lights for the party vvvvvvvvvvvvvv'
STOPPING_PARTY_MESSAGE  = 'Turning off the lights  ^^^^^^^^^^^^^^^^^^^^^^^^^^'

STARTING_CLEANING_MESSAGE =  'Starting to clean the room >>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
STOPPING_CLEANING_MESSAGE  = 'Finish cleaning the room <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'

def cleaner_waiting():
    time.sleep(random.uniform(0, 2))

def cleaner_cleaning(id):
    print(f'Cleaner {id}')
    time.sleep(random.uniform(0, 2))

def guest_waiting():
    time.sleep(random.uniform(0, 2))

def guest_partying(id):
    print(f'Guest {id}')
    time.sleep(random.uniform(0, 1))

#------------------------------------------------------------------------------------------------------------------------------------------
# CLEANER
#------------------------------------------------------------------------------------------------------------------------------------------
def cleaner(start_time, cleaned_count, id, lock_room):
    """
    do the following for TIME seconds
        cleaner will wait to try to clean the room (cleaner_waiting())
        get access to the room
        display message STARTING_CLEANING_MESSAGE
        Take some time cleaning (cleaner_cleaning())
        display message STOPPING_CLEANING_MESSAGE
    """
    time_end = start_time + TIME
    while time.time() < time_end:
        cleaner_waiting()
        lock_room.acquire()
        cleaned_count.value = cleaned_count.value + 1
        print(f"{STARTING_CLEANING_MESSAGE}")
        cleaner_cleaning(id)
        print(f"{STOPPING_CLEANING_MESSAGE}")
        lock_room.release()
            
#------------------------------------------------------------------------------------------------------------------------------------------
# GUEST
#------------------------------------------------------------------------------------------------------------------------------------------
def guest(start_time, party_count, id, lock_room, room_count):
    """
    do the following for TIME seconds
        guest will wait to try to get access to the room (guest_waiting())
        get access to the room
        display message STARTING_PARTY_MESSAGE if this guest is the first one in the room
        Take some time partying (guest_partying())
        display message STOPPING_PARTY_MESSAGE if the guest is the last one leaving in the room
    """
    time_end = start_time + TIME
    while time.time() < time_end:
        guest_waiting()
        room_count.acquire()
        if room_count.value == 0:
            lock_room.acquire()
            print(f"{STARTING_PARTY_MESSAGE}")
            party_count.value = party_count.value + 1
            
            room_count.value = room_count.value + 1
            room_count.release()
            
            guest_partying(id)
            
            room_count.acquire()
            room_count.value = room_count.value - 1
            if room_count.value == 0:
                print(f"{STOPPING_PARTY_MESSAGE}")
                lock_room.release()
            room_count.release()
        else:
            room_count.value = room_count.value + 1
            guest_partying(id)
            room_count.release()
            
            room_count.acquire()
            room_count.value = room_count.value - 1
            if room_count.value == 0:
                print(f"{STOPPING_PARTY_MESSAGE}")
                lock_room.release()
            room_count.release()
        


#------------------------------------------------------------------------------------------------------------------------------------------
# MAIN
#------------------------------------------------------------------------------------------------------------------------------------------
def main():
    # Start time of the running of the program. 
    start_time = time.time()

    # TODO - add any variables, data structures, processes you need
    cleaned_count = mp.Value('i', 0)
    party_count = mp.Value('i', 0)
    room_count = mp.Value('i', 0)
    
    lock_room = mp.Lock()

    # create separate processes for cleaners and guests
    # TODO - add any arguments to cleaner() and guest() that you need
    process_cleaners = []
    for id in range(CLEANING_STAFF):
        process = mp.Process(target=cleaner, args=(start_time, cleaned_count, id+1, lock_room))
        process_cleaners.append(process)
        process.start()

    process_guests = []
    for id in range(HOTEL_GUESTS):
        process = mp.Process(target=guest, args=(start_time, party_count, id+1, lock_room, room_count))
        process_guests.append(process)
        process.start()

    for process in process_cleaners:
        process.join()
    for process in process_guests:
        process.join()

    # Results
    print(f'Room was cleaned {cleaned_count.value} times, there were {party_count.value} parties')


if __name__ == '__main__':
    main()

