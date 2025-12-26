import os
from pathlib import Path
from typing import List

from aoc_2018.day_13.python.mine_cart_madness import (
    Location,
    find_first_crash,
    find_last_cart_location,
    get_tracks_and_carts,
    track_movement_config,
)


def get_input_data(file_name: str) -> List[List[str]]:
    file_path = os.path.join(Path(os.path.dirname(__file__)).parent, file_name)
    with open(file_path) as input_file:
        input_data = input_file.readlines()

    return [list(line.strip("\n")) for line in input_data]


def test_find_first_crash() -> None:
    track, carts = get_tracks_and_carts(get_input_data("simple_input.txt"))
    track_movement = track_movement_config()
    position = find_first_crash(track, track_movement, carts)
    assert position == Location(3, 7)


def test_find_last_cart_location() -> None:
    track, carts = get_tracks_and_carts(get_input_data("simple_input_2.txt"))
    track_movement = track_movement_config()
    position = find_last_cart_location(track, track_movement, carts)
    assert position == Location(4, 6)
