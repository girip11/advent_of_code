from pathlib import Path
from typing import List

from aoc_2021.day_10.python.syntax_scoring import compute_autocompletion_score, compute_syntax_score


def test_compute_syntax_score() -> None:
    lines: List[str] = (
        (Path(__file__).parent.parent / "simple_input.txt").read_text().strip().split("\n")
    )

    assert compute_syntax_score(lines) == 26397


def test_compute_autocompletion_score() -> None:
    lines: List[str] = (
        (Path(__file__).parent.parent / "simple_input.txt").read_text().strip().split("\n")
    )

    assert compute_autocompletion_score(lines) == 288957
