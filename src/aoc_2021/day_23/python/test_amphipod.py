from pathlib import Path

import pytest

from aoc_2021.day_23.python.amphipod import Configuration, parse_input, rearrange_amphipods


@pytest.mark.parametrize(
    "input_file, energy",
    (
        # ("simple_input_part1.txt", 12521),
        ("test_input.txt", 4646),
    ),
)
def test_least_energy_to_rearrange(input_file: str, energy: int) -> None:
    configuration: Configuration = parse_input(
        (Path(__file__).parent.parent / input_file).read_text().strip().split("\n")
    )

    rearranged = rearrange_amphipods(configuration)
    assert all(amph == s.alloted_for for s in rearranged.siderooms for amph in s.amphipods)
    assert rearranged.energy_spent == energy
