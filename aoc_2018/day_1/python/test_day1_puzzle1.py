import os
from pathlib import Path
from typing import List

from aoc_2018.day_1.python.day1_puzzle1 import find_aggregate_frequency


def get_input(input_file_name: str) -> List[int]:
    input_file_path: str = os.path.join(Path(os.path.dirname(__file__)).parent, input_file_name)
    frequencies: List[int] = []

    with open(input_file_path) as input_file:
        frequencies = [int(freq) for freq in input_file]

    return frequencies


def test_aggregate_frequency_1() -> None:
    assert find_aggregate_frequency(get_input("puzzle1_simple_input.txt")) == 4


def test_aggregate_frequency_2() -> None:
    assert find_aggregate_frequency(get_input("puzzle_input.txt")) == 556
