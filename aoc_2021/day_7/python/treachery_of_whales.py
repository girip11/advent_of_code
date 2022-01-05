import sys
from typing import Callable, List


def constant_rate(pos: int, target_pos: int) -> int:
    return abs(pos - target_pos)


def linear_increase_rate(pos: int, target_pos: int) -> int:
    steps = abs(pos - target_pos)
    return (steps * (steps + 1)) // 2


# try aligning  all crabs to each position starting from 0
def compute_optimal_fuel(
    crab_positions: List[int], fuel_rate_computer: Callable[[int, int], int]
) -> int:
    max_position = max(crab_positions)
    print(max_position)

    optimal_fuel: int = sys.maxsize
    optimal_align_pos: int = -1

    for align_pos in range(max_position + 1):
        current_fuel = 0
        for pos in crab_positions:
            current_fuel += fuel_rate_computer(pos, align_pos)

        if current_fuel < optimal_fuel:
            optimal_align_pos = align_pos
            optimal_fuel = current_fuel

    print(optimal_align_pos, optimal_fuel)

    return optimal_fuel


def main(*_: str) -> None:
    crab_positions: List[int] = [int(i) for i in sys.stdin.readline().strip().split(",")]

    print(crab_positions)
    # part-1
    # print(compute_optimal_fuel(crab_positions, constant_rate))

    # part-2
    print(compute_optimal_fuel(crab_positions, linear_increase_rate))


if __name__ == "__main__":
    main(*sys.argv[1:])
