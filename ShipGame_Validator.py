from typing import List, Set, Tuple

# CONST
DIRECTIONS: List[Tuple[int, int]] = [
    (-1, 0),  # UP
    (1, 0),  # DOWN
    (0, -1),  # LEFT
    (0, 1),  # RIGHT
    (-1, -1),  # UP_LEFT
    (-1, 1),  # UP_RIGHT
    (1, -1),  # DOWN_LEFT
    (1, 1),  # DOWN_RIGHT
]

DOCK: List[int] = [1, 2, 2, 3, 3, 4, 5]


class Map:
    def __init__(self, data: List[List[int]]):
        self._data = data

    @property
    def x(self) -> int:
        return len(self._data)

    @property
    def y(self) -> int:
        return len(self._data[0])

    def size(self) -> Tuple[int, int]:
        return self.x, self.y

    # copied from Internet, dont fully know how to write it
    def display(self):
        for row in self._data:
            print(" ".join(["x" if cell == 1 else "." for cell in row]))


# Magic methods are something like operator overloading in C++


class Ship:
    def __init__(self, coordinates: List[Tuple[int, int]]):
        self.coordinates = coordinates

    def __len__(self) -> int:
        """
        Returns the number of parts of the ship (length).
        """
        return len(self.coordinates)

    def __eq__(self, other: "Ship") -> bool:
        """
        Checks if two ships are equal by comparing the number of parts.
        """
        return len(self) == len(other)

    # Not fully writen alone, a lot of errors made, needed external sources
    # To be understood
    def is_orientation_ok(self) -> bool:
        """
        Checks if the ship is  horizontal or vertical.
        """
        if len(self) == 1:
            return True  # A single-field ship is always good

        # Extract x and y coordinates
        x_coords: List[int] = [coord[0] for coord in self.coordinates]
        y_coords: List[int] = [coord[1] for coord in self.coordinates]

        # If there is more than one unique value in both x and y coordinates,
        # the ship is neither horizontal nor vertical
        return len(set(x_coords)) == 1 or len(set(y_coords)) == 1


def initialize_empty_board(board_xsize: int, board_ysize: int):
    """
    Initializes a 2D matrix with zeros.

    Args:
        data_size_x (int): number of rows
        data_size_y (int): number of columns

    Returns:
        list: A 2D list of shape (board_xsize, board_ysize) filled with zeros.
    """
    return [[0] * board_ysize for _ in range(board_xsize)]


def is_within_board(x: int, y: int, board_xsize: int, board_ysize: int) -> bool:
    """
    Checks if the coordinates (x, y) are within the bounds of the board

    Args:
        x (int): row index
        y (int): column index
        board_xsize (int): number of rows in the matrix
        board_ysize (int): number of columns in the matrix

    Returns:
        bool: True if the coordinates are within the board.
    """
    return 0 <= x < board_xsize and 0 <= y < board_ysize


def is_unvisited(row: int, col: int, checked_field: List[List[int]]) -> bool:
    """
    Checks if a cell has not been visited.

    Args:
        row (int): Row index of the cell
        col (int): Column index of the cell
        checked_field (List[List[int]]): Tracks checked fields

    Returns:
        bool: True if the cell has not been visited, False otherwise.
    """
    return checked_field[row][col] == 0


def is_ship_part(row: int, col: int, data: List[List[int]]) -> bool:
    """
    Checks if a cell is part of the ship.

    Args:
        row (int): Row index of the cell
        col (int): Column index of the cell
        data (List[List[int]]): Game map data, where 1 = field with ship

    Returns:
        bool: True if the cell is part of the ship, False otherwise.
    """
    return data[row][col] == 1


def mark_as_visited(row: int, col: int, checked_field: List[List[int]]) -> None:
    """
    Marks a cell as visited.

    Args:
        row (int): Row index
        col (int): Column index
        checked_field (List[List[int]]): Tracks checked fields
    """
    checked_field[row][col] = 1


def explore_ship(
    start_position: Tuple[int, int],
    data: List[List[int]],
    checked_field: List[List[int]],
    size_x: int,
    size_y: int,
) -> Ship:

    ship_coordinates: List[Tuple[int, int]] = []
    stack: List[Tuple[int, int]] = [start_position]
    ship_coordinates.append(start_position)
    # checked_field[start_position[0]][start_position[1]] = 1
    mark_as_visited(start_position[0], start_position[1], checked_field)

    while stack:
        current = stack.pop()
        for row_change, col_change in DIRECTIONS:
            new_row, new_column = current[0] + row_change, current[1] + col_change
            if is_within_board(new_row, new_column, size_x, size_y):
                if is_unvisited(new_row, new_column, checked_field) and is_ship_part(
                    new_row, new_column, data
                ):
                    ship_coordinates.append((new_row, new_column))
                    stack.append((new_row, new_column))
                    mark_as_visited(new_row, new_column, checked_field)

    return Ship(ship_coordinates)


