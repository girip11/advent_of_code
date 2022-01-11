from pathlib import Path

from aoc_2021.day_15.python.chiton import ChitonDensityMap, compute_lowest_risk, parse_input


def test_compute_lowest_risk() -> None:
    chiton_density_map: ChitonDensityMap = parse_input(
        (Path(__file__).parent.parent / "simple_input.txt").read_text().strip().split("\n")
    )

    assert compute_lowest_risk(chiton_density_map, (10, 10)) == 40
