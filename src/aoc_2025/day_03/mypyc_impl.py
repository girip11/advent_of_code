from array import array
from collections.abc import Iterable, Iterator
from functools import reduce


def get_max_joltage(bank: Iterable[int], n_batteries: int, n_slots: int) -> int:
    on_slots = array("I", [0] * n_slots)

    for idx, joltage in enumerate(bank, start=0):
        batteries_left = n_batteries - idx

        # If few batteries are left, ensure slots are adjusted accordingly
        for ith_slot in range(n_slots - min(n_slots, batteries_left), n_slots):
            if on_slots[ith_slot] < joltage:
                # Pick that slot and reset slots following it.
                on_slots[ith_slot] = joltage
                for jth_slot in range(ith_slot + 1, n_slots):
                    on_slots[jth_slot] = 0
                break

    opt_joltage = reduce(lambda acc, b: acc * 10 + b, on_slots, 0)
    # print(opt_joltage)
    return opt_joltage


def get_total_output_joltage_part1(banks: Iterator[str]) -> int:
    return sum(get_max_joltage(map(int, bank), len(bank), n_slots=2) for bank in banks)


def get_total_output_joltage_part2(banks: Iterator[str]) -> int:
    return sum(get_max_joltage(map(int, bank), len(bank), n_slots=12) for bank in banks)
