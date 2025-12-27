import numba
import numpy as np


@numba.njit
def get_forklift_accessible_mask(roll_arrgnmt: np.ndarray) -> np.ndarray:
    n_rows = roll_arrgnmt.shape[0]
    n_cols = roll_arrgnmt.shape[1]

    # Boolean mask for accessible rolls
    mask = np.zeros((n_rows, n_cols), dtype=np.bool_)

    for r in range(n_rows):
        for c in range(n_cols):
            if roll_arrgnmt[r, c] != 1:
                continue

            adj_rolls = 0
            # Check 8 neighbors
            for dr in range(-1, 2):
                for dc in range(-1, 2):
                    if dr == 0 and dc == 0:
                        continue

                    nr = r + dr
                    nc = c + dc

                    if 0 <= nr < n_rows and 0 <= nc < n_cols:
                        adj_rolls += roll_arrgnmt[nr, nc]
                        if adj_rolls >= 4:
                            break

                if adj_rolls >= 4:
                    break

            if adj_rolls < 4:
                mask[r, c] = True

    return mask


@numba.njit
def get_forklift_accessible_rolls_repeated(roll_arrgnmt: np.ndarray, *, repeated: bool) -> int:
    total_rolls_accessible: int = 0

    while True:
        mask = get_forklift_accessible_mask(roll_arrgnmt)

        n_rolls = 0
        n_rows, n_cols = mask.shape
        for r in range(n_rows):
            for c in range(n_cols):
                if mask[r, c]:
                    n_rolls += 1

        total_rolls_accessible += n_rolls

        if not repeated or (n_rolls == 0):
            break

        # forklift removes those rolls
        for r in range(n_rows):
            for c in range(n_cols):
                if mask[r, c]:
                    roll_arrgnmt[r, c] = 0

    return total_rolls_accessible
