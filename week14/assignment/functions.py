"""
Course: CSE 251, week 14
File: common.py
Author: Marcel Pratikto

Instructions:

Depth First Search
https://www.youtube.com/watch?v=9RHO6jU--GU

Breadth First Search
https://www.youtube.com/watch?v=86g8jAQug04


Requesting a family from the server:
family = Request_thread(f'{TOP_API_URL}/family/{id}')

Requesting an individual from the server:
person = Request_thread(f'{TOP_API_URL}/person/{id}')


You will lose 10% if you don't detail your part 1 
and part 2 code below

---------------------------------------------------------------------
Describe how to speed up part 1

First I created a new thread for each children

3 generations
Without threads: 16.42039 seconds
With threads: 5.31134
6 generations
With threads: 7.95897, 13.11685

Then I added more base cases for the recursive function
and not add duplicate people to the tree

6 generations
with threads: 8.52442, 8.28056

---------------------------------------------------------------------
Describe how to speed up part 2

<Add your comments here>

---------------------------------------------------------------------
10% Bonus to speed up part 3

<Add your comments here>

"""
from common import *

# get family (make call to server)
def req_family(id):
    family = Request_thread(f'{TOP_API_URL}/family/{id}')
    family.run()
    return family.response

# get person (make call to server)
def req_person(id):
    person = Request_thread(f'{TOP_API_URL}/person/{id}')
    person.run()
    return person.response

# -----------------------------------------------------------------------------
""" TODO
Goes to the children first until end is reached
then returns back to parents
"""
def depth_fs_pedigree(family_id, tree):
    # recursive base case(s)
    if family_id is None:
        return
    if tree.does_family_exist(family_id):
        return

    # recursive step(s)
    # get family data by making a call to the server
    family_data = req_family(family_id)
    #print(f"FAMILY DATA {family_data}")
    if len(family_data) > 0:
        # add husband, wife, and children to tree
        husband = Person(req_person(family_data['husband_id']))
        if husband is not None and not tree.does_person_exist(husband.id):
            tree.add_person(husband)
        wife = Person(req_person(family_data['wife_id']))
        if wife is not None and not tree.does_person_exist(wife.id):
            tree.add_person(wife)
        children = []
        for child_id in family_data['children']:
            child = Person(req_person(child_id))
            if child is not None and not tree.does_person_exist(child.id):
                tree.add_person(child)
                children.append(child)
            
        # add family to tree
        family = Family(family_id, family_data)
        tree.add_family(family)

        # for each children, recursively call this function until tree completion
        threads = []
        for child in children:
            #depth_fs_pedigree(child.id, tree)
            thread = threading.Thread(target=depth_fs_pedigree, args=(child.id, tree))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()

# -----------------------------------------------------------------------------
def breadth_fs_pedigree(start_id, tree):
    # TODO - implement breadth first retrieval

    print('WARNING: BFS function not written')
    pass


# -----------------------------------------------------------------------------
def breadth_fs_pedigree_limit5(start_id, tree):
    # TODO - implement breadth first retrieval
    #      - Limit number of concurrent connections to the FS server to 5

    print('WARNING: BFS (Limit of 5 threads) function not written')
    pass
