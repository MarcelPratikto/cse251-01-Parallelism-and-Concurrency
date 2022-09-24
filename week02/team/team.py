"""
Course: CSE 251
Lesson Week: 02 - Team Activity
File: team.py
Author: Brother Comeau

Purpose: Playing Card API calls

Instructions:

- Review instructions in I-Learn.

"""

from datetime import datetime, timedelta
import threading
import requests
import json

# Include cse 251 common Python files
from cse251 import *

# TODO Create a class based on (threading.Thread) that will
# make the API call to request data from the website

class Request_thread(threading.Thread):
    # TODO - Add code to make an API call and return the results
    # https://realpython.com/python-requests/
    pass

class Deck:

    def __init__(self, deck_id):
        self.id = deck_id
        self.reshuffle()
        self.remaining = 52


    def reshuffle(self):
        # TODO - add call to reshuffle
        pass

    def draw_card(self):
        # TODO add call to get a card
        response = requests.get(r'https://www.deckofcardsapi.com/api/deck/5bmte546oknh/pile/random/draw/?cards=AS')

        print(response)

        # # Check the status code to see if the request succeeded.
        # if response.status_code == 200:
        #     data = response.json()

        #     # Function is from the cse251 common code 
        #     print_dict(data)

        #     if 'success' in data:
        #         if data['success'] == True:
        #             print(data['remaining'])
        #         else:
        #             print('Error in requesting ID 1')
        #     else:
        #         print('Error in requesting ID 2')
        # else:
        #     print('Error in requesting ID 3')

        draw = response.json()
        print(draw)
        #self.remaining = draw["remaining"]
        #return draw["cards"]

    def cards_remaining(self):
        return self.remaining


    def draw_endless(self):
        if self.remaining <= 0:
            self.reshuffle()
        return self.draw_card()


if __name__ == '__main__':

    # TODO - run the program team_get_deck_id.py and insert
    #        the deck ID here.  You only need to run the 
    #        team_get_deck_id.py program once. You can have
    #        multiple decks if you need them

    deck_id = '5bmte546oknh'

    # Testing Code >>>>>
    deck = Deck(deck_id)
    for i in range(55):
        card = deck.draw_endless()
        print(i, card, flush=True)
    print()
    # <<<<<<<<<<<<<<<<<<

