from pathlib import Path

from aoc_2021.day_12.python.passage_pathing import (
    START_CAVE,
    count_paths_through_caves,
    parse_input,
    should_explore_cave,
    should_explore_cave2,
)


def test_count_paths_through_caves() -> None:
    cave_connections = parse_input(
        (Path(__file__).parent.parent / "simple_input.txt").read_text().strip().split("\n")
    )

    assert count_paths_through_caves(cave_connections[START_CAVE], should_explore_cave) == 10
    assert count_paths_through_caves(cave_connections[START_CAVE], should_explore_cave2) == 36

    cave_connections = parse_input(
        (Path(__file__).parent.parent / "simple_input2.txt").read_text().strip().split("\n")
    )
    assert count_paths_through_caves(cave_connections[START_CAVE], should_explore_cave) == 19
    assert count_paths_through_caves(cave_connections[START_CAVE], should_explore_cave2) == 103
