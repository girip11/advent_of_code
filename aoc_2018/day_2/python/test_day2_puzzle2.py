import os
from pathlib import Path

from aoc_2018.day_2.python.day2_puzzle2 import find_common_letters


def _get_input(input_file):
    input_file_path = os.path.join(Path(os.path.dirname(__file__)).parent, input_file)
    box_ids = []

    with open(input_file_path) as input_file:
        box_ids = [id.strip() for id in input_file]

    return box_ids


def test_find_common_letters_simple():
    assert find_common_letters(_get_input("puzzle2_simple_input.txt")) == "fgij"


def test_find_common_letters_corner_case():
    input = ["abcdef", "abckeh", "abcyef"]
    assert find_common_letters(input) == "abcef"


def test_find_common_letters_large():
    assert (
        find_common_letters(_get_input("puzzle_input.txt"))
        == "pebjqsalrdnckzfihvtxysomg"
    )
