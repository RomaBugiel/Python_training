from typing import List, Tuple, Generator
from collections import deque

# Constants
LAND = "x"
WATER = "."

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


# Map class
class Map:
    """
    Represents the map with islands and water. Map has a functionality of:
    - locate islands
    - find the largest island on the map
    """

    def __init__(self, data: str) -> None:
        rows: List[str] = data.strip().split("\n")
        grid: List[List[str]] = []

        for row in rows:
            grid.append(list(row))

        self._grid: List[List[str]] = grid

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
            print(" ".join(row))

    def neighbors(self, row: int, col: int) -> Generator[Tuple[int, int], None, None]:
        """Generates valid neighbors for a given cell."""
        for row_step, col_step in DIRECTIONS:
            new_row, new_col = row + row_step, col + col_step
            if 0 <= new_row < self.size[0] and 0 <= new_col < self.size[1]:
                yield new_row, new_col


class Island:
    """Island on the map. Provides:
    - find the size of the largest island"""

    def __init__(self, map_object: Map) -> None:
        self.map: Map = map_object
        self.checked: List[List[bool]] = [
            [False] * self.map.size[1] for _ in range(self.map.size[0])
        ]

    def bfs(self, start_row: int, start_col: int) -> int:
        """Perform BFS to calculate island size"""
        queue: deque[Tuple[int, int]] = deque([(start_row, start_col)])
        self.checked[start_row][start_col] = True
        size: int = 0

        while queue:
            row, col = queue.popleft()
            size += 1
            for new_row, new_col in self.map.neighbors(row, col):
                if (
                    self.map.grid[new_row][new_col] == LAND
                    and not self.checked[new_row][new_col]
                ):
                    self.checked[new_row][new_col] = True
                    queue.append((new_row, new_col))
        return size


class Archipelago:
    """
    Represents an archipelago, a collection of islands on a map.
    Provides functionality to find the largest island.
    """

    def __init__(self, map_obj: Map) -> None:
        self.map: Map = map_obj
        self.island_sizes_: List[int] = self._find_islands()

    def _find_islands(self) -> List[int]:
        """Detects all the islands on the map and returns their sizes."""
        island_sizes: List[int] = []
        island_finder = Island(self.map)

        rows, cols = self.map.size

        for row in range(rows):
            for col in range(cols):
                if (
                    self.map.grid[row][col] == LAND
                    and not island_finder.checked[row][col]
                ):
                    # Perform BFS to find the island's size and add it to the list
                    island_size = island_finder.bfs(row, col)
                    island_sizes.append(island_size)
        return island_sizes

    def largest_island(self) -> int:
        """Returns the size of the largest island in the archipelago."""
        return max(self.island_sizes_) if self.island_sizes_ else 0


# Sample data
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
game_map: Map = Map(data)
archipelago: Archipelago = Archipelago(game_map)

# Display the map and largest island size
game_map.display()
print(f"The size of the largest island is: {archipelago.largest_island()}")
