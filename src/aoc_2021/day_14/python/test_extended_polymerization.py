from pathlib import Path

from aoc_2021.day_14.python.extended_polymerization import mce_lce_difference, parse_input


def test_paper_fold() -> None:
    polymer_template, insertion_rules = parse_input(
        (Path(__file__).parent.parent / "simple_input.txt").read_text().strip().split("\n")
    )

    assert mce_lce_difference(polymer_template, insertion_rules, 10) == 1588
