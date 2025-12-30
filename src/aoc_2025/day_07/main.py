import time
from sys import argv

from aoc_2025.day_07 import mypyc_impl


def solve_using_mypyc(input_file: str) -> None:
    with open(input_file) as f:
        start_time = time.perf_counter_ns()
        manifold = [line for line in f if len(line.strip()) > 0]
        root = mypyc_impl.construct_splitter_graph(manifold)
        part1_res = mypyc_impl.get_tachyon_beam_split_count(root)
        part2_res = mypyc_impl.get_tachyon_timelines(root)
        end_time = time.perf_counter_ns()
        print(f"Mypyc Impl, Tachyon beams split: {part1_res}. ")
        print(f"Mypyc Impl, Tachyon timelines: {part2_res}. ")
        print(f"Time taken: {end_time - start_time}ns")


def main(input_file: str) -> None:
    solve_using_mypyc(input_file)


if __name__ == "__main__":
    main(argv[1])
