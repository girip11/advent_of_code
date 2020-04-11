import sys
from functools import reduce
from typing import Callable, List


def get_dest_floor(floor_instructions: str) -> int:
    func: Callable[
        [int, str], int
    ] = lambda acc, ins: acc + 1 if ins == "(" else acc - 1
    return reduce(func, floor_instructions, 0)


def get_first_basement_ins_pos(floor_instructions: str) -> int:
    floor_count: int = 0
    for pos, ins in enumerate(floor_instructions):
        floor_count += 1 if ins == "(" else -1

        if floor_count == -1:
            return pos + 1

    return -1


def main(args: List[str]) -> None:
    """
        This is the entry point.
    """
    floor_instructions: str = sys.stdin.read().strip()
    print(f"Floor: {get_dest_floor(floor_instructions)}")
    print(f"First Basement position: {get_first_basement_ins_pos(floor_instructions)}")


if __name__ == "__main__":
    main(sys.argv)
