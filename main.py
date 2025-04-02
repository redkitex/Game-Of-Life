# Conway's Game of Life
import random, copy, os, time

def dead_state(width, height):
    # Creates a blank board
    return [[0] * width for _ in range(height)]

def random_state(width, height):
    # Iterate over a dead state, randomising the blocks
    state = dead_state(width, height)

    for row in state:
        for i in range(width):
            num = random.random()
            if num > 0.5: # Changing this threshold impacts the probability of a cell being alive/dead
                row[i] = 1

    return state

def add_border_to_state(state):
    # Adds a border of 0s around the state, allowing for the neighbours to be calculated
    state_with_border = copy.deepcopy(state)
    state_with_border.insert(0, [0]*width)
    state_with_border.append([0]*width)

    for row in state_with_border:
        row.insert(0, 0)
        row.append(0)

    return state_with_border


def sum_neighbours(state_with_border, x, y):
    # Corrects the values of x and y for the border of 0s
    x += 1
    y += 1

    # Because each alive cell has a value of 1 and each dead cell 0,
    # the 8 cells surrounding the current one can be added to determine the number of neighbours---
    total = 0
    for i in (y-1, y, y+1):
        total += sum(state_with_border[i][x-1:x+2])
    
    return total - state_with_border[y][x]

def next_state(state):
    new_state = dead_state(width, height)
    state_with_border = add_border_to_state(state)
    for y in range(height):
        for x in range(width):
            num_of_neighbours = sum_neighbours(state_with_border, x, y)
            
            if state[y][x] == 1:
                if num_of_neighbours <= 1 or num_of_neighbours > 3:
                    new_state[y][x] = 0
                elif num_of_neighbours <= 3:
                    new_state[y][x] = 1
            else:
                if num_of_neighbours == 3:
                    new_state[y][x] = 1
    return new_state

def render(state):
    for row in state:
        pretty_row = [""]*width
        for i in range(width):
            if row[i] == 1:
                # Two characters are used to create a white square
                # This usually means you have to zoom out of the terminal to see the full state
                # Alternately single characters can be used by this results in distortion
                pretty_row[i] = "\u2588" + "\u2588"
            else:
                # Two spaces are used to create a black square
                pretty_row[i] = "  "
        print("|"+"".join(pretty_row)+"|")

def load_state_from_seed_file(filename):
    global height, width
    state = []
    
    f = open(dir + "/" + filename, "r")

    for line in f:
        state.append(list(map(int, line.strip())))

    height = len(state)
    width = len(state[0])

    return state

# Either a random soup can be generated...
width = 100
height = 30
initial_state = random_state(width, height)

# ...Or a seed state can be loaded from a text file (Uncomment the below lines)
# initial_state = load_state_from_seed_file("pulsar.txt")
# dir = "" # TODO : Add your directory


render(initial_state)
new_state = next_state(initial_state)
time.sleep(0.1)
os.system('cls')

while True:
    render(new_state)
    new_state = next_state(new_state)
    time.sleep(0.1)
    os.system('cls')