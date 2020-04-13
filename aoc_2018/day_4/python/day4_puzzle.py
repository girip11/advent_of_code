from datetime import datetime, timedelta
from dataclasses import dataclass

import itertools
import re
import sys

from typing import Dict, List, Mapping, Optional, Pattern, Tuple
from functools import reduce


class GuardActivity:
    def __init__(self):
        self._duty_days: Dict[str, List[Tuple[int, int]]] = {}

    def add_duty_day(self, day: str) -> None:
        if day not in self._duty_days:
            self._duty_days[day] = []

    def add_sleep_interval(self, day: str, time_interval: Tuple[int, int]) -> None:
        """
        Time interval contains the minute at which the guard fell asleep
        and the minute at which the guard woke up from sleep.
        Arguments:
            day {str} -- Duty day
            time_interval {Tuple[int, int]} -- sleep interval
        """
        if day not in self._duty_days:
            self.add_duty_day(day)

        self._duty_days[day].append(time_interval)

    def duty_days(self) -> Mapping[str, List[Tuple[int, int]]]:
        return self._duty_days

    def total_sleeping_time(self) -> int:
        def compute_sleeping_time(sleep_intervals: List[Tuple[int, int]]) -> int:
            return reduce(lambda acc, i: acc + (i[1] - i[0]), sleep_intervals, 0)

        time: int = reduce(
            lambda acc, sleep_intervals: acc + compute_sleeping_time(sleep_intervals),
            self._duty_days.values(),
            0,
        )

        return time


@dataclass
class GuardActivityLog:
    time: datetime
    msg: str

    def is_shift_start_log(self) -> bool:
        return "begins shift" in self.msg

    def is_asleep_log(self) -> bool:
        return "asleep" in self.msg

    def is_wakeup_log(self) -> bool:
        return "wakes" in self.msg

    def get_guard_id(self) -> Optional[int]:
        pattern = r".*#(\d*).*"

        if self.is_shift_start_log() and (match := re.match(pattern, self.msg)):
            # match is already checked for None. Suppressing mypy check
            return int(match.groups()[0])  # type: ignore

        return None

    def get_duty_date(self) -> str:
        if self.time.hour == 23:
            return (self.time + timedelta(days=1)).strftime("%Y-%m-%d")

        return self.time.strftime("%Y-%m-%d")


def get_guard_activity_logs(raw_logs: List[str]) -> List[GuardActivityLog]:
    guard_activities: List[GuardActivityLog] = []
    log_pattern: Pattern[str] = re.compile(r"\[(.*)\] (.*)")

    for activity in raw_logs:
        match = log_pattern.match(activity)
        if match and len(match.groups()) == 2:
            activity_time: datetime = datetime.strptime(match.groups()[0], "%Y-%m-%d %H:%M")
            guard_activities.append(GuardActivityLog(activity_time, match.groups()[1]))

    return guard_activities


def get_guard_activities(
    guard_activity_logs: List[GuardActivityLog],
) -> Mapping[int, GuardActivity]:

    guards: Dict[int, GuardActivity] = {}
    current_guard: Optional[int] = None
    sleep_time: Optional[datetime] = None

    for log in guard_activity_logs:
        if log.is_shift_start_log():
            # cleanup the previous sleep time if any before moving on to next guard shift
            # This case is needed when there is no wakeup log found for the guard during
            # the monitored hour
            if current_guard and sleep_time:
                guards[current_guard].add_sleep_interval(
                    sleep_time.strftime("%Y-%m-%d"), (sleep_time.minute, 60)
                )

            current_guard = log.get_guard_id()
            if current_guard:
                if current_guard not in guards:
                    guard_activity: GuardActivity = GuardActivity()
                    guards[current_guard] = guard_activity
                guards[current_guard].add_duty_day(log.get_duty_date())
        elif log.is_asleep_log():
            sleep_time = log.time
        elif log.is_wakeup_log():
            if current_guard and sleep_time:
                guards[current_guard].add_sleep_interval(
                    log.get_duty_date(), (sleep_time.minute, log.time.minute)
                )
                sleep_time = None
        else:
            print(f"Invalid log: {log}")

    return guards


# part 1
def find_sleepiest_guard(guard_activities: Mapping[int, GuardActivity]) -> int:
    """Returns the ID of the guard with most sleep time
    Arguments:
        guard_activities {Mapping[int, GuardActivity]}
    Returns:
        int -- guard ID
    """
    return max(
        guard_activities.keys(),
        key=lambda guard_id: guard_activities[guard_id].total_sleeping_time(),
    )


# common to part 1 and part 2
def find_sleepiest_minute(guard_activity: GuardActivity) -> Tuple[int, int]:
    """Finds the most common minute at which the guard is asleep
    Arguments:
        guard_activity {GuardActivity}
    Returns:
        Tuple[int, int] -- (Minute, Frequency of sleep on that minute)
    """
    monitoring_hour = [0] * 60

    for sleeping_interval in itertools.chain(*guard_activity.duty_days().values()):
        for minute in range(sleeping_interval[0], sleeping_interval[1]):
            monitoring_hour[minute] += 1

    return max(enumerate(monitoring_hour), key=lambda i: i[1])


# part 2
def find_freq_sleepiest_minute(
    guard_activities: Mapping[int, GuardActivity]
) -> Optional[Tuple[int, int]]:
    """
    Finds the guard who sleeps most of the time on a particular minute and the minute of sleep
    Arguments:
        guard_activities {Mapping[int, GuardActivity]}
    Returns:
        Tuple[int, int] -- [Guard ID, Most frequent sleepy minute ]
    """
    sleepiest_minute: int = -1
    sleepiest_minute_freq: int = -1
    sleepiest_guard: Optional[int] = None

    for guard_id, guard_activity in guard_activities.items():
        current_sleepiest_minute, current_sleepiest_minute_freq = find_sleepiest_minute(
            guard_activity
        )

        if current_sleepiest_minute_freq > sleepiest_minute_freq:
            sleepiest_minute_freq = current_sleepiest_minute_freq
            sleepiest_minute = current_sleepiest_minute
            sleepiest_guard = guard_id

    if sleepiest_guard is None:
        return None

    return sleepiest_guard, sleepiest_minute


def main(*_: str) -> None:
    guard_activity_logs: List[GuardActivityLog] = get_guard_activity_logs(
        sorted(activity for activity in sys.stdin)
    )

    guard_activities: Mapping[int, GuardActivity] = get_guard_activities(guard_activity_logs)

    sleepiest_guard: int = find_sleepiest_guard(guard_activities)
    sleepiest_minute, sleepiest_minute_freq = find_sleepiest_minute(
        guard_activities[sleepiest_guard]
    )

    print(
        f"Sleepiest guard by strategy 1 is {sleepiest_guard}. \
        This guard slept the most on {sleepiest_minute} minute {sleepiest_minute_freq} times"
    )
    print(f"Solution to part1: {sleepiest_guard * sleepiest_minute}")

    sleepiest_guard, sleepiest_minute = find_freq_sleepiest_minute(guard_activities) or (-1, -1)
    print(
        f"Sleepiest guard by strategy 2 is {sleepiest_guard}. \
        This guard slept the most on {sleepiest_minute} minute"
    )
    print(f"Solution to part2: {sleepiest_guard * sleepiest_minute}")


if __name__ == "__main__":
    main(*sys.argv)
