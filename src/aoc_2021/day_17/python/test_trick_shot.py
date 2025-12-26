from pathlib import Path

from aoc_2021.day_17.python.trick_shot import (
    TargetRange,
    count_distinct_initial_velocities,
    find_max_height,
    parse_input,
)


def test_find_max_height() -> None:
    target_range: TargetRange = parse_input(
        (Path(__file__).parent.parent / "simple_input.txt").read_text().strip()
    )

    assert find_max_height(target_range) == 45


def test_count_distinct_initial_velocities() -> None:
    target_range: TargetRange = parse_input(
        (Path(__file__).parent.parent / "simple_input.txt").read_text().strip()
    )

    assert count_distinct_initial_velocities(target_range) == 112
