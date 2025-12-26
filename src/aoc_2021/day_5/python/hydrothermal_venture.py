import sys
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class Point:
    x: int  # pylint: disable=invalid-name
    y: int  # pylint: disable=invalid-name


@dataclass(frozen=True)
class Line:
    start: Point
    end: Point

    def is_vertical(self) -> bool:
        return self.start.x == self.end.x

    def is_horizontal(self) -> bool:
        return self.start.y == self.end.y

    def is_diagonal(self) -> bool:
        return not (self.is_vertical() or self.is_horizontal())


def parse_input(line_coordinates: List[str]) -> List[Line]:
    lines: List[Line] = []

    for coordinates in line_coordinates:
        start, end = map(lambda s: s.strip(), coordinates.strip().split("->"))
        start_point = Point(*(int(i) for i in start.split(",")))
        end_point = Point(*(int(i) for i in end.split(",")))
        lines.append(Line(start_point, end_point))

    return lines


def get_points_in_line_segment(line: Line) -> List[Point]:
    if line.is_vertical():
        step = 1 if line.start.y < line.end.y else -1
        return [Point(line.start.x, i) for i in range(line.start.y, line.end.y + step, step)]

    if line.is_horizontal():
        step = 1 if line.start.x < line.end.x else -1
        return [Point(i, line.start.y) for i in range(line.start.x, line.end.x + step, step)]

    # diagonal at 45 degree
    step_x = 1 if line.start.x < line.end.x else -1
    step_y = 1 if line.start.y < line.end.y else -1
    return [
        Point(x, y)
        for x, y in zip(
            range(line.start.x, line.end.x + step_x, step_x),
            range(line.start.y, line.end.y + step_y, step_y),
        )
    ]


def count_most_dangerous_areas(lines: List[Line], consider_diagonal: bool = False) -> int:
    dangerous_spots: Dict[Point, int] = defaultdict(int)

    for line in lines:
        if consider_diagonal is False and line.is_diagonal():
            continue
        points = get_points_in_line_segment(line)
        # print(line, len(points))
        for point in points:
            dangerous_spots[point] += 1

    return len([i for i in dangerous_spots.values() if i >= 2])


def main(*_: str) -> None:
    lines: List[Line] = parse_input(sys.stdin.readlines())
    # print(lines)

    # part-1
    print(count_most_dangerous_areas(lines))

    # part-2
    print(count_most_dangerous_areas(lines, True))


if __name__ == "__main__":
    main(*sys.argv[1:])
