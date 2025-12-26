from pathlib import Path

from aoc_2021.day_11.python.dumbo_octopus import (
    OctopusGrid,
    count_flashes,
    find_synchronization_step,
    parse_input,
)


def test_count_flashes() -> None:
    grid: OctopusGrid = parse_input(
        (Path(__file__).parent.parent / "simple_input.txt").read_text().strip().split("\n")
    )

    assert count_flashes(grid, 10) == 204


def test_find_synchronization_step() -> None:
    grid: OctopusGrid = parse_input(
        (Path(__file__).parent.parent / "simple_input.txt").read_text().strip().split("\n")
    )

    assert find_synchronization_step(grid) == 195
