from aoc_2018.day_3.python.day3_puzzle2 import find_non_overlapping_claim
from aoc_2018.day_3.python.test_day3_puzzle1 import get_input


def test_find_non_overlapping_claim_simple() -> None:
    assert find_non_overlapping_claim(get_input("puzzle2_simple_input.txt")) == "#3"


def test_find_non_overlapping_claim_complex() -> None:
    assert find_non_overlapping_claim(get_input("puzzle_input.txt")) == "#1166"
