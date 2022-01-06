from pathlib import Path
from typing import List

from aoc_2021.day_8.python.seven_segment_search import (
    Entry,
    count_1478_in_output,
    decode_output_digits,
    parse_input,
)


def test_count_1478_in_output() -> None:
    entries: List[Entry] = parse_input(
        (Path(__file__).parent.parent / "simple_input.txt").read_text().strip().split("\n"),
    )

    assert count_1478_in_output(entries) == 26


def test_decode_output_digits() -> None:
    entries: List[Entry] = parse_input(
        (Path(__file__).parent.parent / "simple_input.txt").read_text().strip().split("\n"),
    )

    assert decode_output_digits(entries) == 61229
