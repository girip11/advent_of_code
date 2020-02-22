import os
from pathlib import Path
from typing import List

from aoc_2018.day_1.python.day1_puzzle2 import find_first_repeating_frequency


def _get_input(input_file_name: str) -> List[int]:
    input_file_path: str = os.path.join(
        Path(os.path.dirname(__file__)).parent, input_file_name
    )

    input_frequencies: List[int] = []

    with open(input_file_path) as input_file:
        input_frequencies = list(map(lambda s: int(s), input_file))

    return input_frequencies


def test_first_repeating_frequency_1() -> None:
    assert find_first_repeating_frequency(_get_input("puzzle2_simple_input.txt")) == 10


def test_first_repeating_frequency_2() -> None:
    assert find_first_repeating_frequency(_get_input("puzzle_input.txt")) == 448
