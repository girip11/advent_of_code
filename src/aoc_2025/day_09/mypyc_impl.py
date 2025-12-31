import itertools
from collections import defaultdict

type Position = tuple[int, int]


def get_area(p1: Position, p2: Position) -> int:
    return (abs(p1[0] - p2[0]) + 1) * (abs(p1[1] - p2[1]) + 1)


def get_largest_rectangle_area(red_tiles_xy: list[Position]) -> int:
    return max(get_area(p1, p2) for p1, p2 in itertools.combinations(red_tiles_xy, 2))


def is_within_rg_tile_boundary(
    rect: tuple[Position, Position], boundary_lookup: dict[int, tuple[int, int]]
) -> bool:
    return all(
        (range_[0] <= rect[0][0] <= range_[1]) and (range_[0] <= rect[1][0] <= range_[1])
        for r in range(min(rect[0][1], rect[1][1]), max(rect[0][1], rect[1][1]) + 1)
        if (range_ := boundary_lookup[r])
    )


def get_largest_rectangle_area_with_only_green_red_tiles(red_tiles_xy: list[Position]) -> int:
    boundary_lookup: dict[int, tuple[int, int]] = defaultdict(lambda: (100000, -1))

    # Construct a row level lookup of what columns are red or green tiles.
    # This solution works only if every row occurs twice in the input.
    for p1, p2 in itertools.pairwise(itertools.chain([*red_tiles_xy, red_tiles_xy[0]])):
        if p1[1] == p2[1]:  # same row
            r = p1[1]
            min_idx, max_idx = boundary_lookup[r]
            min_idx = min(min_idx, min(p1[0], p2[0]))
            max_idx = max(max_idx, max(p1[0], p2[0]))
            boundary_lookup[r] = (min_idx, max_idx)
        elif p1[0] == p2[0]:  # same column
            c = p1[0]
            for r in range(min(p1[1], p2[1]), max(p1[1], p2[1]) + 1):
                min_idx, max_idx = boundary_lookup[r]
                min_idx = min(min_idx, c)
                max_idx = max(max_idx, c)
                boundary_lookup[r] = (min_idx, max_idx)

    return max(
        get_area(p1, p2)
        for p1, p2 in itertools.combinations(red_tiles_xy, 2)
        if is_within_rg_tile_boundary((p1, p2), boundary_lookup)
    )
