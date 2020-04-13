import sys
import itertools
from dataclasses import dataclass
from typing import List, Dict, MutableSet, NamedTuple, Optional, Tuple


@dataclass(init=False, frozen=True)
class Coordinate:
    x: int  # pylint: disable=invalid-name
    y: int  # pylint: disable=invalid-name

    def __init__(self, x: int, y: int) -> None:
        super().__setattr__("x", x)
        super().__setattr__("y", y)

    def manhattan_distance(self, other: "Coordinate") -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)


class GridEntry(NamedTuple):
    coordinate: Coordinate
    closest_coordinate: Optional[int]


class ProximityGrid:
    def __init__(self, grid_size: int, special_coordinates: List[Tuple[int, int]]) -> None:
        self._grid_size = grid_size
        self._special_coordinates: Dict[int, Coordinate] = {
            Id: Coordinate(*coordinate) for Id, coordinate in enumerate(special_coordinates)
        }

    # For debugging purposes only
    def _print_proximity_grid(self, grid: List[GridEntry]) -> None:
        for i in grid:
            if i.coordinate.x % self._grid_size == 0:
                print()
            print(i.closest_coordinate, end="\t")
        print()

    def largest_finite_area(self) -> int:
        grid: List[GridEntry] = [None] * (self._grid_size ** 2)  # type: ignore
        infinite_coverage: MutableSet[int] = set()
        area: Dict[int, int] = {sc: 0 for sc in self._special_coordinates}

        self._populate_proximity_grid(grid)
        # self._print_proximity_grid(grid)

        for coordinate, closest in grid:
            if closest is not None:
                if self._is_corner_coordinate(coordinate):
                    infinite_coverage.add(closest)
                else:
                    area[closest] += 1

        coordinates_with_finite_area = [
            sc_id for sc_id in self._special_coordinates if sc_id not in infinite_coverage
        ]

        largest_area_coordinate: int = max(
            coordinates_with_finite_area, key=lambda sc_id: area[sc_id],
        )

        print(
            f"Coordinate {self._special_coordinates[largest_area_coordinate]} \
            has largest area of {area[largest_area_coordinate]}"
        )
        return area[largest_area_coordinate]

    def _populate_proximity_grid(self, grid: List[GridEntry]) -> None:
        grid_coordinates: List[Coordinate] = [
            Coordinate(x, y) for x, y in itertools.product(range(self._grid_size), repeat=2)
        ]

        for coordinate in grid_coordinates:
            location: int = self._get_position_on_grid(coordinate)
            grid[location] = GridEntry(
                coordinate, self._find_closest_special_coordinate(coordinate)
            )

    def _get_position_on_grid(self, coordinate: Coordinate) -> int:
        return (coordinate.y * self._grid_size) + coordinate.x

    def _find_closest_special_coordinate(self, coordinate: Coordinate) -> Optional[int]:
        distances: List[Tuple[int, int]] = [
            (sc_id, sc.manhattan_distance(coordinate))
            for sc_id, sc in self._special_coordinates.items()
        ]

        distances = sorted(distances, key=lambda entry: entry[1])

        if len(distances) > 1 and distances[0][1] == distances[1][1]:
            return None

        return distances[0][0]

    def _is_corner_coordinate(self, coordinate: Coordinate) -> bool:
        return (coordinate.x == 0 or coordinate.x == self._grid_size - 1) or (
            coordinate.y == 0 or coordinate.y == self._grid_size - 1
        )

    def proximity_region_size(self, region_size: int) -> int:
        region_coordinates: int = 0
        grid_coordinates: List[Coordinate] = [
            Coordinate(x, y) for x, y in itertools.product(range(self._grid_size), repeat=2)
        ]

        for coordinate in grid_coordinates:
            distance_sum: int = sum(
                coordinate.manhattan_distance(sc) for sc in self._special_coordinates.values()
            )
            if distance_sum < region_size:
                region_coordinates += 1

        return region_coordinates


def main(*_: str) -> None:
    coordinates_list: List[Tuple[int, int]] = [
        (int(coordinate.split(",")[0]), int(coordinate.split(",")[1])) for coordinate in sys.stdin
    ]

    grid_size = max(*[x for x, _ in coordinates_list], *[y for _, y in coordinates_list])

    proximity_grid = ProximityGrid(grid_size + 1, coordinates_list)
    # pg = ProximityGrid(10, coordinates_list)
    # pg.print_proximity_grid()

    # part1
    print(proximity_grid.largest_finite_area())
    # part2
    print(proximity_grid.proximity_region_size(10000))


if __name__ == "__main__":
    main(*sys.argv)
