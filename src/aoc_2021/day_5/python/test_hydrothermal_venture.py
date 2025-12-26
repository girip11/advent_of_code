from pathlib import Path
from typing import List

from aoc_2021.day_5.python.hydrothermal_venture import Line, count_most_dangerous_areas, parse_input


def test_count_most_dangerous_areas() -> None:
    lines: List[Line] = parse_input(
        (Path(__file__).parent.parent / "simple_input.txt").read_text().strip().split("\n")
    )

    assert count_most_dangerous_areas(lines) == 5
    assert count_most_dangerous_areas(lines, True) == 12
