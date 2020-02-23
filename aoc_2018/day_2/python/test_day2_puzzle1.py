import os
from pathlib import Path
from typing import List

from aoc_2018.day_2.python.day2_puzzle1 import calculate_checksum


def get_input(input_file_name: str) -> List[str]:
    input_file_path: str = os.path.join(
        Path(os.path.dirname(__file__)).parent, input_file_name
    )
    box_ids: List[str] = []

    with open(input_file_path) as input_file:
        box_ids = [id.strip() for id in input_file]

    return box_ids


def test_calculate_checksum_simple() -> None:
    assert calculate_checksum(get_input("puzzle1_simple_input.txt")) == 12


def test_calculate_checksum_large() -> None:
    assert calculate_checksum(get_input("puzzle_input.txt")) == 4693
