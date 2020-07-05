from aoc_2018.day_9.python.day9_puzzle import get_highest_score


def test_highest_score():
    assert get_highest_score(10, 1618) == 8317
    assert get_highest_score(13, 7999) == 146373
    assert get_highest_score(17, 1104) == 2764
    assert get_highest_score(21, 6111) == 54718
    assert get_highest_score(30, 5807) == 37305
