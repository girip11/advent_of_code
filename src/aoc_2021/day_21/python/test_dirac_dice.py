from pathlib import Path
from typing import List

from aoc_2021.day_21.python.dirac_dice import Player, parse_input, play_for_win


def test_unique_beacons() -> None:
    players: List[Player] = parse_input(
        (Path(__file__).parent.parent / "simple_input.txt").read_text().strip().split("\n")
    )
    turns, winner, loser = play_for_win(players, 1000)
    assert turns == 331
    assert winner.id_ == 1 and winner.score == 1000
    assert loser.id_ == 2 and loser.score == 745
