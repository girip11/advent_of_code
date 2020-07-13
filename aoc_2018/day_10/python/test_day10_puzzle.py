import os
from pathlib import Path
from typing import List

from aoc_2018.day_10.python.day10_puzzle import time_taken_for_msg, get_points, Point


def get_positions(file_name: str) -> List[str]:
    file_path = os.path.join(Path(os.path.dirname(__file__)).parent, file_name)
    with open(file_path) as input_file:
        positions = [line for line in input_file]

    return positions


def test_time_taken_for_msg_formation():
    points: List[Point] = get_points(get_positions("simple_input.txt"))
    assert time_taken_for_msg(points) == 3

    points: List[Point] = get_points(get_positions("puzzle_input.txt"))
    assert time_taken_for_msg(points) == 10932
