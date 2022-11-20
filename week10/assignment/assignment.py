"""
Course: CSE 251
Lesson Week: 10
File: assignment.py
Author: Marcel Pratikto

Purpose: assignment for week 10 - reader writer problem

Instructions:

- Review TODO comments

- writer: a process that will send numbers to the reader.  
  The values sent to the readers will be in consecutive order starting
  at value 1.  Each writer will use all of the sharedList buffer area
  (ie., BUFFER_SIZE memory positions)

- reader: a process that receive numbers sent by the writer.  The reader will
  accept values until indicated by the writer that there are no more values to
  process.  
  
- Display the numbers received by the reader printing them to the console.

- Create WRITERS writer processes

- Create READERS reader processes

- You can use sleep() statements for any process.

- You are able (should) to use lock(s) and semaphores(s).  When using locks, you can't
  use the arguments "block=False" or "timeout".  Your goal is to make your
  program as parallel as you can.  Over use of lock(s), or lock(s) in the wrong
  place will slow down your code.

- You must use ShareableList between the two processes.  This shareable list
  will contain different "sections".  There can only be one shareable list used
  between your processes.
  1) BUFFER_SIZE number of positions for data transfer. This buffer area must
     act like a queue - First In First Out.
  2) current value used by writers for consecutive order of values to send
  3) Any indexes that the processes need to keep track of the data queue
  4) Any other values you need for the assignment

- Not allowed to use Queue(), Pipe(), List() or any other data structure.

- Not allowed to use Value() or Array() or any other shared data type from 
  the multiprocessing package.

- When each reader reads a value from the sharedList, use the following code to display
  the value:
  
                    print(<variable>, end=', ', flush=True)

Add any comments for me:


"""
import random
from multiprocessing.managers import SharedMemoryManager
import multiprocessing as mp
import time

BUFFER_SIZE = 10
READERS = 2
WRITERS = 2
END_MESSAGE = -1
_items_read = 0

#--------------------------------------------------------------------------------------------------------
# target functions
#--------------------------------------------------------------------------------------------------------
def read_sl(reader_sem, writer_sem, sl):
  items_read = 0
  current_index = 0
  item = ''
  while item != END_MESSAGE:
    writer_sem.release()
    item = sl[current_index]
    if item == END_MESSAGE:
      break
    print(item, end=', ', flush=True)
    current_index += 1
    if current_index == BUFFER_SIZE:
      current_index = 0
    items_read += 1
    reader_sem.acquire()
  # store the amount of items read on the last position of the shared list
  sl[-1] = items_read


def write_sl(reader_sem, writer_sem, sl, items_to_send):
  current_index = 0
  for item in range(items_to_send):
    reader_sem.release()
    sl[current_index] = item
    current_index += 1
    if current_index == BUFFER_SIZE:
      current_index = 0
    writer_sem.acquire()
  # signal that we've created the required amount of items, END
  reader_sem.release()
  sl[current_index] = END_MESSAGE
  writer_sem.acquire()

#--------------------------------------------------------------------------------------------------------
# MAIN
#--------------------------------------------------------------------------------------------------------
def main():

    # This is the number of values that the writer will send to the reader
    items_to_send = random.randint(1000, 10000)

    smm = SharedMemoryManager()
    smm.start()

    # TODO - Create a ShareableList to be used between the processes
    sl = smm.ShareableList(range(BUFFER_SIZE))

    # TODO - Create any lock(s) or semaphore(s) that you feel you need
    reader_sem = mp.Semaphore(READERS)
    writer_sem = mp.Semaphore(WRITERS)

    # TODO - create reader and writer processes
    reader = mp.Process(target=read_sl, args=(reader_sem, writer_sem, sl))
    writer = mp.Process(target=write_sl, args=(reader_sem, writer_sem, sl, items_to_send))

    # TODO - Start the processes and wait for them to finish
    writer.start()
    time.sleep(0.05)
    reader.start()
    writer.join()
    reader.join()

    print()
    print(f'{items_to_send} values sent')

    # TODO - Display the number of numbers/items received by the reader.
    #        Can not use "items_to_send", must be a value collected
    #        by the reader processes.
    # print(f'{<your variable>} values received')
    print(f'{sl[-1]} values received')
    smm.shutdown()

if __name__ == '__main__':
    main()
