import heapq
import sys
from functools import reduce
from operator import mul
from typing import List, Set, Tuple

HeightMap = List[List[int]]
Position = Tuple[int, int]


def parse_input(lines: List[str]) -> HeightMap:
    return [[*map(int, line.strip())] for line in lines]


def is_low_point(position: Position, height_map: HeightMap) -> bool:
    rows = len(height_map)
    cols = len(height_map[0])
    x, y = position  # pylint: disable=invalid-name

    # up
    # down
    # left
    # right
    return (
        (x == 0 or height_map[x][y] < height_map[x - 1][y])
        and (x == rows - 1 or height_map[x][y] < height_map[x + 1][y])
        and (y == 0 or height_map[x][y] < height_map[x][y - 1])
        and (y == cols - 1 or height_map[x][y] < height_map[x][y + 1])
    )


def compute_low_points(height_map: HeightMap) -> List[Position]:
    low_points: List[Position] = []

    for rowno, row in enumerate(height_map):
        for colno, height in enumerate(row):
            pos = (rowno, colno)
            if is_low_point(pos, height_map):
                print(pos, height)
                low_points.append(pos)

    return low_points


def compute_risk_levels(height_map: HeightMap) -> int:
    total_risk_level: int = 0

    for ptx, pty in compute_low_points(height_map):
        total_risk_level += height_map[ptx][pty] + 1

    return total_risk_level


def get_neighbors(low_pt: Position, rows: int, cols: int) -> List[Position]:
    x, y = low_pt  # pylint: disable=invalid-name
    neighbors: List[Position] = []
    if x > 0:
        neighbors.append((x - 1, y))
    if x < rows - 1:
        neighbors.append((x + 1, y))
    if y > 0:
        neighbors.append((x, y - 1))
    if y < cols - 1:
        neighbors.append((x, y + 1))

    return neighbors


def compute_basin_size(height_map: HeightMap, low_pt: Position) -> int:
    rows = len(height_map)
    cols = len(height_map[0])
    visited: Set[Position] = set()
    size: int = 0
    positions_to_explore: List[Position] = [low_pt]

    while len(positions_to_explore) > 0:
        current_pos = positions_to_explore.pop(0)

        if current_pos not in visited:
            for neighbor_pos in get_neighbors(current_pos, rows, cols):
                if (
                    neighbor_pos not in visited
                    and height_map[neighbor_pos[0]][neighbor_pos[1]] != 9
                ):
                    positions_to_explore.append(neighbor_pos)

            size += 1  # count the current position
            visited.add(current_pos)

    return size


def find_largest_n_basins(height_map: HeightMap, top_n: int) -> List[int]:
    basin_sizes: List[int] = []

    for lowpt in compute_low_points(height_map):
        basin_size = compute_basin_size(height_map, lowpt)
        heapq.heappush(basin_sizes, basin_size)

    print(basin_sizes)
    return heapq.nlargest(top_n, basin_sizes)


def main(*_: str) -> None:
    height_map: HeightMap = parse_input(sys.stdin.readlines())

    print(height_map)
    # part-1
    print(compute_risk_levels(height_map))

    # part-2
    largest_basins = find_largest_n_basins(height_map, 3)
    print(largest_basins)
    print(reduce(mul, largest_basins))


if __name__ == "__main__":
    main(*sys.argv[1:])
