from collections.abc import Iterator

ADJACENT_POSITIONS: list[tuple[int, int]] = [
    (0, -1),  # left
    (-1, -1),  # left up
    (-1, 0),  # up
    (-1, 1),  # right up
    (0, 1),  # right
    (1, 1),  # right down
    (1, 0),  # down
    (1, -1),  # left down
]


def get_adjacent_positions(r: int, c: int, n_r: int, n_c: int) -> Iterator[tuple[int, int]]:
    return filter(
        lambda e: (0 <= e[0] < n_r) and (0 <= e[1] < n_c),
        ((r + i, c + j) for (i, j) in ADJACENT_POSITIONS),
    )


# part-1
def get_forklift_accessible_rolls(roll_arrgnmt: list[list[str]]) -> set[tuple[int, int]]:
    n_rows = len(roll_arrgnmt)
    n_cols = len(roll_arrgnmt[0])
    rolls_accessible: set[tuple[int, int]] = set()

    for r in range(0, n_rows):
        for c in range(0, n_cols):
            if roll_arrgnmt[r][c] != "@":
                continue

            adj_rolls: int = 0
            for i, j in get_adjacent_positions(r, c, n_rows, n_cols):
                adj_rolls += int(roll_arrgnmt[i][j] == "@")
                if adj_rolls >= 4:
                    break
            else:
                rolls_accessible.add((r, c))

    return rolls_accessible


def get_forklift_accessible_rolls_repeated(
    roll_arrgnmt: list[list[str]], *, repeated: bool
) -> int:
    total_rolls_accessible: int = 0
    # iteration = 1

    while True:
        rolls_accessible = get_forklift_accessible_rolls(roll_arrgnmt)
        n_rolls = len(rolls_accessible)
        total_rolls_accessible += n_rolls
        # print(f"{iteration}, {n_rolls}")
        # iteration += 1

        if not repeated or (n_rolls == 0):
            break

        # forklist removes those rolls
        for i, j in rolls_accessible:
            roll_arrgnmt[i][j] = "."

    return total_rolls_accessible
