import os
from pathlib import Path

from puzzle1 import find_aggregate_frequency


def test_aggregate_frequency_1():
    input_file_path = os.path.join(
        Path(os.path.dirname(__file__)).parent, "puzzle1_simple_input.txt"
    )
    with open(input_file_path) as input_file:
        input_frequencies = map(lambda s: int(s), input_file)
        assert find_aggregate_frequency(input_frequencies) == 4


def test_aggregate_frequency_2():
    input_file_path = os.path.join(
        Path(os.path.dirname(__file__)).parent, "puzzle_input.txt"
    )
    with open(input_file_path) as input_file:
        input_frequencies = map(lambda s: int(s), input_file)
        assert find_aggregate_frequency(input_frequencies) == 556
