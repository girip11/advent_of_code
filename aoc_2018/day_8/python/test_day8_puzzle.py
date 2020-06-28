import os
import re
from pathlib import Path
from typing import List

from aoc_2018.day_8.python import day8_puzzle_part1, day8_puzzle_part2


def get_license_numbers(file_name: str) -> List[int]:
    file_path = os.path.join(Path(os.path.dirname(__file__)).parent, file_name)
    with open(file_path) as input_file:
        license_numbers = [int(match) for match in re.findall(r"\d+", input_file.readline())]

    return license_numbers


def test_part1_metadata_sum():
    license_numbers: List[int] = get_license_numbers("simple_input.txt")
    assert day8_puzzle_part1.get_metadata_sum(license_numbers) == 138

    license_numbers: List[int] = get_license_numbers("puzzle_input.txt")
    assert day8_puzzle_part1.get_metadata_sum(license_numbers) == 40701


def test_part2_metadata_sum():
    files_to_output_map = {"simple_input.txt": 138, "puzzle_input.txt": 40701}

    for file_name, output in files_to_output_map.items():
        license_numbers: List[int] = get_license_numbers(file_name)
        root_node = day8_puzzle_part2.get_nodes(license_numbers)
        assert root_node is not None
        assert day8_puzzle_part2.get_metadata_sum(root_node) == output


def test_part2_root_node_value():
    files_to_output_map = {"simple_input.txt": 66, "puzzle_input.txt": 21399}

    for file_name, output in files_to_output_map.items():
        license_numbers: List[int] = get_license_numbers(file_name)
        root_node = day8_puzzle_part2.get_nodes(license_numbers)
        assert root_node is not None
        assert day8_puzzle_part2.get_root_node_value(root_node) == output
