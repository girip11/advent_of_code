import sys
from typing import List, Tuple
from functools import reduce


class Claim:
    """Claim containing the following details
    * ID, 
    * x and y offsets of the claimed section from the beginning of the fabric and
    * The width and height of the claimed section on the fabric. 
    """

    claim_id: str
    x_offset: int
    y_offset: int
    width: int
    height: int

    def __init__(
        self, claim_id: str, x_offset: int, y_offset: int, width: int, height: int
    ) -> None:
        self.claim_id = claim_id
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.width = width
        self.height = height

    def __str__(self) -> str:
        """Returns the string representation in the format
            '<claim id> @ <x_offset>,<y_offset>: <width>x<height>'
        """
        return f"{self.claim_id} @ {self.x_offset},{self.y_offset}: {self.width}x{self.height}"


def main(*_: str) -> None:
    claims: List[Claim] = list(map(parse_claim, sys.stdin))

    print(f"Square inches with claims >= 2: {find_square_inches_with_overlapping_claims(claims)} ")


# TODO: better way of parsing is using regex and pattern matching
def parse_claim(claim_str: str) -> Claim:
    """Claim string example : "#1305 @ 148,699: 27x18"
    
    Arguments:
        claim_str {str} -- [description]
    
    Returns:
        Claim -- [description]
    """
    claim_id: str = claim_str.split("@")[0].strip()
    x_offset, y_offset = map(int, claim_str.split("@")[1].split(":")[0].strip().split(","))
    width, height = map(int, claim_str.split("@")[1].split(":")[1].strip().split("x"))
    return Claim(claim_id, x_offset, y_offset, width, height)


# implements approach 3 from ../puzzle_approaches.md
def find_square_inches_with_overlapping_claims(claims: List[Claim]) -> int:
    fabric_dimensions: Tuple[int, int] = get_fabric_dimensions_from_claims(claims)
    fabric: List[int] = get_fabric(fabric_dimensions)
    mark_fabric_with_claims(fabric=fabric, fabric_dimensions=fabric_dimensions, claims=claims)
    return reduce(lambda total, count: (total + 1) if count >= 2 else total, fabric, 0)


def get_fabric_dimensions_from_claims(claims: List[Claim]) -> Tuple[int, int]:
    max_x = claims[0].y_offset + claims[0].height
    max_y = claims[0].x_offset + claims[0].width

    for i, claim in enumerate(claims):
        if i > 0:
            max_x = max(max_x, claim.y_offset + claim.height)
            max_y = max(max_y, claim.x_offset + claim.width)

    # print(f"Fabric dimensions: {max_x} x {max_y}")
    return max_x, max_y


def get_fabric(dimensions: Tuple[int, int]) -> List[int]:
    return [0] * (dimensions[0] * dimensions[1])


def mark_fabric_with_claims(
    *, fabric: List[int], fabric_dimensions: Tuple[int, int], claims: List[Claim]
) -> None:
    pos: int = 0
    for claim in claims:
        for i in range(claim.y_offset, claim.y_offset + claim.height):
            for j in range(claim.x_offset, claim.x_offset + claim.width):
                pos = (i * fabric_dimensions[1]) + j
                fabric[pos] += 1


if __name__ == "__main__":
    main(*sys.argv)
