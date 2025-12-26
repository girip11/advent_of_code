import sys
from itertools import cycle
from typing import List, MutableSet, Optional


def find_first_repeating_frequency(frequencies: List[int]) -> Optional[int]:
    """
    Input: Accepts an array containing a positive or negative frequency value.
    This methods returns the first repeating among the aggregated frequencies.
    """
    first_repeating_frequency = None

    if len(frequencies) == 0:
        return first_repeating_frequency

    current_frequency: int = 0
    computed_frequencies: MutableSet[int] = {current_frequency}

    for count, freq in enumerate(cycle(frequencies)):
        current_frequency += freq

        # In python, set contains and add operations take up O(1)
        if current_frequency in computed_frequencies:
            first_repeating_frequency = current_frequency
            print(f"Iterations spent: {count}")
            break

        computed_frequencies.add(current_frequency)

    print(f"Total unique frequencies: {len(computed_frequencies)}")
    return first_repeating_frequency


def main(*_: str) -> None:
    """
    This is the entry point.
    """
    input_frequencies: List[int] = list(map(int, sys.stdin))

    print(f"First repeating frequency: {find_first_repeating_frequency(input_frequencies)}")


if __name__ == "__main__":
    main(*sys.argv)
