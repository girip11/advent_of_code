import time
from sys import argv

from aoc_2025.day_10 import mypyc_impl, part2
from aoc_2025.day_10.mypyc_impl import Machine


def solve_using_mypyc(input_file: str) -> None:
    with open(input_file) as f:
        start_time = time.perf_counter_ns()
        machines: list[Machine] = mypyc_impl.parse_machines(iter(f))
        part1_res = mypyc_impl.compute_fewest_button_presses(machines)
        part2_res = part2.compute_fewest_joltage_button_presses(machines)
        end_time = time.perf_counter_ns()
        print(f"Mypyc Impl, Part 1 result: {part1_res}. ")
        print(f"Mypyc Impl, Part 2 result: {part2_res}. ")
        print(f"Time taken: {end_time - start_time}ns")


def main(input_file: str) -> None:
    solve_using_mypyc(input_file)


if __name__ == "__main__":
    main(argv[1])
