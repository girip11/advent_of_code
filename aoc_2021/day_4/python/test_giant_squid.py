from pathlib import Path

from aoc_2021.day_4.python.giant_squid import (
    BingoBoard,
    compute_first_winning_board_score,
    compute_last_winning_board_score,
    parse_input,
)


def test_compute_power_consumption() -> None:
    random_bingo_numbers, boards = parse_input(
        (Path(__file__).parent.parent / "simple_input.txt").read_text().strip().split("\n")
    )
    bingo_boards = [BingoBoard(board) for board in boards]

    assert compute_first_winning_board_score(random_bingo_numbers, bingo_boards) == 4512


def test_compute_life_support_rating() -> None:
    random_bingo_numbers, boards = parse_input(
        (Path(__file__).parent.parent / "simple_input.txt").read_text().strip().split("\n")
    )
    bingo_boards = [BingoBoard(board) for board in boards]

    assert compute_last_winning_board_score(random_bingo_numbers, bingo_boards) == 1924
