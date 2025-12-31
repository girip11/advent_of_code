import time
from pathlib import Path
from sys import argv
from typing import cast

from aoc_2025.day_08 import mypyc_impl
from aoc_2025.day_08.mypyc_impl import CircuitManager


def solve_using_mypyc(input_file: str) -> None:
    n = 10 if Path(input_file).stem == "sample" else 1000
    with open(input_file) as f:
        start_time = time.perf_counter_ns()
        j_boxes: list[tuple[int, int, int]] = [
            cast(tuple[int, int, int], tuple(map(int, line.split(","))))
            for line in f
            if len(line.strip()) > 0
        ]
        circuit_mgr = CircuitManager(j_boxes)
        part1_res = mypyc_impl.get_circuit_size(circuit_mgr, n)
        part2_res = mypyc_impl.get_farthest_junction_boxes(circuit_mgr)
        end_time = time.perf_counter_ns()
        print(f"Mypyc Impl, Part 1 result: {part1_res}. ")
        print(f"Mypyc Impl, Part 2 result: {part2_res}. ")
        print(f"Time taken: {end_time - start_time}ns")


def main(input_file: str) -> None:
    solve_using_mypyc(input_file)


if __name__ == "__main__":
    main(argv[1])
