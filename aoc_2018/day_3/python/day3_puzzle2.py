import sys
from typing import List, Tuple, Optional

from aoc_2018.day_3.python.day3_puzzle1 import (
    Claim,
    get_fabric,
    get_fabric_dimensions_from_claims,
    mark_fabric_with_claims,
    parse_claim,
)


def main(*_: str) -> None:
    claims: List[Claim] = list(map(parse_claim, sys.stdin))
    print(f"Non overlapping claim: {find_non_overlapping_claim(claims)} ")


def find_non_overlapping_claim(claims: List[Claim]) -> Optional[str]:
    """Returns the ID of the claim which does not overlap with other claims
    
    Arguments:
        claims {List[Claim]}
    
    Returns:
        Optional[str] - None if no such claim is found else the claim ID
    """
    fabric_dimensions: Tuple[int, int] = get_fabric_dimensions_from_claims(claims)
    fabric: List[int] = get_fabric(fabric_dimensions)
    mark_fabric_with_claims(fabric=fabric, fabric_dimensions=fabric_dimensions, claims=claims)

    for claim in claims:
        if _is_overlapping(fabric, fabric_dimensions, claim) is False:
            return claim.claim_id

    return None


def _is_overlapping(fabric: List[int], fabric_dimensions: Tuple[int, int], claim: Claim) -> bool:
    for i in range(claim.y_offset, claim.y_offset + claim.height):
        for j in range(claim.x_offset, claim.x_offset + claim.width):
            pos = (i * fabric_dimensions[1]) + j
            if fabric[pos] >= 2:
                return True
    return False


if __name__ == "__main__":
    main(*sys.argv)
