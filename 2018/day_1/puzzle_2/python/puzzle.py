import sys


def find_first_repeating_frequency(frequencies):
    """
        Input: Accepts an array containing a positive or negative frequency value.
        This methods returns the first repeating among the aggregated frequencies.
    """
    current_frequency = 0
    computed_frequencies = {current_frequency}
    first_repeating_frequency = None
    input_freq_count = len(frequencies)

    if input_freq_count == 0:
        return first_repeating_frequency

    counter = 0

    while first_repeating_frequency == None:
        current_frequency += frequencies[counter % input_freq_count]

        # In python, set contains and add operations take up O(1)
        if current_frequency in computed_frequencies:
            first_repeating_frequency = current_frequency
            break
        else:
            computed_frequencies.add(current_frequency)
            # increment when adding a new frequency
            counter += 1

    print(f"Iterations spent: {counter}")
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
    input_frequencies = []

    for line in sys.stdin:
        if freq := _parse_int(line):
            input_frequencies.append(freq)

    print(
        f"First repeating frequency: {find_first_repeating_frequency(input_frequencies)}"
    )


if __name__ == "__main__":
    main(sys.argv)
