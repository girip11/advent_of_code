import os
from pathlib import Path
from typing import List

from aoc_2018.day_7.python.day7_puzzle import (
    computer_instructions_traversal_order,
    compute_traversal_duration,
)


def get_raw_instructions(file_name: str) -> List[str]:
    file_path = os.path.join(Path(os.path.dirname(__file__)).parent, file_name)
    with open(file_path) as input_file:
        raw_instructions = input_file.readlines()

    return raw_instructions


def test_part1():
    raw_instructions: List[str] = get_raw_instructions("simple_input.txt")
    assert computer_instructions_traversal_order(iter(raw_instructions)) == "CABDFE"

    raw_instructions = get_raw_instructions("puzzle_input.txt")
    assert (
        computer_instructions_traversal_order(iter(raw_instructions))
        == "OUGLTKDJVBRMIXSACWYPEQNHZF"
    )


def test_part2():
    raw_instructions: List[str] = get_raw_instructions("simple_input.txt")
    assert compute_traversal_duration(iter(raw_instructions), 2) == 258

    raw_instructions = get_raw_instructions("puzzle_input.txt")
    assert compute_traversal_duration(iter(raw_instructions), 5) == 929
