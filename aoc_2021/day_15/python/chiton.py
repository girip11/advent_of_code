import heapq
import sys
from collections.abc import Iterable as IterableABC
from typing import Iterator, List, Set, Tuple

ChitonDensityMap = List[List[int]]
Position = Tuple[int, int]


def parse_input(lines: List[str]) -> ChitonDensityMap:
    return [[int(density) for density in line.strip()] for line in lines]


def node_neighbors(position: Position, map_size: Tuple[int, int]) -> List[Position]:
    x, y = position  # pylint: disable=invalid-name
    rows, cols = map_size
    return [
        pos
        for pos in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        if 0 <= pos[0] < rows and 0 <= pos[1] < cols
    ]


class CostMatrix(IterableABC):
    _cost_matrix: List[List[Tuple[Position, int]]]

    def __init__(self, map_size: Tuple[int, int]) -> None:
        self._cost_matrix = [[((-1, -1), sys.maxsize)] * map_size[1] for rc in range(map_size[0])]
        self._cost_matrix[0][0] = ((-1, -1), 0)

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
    solved_nodes: Set[Position] = set()
    unsolved_nodes: List[Tuple[int, Position]] = [(0, (0, 0))]
    end_node: Position = (map_size[0] - 1, map_size[1] - 1)

    while unsolved_nodes:
        current_cost, current_node = heapq.heappop(unsolved_nodes)

        if current_node in solved_nodes:
            continue

        if current_node == end_node:  # stop since we have reached destination
            break

        solved_nodes.add(current_node)

        for neighbor in node_neighbors(current_node, map_size):
            if neighbor in solved_nodes:
                continue

            new_cost = current_cost + chiton_density_map[neighbor[0]][neighbor[1]]

            if new_cost < cost_matrix[neighbor][1]:
                cost_matrix[neighbor] = (current_node, new_cost)
                heapq.heappush(unsolved_nodes, (new_cost, neighbor))

    return cost_matrix


def compute_lowest_risk(chiton_density_map: ChitonDensityMap, map_size: Tuple[int, int]) -> int:
    end_pos: Position = (map_size[0] - 1, map_size[1] - 1)
    cost_matrix: CostMatrix = compute_cost_matrix(chiton_density_map, map_size)
    return cost_matrix[end_pos][1]


def iterate_tiles(
    tile_size: Tuple[int, int], expand_by: int, start_tile: int
) -> Iterator[Tuple[int, int]]:
    tile_num: int = 0

    # iterate by row and column of tiles
    for i in range(0, expand_by):
        for j in range(0, expand_by):  # pylint: disable=invalid-name
            if tile_num >= start_tile:
                yield (tile_size[0] * i, tile_size[1] * j)
            tile_num += 1


def get_neighbor_tile_pos(
    current_tile_pos: Position, tile_size: Tuple[int, int], map_size: Tuple[int, int]
) -> Position:
    left_tile_pos = (current_tile_pos[0], current_tile_pos[1] - tile_size[1])

    if 0 <= left_tile_pos[0] < map_size[0] and 0 <= left_tile_pos[1] < map_size[1]:
        return left_tile_pos

    # position from upper tile
    return (current_tile_pos[0] - tile_size[0], current_tile_pos[1])


def prepare_density_map(
    chiton_density_tile: ChitonDensityMap,
    tile_size: Tuple[int, int],
    expand_by: int,
) -> ChitonDensityMap:
    map_size = (tile_size[0] * expand_by, tile_size[1] * expand_by)
    complete_density_map = [
        chiton_density_tile[i % tile_size[0]] * expand_by for i in range(map_size[0])
    ]

    # skip the first tile
    for start_row, start_col in iterate_tiles(tile_size, expand_by, 1):
        for i in range(start_row, start_row + tile_size[0]):
            for j in range(start_col, start_col + tile_size[1]):  # pylint: disable=invalid-name
                neighbor_tile_pos = get_neighbor_tile_pos((i, j), tile_size, map_size)
                complete_density_map[i][j] = (
                    complete_density_map[neighbor_tile_pos[0]][neighbor_tile_pos[1]] + 1
                ) % 10 or 1

    return complete_density_map


def main(*_: str) -> None:
    chiton_density_tile: ChitonDensityMap = parse_input(sys.stdin.readlines())
    tile_size: Tuple[int, int] = (len(chiton_density_tile), len(chiton_density_tile[0]))

    # part-1
    print(compute_lowest_risk(chiton_density_tile, tile_size))

    # part-2
    expand_by: int = 5
    complete_density_map: ChitonDensityMap = prepare_density_map(
        chiton_density_tile, tile_size, expand_by
    )
    map_size = (tile_size[0] * expand_by, tile_size[1] * expand_by)

    print(compute_lowest_risk(complete_density_map, map_size))


if __name__ == "__main__":
    main(*sys.argv[1:])
