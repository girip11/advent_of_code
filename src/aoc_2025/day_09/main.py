import time
from sys import argv
from typing import cast

from aoc_2025.day_09 import mypyc_impl
from aoc_2025.day_09.mypyc_impl import Position


def solve_using_mypyc(input_file: str) -> None:
    with open(input_file) as f:
        start_time = time.perf_counter_ns()
        red_tiles_xy: list[Position] = [
            cast(Position, tuple(map(int, line.split(",")))) for line in f if len(line.strip()) > 0
        ]
        part1_res = mypyc_impl.get_largest_rectangle_area(red_tiles_xy=red_tiles_xy)
        part2_res = mypyc_impl.get_largest_rectangle_area_with_only_green_red_tiles(
            red_tiles_xy=red_tiles_xy
        )
        end_time = time.perf_counter_ns()
        print(f"Mypyc Impl, Part 1 result: {part1_res}. ")
        print(f"Mypyc Impl, Part 2 result: {part2_res}. ")
        print(f"Time taken: {end_time - start_time}ns")


def main(input_file: str) -> None:
    solve_using_mypyc(input_file)


if __name__ == "__main__":
    main(argv[1])
