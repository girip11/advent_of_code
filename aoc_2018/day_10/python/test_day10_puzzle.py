import os
from pathlib import Path
from typing import List

from aoc_2018.day_10.python.day10_puzzle import Point, get_points, time_taken_for_msg


def get_positions(file_name: str) -> List[str]:
    file_path = os.path.join(Path(os.path.dirname(__file__)).parent, file_name)
    with open(file_path) as input_file:
        positions = input_file.readlines()

    return positions


def test_time_taken_for_msg_formation() -> None:
    points: List[Point] = get_points(iter(get_positions("simple_input.txt")))
    assert time_taken_for_msg(points) == 3

    points = get_points(iter(get_positions("puzzle_input.txt")))
    assert time_taken_for_msg(points) == 10932
