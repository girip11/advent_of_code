from dataclasses import dataclass
import sys
from functools import reduce
from typing import Callable, List, Iterable, Tuple


@dataclass(init=False)
class PresentBox:
    length: int
    width: int
    height: int
    # When we have a n tuple this is the way to use typehints
    # Reference: https://github.com/python/typing/issues/30
    smallest_side: Tuple[int, ...]

    def __init__(self, length: int, width: int, height: int) -> None:
        self.length = length
        self.width = width
        self.height = height
        self.smallest_side = tuple(sorted([length, width, height])[:2])

    def area(self) -> int:
        return (
            (2 * self.length * self.width)
            + (2 * self.width * self.height)
            + (2 * self.height * self.length)
        )

    def smallest_side_area(self) -> int:
        return self.smallest_side[0] * self.smallest_side[1]

    def smallest_side_perimeter(self) -> int:
        return 2 * (self.smallest_side[0] + self.smallest_side[1])

    def volume(self) -> int:
        return self.length * self.width * self.height


def find_wrapping_paper_length(present_boxes: Iterable[PresentBox]) -> int:
    func: Callable[
        [int, PresentBox], int
    ] = lambda acc, pb: acc + pb.area() + pb.smallest_side_area()
    return reduce(func, present_boxes, 0)


def find_ribbon_length(present_boxes: Iterable[PresentBox]) -> int:
    func: Callable[
        [int, PresentBox], int
    ] = lambda acc, pb: acc + pb.smallest_side_perimeter() + pb.volume()
    return reduce(func, present_boxes, 0)


def main(*_: str) -> None:
    """
        This is the entry point.
    """
    present_boxes: List[PresentBox] = [PresentBox(*map(int, dim.split("x"))) for dim in sys.stdin]

    print(find_wrapping_paper_length(present_boxes))
    print(find_ribbon_length(present_boxes))


if __name__ == "__main__":
    main(*sys.argv)
