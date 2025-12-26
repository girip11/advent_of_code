from pathlib import Path
from typing import List

from aoc_2021.day_18.python.snailfish import (
    SnailfishNumber,
    largest_magnitude,
    parse_input,
    perform_addition,
)


def test_magnitude() -> None:
    snailfish_numbers: List[SnailfishNumber]
    for input_file, magnitude in [
        ("simple_input.txt", 3993),
        ("simple_input2.txt", 3488),
        ("simple_input3.txt", 4140),
    ]:
        snailfish_numbers = parse_input(
            (Path(__file__).parent.parent / input_file).read_text().strip().split("\n")
        )
        result = perform_addition(snailfish_numbers)
        assert result.magnitude() == magnitude


def test_largest_magnitude() -> None:
    snailfish_numbers: List[SnailfishNumber]
    for input_file, magnitude in [("simple_input3.txt", 3993)]:
        snailfish_numbers = parse_input(
            (Path(__file__).parent.parent / input_file).read_text().strip().split("\n")
        )

        assert largest_magnitude(snailfish_numbers) == magnitude
