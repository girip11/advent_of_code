import sys


def find_first_repeating_frequency(frequencies):
    """
        Input: Accepts an array containing a positive or negative frequency value.
        This methods returns the first repeating among the aggregated frequencies.
    """
    current_frequency = 0
    known_frequencies = {current_frequency}
    first_repeating_frequency = None

    counter = 0
    iterations = 0

    while first_repeating_frequency == None:
        if counter == len(frequencies):
            counter = 0

        current_frequency += frequencies[counter]

        if current_frequency in known_frequencies:
            first_repeating_frequency = current_frequency
            break
        else:
            known_frequencies.add(current_frequency)
            counter += 1

        iterations += 1

    print(f"Iterating spent: {iterations}")
    print(f"Total unique frequencies: {len(known_frequencies)}")
    return first_repeating_frequency


def main(args):
    """
        This is the entry point.
    """
    if len(args) != 2 or len(args[1].strip()) == 0:
        print("Please provide the input file for the puzzle.")
        print("Usage: puzzle_1.py <input_file>")
        return

    input_frequencies = []

    with open(args[1], "r") as frequencies_file:
        for freq in frequencies_file:
            if freq:
                input_frequencies.append(int(freq))

    print(
        f"First repeating frequency: {find_first_repeating_frequency(input_frequencies)}"
    )


if __name__ == "__main__":
    main(sys.argv)
