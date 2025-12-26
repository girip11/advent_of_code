from pathlib import Path

from aoc_2021.day_9.python.smoke_basin import (
    HeightMap,
    compute_risk_levels,
    find_largest_n_basins,
    parse_input,
)


def test_compute_risk_levels() -> None:
    height_map: HeightMap = parse_input(
        (Path(__file__).parent.parent / "simple_input.txt").read_text().strip().split("\n"),
    )

    assert compute_risk_levels(height_map) == 15


def test_find_largest_n_basins() -> None:
    height_map: HeightMap = parse_input(
        (Path(__file__).parent.parent / "simple_input.txt").read_text().strip().split("\n"),
    )

    assert find_largest_n_basins(height_map, 3) == [14, 9, 9]
