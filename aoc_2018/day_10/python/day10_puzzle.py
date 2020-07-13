import re
import sys
import itertools
from typing import ClassVar, Iterator, List, Tuple, Set
from dataclasses import dataclass


def main(*_: str) -> None:
    points = get_points(iter(sys.stdin))
    # for p in points:
    #     print(p)
    print(time_taken_for_msg(points))
    display_points(points)


@dataclass
class Point:
    pattern: ClassVar[re.Pattern] = re.compile(r"<\s*(-?\d+),\s*(-?\d+)>")

    x_pos: int
    y_pos: int
    x_vel: int
    y_vel: int

    def move(self):
        self.x_pos += self.x_vel
        self.y_pos += self.y_vel

    @staticmethod
    def to_set(points) -> Set[Tuple[int, int]]:
        return {(point.x_pos, point.y_pos) for point in points}

    @staticmethod
    def from_text(text: str) -> "Point":
        position, velocity = Point.pattern.finditer(text)
        return Point(*map(int, position.groups()), *map(int, velocity.groups()))


def get_points(raw_input: Iterator[str],) -> List[Point]:
    return [Point.from_text(position_text) for position_text in raw_input]


def time_taken_for_msg(points: List[Point]) -> int:
    seconds_counter: int = -1
    points_mover = move_points(points)

    for seconds_counter in itertools.count(start=1):
        next(points_mover)
        current_positions = Point.to_set(points)
        min_x, max_x, min_y, max_y = min_max_positions(points)

        if (
            (min_x, min_y) in current_positions
            and (max_x, min_y) in current_positions
            and (min_x, max_y) in current_positions
            and (max_x, max_y) in current_positions
        ):
            break

    return seconds_counter


def move_points(points: List[Point]) -> Iterator[None]:
    while True:
        for point in points:
            point.move()
        yield


def min_max_positions(points: List[Point]) -> Tuple[int, int, int, int]:
    return (
        min(p.x_pos for p in points),
        max(p.x_pos for p in points),
        min(p.y_pos for p in points),
        max(p.y_pos for p in points),
    )


def display_points(points: List[Point]):
    current_positions = Point.to_set(points)
    min_x, max_x, min_y, max_y = min_max_positions(points)

    for y_pos in range(min_y, max_y + 1):
        for x_pos in range(min_x, max_x + 1):
            print("#" if (x_pos, y_pos) in current_positions else ".", sep="", end="")
        print()


if __name__ == "__main__":
    main(*sys.argv)
