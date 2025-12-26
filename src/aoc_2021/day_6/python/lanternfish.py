import sys
from collections import defaultdict
from typing import Dict, List

NEW_BORN_INTERNAL_TIMER = 8
INTERNAL_TIMER_RESET = 6


# This doesnot scale well when the days increase as the fishes increase exponentially
def simulate_lanternfish(lanternfish_internal_timers: List[int], days: int) -> int:
    internal_timers: List[int] = lanternfish_internal_timers.copy()

    for day in range(days):
        new_borns: int = 0
        for lanternfish_idx, _ in enumerate(internal_timers):
            timer = internal_timers[lanternfish_idx]
            if timer == 0:
                internal_timers[lanternfish_idx] = INTERNAL_TIMER_RESET  # reset timer to 6
                new_borns += 1  # add a new born
            else:
                internal_timers[lanternfish_idx] -= 1
        print(f"{day}:{new_borns}")
        internal_timers.extend([NEW_BORN_INTERNAL_TIMER] * new_borns)

    return len(internal_timers)


def simulate_lanternfish2(lanternfish_internal_timers: List[int], days: int) -> int:
    internal_timer_buckets: Dict[int, int] = defaultdict(int)

    for i in range(9):
        internal_timer_buckets[i] = 0

    for timer in lanternfish_internal_timers:
        internal_timer_buckets[timer] += 1

    for day in range(days):
        print(day)
        new_parents = new_borns = internal_timer_buckets[0]
        for internal_timer in sorted(internal_timer_buckets.keys()):
            if internal_timer > 0:
                internal_timer_buckets[internal_timer - 1] = internal_timer_buckets[internal_timer]

        internal_timer_buckets[NEW_BORN_INTERNAL_TIMER] = new_borns
        # fish from day 7 and new parents
        internal_timer_buckets[INTERNAL_TIMER_RESET] += new_parents

    return sum(internal_timer_buckets.values())


def main(*_: str) -> None:
    lanternfish_internal_timers: List[int] = [
        int(i) for i in sys.stdin.readline().strip().split(",")
    ]

    # part-1
    print(simulate_lanternfish(lanternfish_internal_timers, 80))

    # part-2
    print(simulate_lanternfish2(lanternfish_internal_timers, 256))


if __name__ == "__main__":
    main(*sys.argv[1:])
