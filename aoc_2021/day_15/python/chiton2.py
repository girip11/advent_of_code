import sys
from collections.abc import Iterable
from typing import Iterator, List, Tuple

ChitonDensityMap = List[List[int]]
Position = Tuple[int, int]


def parse_input(lines: List[str]) -> ChitonDensityMap:
    return [[int(density) for density in line.strip()] for line in lines]


def node_neighbors(position: Position, map_size: Tuple[int, int]) -> List[Position]:
    x, y = position  # pylint: disable=invalid-name
    rows, cols = map_size
    return [pos for pos in [(x - 1, y), (x, y - 1)] if 0 <= pos[0] < rows and 0 <= pos[1] < cols]


class CostMatrix(Iterable):
    _cost_matrix: List[List[Tuple[Position, int]]]

    def __init__(self, map_size: Tuple[int, int]) -> None:
        self._cost_matrix = [[((-1, -1), 0)] * map_size[1] for rc in range(map_size[0])]

    def __getitem__(self, pos: Position) -> Tuple[Position, int]:
        return self._cost_matrix[pos[0]][pos[1]]

    def __setitem__(self, pos: Position, value: Tuple[Position, int]) -> None:
        self._cost_matrix[pos[0]][pos[1]] = value

    def __iter__(self) -> Iterator[List[Tuple[Position, int]]]:
        return iter(self._cost_matrix)


def compute_cost_matrix(
    chiton_density_map: ChitonDensityMap, map_size: Tuple[int, int]
) -> CostMatrix:
    cost_matrix: CostMatrix = CostMatrix(map_size)

    for rowno, row in enumerate(chiton_density_map):
        for colno, value in enumerate(row):
            neighbors = node_neighbors((rowno, colno), map_size)
            shortest_path_neighbor = min(
                neighbors, default=None, key=lambda n_pos: cost_matrix[n_pos][1]
            )
            if shortest_path_neighbor is not None:
                _, shortest_path_cost = cost_matrix[shortest_path_neighbor]
                cost_matrix[(rowno, colno)] = (shortest_path_neighbor, shortest_path_cost + value)
            else:
                print("here")

    for rowno, row in enumerate(cost_matrix):
        for colno, _ in enumerate(row):
            print(cost_matrix[(rowno, colno)][1], end="  ")
        print()

    return cost_matrix


def compute_lowest_total_risk(chiton_density_map: ChitonDensityMap) -> int:
    map_size: Tuple[int, int] = (len(chiton_density_map), len(chiton_density_map[0]))
    end_pos: Position = (map_size[0] - 1, map_size[1] - 1)
    cost_matrix: CostMatrix = compute_cost_matrix(chiton_density_map, map_size)
    return cost_matrix[end_pos][1]


def main(*_: str) -> None:
    chiton_density_map: ChitonDensityMap = parse_input(sys.stdin.readlines())
    # chiton_density_map: ChitonDensityMap = parse_input(
    #     (FilePath(__file__).parent.parent / "puzzle_input.txt").read_text().strip().split("\n")
    # )

    print(chiton_density_map)

    # part-1
    print(compute_lowest_total_risk(chiton_density_map))

    # part-2
    # print(mce_lce_difference(polymer_template, insertion_rules, 40))


if __name__ == "__main__":
    main(*sys.argv[1:])
