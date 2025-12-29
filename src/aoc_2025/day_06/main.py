import time
from sys import argv

from aoc_2025.day_06 import mypyc_impl


def solve_using_mypyc(input_file: str) -> None:
    with open(input_file) as f:
        homework = [line for line in f if len(line.strip()) > 0]
        start_time = time.perf_counter_ns()
        result = mypyc_impl.get_math_homework_result(iter(homework))
        end_time = time.perf_counter_ns()
        print(f"Mypyc Impl, Homework result: {result}. ")
        print(f"Time taken: {end_time - start_time}ns")

        start_time = time.perf_counter_ns()
        result = mypyc_impl.get_math_homework_result_part2(homework)
        end_time = time.perf_counter_ns()
        print(f"Mypyc Impl, Homework result part 2: {result}. ")
        print(f"Time taken: {end_time - start_time}ns")


def main(input_file: str) -> None:
    solve_using_mypyc(input_file)


if __name__ == "__main__":
    main(argv[1])
