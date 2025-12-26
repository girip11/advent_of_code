import sys
from typing import List, Tuple


def main(*_: str) -> None:
    serial_number: int = int(sys.stdin.readline())
    grid_size: int = 300

    fuel_cell_grid: List[List[int]] = get_fuel_cell_grid(serial_number, grid_size)
    # part1
    print(find_max_power_level_of_subgrid(fuel_cell_grid, 3))

    # part2
    print(find_largest_power_subgrid(fuel_cell_grid, 300))


def get_fuel_cell_grid(serial_number: int, grid_size: int = 300) -> List[List[int]]:
    return [
        [get_power_level((x, y), serial_number) for x in range(grid_size)] for y in range(grid_size)
    ]


Coordinate = Tuple[int, int]


def get_power_level(fuel_cell_coordinate: Coordinate, serial_number: int) -> int:
    x, y = fuel_cell_coordinate  # pylint: disable=invalid-name
    rack_id: int = x + 10

    power_level: int = ((rack_id * y) + serial_number) * rack_id
    power_level = 0 if power_level < 100 else int(str(power_level)[-3])

    return power_level - 5


# part 1
def find_max_power_level_of_subgrid(
    fuel_cell_grid: List[List[int]], sub_grid_size: int
) -> Tuple[Coordinate, int]:
    max_power_level: Tuple[Coordinate, int] = max(
        (
            ((row, col), sub_grid_power_level(fuel_cell_grid, sub_grid_size, (row, col)))
            for row in range(len(fuel_cell_grid) - sub_grid_size)
            for col in range(len(fuel_cell_grid[row]) - sub_grid_size)
        ),
        key=lambda pair: pair[1],
    )

    print(f"Subgrid size: {sub_grid_size}, max power level:{max_power_level}")

    # map row to y and col to x
    return ((max_power_level[0][1], max_power_level[0][0]), max_power_level[1])


def sub_grid_power_level(
    fuel_cell_grid: List[List[int]], sub_grid_size: int, start_position: Coordinate
) -> int:
    row, col = start_position
    return sum(
        fuel_cell_grid[sub_row][sub_col]
        for sub_row in range(row, row + sub_grid_size)
        for sub_col in range(col, col + sub_grid_size)
    )


# part 2
# TODO: See if you can store the smaller grid sizes in a dict and reuse for
#
# Alternative way: No need to run the program till 300.
# Power level will increase and then starts decreasing after some point
# find the max point after which the power levels start decreaing.
def find_largest_power_subgrid(
    fuel_cell_grid: List[List[int]], max_subgrid_size: int
) -> Tuple[Coordinate, int]:
    max_power_level_subgrid: Tuple[Tuple[Coordinate, int], int] = max(
        (
            (find_max_power_level_of_subgrid(fuel_cell_grid, subgrid), subgrid)
            for subgrid in range(max_subgrid_size)
        ),
        key=lambda triple: triple[0][1],
    )
    print(max_power_level_subgrid)
    return (
        (max_power_level_subgrid[0][0][1], max_power_level_subgrid[0][0][0]),
        max_power_level_subgrid[1],
    )


if __name__ == "__main__":
    main(*sys.argv)
