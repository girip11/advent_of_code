import sys
from functools import reduce
from typing import List, Iterable


def find_aggregate_frequency(frequencies: Iterable[int]) -> int:
    """
        Input: Accepts a list containing a positive or negative frequency values.
        This methods returns the final sum of all the frequencies.
    """

    # tryout functional programming in python
    return reduce(lambda a, b: a + b, frequencies)


def main(args: List[str]) -> None:
    """
        This is the entry point.
    """
    input_frequencies: Iterable[int] = map(int, sys.stdin)
    print(f"Final frequency: {find_aggregate_frequency(input_frequencies)}")


if __name__ == "__main__":
    main(sys.argv)
