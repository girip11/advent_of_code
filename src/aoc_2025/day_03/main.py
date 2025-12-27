import time
from sys import argv

from aoc_2025.day_03 import mypyc_impl


def solve_using_mypyc(input_file: str) -> None:
    with open(input_file) as f:
        banks = [bank for line in f if (bank := line.strip())]
        # part-1
        start_time = time.perf_counter_ns()
        total_joltage = mypyc_impl.get_total_output_joltage_part1(banks=iter(banks))
        end_time = time.perf_counter_ns()
        print(
            f"Mypyc Impl, Invalid PRD IDs sum: {total_joltage}. Time taken: {end_time - start_time}ns"
        )

        # part-1
        start_time = time.perf_counter_ns()
        total_joltage = mypyc_impl.get_total_output_joltage_part2(banks=iter(banks))
        end_time = time.perf_counter_ns()
        print(
            f"Mypyc Impl, Invalid PRD IDs sum: {total_joltage}. Time taken: {end_time - start_time}ns"
        )


def main(input_file: str) -> None:
    solve_using_mypyc(input_file)


if __name__ == "__main__":
    main(argv[1])
