import os
from pathlib import Path

from aoc_2018.day_1.python.day1_puzzle1 import find_aggregate_frequency


def _get_input(input_file):
    input_file_path = os.path.join(Path(os.path.dirname(__file__)).parent, input_file)
    frequencies = []

    with open(input_file_path) as input_file:
        frequencies = [int(freq) for freq in input_file]

    return frequencies


def test_aggregate_frequency_1():
    assert find_aggregate_frequency(_get_input("puzzle1_simple_input.txt")) == 4


def test_aggregate_frequency_2():
    assert find_aggregate_frequency(_get_input("puzzle_input.txt")) == 556
