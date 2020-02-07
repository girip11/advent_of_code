import sys


def _parse_int(s):
    return int(s) if s else None


def find_aggregate_frequency(frequencies_file):
    """
        Input: Accepts a file with each line containing a positive or negative frequency value.
        This methods returns the final sum of all the frequencies.
    """
    aggregated_frequency = 0

    with open(frequencies_file, "r") as frequencies:

        for frequency_str in frequencies:
            try:
                if frequency := _parse_int(frequency_str):
                    aggregated_frequency += frequency
            except ValueError:
                print(f"Invalid frequency value received. Value: {frequency_str}")

    return aggregated_frequency


def main(args):
    """
        This is the entry point.
    """
    if len(args) != 2 or len(args[1].strip()) == 0:
        print("Please provide the input file for the puzzle.")
        print("Usage: puzzle_1.py <input_file>")
        return

    print(f"Final frequency: {find_aggregate_frequency(args[1])}")


if __name__ == "__main__":
    main(sys.argv)