def find_ships(game_map: "Map") -> List[Ship]:
    """
    Detects all ships and returns a list of their coordinates.

    Args:
        game_map ('Map'): The game map object containing board game.

    Returns:
        List[List[Tuple[int, int]]]: A list of lists, where each sublist contains coordinates of a ship.
    """

    ship_list: List[Ship] = []

    # Get map size and data
    board_xsize, board_ysize = game_map.size()
    board = game_map._data

    checked_field = initialize_empty_board(board_xsize, board_ysize)

    for row in range(board_xsize):
        for column in range(board_ysize):
            if is_unvisited(row, column, checked_field) and is_ship_part(
                row, column, board  # Using board instead of data
            ):
                ship = explore_ship(
                    (row, column), board, checked_field, board_xsize, board_ysize
                )
                ship_list.append(ship)

    return ship_list


def check_nb_of_ships(ship_list: List[Ship]) -> bool:
    """
    Checks if the number of ships in the list matches the reference

    Args:
        ship_list (List[List[Tuple[int, int]]]): List of ships,

    Returns:
        bool: True if the number of ships matches the reference
    """
    sample: List[int] = [len(ship) for ship in ship_list]

    DOCK.sort()
    sample.sort()

    return DOCK == sample


def check_ship_orientation(ship_list: List[Ship]) -> bool:
    """
    Checks if all ships in the list are aligned either horizontally or vertically.

    Args:
        ship_list (List[Ship]): A list of Ship objects to check.

    Returns:
        bool:
        - True if all ships in the list are correctly aligned.
        - False if at least one ship is neither horizontal nor vertical.
    """
    # all() makes end
    # map returns result of is_ship_orientation_ok for every object in ship_list

    # return all(map(is_orientation_ok, ship_list))
    # Dosnt work as above, changed
    return all(map(lambda ship: ship.is_orientation_ok(), ship_list))


def check_separation(ship_list: List[Ship], board_size: Tuple[int, int]) -> bool:
    """
    Checks if ships on the board do not touch each other, including diagonally.

    Args:
        ship_list (List[Ship]): A list of Ship objects.
        board_size (Tuple[int, int]): The size of the board as (rows, columns).

    Returns:
        bool:
        - True if no ships touch each other.
        - False otherwise.
    """
    rows, cols = board_size

    occupied_fields: Set[Tuple[int, int]] = set()
    adjacent_fields: Set[Tuple[int, int]] = set()

    for ship in ship_list:
        for row, col in ship.coordinates:
            occupied_fields.add((row, col))

            # Add surrounding fields to each ship to adjacent_fields
            for row_change, col_change in DIRECTIONS:
                new_row, new_col = row + row_change, col + col_change
                if is_within_board(new_row, new_col, rows, cols):
                    adjacent_fields.add((new_row, new_col))

    # return occupied_fields.isdisjoint(adjacent_fields - occupied_fields)
    return occupied_fields.isdisjoint(adjacent_fields)


def transform_string_to_list(data: str) -> List[List[int]]:
    rows: List[str] = data.strip().split("\n")
    matrix: List[List[int]] = [
        [1 if element == "x" else 0 for element in row.split()] for row in rows
    ]
    return matrix


if __name__ == "__main__":

    data = """\
    . x x x . . x
    . x . x x . .
    x x . . . x .
    x . x . x . .
    . . x . x . x
    x x . . x . .
    """

    transformed_data: List[List[int]] = transform_string_to_list(data)
    game_map: Map = Map(transformed_data)

    ships: List[Ship] = find_ships(game_map)
    print(f"Ships found: {ships}")

    if check_nb_of_ships(ships):
        print("The number of ships is correct.")
    else:
        print("The number of ships is incorrect.")

    if check_ship_orientation(ships):
        print("All ships are aligned correctly.")
    else:
        print("Not all ships are aligned correctly.")

    board_size = game_map.size()
    if check_separation(ships, board_size):
        print("Ships are properly separated.")
    else:
        print("Ships are too close to each other.")
