from pathlib import Path
from typing import List

from aoc_2021.day_7.python.treachery_of_whales import (
    compute_optimal_fuel,
    constant_rate,
    linear_increase_rate,
)


def test_compute_optimal_fuel() -> None:
    crab_positions: List[int] = [
        *map(
            int, (Path(__file__).parent.parent / "simple_input.txt").read_text().strip().split(",")
        )
    ]

    assert compute_optimal_fuel(crab_positions, constant_rate) == 37
    assert compute_optimal_fuel(crab_positions, linear_increase_rate) == 168
