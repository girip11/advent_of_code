import sys
from functools import reduce
from typing import List, MutableMapping

from aoc_2018.day_3.python.day3_puzzle1 import Claim, parse_claim


# implements using approach 2 from ../puzzle_approaches.md
def find_square_inches_with_overlapping_claims(claims: List[Claim]) -> int:
    all_points: MutableMapping[str, List[str]] = {}

    for claim in claims:
        for row in range(claim.y_offset, claim.y_offset + claim.height):
            for col in range(claim.x_offset, claim.x_offset + claim.width):
                claim_pos: str = f"{row}_{col}"
                if claim_pos in all_points:
                    all_points[claim_pos].append(claim.claim_id)
                else:
                    all_points[claim_pos] = [claim.claim_id]

    return reduce(
        lambda total, item: (total + 1) if len(item[1]) >= 2 else total,
        all_points.items(),
        0,
    )


def main(*_: str) -> None:
    claims: List[Claim] = list(map(parse_claim, sys.stdin))

    print(f"Square inches with claims >= 2: {find_square_inches_with_overlapping_claims(claims)} ")


if __name__ == "__main__":
    main(*sys.argv)
