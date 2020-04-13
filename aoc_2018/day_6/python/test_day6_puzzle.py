from typing import List, Tuple
from .day6_puzzle import ProximityGrid


def test_largest_area() -> None:
    coordinates: List[Tuple[int, int]] = [
        (1, 1),
        (1, 6),
        (8, 3),
        (3, 4),
        (5, 5),
        (8, 9),
    ]

    prox_grid: ProximityGrid = ProximityGrid(10, coordinates)
    assert prox_grid.largest_finite_area() == 17


def test_region_size() -> None:
    coordinates: List[Tuple[int, int]] = [
        (1, 1),
        (1, 6),
        (8, 3),
        (3, 4),
        (5, 5),
        (8, 9),
    ]

    prox_grid: ProximityGrid = ProximityGrid(10, coordinates)
    assert prox_grid.proximity_region_size(32) == 16
