import os
from pathlib import Path
from typing import List

from aoc_2018.day_2.python.day2_puzzle2 import find_common_letters
from aoc_2018.day_2.python.test_day2_puzzle1 import get_input


def test_find_common_letters_simple() -> None:
    assert find_common_letters(get_input("puzzle2_simple_input.txt")) == "fgij"


def test_find_common_letters_corner_case() -> None:
    input: List[str] = ["abcdef", "abckeh", "abcyef"]
    assert find_common_letters(input) == "abcef"


def test_find_common_letters_large():
    assert (
        find_common_letters(get_input("puzzle_input.txt"))
        == "pebjqsalrdnckzfihvtxysomg"
    )
