from pathlib import Path
from typing import List

from aoc_2021.day_6.python.lanternfish import simulate_lanternfish, simulate_lanternfish2


def test_count_lanternfish() -> None:
    internal_timers: List[int] = [
        *map(
            int, (Path(__file__).parent.parent / "simple_input.txt").read_text().strip().split(",")
        )
    ]

    assert simulate_lanternfish(internal_timers, 80) == 5934
    assert simulate_lanternfish2(internal_timers, 256) == 26984457539
