import sys
from functools import reduce
from typing import List, Iterable


def find_aggregate_frequency(frequencies: List[int]) -> int:
    """
        Input: Accepts a list containing a positive or negative frequency values.
        This methods returns the final sum of all the frequencies.
    """

    # tryout functional programming in python
    return reduce(lambda a, b: a + b, frequencies)


def _parse_int(s: str) -> int:
    """
        Just removes leading and trailing spaces if any and converts the string to int.
    """
    return int(s) if (s := s.strip()) else None


def main(args: List[str]) -> None:
    """
        This is the entry point.
    """
    input_frequencies: Iterable[int] = map(_parse_int, sys.stdin)
    print(f"Final frequency: {find_aggregate_frequency(input_frequencies)}")


if __name__ == "__main__":
    main(sys.argv)
