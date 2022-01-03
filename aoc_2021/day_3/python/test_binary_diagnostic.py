from aoc_2021.day_3.python.binary_diagnostic import (
    compute_life_support_rating,
    compute_power_consumption,
)

diagnostics = [
    "00100",
    "11110",
    "10110",
    "10111",
    "10101",
    "01111",
    "00111",
    "11100",
    "10000",
    "11001",
    "00010",
    "01010",
]


def test_compute_power_consumption() -> None:
    assert compute_power_consumption(diagnostics) == 198


def test_compute_life_support_rating() -> None:
    assert compute_life_support_rating(diagnostics) == 230
