import time
from sys import argv

import numpy as np

from aoc_2025.day_04 import mypyc_impl, numba_impl


def solve_using_mypyc(input_file: str) -> None:
    with open(input_file) as f:
        rolls = [list(roll) for line in f if (roll := line.strip())]
        start_time = time.perf_counter_ns()
        rolls_accessible = mypyc_impl.get_forklift_accessible_rolls_repeated(rolls, repeated=False)
        end_time = time.perf_counter_ns()
        print(
            f"Mypyc Impl, Rolls acccessible: {rolls_accessible}. Time taken: {end_time - start_time}ns"
        )

        # part-2
        start_time = time.perf_counter_ns()
        rolls_accessible = mypyc_impl.get_forklift_accessible_rolls_repeated(rolls, repeated=True)
        end_time = time.perf_counter_ns()
        print(
            f"Mypyc Impl, Rolls acccessible: {rolls_accessible}. Time taken: {end_time - start_time}ns"
        )


def solve_using_numba(input_file: str) -> None:
    with open(input_file) as f:
        rolls: np.ndarray = np.array(
            [list(map(lambda c: int(c == "@"), roll)) for line in f if (roll := line.strip())],
            dtype=np.int8,
        )
        # JIT priming
        _ = numba_impl.get_forklift_accessible_rolls_repeated(rolls, repeated=False)
        # part-1
        start_time = time.perf_counter_ns()
        rolls_accessible = numba_impl.get_forklift_accessible_rolls_repeated(rolls, repeated=False)
        end_time = time.perf_counter_ns()
        print(
            f"Numba Impl, Rolls acccessible: {rolls_accessible}. Time taken: {end_time - start_time}ns"
        )

        # part-2
        start_time = time.perf_counter_ns()
        rolls_accessible = numba_impl.get_forklift_accessible_rolls_repeated(rolls, repeated=True)
        end_time = time.perf_counter_ns()
        print(
            f"Numba Impl, Rolls acccessible: {rolls_accessible}. Time taken: {end_time - start_time}ns"
        )


def main(input_file: str) -> None:
    solve_using_mypyc(input_file)
    solve_using_numba(input_file)


if __name__ == "__main__":
    main(argv[1])
