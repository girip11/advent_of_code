from pathlib import Path
from typing import List

from aoc_2021.day_19.python.beacon_scanner import (
    Scanner,
    find_total_beacons,
    largest_manhattan_distance,
    parse_beacon_positions,
)


def test_unique_beacons() -> None:
    scanners: List[Scanner] = parse_beacon_positions(
        (Path(__file__).parent.parent / "simple_input.txt").read_text().strip().split("\n")
    )
    assert find_total_beacons(scanners) == 79
    assert largest_manhattan_distance(scanners) == 3621
