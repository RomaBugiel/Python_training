# Validate ship game board:
# 
#     all ships has to be used
#     ship sizes: [number x length]: [1x1], [2x2], [2x3], [1x4], [1x5]
#     can be only horizontal or verical
#     cannot touch
# 
# Problemy podczas pisania kodu:
# 
#     ogolnie syntax pythonowy, musze sprawdzac jak sie definiuje set, mape, liste
#     list comprehesion - tu nie mam wprawy, wiem ze w tym miejscu jest dobrze tego uzyc ale potrzebuje sprawdzic sobie syntax i przyklady -- do zrobienia z ~20 prostych cwiczen
#     robie bledy typu: && zamiast and, || zamiast or
#     nie pamietam funkcji typu all(), pop(), append() (wiem ze one sa, ale musze sobie sprawdzic czy add czy append jest uzywane do konkretnej listy)
#     funckji transform_to_2D nie umialam napisac sama, nie pamietam operacji na stringach jak split()...
#     w funkcji check_separation nie umialam napisac z glowy tych warunkow (pod katem skladni): if (adj_r, adj_c) not in ship_positions if adjacent_positions & ship_positions
#     Inne bledy:
#         dodalam liste do krotki: new_pos = new_pos + [stepv, steph]
#         for r in data_size_x zamiast for r in range(data_size_x):
#         DFS (Depth-First Search) lub BFS (Breadth-First Search) - w ogole nie znam tych algorytmow -- do ogarniecia


def validateMap(check_list):
  return all(check_list)
     

def findShips(data):
    # Store ships
    ship_list = []

    # Board sizes
    data_size_x = len(data)
    data_size_y = len(data[0])

    # List of fields that have been checked
    checked_field = [[0 for _ in range(data_size_y)] for _ in range(data_size_x)]

    # Iterate through the board
    for r in range(data_size_x):
        for c in range(data_size_y):
            # Skip if checked
            if checked_field[r][c] == 1:
                continue

            # New ship
            if data[r][c] == 1 and checked_field[r][c] == 0:
                ship = set()
                ship_seed = (r, c)
                ship.add(ship_seed)
                checked_field[r][c] = 1

                # Check fields around seed
                step_vertical = [-1, 0, 1]
                step_horizontal = [-1, 0, 1]

                # Make a list of neighbours to be checked
                stack = [ship_seed]

                while stack:
                    current = stack.pop() # remove from list and check neighbours
                    for stepv in step_vertical:
                        for steph in step_horizontal:
                            new_pos = (current[0] + stepv, current[1] + steph)

                            # Check borders and check checked_field
                            if (0 <= new_pos[0] < data_size_x and
                                0 <= new_pos[1] < data_size_y and
                                checked_field[new_pos[0]][new_pos[1]] == 0):

                                if data[new_pos[0]][new_pos[1]] == 1:
                                    ship.add(new_pos)
                                    stack.append(new_pos)

                                checked_field[new_pos[0]][new_pos[1]] = 1

                # Dodanie statku do listy
                ship_list.append(list(ship))

    return ship_list
     

def check_nb_of_ships(ship_list):

  reference = [1, 2, 2, 3, 3, 4, 5]
  sample = set()

  #for l in range(ship_list):
  #  sample.add(len(l))

  # Better way:
  sample = [len(ship) for ship in ship_list]

  reference.sort()
  sample.sort()

  #if reference == sample:
  #  return True
  #else:
  #  return False

  #Better way:
  return reference == sample

     

def check_ship_orientation(ship_list):

  for ship in ship_list:

    if len(ship) == 1:
      continue

    diff_x = 0
    diff_y = 0

    for coord in ship:
      diff_x += abs((ship[0][0] - coord[0]))
      diff_y += abs((ship[0][1] - coord[1]))

    if not (diff_x == 0 or diff_y == 0):
      return False
    else:
      return True
     

