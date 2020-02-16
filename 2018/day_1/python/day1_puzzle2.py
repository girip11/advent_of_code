import sys

from itertools import cycle


def find_first_repeating_frequency(frequencies):
    """
        Input: Accepts an array containing a positive or negative frequency value.
        This methods returns the first repeating among the aggregated frequencies.
    """
    first_repeating_frequency = None

    if len(frequencies) == 0:
        return first_repeating_frequency

    current_frequency = 0
    computed_frequencies = {current_frequency}

    for c, freq in enumerate(cycle(frequencies)):
        current_frequency += freq

        # In python, set contains and add operations take up O(1)
        if current_frequency in computed_frequencies:
            first_repeating_frequency = current_frequency
            print(f"Iterations spent: {c}")
            break
        else:
            computed_frequencies.add(current_frequency)

    print(f"Total unique frequencies: {len(computed_frequencies)}")
    return first_repeating_frequency


def _parse_int(s):
    """
        Just removes leading and trailing spaces if any and converts the string to int.
    """
    return int(s) if (s := s.strip()) else None


def main(args):
    """
        This is the entry point.
    """
    input_frequencies = list(map(_parse_int, sys.stdin))

    print(
        f"First repeating frequency: {find_first_repeating_frequency(input_frequencies)}"
    )


if __name__ == "__main__":
    main(sys.argv)
