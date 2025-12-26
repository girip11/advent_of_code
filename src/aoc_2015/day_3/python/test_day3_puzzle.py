from .day3_puzzle import houses_gifted_by_santa, houses_gifted_by_santa_and_robot


def test_houses_gifted_by_santa() -> None:
    navigation: str = "^v^v^v^v^v"
    assert houses_gifted_by_santa(navigation) == 2


def test_houses_gifted_by_santa_and_robot() -> None:
    navigation: str = "^v^v^v^v^v"
    assert houses_gifted_by_santa_and_robot(navigation) == 11
