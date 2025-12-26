from pathlib import Path
from typing import List

import pytest

from aoc_2021.day_22.python.reactor_reboot import (
    RebootStep,
    count_on_cubes_post_reboot,
    parse_input,
)


@pytest.mark.parametrize(
    "input_file, count",
    (
        ("simple_input1.txt", 39),
        ("simple_input3.txt", 2758514936282235),
    ),
)
def test_count_turnedon_cubes(input_file: str, count: int) -> None:
    reboot_steps: List[RebootStep] = parse_input(
        (Path(__file__).parent.parent / input_file).read_text().strip().split("\n")
    )

    assert count_on_cubes_post_reboot(reboot_steps) == count
