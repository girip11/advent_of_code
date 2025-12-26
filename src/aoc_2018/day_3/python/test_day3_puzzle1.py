import os
from pathlib import Path
from typing import List

from aoc_2018.day_3.python.day3_puzzle1 import (
    Claim,
    find_square_inches_with_overlapping_claims,
    parse_claim,
)


def get_input(input_file_name: str) -> List[Claim]:
    input_file_path: str = os.path.join(Path(os.path.dirname(__file__)).parent, input_file_name)

    claims: List[Claim] = []

    with open(input_file_path) as input_file:
        claims = [parse_claim(claim_str) for claim_str in input_file]

    return claims


def test_find_square_inches_with_multiple_claims_simple() -> None:
    assert find_square_inches_with_overlapping_claims(get_input("puzzle1_simple_input.txt")) == 4


def test_find_square_inches_with_multiple_claims_complex() -> None:
    assert find_square_inches_with_overlapping_claims(get_input("puzzle_input.txt")) == 107663
