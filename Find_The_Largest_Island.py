from typing import List, Tuple, Generator
from collections import deque

# Constants
LAND = 1
WATER = 0

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


class Coordinates:
    """Single coordinates on a map."""
    def __init__(self, row: int, col: int) -> None:
        self.row = row
        self.col = col

    def __repr__(self) -> str:
        return f"Coordinates(row={self.row}, col={self.col})"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Coordinates):
            return self.row == other.row and self.col == other.col
        return False

    def __hash__(self) -> int:
        return hash((self.row, self.col))


# Map class
class Map:
    """
    Represents the map with islands and water. Map has a functionality of:
    - locate islands
    - find the largest island on the map
    """

    def __init__(self, data: List[List[int]]) -> None:  # Expecting a List of Lists of ints now
        self._grid: List[List[int]] = data  # Assign the transformed data directly
        self._visited: List[List[bool]] = [
            [False] * self.size[1] for _ in range(self.size[0])
        ]  # To track visited coordinates

    @property
    def size(self) -> Tuple[int, int]:
        """Returns the dimension of the map (rows, columns)"""
        return len(self._grid), len(self._grid[0])

    @property
    def grid(self) -> List[List[str]]:
        """Provides access to attribute grid"""
        return self._grid

    def display(self) -> None:
        for row in self._grid:
            print(" ".join(map(str, row)))

    def neighbors(self, coord: Coordinates) -> Generator[Coordinates, None, None]:
        """Generates valid neighbors for a given cell."""
        for row_step, col_step in DIRECTIONS:
            new_row, new_col = coord.row + row_step, coord.col + col_step
            if self.within_grid(Coordinates(new_row, new_col)):
                yield Coordinates(new_row, new_col)

    def within_grid(self, coord: Coordinates) -> bool:
        """Checks if the coordinates are within the grid boundaries."""
        return 0 <= coord.row < self.size[0] and 0 <= coord.col < self.size[1]

    def is_LAND(self, coord: Coordinates) -> bool:
        """Checks if the given coordinates represent LAND."""
        return self._grid[coord.row][coord.col] == LAND

    def is_visited(self, coord: Coordinates) -> bool:
        """Checks if the given coordinates have been visited."""
        return self._visited[coord.row][coord.col]

    def mark_visited(self, coord: Coordinates) -> None:
        """Marks the given coordinates as visited."""
        self._visited[coord.row][coord.col] = True


class Island:
    """Island on the map. Provides:
    - coordinates of the island
    - size of the island"""

    def __init__(self, map_object: "Map") -> None:
        self.map: "Map" = map_object
        self.coordinates: List[Coordinates] = []  # Keeps island coordinates

    def bfs(self, start_coord: Coordinates) -> None:
        """Perform BFS to find all coordinates of the island."""
        queue: deque[Coordinates] = deque([start_coord])
        self.map.mark_visited(start_coord)  # Mark the starting coordinate as visited
        self.coordinates.append(start_coord)

        while queue:
            coord = queue.popleft()
            #print(f"Coordinate taken from queue: {coord}")
            #print(f"Is within LAND?: {self.map.is_LAND(coord)}")

            # Check all four neighboring coordinates
            for new_coord in self.map.neighbors(coord):
                if self.map.is_LAND(new_coord) and not self.map.is_visited(new_coord):
                    self.map.mark_visited(new_coord)
                    queue.append(new_coord)
                    self.coordinates.append(new_coord)
                    #print(f"Added new coordinate: {new_coord}")

    def size(self) -> int:
        """Returns the size of the island (number of coordinates)."""
        return len(self.coordinates)


class Archipelago:
    """
    Represents an archipelago, a collection of islands on a map.
    Provides functionality to find the largest island and print island coordinates.
    """

    def __init__(self, map_obj: Map) -> None:
        self.map: Map = map_obj
        self.islands_: List[Island] = self._find_islands()

    def _find_islands(self) -> List[Island]:
        islands: List[Island] = []
        island_finder = Island(self.map)

        for row in range(self.map.size[0]):
            for col in range(self.map.size[1]):
                coord = Coordinates(row, col)

                if self.map.is_LAND(coord) and not self.map.is_visited(coord):
                    #print(f"Found new land at {coord}")
                    island_finder.bfs(coord)
                    islands.append(island_finder)  # Add the island to the list here
                    island_finder = Island(self.map)  # Then create a new island for the next one

        return islands

    def largest_island(self) -> int:
        """Returns the size of the largest island in the archipelago."""
        return max(island.size() for island in self.islands_) if self.islands_ else 0

    def print_islands_coordinates(self) -> None:
        """Prints the coordinates of each island."""
        if not self.islands_:
            print("No islands found.")
            return

        for island_index, island in enumerate(self.islands_, start=1):
            print(f"Island {island_index} coordinates:")
            for coord in island.coordinates:
                print(f"  {coord}")

def transform_string_to_list_advanced(data: str) -> List[List[int]]:
    def row_generator(rows: List[str]) -> List[int]:
        for row in rows:
            # Sprawdzamy, czy każda linia ma długość 8, jeśli nie to ignorujemy ją
            if len(row) == 8:
                yield [1 if element == "x" else 0 for element in row]

    # Usuwamy puste linie, a następnie dzielimy na wiersze
    rows: List[str] = [row for row in data.strip().split("\n") if row.strip()]

    return list(row_generator(rows))

def transform_string_to_list(data: str) -> List[List[int]]:
    rows: List[str] = data.strip().split("\n")
    matrix: List[List[int]] = []
    for row in rows:
        row_list: List[int] = []
        for element in row.split():
            row_list.append(1 if element == "x" else 0)
        matrix.append(row_list)
    return matrix

# Sample data
#data: str = """
#. x . . . . . .
#x . . . . . . .
#. . . . . . . .
#. . . . . . . .
#. . . . . . . .
#. . . . . . . .
#. . . . . . . .
#. . . . . . . .
#"""

data: str = """
. x . . . . . x
x x . x . . x .
. . . . . . . .
. x x x . . x .
. x x . . . x x
x . . . x . x .
. . . x x . . .
. . . x . x x x
"""

# Create map and archipelago objects
transformed_data: List[List[int]] = transform_string_to_list(data)
game_map: Map = Map(transformed_data)
game_map.display()

archipelago: Archipelago = Archipelago(game_map)
archipelago.print_islands_coordinates()

print(f"The size of the largest island is: {archipelago.largest_island()}")

