import os
from pathlib import Path
from typing import List

from .day2_puzzle1 import PresentBox, find_wrapping_paper_length, find_ribbon_length


def test_find_wrapping_paper_length() -> None:
    input: List[PresentBox] = [PresentBox(2, 3, 4), PresentBox(1, 1, 10)]
    assert find_wrapping_paper_length(input) == 101


def test_find_ribbon_length() -> None:
    input: List[PresentBox] = [PresentBox(2, 3, 4), PresentBox(1, 1, 10)]
    assert find_ribbon_length(input) == 48
