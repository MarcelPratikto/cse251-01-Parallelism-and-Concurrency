"""
------------------------------------------------------------------------------
Course: CSE 251
Lesson Week: 03
File: assignment.py
Author: Marcel Pratikto

Purpose: Video Frame Processing

Instructions:

- Follow the instructions found in Canvas for this assignment
- No other packages or modules are allowed to be used in this assignment.
  Do not change any of the from and import statements.
- Only process the given MP4 files for this assignment

------------------------------------------------------------------------------
"""

from matplotlib.pylab import plt  # load plot library
from PIL import Image
import numpy as np
import timeit
import multiprocessing as mp
import threading

# Include cse 251 common Python files
from cse251 import *

# 4 more than the number of cpu's on your computer
CPU_COUNT = mp.cpu_count() + 4 
#CPU_COUNT = 4 

# TODO Your final video need to have 300 processed frames.  However, while you are 
# testing your code, set this much lower
FRAME_COUNT = 20

RED   = 0
GREEN = 1
BLUE  = 2


def create_new_frame(image_file, green_file, process_file):
    """ Creates a new image file from image_file and green_file """

    # this print() statement is there to help see which frame is being processed
    #print(f'{process_file[-7:-4]}', end=',', flush=True)

    image_img = Image.open(image_file)
    green_img = Image.open(green_file)

    # Make Numpy array
    np_img = np.array(green_img)

    # Mask pixels 
    mask = (np_img[:, :, BLUE] < 120) & (np_img[:, :, GREEN] > 120) & (np_img[:, :, RED] < 120)

    # Create mask image
    mask_img = Image.fromarray((mask*255).astype(np.uint8))

    image_new = Image.composite(image_img, green_img, mask_img)
    image_new.save(process_file)


# TODO add any functions to need here
def separate_process(num_cores, num_img):
  total_per_core = num_img // num_cores + 1
  print("\n")
  print(f"total_per_core: {total_per_core}")
  r = []
  tracker = 1
  while tracker < num_img+1:
    start = tracker
    end = tracker + total_per_core
    if end >= num_img:
      end = num_img
    r.append((start, end))
    tracker = end + 1
  print(f"r: {r}")

  # p = []
  # for i in range(len(r)):
  #   p.append(mp.Process(target=merge_img_green, args=r[i]))
  # for core in p:
  #   core.start()
  # for core in p:
  #   core.join()
  with mp.Pool(num_cores) as p: 
    for i in range(len(r)):
      merge_img_green(r[i][0], r[i][1])

def merge_img_green(start, end):
  p = []
  for image_number in range(start, end+1):
    image_file = rf'elephant/image{image_number:03d}.png'
    green_file = rf'green/image{image_number:03d}.png'
    process_file = rf'processed/image{image_number:03d}.png'
    p.append(threading.Thread(target=create_new_frame, args=(image_file, green_file, process_file)))
  for thread in p:
    thread.start()
  for thread in p:
    thread.join()


if __name__ == '__main__':
    
    # single_file_processing(300)
    # print('cpu_count() =', cpu_count())

    all_process_time = timeit.default_timer()
    log = Log(show_terminal=True)

    xaxis_cpus = []
    yaxis_times = []

    num_img = 0
    for img in os.scandir("elephant"):
      num_img += 1

    # TODO Process all frames trying 1 cpu, then 2, then 3, ... to CPU_COUNT
    #      add results to xaxis_cpus and yaxis_times
    for i in range(1, CPU_COUNT+1):
      start = timeit.default_timer() - all_process_time
      separate_process(i, num_img)
      end = timeit.default_timer() - all_process_time
      total_time = end - start
      #print(f"Time for {num_img} frames using {i} processes: {total_time}")
      log.write(f"Time for {num_img} frames using {i} processes: {total_time}")
      xaxis_cpus.append(i)
      yaxis_times.append(end - start)

    # sample code: remove before submitting  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # process one frame #10
    # image_number = 10

    # image_file = rf'elephant/image{image_number:03d}.png'
    # green_file = rf'green/image{image_number:03d}.png'
    # process_file = rf'processed/image{image_number:03d}.png'

    # start_time = timeit.default_timer()
    # create_new_frame(image_file, green_file, process_file)
    # print(f'\nTime To Process all images = {timeit.default_timer() - start_time}')
    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    log.write(f'Total Time for ALL processing: {timeit.default_timer() - all_process_time}')

    # create plot of results and also save it to a PNG file
    plt.plot(xaxis_cpus, yaxis_times, label=f'{FRAME_COUNT}')
    
    plt.title('CPU Core yaxis_times VS CPUs')
    plt.xlabel('CPU Cores')
    plt.ylabel('Seconds')
    plt.legend(loc='best')

    plt.tight_layout()
    plt.savefig(f'Plot for {FRAME_COUNT} frames.png')
    plt.show()
