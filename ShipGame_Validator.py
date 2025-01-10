# Validate ship game board:
#
#     all ships has to be used
#     ship sizes: [number x length]: [1x1], [2x2], [2x3], [1x4], [1x5]
#     can be only horizontal or verical
#     cannot touch

from typing import List, Set, Tuple

class Map:
    def __init__(self, data: List[List[int]]):
        self._data = data

# Property ensures, that the atribute is updated automatically. Ex. when ones creates object game_map1, x and y are created normally via constructor and even if data changes for game_map1, x and y would be the same. If x and y are defined as property, they will be updated.
    @property
    def x(self) -> int:
        return len(self._data)

    @property
    def y(self) -> int:
        return len(self._data[0])

    def size(self) -> Tuple[int, int]:
        return self.x, self.y

    def display(self):
        for row in self._data:
            print(" ".join(["x" if cell == 1 else "." for cell in row]))

def validate_map(check_list: List[bool]) -> bool:
    return all(check_list)

def find_ships(game_map: Map) -> List[List[Tuple[int, int]]]:
    ship_list: List[List[Tuple[int, int]]] = []

    # Board sizes
    data_size_x, data_size_y = game_map.size()
    data = game_map._data

    checked_field: List[List[int]] = [[0 for _ in range(data_size_y)] for _ in range(data_size_x)]

    for r in range(data_size_x):
        for c in range(data_size_y):
            if checked_field[r][c] == 1:
                continue

            if data[r][c] == 1:
                ship: Set[Tuple[int, int]] = set()
                ship_seed: Tuple[int, int] = (r, c)
                ship.add(ship_seed)
                checked_field[r][c] = 1

                step_vertical = [-1, 0, 1]
                step_horizontal = [-1, 0, 1]

                stack: List[Tuple[int, int]] = [ship_seed]

                while stack:
                    current = stack.pop()
                    for stepv in step_vertical:
                        for steph in step_horizontal:
                            new_pos: Tuple[int, int] = (current[0] + stepv, current[1] + steph)

                            if (
                                0 <= new_pos[0] < data_size_x
                                and 0 <= new_pos[1] < data_size_y
                                and checked_field[new_pos[0]][new_pos[1]] == 0
                            ):

                                if data[new_pos[0]][new_pos[1]] == 1:
                                    ship.add(new_pos)
                                    stack.append(new_pos)

                                checked_field[new_pos[0]][new_pos[1]] = 1

                ship_list.append(list(ship))

    return ship_list

def check_nb_of_ships(ship_list: List[List[Tuple[int, int]]]) -> bool:
    reference: List[int] = [1, 2, 2, 3, 3, 4, 5]
    sample: List[int] = [len(ship) for ship in ship_list]

    reference.sort()
    sample.sort()

    return reference == sample

def check_ship_orientation(ship_list: List[List[Tuple[int, int]]]) -> bool:
    for ship in ship_list:
        if len(ship) == 1:
            continue

        x_coords: List[int] = [coord[0] for coord in ship]
        y_coords: List[int] = [coord[1] for coord in ship]

        if len(set(x_coords)) > 1 and len(set(y_coords)) > 1:
            return False

    return True

def check_separation(ship_list: List[List[Tuple[int, int]]]) -> bool:
    ship_positions: Set[Tuple[int, int]] = set()
    for ship in ship_list:
        for r, c in ship:
            ship_positions.add((r, c))

    directions: List[Tuple[int, int]] = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

    for r, c in ship_positions:
        for dr, dc in directions:
            adj_r, adj_c = r + dr, c + dc
            if (adj_r, adj_c) in ship_positions:
                return False

    return True

def transform_string_to_list(data: str) -> List[List[int]]:
    rows: List[str] = data.strip().split("\n")
    matrix: List[List[int]] = [[1 if element == "x" else 0 for element in row.split()] for row in rows]
    return matrix

print("Start validation")

data: str = """
  . x . . . . x .
  . x . x x . . .
  . . . . . . . .
  . x x x x x . .
  . . . . . . . .
  x x x . . x . x
  . . . . x . . .
  x x x x . x . .
"""

data_num: List[List[int]] = transform_string_to_list(data)
game_map = Map(data_num)

game_map.display()

ship_list: List[List[Tuple[int, int]]] = find_ships(game_map)

condition_nb_of_ships: bool = check_nb_of_ships(ship_list)
condition_ship_orientation: bool = check_ship_orientation(ship_list)
condition_separation: bool = check_separation(ship_list)

print(f"Number of ships: {condition_nb_of_ships}")
print(f"Ships separation: {condition_separation}")
print(f"Ship orientation: {condition_ship_orientation}")

check_list: List[bool] = [
    condition_nb_of_ships,
    condition_ship_orientation,
    condition_separation,
]

is_map_correct: bool = validate_map(check_list)

if is_map_correct:
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
