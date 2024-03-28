###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name:
# Collaborators:
# Time:

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    # TODO: Your code here
    cows = {}
    with open(filename, 'r') as file:
        for line in file:
            vals = line.split(sep=',')
            cows[vals[0]] = vals[1].split('\n')[0]
    return cows

# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # TODO: Your code here
    #create sorted dict. using lambda expr. as key function, element is a item from dictionary
    #element[0] - name, elemnet[1] - weight
    #sort from the heaviest to lightest
    sorted_cows = {key : val for key, val in sorted(cows.items(), key=lambda element: element[1], reverse=True)}

    course = []
    whole_plan = []
    load = 0
    
    for i in range(len(sorted_cows)):
        for add in sorted_cows.keys():
            #curent load + next cow
            if load + int(sorted_cows[add]) <= limit:
                course.append(add)
                load += int(sorted_cows[add])
            else:
                #append to plan and erase current load
                whole_plan.append(course)
                course = []
                load = 0
                #braek adding
                break  
        for el in whole_plan[-1]:
            try: del sorted_cows[el]
            except: pass

    return whole_plan

# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # TODO: Your code here
    cow_set = set(cows)
    partitions = get_partitions(cow_set)
    #assume worst is the best
    best = len(cows)
    out = []
    for cows_part in partitions:
        deny = False
        for trip in cows_part:
            if deny: break
            weight = 0
            #sum weights
            for cow in trip:
                if deny: break
                weight += int(cows[cow])
                #deny a whole partition
                if weight > limit: deny = True

        if not deny and len(cows_part) < best:
            best = len(cows_part)
            out = cows_part
    return out

        
# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.
    
    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    # TODO: Your code here
    cows = load_cows('ps1_cow_data_2.txt')

    #test greedy
    start = time.time()
    greedy = greedy_cow_transport(cows)
    stop = time.time()  
    greedy_time = stop - start

    #test brute force
    start = time.time()
    brute = brute_force_cow_transport(cows)
    stop = time.time()
    brute_time = stop - start

    print(f"""
Greedy Algorithm:
    time: {greedy_time}
    trips: {len(greedy)}
    transports: {greedy}

Brute Force Algorithm:
    time: {brute_time}
    trips: {len(brute)}
    transports: {brute}
    """)
    
compare_cow_transport_algorithms()