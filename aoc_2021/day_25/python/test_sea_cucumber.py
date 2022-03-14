from pathlib import Path

import pytest

from aoc_2021.day_25.python.sea_cucumber import (
    SeaFloorMap,
    count_sea_cucumber_movement,
    parse_input,
)


@pytest.mark.parametrize(
    "input_file, steps",
    (("simple_input2.txt", 58),),
)
def test_sea_cucumber_moving_steps(input_file: str, steps: int) -> None:
    sea_floor_map: SeaFloorMap = parse_input(
        (Path(__file__).parent.parent / input_file).read_text().strip().split("\n")
    )

    assert count_sea_cucumber_movement(sea_floor_map) == steps
