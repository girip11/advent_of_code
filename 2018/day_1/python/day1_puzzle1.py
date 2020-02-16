import sys
from functools import reduce


def find_aggregate_frequency(frequencies):
    """
        Input: Accepts a list containing a positive or negative frequency values.
        This methods returns the final sum of all the frequencies.
    """

    # tryout functional programming in python
    return reduce(lambda a, b: a + b, frequencies)


def _parse_int(s):
    """
        Just removes leading and trailing spaces if any and converts the string to int.
    """
    return int(s) if (s := s.strip()) else None


def main(args):
    """
        This is the entry point.
    """
    input_frequencies = map(_parse_int, sys.stdin)
    print(f"Final frequency: {find_aggregate_frequency(input_frequencies)}")


if __name__ == "__main__":
    main(sys.argv)
