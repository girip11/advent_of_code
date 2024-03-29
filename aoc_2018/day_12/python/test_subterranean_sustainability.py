import os
from pathlib import Path
from typing import List

from aoc_2018.day_12.python.subterranean_sustainability import (
    parse_input_data,
    subterranean_sustainability,
)


def get_input_data(file_name: str) -> List[str]:
    file_path = os.path.join(Path(os.path.dirname(__file__)).parent, file_name)
    with open(file_path) as input_file:
        input_data = input_file.readlines()

    return input_data


def test_subterranean_sustainability() -> None:
    result = subterranean_sustainability(*parse_input_data(get_input_data("simple_input.txt")), 20)
    assert result == 325
