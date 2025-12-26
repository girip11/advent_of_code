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


def solve_using_codon(input_file: str) -> None:
    pass
    # with open(input_file) as f:
    #     instructions = [cl for line in f if (cl := line.strip())]

    #     # prime the JIT
    #     _ = codon_impl.get_password(ins=instructions)
    #     start_time = time.perf_counter_ns()
    #     passwd = codon_impl.get_password(ins=instructions)
    #     end_time = time.perf_counter_ns()
    #     print(f"Codon Impl, Password: {passwd}. Time taken: {end_time - start_time}ns")


def main(input_file: str) -> None:
    solve_using_mypyc(input_file)
    # solve_using_codon(input_file)


if __name__ == "__main__":
    main(argv[1])
