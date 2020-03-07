from dataclasses import dataclass
import sys
from functools import reduce
from typing import List, Iterable, Tuple


@dataclass(init=False)
class PresentBox:
    l: int
    w: int
    h: int
    smallest_side: Tuple[int, int]

    def __init__(self, l: int, w: int, h: int) -> None:
        self.l = l
        self.w = w
        self.h = h
        self.smallest_side = tuple(sorted([l, w, h])[:2])

    def area(self) -> int:
        return (2 * self.l * self.w) + (2 * self.w * self.h) + (2 * self.h * self.l)

    def smallest_side_area(self) -> int:
        return self.smallest_side[0] * self.smallest_side[1]

    def smallest_side_perimeter(self) -> int:
        return 2 * (self.smallest_side[0] + self.smallest_side[1])

    def volume(self) -> int:
        return self.l * self.w * self.h


def find_wrapping_paper_length(present_boxes: Iterable[PresentBox]) -> int:
    return reduce(
        lambda acc, pb: acc + pb.area() + pb.smallest_side_area(), present_boxes, 0
    )


def find_ribbon_length(present_boxes: Iterable[PresentBox]) -> int:
    return reduce(
        lambda acc, pb: acc + pb.smallest_side_perimeter() + pb.volume(),
        present_boxes,
        0,
    )


def main(args: List[str]) -> None:
    """
        This is the entry point.
    """
    present_boxes: List[PresentBox] = [
        PresentBox(*map(int, dim.split("x"))) for dim in sys.stdin
    ]

    print(find_wrapping_paper_length(present_boxes))
    print(find_ribbon_length(present_boxes))


if __name__ == "__main__":
    main(sys.argv)
