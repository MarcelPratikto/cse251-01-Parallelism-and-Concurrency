"""
Course: CSE 251
Lesson Week: 07
File: assingnment.py
Author: Marcel Pratikto
Purpose: Process Task Files

Instructions:  See I-Learn

TODO
Add your comments here on the pool sizes that you used for your assignment and
why they were the best choices.

TEST
I started with 4:
Then went to 8:
Then 16: 
Then 20:


"""

from datetime import datetime, timedelta
import requests
import multiprocessing as mp
from matplotlib.pylab import plt
import numpy as np
import glob
import math 

# Include cse 251 common Python files - Dont change
from cse251 import *

TYPE_PRIME  = 'prime'
TYPE_WORD   = 'word'
TYPE_UPPER  = 'upper'
TYPE_SUM    = 'sum'
TYPE_NAME   = 'name'

# Global lists to collect the task results
result_primes = []
result_words = []
result_upper = []
result_sums = []
result_names = []

def is_prime(n: int):
    """Primality test using 6k+-1 optimization.
    From: https://en.wikipedia.org/wiki/Primality_test
    """
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i ** 2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True
 
def task_prime(value):
    """
    Use the is_prime() above
    Add the following to the global list:
        {value} is prime
            - or -
        {value} is not prime
    """
    if is_prime(value):
        result_primes.append(f"{value} is prime")
    else:
        result_primes.append(f"{value} is not prime")

def task_word(word):
    """
    search in file 'words.txt'
    Add the following to the global list:
        {word} Found
            - or -
        {word} not found *****
    """
    with open("words.txt", "r") as file: # auto closes without having to close()
        file_content = [line.rstrip() for line in file]
        word_found = False
        if word in file_content:
            word_found = True
        #print(f"file_content {file_content}")
        print(f"word_found: {word_found}")
        if word_found:
            result_words.append(f"{word} Found")
        else:
            result_words.append(f"{word} not found *****")

def task_upper(text):
    """
    Add the following to the global list:
        {text} ==>  uppercase version of {text}
    """
    result_upper.append(f"{text.upper()} ==> uppercase version of {text}")

def task_sum(start_value, end_value):
    """
    Add the following to the global list:
        sum of {start_value:,} to {end_value:,} = {total:,}
    """
    total = 0
    for i in range(start_value, end_value+1):
        total += i
    result_sums.append(total)

def task_name(url):
    """
    use requests module
    Add the following to the global list:
        {url} has name <name>
            - or -
        {url} had an error receiving the information
    """
    request = requests.get(url)
    content = request.json()
    print(f"content: {content}")
    name = content["name"]
    print(f"name: {name}")
    if request.ok:
        result_names.append(f"{url} has name {name}")

def main():
    log = Log(show_terminal=True)
    log.start_timer()

    # TODO Create process pools
    # pools = []
    # for i in range(4):
    #     pools.append(mp.Pool)
    pool = mp.Pool(4)

    count = 0
    task_files = glob.glob("*.task")
    for filename in task_files:
        # print()
        # print(filename)
        task = load_json_file(filename)
        print(task)
        count += 1
        task_type = task['task']
        if task_type == TYPE_PRIME:
            task_prime(task['value'])
        elif task_type == TYPE_WORD:
            task_word(task['word'])
        elif task_type == TYPE_UPPER:
            task_upper(task['text'])
        elif task_type == TYPE_SUM:
            task_sum(task['start'], task['end'])
        elif task_type == TYPE_NAME:
            task_name(task['url'])
        else:
            log.write(f'Error: unknown task type {task_type}')

    # TODO start and wait pools
    pool.close()
    pool.join()

    # Do not change the following code (to the end of the main function)
    def log_list(lst, log):
        for item in lst:
            log.write(item)
        log.write(' ')
    
    log.write('-' * 80)
    log.write(f'Primes: {len(result_primes)}')
    log_list(result_primes, log)

    log.write('-' * 80)
    log.write(f'Words: {len(result_words)}')
    log_list(result_words, log)

    log.write('-' * 80)
    log.write(f'Uppercase: {len(result_upper)}')
    log_list(result_upper, log)

    log.write('-' * 80)
    log.write(f'Sums: {len(result_sums)}')
    log_list(result_sums, log)

    log.write('-' * 80)
    log.write(f'Names: {len(result_names)}')
    log_list(result_names, log)

    log.write(f'Number of Primes tasks: {len(result_primes)}')
    log.write(f'Number of Words tasks: {len(result_words)}')
    log.write(f'Number of Uppercase tasks: {len(result_upper)}')
    log.write(f'Number of Sums tasks: {len(result_sums)}')
    log.write(f'Number of Names tasks: {len(result_names)}')
    log.stop_timer(f'Finished processes {count} tasks')

if __name__ == '__main__':
    main()
