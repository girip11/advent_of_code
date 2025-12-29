import time
from sys import argv

from aoc_2025.day_05 import mypyc_impl


def solve_using_mypyc(input_file: str) -> None:
    with open(input_file) as f:
        db = iter(f)
        start_time = time.perf_counter_ns()
        avail_fresh_ingredients, total_fresh_ingredients = (
            mypyc_impl.count_available_fresh_ingredients(db)
        )
        end_time = time.perf_counter_ns()
        print(f"Mypyc Impl, Available fresh ingredients: {avail_fresh_ingredients}. ")
        print(f"Mypyc Impl, Total fresh ingredients: {total_fresh_ingredients}. ")
        print(f"Time taken: {end_time - start_time}ns")


def main(input_file: str) -> None:
    solve_using_mypyc(input_file)


if __name__ == "__main__":
    main(argv[1])
