from aoc_2021.day_1.python.sonar_sweep import (
    count_measurement_increase,
    count_sliding_window_increase,
)


def test_count_measurement_increase() -> None:
    measurements = [
        199,
        200,
        208,
        210,
        200,
        207,
        240,
        269,
        260,
        263,
    ]
    assert count_measurement_increase(measurements) == 7


def test_count_sliding_window_increase() -> None:
    measurements = [
        199,
        200,
        208,
        210,
        200,
        207,
        240,
        269,
        260,
        263,
    ]
    assert count_sliding_window_increase(measurements, 3) == 5
