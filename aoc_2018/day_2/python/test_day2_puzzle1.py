import os
from pathlib import Path

from aoc_2018.day_2.python.day2_puzzle1 import calculate_checksum


def _get_input(input_file):
    input_file_path = os.path.join(Path(os.path.dirname(__file__)).parent, input_file)
    box_ids = []

    with open(input_file_path) as input_file:
        box_ids = [id.strip() for id in input_file]

    return box_ids


def test_calculate_checksum_simple():
    assert calculate_checksum(_get_input("puzzle1_simple_input.txt")) == 12


def test_calculate_checksum_large():
    assert calculate_checksum(_get_input("puzzle_input.txt")) == 4693
