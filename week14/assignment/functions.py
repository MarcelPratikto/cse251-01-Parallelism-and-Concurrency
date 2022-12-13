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

First I got it working without threads
3 generations without threads: 16.42039 seconds

Then I created a new thread for each children
3 generations with threads: 5.31134
6 generations with threads: 13.11685

Then I added more base cases for the recursive function
and not add duplicate people to the tree

6 generations with threads: 8.52442, 8.28056, 7.37254

---------------------------------------------------------------------
Describe how to speed up part 2

First I got it working without threads
3 generations without threads: 20.66656 seconds
6 generations without threads: 26.74068

---------------------------------------------------------------------
10% Bonus to speed up part 3

<Add your comments here>

"""
from common import *

# get family (make call to server)
def req_family(id):
    # if id is None:
    #     return None
    family = Request_thread(f'{TOP_API_URL}/family/{id}')
    family.start()
    family.join()
    return family.response

# get person (make call to server)
def req_person(id):
    # if id is None:
    #     return None
    person = Request_thread(f'{TOP_API_URL}/person/{id}')
    person.start()
    person.join()
    return person.response

# -----------------------------------------------------------------------------
"""
https://en.wikipedia.org/wiki/Depth-first_search

Creates family in node
then goes to first child node,
repeat until a leaf is reached.
The recursion will return to its last position,
then go to the other child nodes.
"""
def depth_fs_pedigree(family_id, tree):
    # print(f"family_id: {family_id}")
    # recursive base case(s)
    if family_id is None:
        return
    if tree.does_family_exist(family_id):
        return

    # recursive step(s)
    # get family data by making a call to the server
    family_data = req_family(family_id)
    # print(f"FAMILY DATA {family_data}")
    if len(family_data) > 0:
        # add husband
        husband = Person(req_person(family_data['husband_id']))
        if husband is not None and not tree.does_person_exist(husband.id):
            tree.add_person(husband)
        # add wife
        wife = Person(req_person(family_data['wife_id']))
        if wife is not None and not tree.does_person_exist(wife.id):
            tree.add_person(wife)
        # add children
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
"""
https://en.wikipedia.org/wiki/Breadth-first_search

from the root,
iterate through each generation
until all leaves are reached.
"""
def add_family_to_tree(family_id, tree):
    if family_id is None:
        return {}
    if tree.does_family_exist(family_id):
        return {}
    family_data = req_family(family_id)
    if len(family_data) > 0:
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
    # print(f"family_id: {family_id}")
    # print(f"family_data: {family_data}")
    if len(family_data) > 0:
        family = Family(family_id, family_data)
        tree.add_family(family)
    # return the data of the family that was just added
    return family_data

def breadth_fs_pedigree(start_id, tree):
    # store the order of families, by generations
    # ex: {0:[family_0], 1:[family_1, family_2], ...}
    # ex: family_0 = {husband_id, wife_id, [child_0_id, ...]}
    # start with the root
    generations = {}
    generation = 0
    families_data = []
    families_data.append(add_family_to_tree(start_id, tree))
    generations[generation] = families_data
    #print(f"generation {generation} : {generations[generation]}")
    
    # iterate through all of root's children
    # before diving deeper into more child nodes TODO
    current_fam = 0
    current_node = generations[generation][current_fam]
    # print(f"current_node: {current_node}")
    # print(f"current_node['id']: {current_node['id']}")
    # print(f"current_node['children']: {current_node['children']}")
    # for child_id in current_node['children']:
    #     print(f"child_id: {child_id}")
    families_data = []
    stop_loop = False
    while not stop_loop:
        # if current_node['id'] is None:
        #     continue
        # if tree.does_family_exist(current_node['id']):
        #     continue
        for child_id in current_node['children']:
            family_data = add_family_to_tree(child_id, tree)
            if len(family_data) > 0:
                families_data.append(family_data)
        next_fam = current_fam + 1
        if next_fam < len(generations[generation]):
            current_fam = next_fam
        else:
            stop_loop = True
            for family in families_data:
                if len(family) > 0:
                    stop_loop = False
            if not stop_loop:
                generation += 1
                generations[generation] = families_data
                current_fam = 0
                families_data = []
                current_node = generations[generation][current_fam]

# -----------------------------------------------------------------------------
def breadth_fs_pedigree_limit5(start_id, tree):
    # TODO - implement breadth first retrieval
    #      - Limit number of concurrent connections to the FS server to 5

    print('WARNING: BFS (Limit of 5 threads) function not written')
    pass




"""
requesting a family from the server:
request = Request_thread(f'{TOP_API_URL}/family/{id}')
request.start()
request.join()
if request.status_code == 200:
    family = Family(request.response)
    tree.add_family(family)
example JSON returned from the server
{
    'id': ---,
    'husband_id': ---,
    'wife_id': ---,
    'children': [---,---,---,---,...]
}

requesting individual from the server:
request = Request_thread(f'{TOP_API_URL}/person/{id}')
{
    'id': 2373683567,
    'name': 'Stella',
    'birth': '9-3-1846',
    'parent_id': 5428641880,
    'family_id': 6128784944
}
"""