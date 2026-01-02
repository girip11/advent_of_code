import time
from sys import argv

from aoc_2025.day_11 import mypyc_impl


def solve_using_mypyc(input_file: str) -> None:
    with open(input_file) as f:
        start_time = time.perf_counter_ns()
        in_conn: dict[str, list[str]] = {
            comp[0]: comp[1].strip().split(" ") for line in f if (comp := line.split(":"))
        }
        levels = mypyc_impl.get_device_levels(in_conn, src="you", dest="out")
        part1_res = mypyc_impl.get_total_paths_between_src_dest(
            in_conn, levels, src="you", dest="out"
        )
        levels = mypyc_impl.get_device_levels(in_conn, src="svr", dest="out")
        part2_res = mypyc_impl.get_total_paths_between_src_dest_with_hops(
            in_conn, levels, src="svr", dest="out", hops={"dac", "fft"}
        )
        end_time = time.perf_counter_ns()
        print(f"Mypyc Impl, Part 1 result: {part1_res}. ")
        print(f"Mypyc Impl, Part 2 result: {part2_res}. ")
        print(f"Time taken: {end_time - start_time}ns")


def main(input_file: str) -> None:
    solve_using_mypyc(input_file)


if __name__ == "__main__":
    main(argv[1])
