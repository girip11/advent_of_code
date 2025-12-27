import time
from sys import argv

from aoc_2025.day_02 import mypyc_impl


def solve_using_mypyc(input_file: str) -> None:
    with open(input_file) as f:
        input_ = f.read().strip()
        # part-1
        start_time = time.perf_counter_ns()
        passwd = mypyc_impl.get_invalid_prd_ids_sum(prd_id_ranges=input_)
        end_time = time.perf_counter_ns()
        print(f"Mypyc Impl, Invalid PRD IDs sum: {passwd}. Time taken: {end_time - start_time}ns")

        # part-2
        start_time = time.perf_counter_ns()
        passwd = mypyc_impl.get_invalid_prd_ids_sum_multi_seq_len_repeats(prd_id_ranges=input_)
        end_time = time.perf_counter_ns()
        print(f"Mypyc Impl, Invalid PRD IDs sum: {passwd}. Time taken: {end_time - start_time}ns")


def main(input_file: str) -> None:
    solve_using_mypyc(input_file)


if __name__ == "__main__":
    main(argv[1])
