import sys
import os
from pathlib import Path
from typing import Iterable, List, Mapping
from .day4_puzzle import (
    GuardActivity,
    GuardActivityLog,
    get_guard_activity_logs,
    get_guard_activities,
    find_sleepiest_guard,
    find_sleepiest_minute,
    find_freq_sleepiest_minute,
)


def get_input(input_file_name: str) -> Mapping[int, GuardActivity]:
    input_file_path: str = os.path.join(
        Path(os.path.dirname(__file__)).parent, input_file_name
    )

    guard_activities: Mapping[int, GuardActivity] = {}

    with open(input_file_path) as input_file:
        guard_activity_logs: List[GuardActivityLog] = get_guard_activity_logs(
            sorted(activity for activity in input_file)
        )
        guard_activities = get_guard_activities(guard_activity_logs)

    return guard_activities


def test_find_sleepiest_guard() -> None:
    guards: Mapping[int, GuardActivity] = get_input("puzzle_simple_input.txt")
    sleepiest_guard: int = find_sleepiest_guard(guards)
    assert sleepiest_guard == 10
    assert find_sleepiest_minute(guards[sleepiest_guard]) == (24, 2)


def test_find_freq_sleepiest_minute() -> None:
    guards: Mapping[int, GuardActivity] = get_input("puzzle_simple_input.txt")
    assert find_freq_sleepiest_minute(guards) == (99, 45)
