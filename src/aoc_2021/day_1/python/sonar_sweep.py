import sys
from typing import List


def count_sliding_window_increase(measurements: List[int], window_size: int) -> int:
    num = len(measurements)

    totals = [sum(measurements[idx : idx + window_size]) for idx in range(0, num - window_size + 1)]

    return count_measurement_increase(totals)


def count_measurement_increase(measurements: List[int]) -> int:
    num = len(measurements)
    counter: int = 0
    for idx in range(0, num - 1):
        if measurements[idx + 1] > measurements[idx]:
            counter += 1

    return counter


def main(*_: str) -> None:
    depth_measurements: List[int] = list(map(int, sys.stdin.readlines()))
    print(count_measurement_increase(depth_measurements))
    print(count_sliding_window_increase(depth_measurements, 3))


if __name__ == "__main__":
    main(*sys.argv[1:])
