from aoc_2018.day_1.python.day1_puzzle2 import find_first_repeating_frequency
from aoc_2018.day_1.python.test_day1_puzzle1 import get_input


def test_first_repeating_frequency_1() -> None:
    assert find_first_repeating_frequency(get_input("puzzle2_simple_input.txt")) == 10


def test_first_repeating_frequency_2() -> None:
    assert find_first_repeating_frequency(get_input("puzzle_input.txt")) == 448
