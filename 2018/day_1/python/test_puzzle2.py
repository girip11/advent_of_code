import os
from pathlib import Path

from puzzle2 import find_first_repeating_frequency


def test_first_repeating_frequency_1():
    input_file_path = os.path.join(
        Path(os.path.dirname(__file__)).parent, "puzzle2_simple_input.txt"
    )
    with open(input_file_path) as input_file:
        input_frequencies = list(map(lambda s: int(s), input_file))
        assert find_first_repeating_frequency(input_frequencies) == 10


def test_first_repeating_frequency_2():
    input_file_path = os.path.join(
        Path(os.path.dirname(__file__)).parent, "puzzle_input.txt"
    )
    with open(input_file_path) as input_file:
        input_frequencies = list(map(lambda s: int(s), input_file))
        assert find_first_repeating_frequency(input_frequencies) == 448
