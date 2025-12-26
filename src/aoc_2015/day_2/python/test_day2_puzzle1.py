from typing import List

from .day2_puzzle1 import PresentBox, find_ribbon_length, find_wrapping_paper_length


def test_find_wrapping_paper_length() -> None:
    input_boxes: List[PresentBox] = [PresentBox(2, 3, 4), PresentBox(1, 1, 10)]
    assert find_wrapping_paper_length(input_boxes) == 101


def test_find_ribbon_length() -> None:
    input_boxes: List[PresentBox] = [PresentBox(2, 3, 4), PresentBox(1, 1, 10)]
    assert find_ribbon_length(input_boxes) == 48
