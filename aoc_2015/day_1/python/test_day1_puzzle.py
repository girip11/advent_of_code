import os
from pathlib import Path
from typing import List

from aoc_2015.day_1.python.day1_puzzle import (
    get_dest_floor,
    get_first_basement_ins_pos,
)


def test_get_dest_floor() -> None:
    assert get_dest_floor("") == 0
    assert get_dest_floor(")())())") == -3
    assert get_dest_floor("))(((((") == 3


def test_get_first_basement_ins_pos() -> None:
    assert get_first_basement_ins_pos("()())") == 5
