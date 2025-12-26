import sys
from collections import deque
from copy import deepcopy
from itertools import chain
from typing import Deque, Iterable, List, Set, Tuple

OctopusGrid = List[List[int]]
Position = Tuple[int, int]


def parse_input(lines: List[str]) -> OctopusGrid:
    return [[*map(int, line.strip())] for line in lines]


def get_adjacent_positions(position: Position) -> List[Position]:
    row, col = position
    return [
        pos
        for pos in [
            (row - 1, col),  # up
            (row + 1, col),  # down
            (row, col - 1),  # left
            (row, col + 1),  # right
            (row - 1, col - 1),  # upleft
            (row - 1, col + 1),  # upright
            (row + 1, col - 1),  # down left
            (row + 1, col + 1),  # down right
        ]
        if 0 <= pos[0] <= 9 and 0 <= pos[1] <= 9
    ]


def raise_energy_levels(grid: OctopusGrid, neighbors: Iterable[Position]) -> None:
    for row, col in neighbors:
        grid[row][col] += 1


def simulate_ripple_flashes(grid: OctopusGrid, flashed: Set[Position], current: Position) -> int:
    flashes: int = 0
    neighbors: Deque[Position] = deque([current])

    while len(neighbors) > 0:
        current = neighbors.popleft()
        if current in flashed:
            continue

        energy_level = grid[current[0]][current[1]]
        if energy_level > 9:
            flashes += 1
            grid[current[0]][current[1]] = 0  # flashes
            flashed.add(current)
            current_nonflashed_neighbors = [
                neighbor for neighbor in get_adjacent_positions(current) if neighbor not in flashed
            ]
            raise_energy_levels(grid, current_nonflashed_neighbors)
            neighbors.extend(current_nonflashed_neighbors)

    return flashes


def simulate_flashes(grid: OctopusGrid) -> int:
    flashed: Set[Position] = set()
    flashes: int = 0
    for rowno, row in enumerate(grid):
        for colno, _ in enumerate(row):
            current = (rowno, colno)
            if current in flashed:  # same as enery level 0
                continue

            grid[rowno][colno] += 1  # increase energy level
            if grid[rowno][colno] > 9:  # this one can flash
                flashes += simulate_ripple_flashes(grid, flashed, current)

    return flashes


def count_flashes(grid: OctopusGrid, steps: int) -> int:
    flashes: int = 0

    for step in range(steps):
        print(step)
        flashes += simulate_flashes(grid)

    return flashes


def find_synchronization_step(grid: OctopusGrid) -> int:
    step = 0

    while True:
        simulate_flashes(grid)
        step += 1

        if sum(chain(*grid)) == 0:
            print(f"sync step:{step}")
            break

    return step


def main(*_: str) -> None:
    grid: OctopusGrid = parse_input(sys.stdin.readlines())

    print(grid)
    # part-1
    print(count_flashes(deepcopy(grid), 100))

    # # part-2
    print(find_synchronization_step(grid))


if __name__ == "__main__":
    main(*sys.argv[1:])
