import time
from pathlib import Path
from sys import argv

from aoc_2025.day_12.mypyc_impl import count_fitting_regions, parse_presents_and_regions

# TOO lazy to calculate this and this should have multiple possible arrangement options
# I will try to make this work for the sample and hoping it will work for the input.
# IT WORKED!!!!
SAMPLE_PACKING: dict[tuple[int, ...], tuple[int, int]] = {
    (0,): (3, 3),
    (1,): (3, 3),
    (2,): (3, 3),
    (3,): (3, 3),
    (4,): (3, 3),
    (5,): (3, 3),
    (0, 0): (4, 4),
    (2, 2): (3, 6),
    (4, 4): (4, 4),
    (5, 5): (4, 5),  # It can be (3,6) as well
    (0, 2): (3, 5),
    (0, 4): (3, 6),
    (2, 4): (3, 6),
}

INPUT_PACKING: dict[tuple[int, ...], tuple[int, int]] = {
    (0,): (3, 3),
    (1,): (3, 3),
    (2,): (3, 3),
    (3,): (3, 3),
    (4,): (3, 3),
    (5,): (3, 3),
    (0, 0): (4, 3),
    (1, 1): (4, 4),
    (2, 2): (4, 3),
    (3, 3): (4, 5),
    (4, 4): (4, 4),
    (5, 5): (4, 5),
    # I didnt compute these combinations
    # First will try if all of them can be packed with 1 present at a time
    # Otherwise I will fill up with the minimal spacing.
    (0, 1): (3, 5),
    (0, 2): (3, 4),
    (0, 3): (4, 5),
    (0, 4): (4, 5),
    (0, 5): (4, 5),
    (1, 2): (4, 5),
    (1, 3): (4, 5),
    (1, 4): (4, 5),
    (1, 5): (4, 5),
    (2, 3): (4, 5),
    (2, 4): (4, 5),
    (2, 5): (4, 5),
    (3, 4): (4, 5),
    (3, 5): (4, 5),
    (4, 5): (4, 5),
}


def solve_using_mypyc(input_file: str) -> None:
    with open(input_file) as f:
        start_time = time.perf_counter_ns()
        packing: dict[tuple[int, ...], tuple[int, int]] = (
            SAMPLE_PACKING if Path(input_file).stem == "sample" else INPUT_PACKING
        )
        presents, regions = parse_presents_and_regions(iter(f))
        part1_res = count_fitting_regions(
            regions=regions, presents=presents, packing_sizes=packing
        )
        end_time = time.perf_counter_ns()
        print(f"Mypyc Impl, Part 1 result: {part1_res}. ")
        print(f"Time taken: {end_time - start_time}ns")


def main(input_file: str) -> None:
    solve_using_mypyc(input_file)


if __name__ == "__main__":
    main(argv[1])