def check_ship_orientation_SOURCE(ship_list):

    for ship in ship_list:

        if len(ship) == 1:
            continue

        # Create two lists, one with x coordinates of single ship, and second with y
        x_coords = [coord[0] for coord in ship]
        y_coords = [coord[1] for coord in ship]

       #Using set, verifiy if cooridantes are the sem
        if len(set(x_coords)) > 1 and len(set(y_coords)) > 1:
            #print("Here: ")
            #print(ship)
            return False  # Diagonal or not in line

    return True
     

def check_separation(ship_list):

    #max_rows = len(data)
    #max_cols = len(data[0])

    #Create all fields with ships
    ship_positions = set()
    for ship in ship_list:
        for r, c in ship:
            ship_positions.add((r, c))

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

    #Fields adjacent to ship field
    adjacent_positions = set()

    for ship in ship_list:
        for r, c in ship:
            for dr, dc in directions:
                adj_r, adj_c = r + dr, c + dc
                if (adj_r, adj_c) not in ship_positions:
                    adjacent_positions.add((adj_r, adj_c))

    #If there is no common parts, ships are not touching each other (including diagonals)
    return not (adjacent_positions & ship_positions)
     

# Helping function, while first version was not working
def check_separation_2(ship_list):

  #Check set of all fields with ships
  ship_positions = set()

  for ship in ship_list:
    for r, c in ship:
      ship_positions.add((r, c))

    # Możliwe kierunki do sprawdzenia sąsiedztwa
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

    for r, c in ship_positions:
        for dr, dc in directions:
            adj_r, adj_c = r + dr, c + dc
            if (adj_r, adj_c) in ship_positions:
                return False  # Statki stykają się
    return True  # Statki są oddzielone
     

def transform_to_2D(data):

    # Divide data into rows
    rows = data.strip().split('\n')
    # Divied rows into elements
    matrix = [ [1 if element == 'x' else 0 for element in row.split()] for row in rows ]

    return matrix
     

print("Start validation")

# Data

data = """
  . x . . . . x .
  . x . x x . . .
  . . . . . . . .
  . x x x x x . .
  . . . . . . . .
  x x x . . x . x
  . . . . x . . .
  x x x x . x . .
"""

data_good = """
  . x . . . . x .
  . x . x x . . .
  . . . . . . . .
  . x x x x x . .
  . . . . . . . .
  x x x . . x . .
  . . . . . x . .
  x x x x . x . .
"""

# Body

# -- Transform data into 2D list with numerical data
data_num = transform_to_2D(data)
for row in data_num:
  print(row)

# -- Find ships
_ship_list = findShips(data_num)
#print(_ship_list)

# -- Validate if map is proper

_condition_nb_of_ships = check_nb_of_ships(_ship_list)
_condition_ship_orientation = check_ship_orientation_SOURCE(_ship_list)
_condition_separation = check_separation(_ship_list)

print(f"Number of ships: {_condition_nb_of_ships}")
print(f"Ships separation: {_condition_separation}")
print(f"Ship orientation: {_condition_ship_orientation}")


_check_list = [_condition_nb_of_ships, _condition_ship_orientation, _condition_separation]
_is_map_correct = validateMap(_check_list)

if _is_map_correct == 1:
    print("Validation finished: Map correct")
else:
    print("Validation finished: Map wrong")

     

# Start validation
# [0, 1, 0, 0, 0, 0, 1, 0]
# [0, 1, 0, 1, 1, 0, 0, 0]
# [0, 0, 0, 0, 0, 0, 0, 0]
# [0, 1, 1, 1, 1, 1, 0, 0]
# [0, 0, 0, 0, 0, 0, 0, 0]
# [1, 1, 1, 0, 0, 1, 0, 1]
# [0, 0, 0, 0, 1, 0, 0, 0]
# [1, 1, 1, 1, 0, 1, 0, 0]
# Number of ships: False
# Ships separation: True
# Ship orientation: False
# Validation finished: Map wrong

