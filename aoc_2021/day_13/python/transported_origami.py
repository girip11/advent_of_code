import sys
from dataclasses import dataclass
from typing import List, Set, Tuple

Point = Tuple[int, int]


@dataclass(frozen=True)
class FoldInstruction:
    fold_at: int
    fold_up: bool  # horizontal


def parse_input(lines: List[str]) -> Tuple[List[Point], List[FoldInstruction]]:
    points: List[Point] = []
    fold_instructions: List[FoldInstruction] = []
    for line in lines:
        line = line.strip()
        if len(line) == 0:
            continue
        if "fold along" in line:
            axis, value = line.replace("fold along", "").strip().split("=")
            fold_instructions.append(FoldInstruction(int(value), axis == "y"))
        else:
            x, y = map(int, line.split(","))  # pylint: disable=invalid-name
            points.append((x, y))

    return (points, fold_instructions)


class TransparentPaper:
    _points: Set[Point]
    _size: Tuple[int, int]

    def __init__(self, points: List[Point]) -> None:
        self._points = set(points)

    @property
    def marked(self) -> int:
        return len(self._points)

    def fold(self, fold_ins: FoldInstruction) -> None:
        if fold_ins.fold_up:
            self.fold_up(fold_ins.fold_at)
        else:
            self.fold_left(fold_ins.fold_at)

    def fold_up(self, fold_at: int) -> None:
        print("folding up", fold_at)
        self._points = {(x, y if y <= fold_at else (2 * fold_at - y)) for x, y in self._points}

    def fold_left(self, fold_at: int) -> None:
        print("folding left", fold_at)
        self._points = {(x if x < fold_at else (2 * fold_at - x), y) for x, y in self._points}

    def display(self) -> None:
        max_x = max(map(lambda point: point[0], self._points))
        max_y = max(map(lambda point: point[1], self._points))
        size = (max_x + 1, max_y + 1)

        for row in range(size[1]):
            for col in range(size[0]):
                content = "#" if (col, row) in self._points else "."
                print(content, sep="", end="")
            print("")


def main(*_: str) -> None:
    points, fold_instructions = parse_input(sys.stdin.readlines())
    print(len(points))
    print(fold_instructions)

    transparent_paper: TransparentPaper = TransparentPaper(points)

    # part-1
    transparent_paper.fold(fold_instructions[0])
    print(transparent_paper.marked)

    # part-2
    for ins in fold_instructions[1:]:
        transparent_paper.fold(ins)

    transparent_paper.display()


if __name__ == "__main__":
    main(*sys.argv[1:])
