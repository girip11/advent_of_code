import sys
from dataclasses import dataclass
from typing import ClassVar, List, Optional, Tuple

Position = Tuple[int, int]


@dataclass
class SeaFloorMap:
    EAST: ClassVar[str] = ">"
    SOUTH: ClassVar[str] = "v"
    map_: List[List[str]]

    def can_move(self, sea_cucumber: str, cur_pos: Position) -> Optional[Position]:
        row, col = cur_pos
        if sea_cucumber == SeaFloorMap.EAST:
            # adjacent is right. Roll over to left happens on reaching end
            col = (col + 1) % len(self.map_[row])
        else:
            # adjacent is down. Roll over to top happens on reaching end
            row = (row + 1) % len(self.map_)

        return (row, col) if self.map_[row][col] == "." else None

    def move(self, sea_cucumber: str, src: Position, dest: Position) -> None:
        self.map_[src[0]][src[1]] = "."
        self.map_[dest[0]][dest[1]] = sea_cucumber

    def sea_cucumber_herd(self, herd_type: str) -> List[Position]:
        return [
            (r_id, c_id)
            for r_id, row in enumerate(self.map_)
            for c_id, col in enumerate(row)
            if self.map_[r_id][c_id] == herd_type
        ]

    def __str__(self) -> str:
        content: List[str] = []
        for row in self.map_:
            content.append("".join(row))
        return "\n".join(content)


def move_sea_cucumber_herd(sea_floor_map: SeaFloorMap, herd_type: str) -> int:
    movements: List[Tuple[str, Position, Position]] = []

    for cur_pos in sea_floor_map.sea_cucumber_herd(herd_type):
        if dest := sea_floor_map.can_move(herd_type, cur_pos):
            movements.append((herd_type, cur_pos, dest))

    for sea_cucumber, src, dest in movements:
        sea_floor_map.move(sea_cucumber, src, dest)

    return len(movements)


def count_sea_cucumber_movement(sea_floor_map: SeaFloorMap) -> int:
    steps: int = 0
    moving: bool = True

    while moving:
        moving = move_sea_cucumber_herd(sea_floor_map, SeaFloorMap.EAST) > 0
        moving = move_sea_cucumber_herd(sea_floor_map, SeaFloorMap.SOUTH) > 0 or moving
        steps += 1

    return steps


def parse_input(lines: List[str]) -> SeaFloorMap:
    sea_floor: List[List[str]] = []
    for line in lines:
        if line := line.strip():
            sea_floor.append(list(line))

    return SeaFloorMap(sea_floor)


def main(*_: str) -> None:
    input_lines = sys.stdin.readlines()

    sea_floor_map = parse_input(input_lines)
    print(sea_floor_map)

    # part-1
    print(f"Steps: {count_sea_cucumber_movement(sea_floor_map)}")


if __name__ == "__main__":
    main(*sys.argv[1:])
