import heapq
import itertools
import sys
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Set, Tuple


@dataclass(frozen=True)
class TargetRange:
    horizontal_range: Tuple[int, int]
    vertical_range: Tuple[int, int]

    def is_in_horizontal_range(self, value: int) -> bool:
        return self.horizontal_range[0] <= value <= self.horizontal_range[1]

    def is_beyond_horizontal_range(self, value: int) -> bool:
        return value > self.horizontal_range[1]

    def is_in_vertical_range(self, value: int) -> bool:
        return self.vertical_range[0] <= value <= self.vertical_range[1]

    def is_beyond_vertical_range(self, value: int) -> bool:
        return value < self.vertical_range[0]


def parse_input(line: str) -> TargetRange:
    x_range_start, x_range_end = map(
        int, line[line.index("x") : line.index(",")].split("=")[1].split("..")
    )
    y_range_start, y_range_end = map(int, line[line.index("y") :].split("=")[1].split(".."))

    return TargetRange((x_range_start, x_range_end), (y_range_start, y_range_end))


def find_max_vertical_velocity(target_range: TargetRange) -> int:
    return max(abs(i) for i in target_range.vertical_range) - 1


def compute_horizontal_velocity(target_range: TargetRange) -> Dict[int, List[int]]:
    horizontal_velocities: Dict[int, List[int]] = defaultdict(list)

    for init_vel in range(max(target_range.horizontal_range), 0, -1):
        current_vel: int = init_vel
        pos: int = init_vel
        step: int = 1
        while not target_range.is_beyond_horizontal_range(pos) and current_vel >= 0:
            if target_range.is_in_horizontal_range(pos):
                horizontal_velocities[init_vel].append(step)
                if current_vel == 0:
                    horizontal_velocities[init_vel].append(sys.maxsize)

            current_vel -= 1
            pos += current_vel
            step += 1

    return horizontal_velocities


def compute_vertical_velocity(target_range: TargetRange) -> Dict[int, List[int]]:
    vertical_velocities: Dict[int, List[int]] = defaultdict(list)
    max_vertical_velocity: int = find_max_vertical_velocity(target_range) + 1

    for init_vel in range(min(target_range.vertical_range), max_vertical_velocity, 1):
        if init_vel > 0:
            current_vel: int = -init_vel
            pos: int = 0
            step: int = (init_vel * 2) + 1  # marks symmetric up and down
        else:
            current_vel = init_vel
            pos = init_vel
            step = 1

        while not target_range.is_beyond_vertical_range(pos):
            if target_range.is_in_vertical_range(pos):
                heapq.heappush(vertical_velocities[step], init_vel)

            current_vel -= 1
            pos += current_vel
            step += 1

    return vertical_velocities


def find_max_height(target_range: TargetRange) -> int:
    horizontal_velocities: Dict[int, List[int]] = compute_horizontal_velocity(target_range)
    vertical_velocities: Dict[int, List[int]] = compute_vertical_velocity(target_range)
    max_vertical_velocity: int

    max_steps: int = max(itertools.chain(*horizontal_velocities.values()))
    if max_steps == sys.maxsize:  # steps dont' matter
        max_vertical_velocity = find_max_vertical_velocity(target_range)
    else:
        max_vertical_velocity = max(itertools.chain(*vertical_velocities.values()))

    return int((max_vertical_velocity * (max_vertical_velocity + 1)) / 2)


def count_distinct_initial_velocities(target_range: TargetRange) -> int:
    horizontal_velocities: Dict[int, List[int]] = compute_horizontal_velocity(target_range)
    vertical_velocities: Dict[int, List[int]] = compute_vertical_velocity(target_range)
    max_steps = max(vertical_velocities.keys())
    distinct_initial_velocities: int = 0

    for _, steps in horizontal_velocities.items():
        distinct_steps: Set[int] = set()
        for stepno, step in enumerate(steps):
            if step == sys.maxsize:
                for i in range(steps[stepno - 1] + 1, max_steps + 1):
                    for vel in vertical_velocities[i]:
                        distinct_steps.add(vel)
            else:
                for vel in vertical_velocities[step]:
                    distinct_steps.add(vel)

        distinct_initial_velocities += len(distinct_steps)

    return distinct_initial_velocities


def main(*_: str) -> None:
    target_range: TargetRange = parse_input(sys.stdin.readline().strip())

    print(target_range)

    # part-1
    print(find_max_height(target_range))

    # part-2
    print(count_distinct_initial_velocities(target_range))


if __name__ == "__main__":
    main(*sys.argv[1:])
