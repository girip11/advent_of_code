from aoc_2018.day_11.python.day11_puzzle import (
    get_fuel_cell_grid,
    get_power_level,
    find_max_power_level_of_subgrid,
)


def test_get_power_level():
    assert get_power_level((3, 5), 8) == 4
    assert get_power_level((122, 79), 57) == -5
    assert get_power_level((217, 196), 39) == 0
    assert get_power_level((101, 153), 71) == 4


def test_find_largest_power_subgrid():
    assert find_max_power_level_of_subgrid(get_fuel_cell_grid(18, 300), 3) == ((33, 45), 29)
    assert find_max_power_level_of_subgrid(get_fuel_cell_grid(42, 300), 3) == ((21, 61), 30)
    assert find_max_power_level_of_subgrid(get_fuel_cell_grid(1718, 300), 3) == ((243, 34), 31)
