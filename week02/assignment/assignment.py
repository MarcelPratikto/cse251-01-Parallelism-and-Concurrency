"""
Course: CSE 251 
Lesson Week: 02
File: assignment.py 
Author: Brother Comeau

Purpose: Retrieve Star Wars details from a server

Instructions:

- Each API call must only retrieve one piece of information
- You are not allowed to use any other modules/packages except for the ones used
  in this assignment.
- Run the server.py program from a terminal/console program.  Simply type
  "python server.py"
- The only "fixed" or hard coded URL that you can use is TOP_API_URL.  Use this
  URL to retrieve other URLs that you can use to retrieve information from the
  server.
- You need to match the output outlined in the decription of the assignment.
  Note that the names are sorted.
- You are requied to use a threaded class (inherited from threading.Thread) for
  this assignment.  This object will make the API calls to the server. You can
  define your class within this Python file (ie., no need to have a seperate
  file for the class)
- Do not add any global variables except for the ones included in this program.

The call to TOP_API_URL will return the following Dictionary(JSON).  Do NOT have
this dictionary hard coded - use the API call to get this.  Then you can use
this dictionary to make other API calls for data.

{
   "people": "http://127.0.0.1:8790/people/", 
   "planets": "http://127.0.0.1:8790/planets/", 
   "films": "http://127.0.0.1:8790/films/",
   "species": "http://127.0.0.1:8790/species/", 
   "vehicles": "http://127.0.0.1:8790/vehicles/", 
   "starships": "http://127.0.0.1:8790/starships/"
}
"""

from datetime import datetime, timedelta
import requests
import json
import threading

# Include cse 251 common Python files
from cse251 import *

# Const Values
TOP_API_URL = 'http://127.0.0.1:8790'

# Global Variables
call_count = 0


# Creates a thread that gets requests and stores response
class Threaded(threading.Thread):
  def __init__(self, url):
    threading.Thread.__init__(self)
    self.url = url
    self.response = {}

  def run(self):
    global call_count
    call_count += 1    
    response = requests.get(self.url)
    # Check the status code to see if the request succeeded.
    if response.status_code == 200:
      self.response = response.json()
    else:
      print('RESPONSE = ', response.status_code)

# retrieve_data (not multi-thread)
def retrieve_data(url):
  req = Threaded(url)
  req.start()
  req.join()
  return req.response

# retrieve data (multi-thread)
def retrieve_data_multiple(data, name):
  threads = []
  num = len(data)
  arr = []
  for i in range(num):    
    threads.append(Threaded(data[i]))    
  for i in range(len(threads)):
    threads[i].start()    
  for i in range(len(threads)):
    threads[i].join()
    dat = threads[i].response
    arr.append(dat[name])
  return arr

# convert items in array to one long string
def to_string(arr):
  temp_string = ""
  for item in arr:
    temp_string += item + ", "
  return temp_string

# MAIN
def main():
  log = Log(show_terminal=True)
  log.start_timer('Starting to retrieve data from the server')
  log.write("-----------------------------------------")    

  # Retrieve Top API urls
  top_url = retrieve_data(TOP_API_URL)
  # print(top_url)

  # Retrieve Details on film 6
  film_num = 6
  film_data = retrieve_data(f"{top_url['films']}{film_num}")
  # print(film_6)
  
  title = film_data['title']
  director = film_data['director']
  producer = film_data['producer']
  released = film_data['release_date']
  
  # get data from film
  characters = retrieve_data_multiple(film_data['characters'], 'name')
  characters.sort()
  planets = retrieve_data_multiple(film_data['planets'], 'name')
  planets.sort()
  starships = retrieve_data_multiple(film_data['starships'], 'name')
  starships.sort()
  vehicles = retrieve_data_multiple(film_data['vehicles'], 'name')
  vehicles.sort()
  species = retrieve_data_multiple(film_data['species'], 'name')
  species.sort()

  # Display results
  log.write(f"Title   : {title}")
  log.write(f"Director: {director}")
  log.write(f"Producer: {producer}")
  log.write(f"Released: {released}")
  log.write()

  log.write(f"Characters: {len(characters)}")
  log.write(to_string(characters))
  log.write()

  log.write(f"Planets: {len(planets)}")
  log.write(to_string(planets))
  log.write()

  log.write(f"Starships: {len(starships)}")
  log.write(to_string(starships))
  log.write()

  log.write(f"Vehicles: {len(vehicles)}")
  log.write(to_string(vehicles))
  log.write()

  log.write(f"Species: {len(species)}")
  log.write(to_string(species))
  log.write()

  log.stop_timer('Total Time To complete')
  log.write(f'There were {call_count} calls to the server')
    

if __name__ == "__main__":
    main()
