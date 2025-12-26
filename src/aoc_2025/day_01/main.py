import time
from sys import argv

from numba.typed import List

from aoc_2025.day_01 import codon_impl, mypyc_impl, numba_impl


def main(input_file: str) -> None:
    with open(input_file) as f:
        instructions = [cl for line in f if (cl := line.strip())]

        # part 1
        start_time = time.perf_counter_ns()
        passwd = mypyc_impl.get_password(ins=instructions)
        end_time = time.perf_counter_ns()
        print(f"Mypyc Impl, Password: {passwd}. Time taken: {end_time - start_time}ns")

        # prime the JIT
        _ = codon_impl.get_password(ins=instructions)
        start_time = time.perf_counter_ns()
        passwd = codon_impl.get_password(ins=instructions)
        end_time = time.perf_counter_ns()
        print(f"Codon Impl, Password: {passwd}. Time taken: {end_time - start_time}ns")

        # prime the JIT compiler
        _ = numba_impl.get_password(ins=instructions)
        start_time = time.perf_counter_ns()
        passwd = numba_impl.get_password(ins=instructions)
        end_time = time.perf_counter_ns()
        print(f"Numba Impl, Password: {passwd}. Time taken: {end_time - start_time}ns")

        # prime the JIT compiler
        numba_input = List([s.encode("utf-8") for s in instructions if s])
        _ = numba_impl.get_password_fast(instrs=numba_input)
        start_time = time.perf_counter_ns()
        passwd = numba_impl.get_password_fast(instrs=numba_input)
        end_time = time.perf_counter_ns()
        print(f"Numba Impl Fast, Password: {passwd}. Time taken: {end_time - start_time}ns")

        # part 2
        start_time = time.perf_counter_ns()
        passwd = mypyc_impl.get_password_method2(ins=instructions)
        end_time = time.perf_counter_ns()
        print(f"Mypyc Impl, Password: {passwd}. Time taken: {end_time - start_time}ns")

        # prime the JIT
        _ = codon_impl.get_password_method2(ins=instructions)
        start_time = time.perf_counter_ns()
        passwd = codon_impl.get_password_method2(ins=instructions)
        end_time = time.perf_counter_ns()
        print(f"Codon Impl, Password: {passwd}. Time taken: {end_time - start_time}ns")

        # prime the JIT compiler
        _ = numba_impl.get_password_method2(ins=instructions)
        start_time = time.perf_counter_ns()
        passwd = numba_impl.get_password_method2(ins=instructions)
        end_time = time.perf_counter_ns()
        print(f"Numba Impl, Password: {passwd}. Time taken: {end_time - start_time}ns")

        # prime the JIT compiler
        _ = numba_impl.get_password_method2_fast(instrs=numba_input)
        start_time = time.perf_counter_ns()
        passwd = numba_impl.get_password_method2_fast(instrs=numba_input)
        end_time = time.perf_counter_ns()
        print(f"Numba Impl Fast, Password: {passwd}. Time taken: {end_time - start_time}ns")


if __name__ == "__main__":
    main(argv[1])
