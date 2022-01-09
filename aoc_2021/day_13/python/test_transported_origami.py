from pathlib import Path

from aoc_2021.day_13.python.transported_origami import TransparentPaper, parse_input


def test_paper_fold() -> None:
    points, fold_instructions = parse_input(
        (Path(__file__).parent.parent / "simple_input.txt").read_text().strip().split("\n")
    )

    paper = TransparentPaper(points)
    paper.fold(fold_instructions[0])
    assert paper.marked == 17

    paper.fold(fold_instructions[1])
    assert paper.marked == 16
