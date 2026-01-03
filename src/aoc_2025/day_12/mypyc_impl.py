# My logic: for every present, combine 2 of them(if n > 1) and use that rectangle
# to keep filling the available region. After filling each present in pairs
# there might be some presents left(n=1). Try to fill them as 3*3 rectange in the remaining space
# If not, combine each of them and see if we can fill.
# This logic is not generic. I came up with this after profiling the sample and the input
# Input is too large and I am not sure if this logic will work.
# `46x37: 23 26 23 34 38 36` So this made me to pack 2 at a time.
# To reduce complexity, I will handcraft the matrix that gives the rectangle size
# when 2 presents are combined for sample and input.
import itertools
import re
from collections.abc import Generator, Iterator
from dataclasses import dataclass, field
from functools import cached_property
from typing import cast

type Shape = tuple[tuple[str, str, str], tuple[str, str, str], tuple[str, str, str]]


@dataclass(frozen=True)
class Present:
    id_: int
    shape: Shape

    @property
    def filled(self) -> int:
        return sum(1 for c in itertools.chain.from_iterable(self.shape) if c == "#")


@dataclass
class Column:
    tr: int
    tc: int
    start: int
    width: int = field(default=0)
    entries: list[tuple[int, int]] = field(default_factory=list)

    def try_add(self, entry: tuple[int, int]) -> bool:
        curr_width = max(self.width, entry[1])
        # exceeds column boundary
        if self.start + curr_width > self.tc:
            return False

        # Not enough rows to be placed
        if (self.tr - sum(e[0] for e in self.entries)) < entry[0]:
            return False

        # Can be placed.
        self.width = curr_width
        self.entries.append(entry)
        return True


@dataclass
class Region:
    size: tuple[int, int]
    presents: list[int]
    columns: list[Column] = field(init=False)

    def __post_init__(self) -> None:
        self.columns = [Column(tr=self.size[0], tc=self.size[1], start=0)]

    @cached_property
    def cells(self) -> int:
        return self.size[0] * self.size[1]

    def reset_columns(self) -> None:
        self.columns = [Column(tr=self.size[0], tc=self.size[1], start=0)]

    def fill(self, fill_shape: tuple[int, int]) -> bool:
        if any(col.try_add(fill_shape) for col in self.columns):
            return True
        # Check the feasibility of adding a new column
        new_col_start = self.columns[-1].start + self.columns[-1].width
        if (self.size[1] - new_col_start) < fill_shape[1]:
            return False  # Early exit

        new_column = Column(tr=self.size[0], tc=self.size[1], start=new_col_start)
        self.columns.append(new_column)
        return new_column.try_add(fill_shape)


PRESENT_INDEX = re.compile(r"\d+:")


def parse_presents_and_regions(lines: Iterator[str]) -> tuple[list[Present], list[Region]]:
    regions: list[Region] = []
    presents: list[Present] = []

    while True:
        try:
            line = next(lines)
            match line.strip():
                case idx if idx.endswith(":"):
                    present_id = int(idx.rstrip(":"))
                    shape: Shape = cast(Shape, tuple(tuple(next(lines).strip()) for i in range(3)))
                    presents.append(Present(id_=present_id, shape=shape))
                case reg_row if "x" in reg_row:
                    size = cast(
                        tuple[int, int],
                        tuple(map(int, reg_row.split(":")[0].split("x"))),
                    )
                    p_counts: list[int] = list(
                        map(lambda v: int(v), reg_row.split(":")[1].strip().split(" "))
                    )
                    regions.append(Region(size=size, presents=p_counts))
                case _:
                    pass
        except StopIteration:
            break

    # print(presents)
    # print(regions)
    return (presents, regions)


def does_overflow(region: Region, presents: list[Present]) -> bool:
    return (
        sum(
            presents[p_idx].filled * count
            for p_idx, count in enumerate(region.presents)
            if count > 0
        )
        > region.cells
    )


def get_n_presents(
    reg: Region, n: int, packing_sizes: dict[tuple[int, ...], tuple[int, int]]
) -> Generator[tuple[int, ...]]:
    presents: list[int] = reg.presents.copy()

    # Return the presents in pairs. This is just to make life easier rather than
    # generating combinations like taking 1 at a time, then 2 at a time,
    for p_idx, p_count in sorted(enumerate(reg.presents), key=lambda e: e[1], reverse=True):
        presents[p_idx] = p_count % n
        for _ in range(p_count // n):
            yield tuple([p_idx] * n)

    # Loop through the remaining presents
    while sum(presents) > 0:
        rem_presents = [idx for idx in range(len(presents)) if presents[idx] > 0]

        if len(rem_presents) > 1:
            pair = min(
                [(i, j) for (i, j) in itertools.combinations(rem_presents, 2)],
                key=lambda p: packing_sizes[p],
            )

            presents[pair[0]] -= 1
            presents[pair[1]] -= 1
            yield pair
        else:
            if len(rem_presents) == 1:
                presents[rem_presents[0]] -= 1
                yield (rem_presents[0],)


def can_presents_fit_region(
    reg: Region, presents: list[Present], packing_sizes: dict[tuple[int, ...], tuple[int, int]]
) -> bool:
    # Keep track of the region filled
    presents_filled: list[int] = reg.presents.copy()

    # Iterate through the presents from most count to least.
    # Finish packing things as even numbers and then finally see if you can place
    # different shapes combined in the remaining space.
    for n in [1, 2]:
        # print(f"Trying with packing {n} present at a time.")
        # By sorting, I am just trying to place shapes of similar size closer
        for pair in sorted(
            # I want the single items to be placed at last, hence negative pair length
            get_n_presents(reg, n, packing_sizes),
            key=lambda p: (-len(p), packing_sizes[p]),
        ):
            # print(n, reg.size, pair)
            packing_size = packing_sizes[pair]
            for i, j in [(0, 1), (1, 0)] if packing_size[0] != packing_size[1] else [(0, 1)]:
                if reg.fill((packing_size[i], packing_size[j])):
                    for idx in range(len(pair)):
                        presents_filled[pair[idx]] -= 1
                    break
            else:
                # Cannot fill this present
                break
        else:
            break

        # reset for next iteration
        presents_filled = reg.presents.copy()
        reg.reset_columns()

    return sum(presents_filled) == 0


def count_fitting_regions(
    regions: list[Region],
    presents: list[Present],
    packing_sizes: dict[tuple[int, ...], tuple[int, int]],
) -> int:
    reg_count: int = 0
    for idx, reg in enumerate(regions):
        if does_overflow(reg, presents):
            continue
        if can_presents_fit_region(reg, presents, packing_sizes):
            reg_count += 1
        else:
            print(f"Cannot fill region: {idx}, {reg}")

    return reg_count
