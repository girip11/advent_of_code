from pathlib import Path

import pytest

from aoc_2021.day_24.python.alu import (
    Monad,
    find_largest_model_number,
    find_smallest_model_number,
    parse_input,
)


@pytest.mark.parametrize(
    "input_file, largest_model_number",
    (("puzzle_input.txt", "12996997829399"),),
)
def test_largest_valid_model_number(input_file: str, largest_model_number: str) -> None:
    monad: Monad = parse_input(
        (Path(__file__).parent.parent / input_file).read_text().strip().split("\n")
    )

    assert "".join(map(str, find_largest_model_number(monad))) == largest_model_number


@pytest.mark.parametrize(
    "input_file, smallest_model_number",
    (("puzzle_input.txt", "11841231117189"),),
)
def test_smallest_valid_model_number(input_file: str, smallest_model_number: str) -> None:
    monad: Monad = parse_input(
        (Path(__file__).parent.parent / input_file).read_text().strip().split("\n")
    )

    assert "".join(map(str, find_smallest_model_number(monad))) == smallest_model_number
