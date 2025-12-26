from aoc_2018.day_5.python.day5_puzzle import (
    find_best_polymer_reaction,
    polymer_units_after_reaction,
)


def test_polymer_units_after_reaction() -> None:
    assert polymer_units_after_reaction("dabAcCaCBAcCcaDA") == 10


def test_find_best_polymer_reaction() -> None:
    assert find_best_polymer_reaction("dabAcCaCBAcCcaDA") == 4
