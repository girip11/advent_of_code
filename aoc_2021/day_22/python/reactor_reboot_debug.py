"""Though inefficient, I used this script for debugging the actual solution."""
import sys
from dataclasses import dataclass
from typing import Iterator, List, Set, Tuple

Point = Tuple[int, int, int]


@dataclass(frozen=True, eq=True)
class Cuboid:
    x_range: range
    y_range: range
    z_range: range

    def __str__(self) -> str:
        return (
            f"x={self.x_range.start}..{self.x_range.stop-1},"
            + f"y={self.y_range.start}..{self.y_range.stop-1},"
            + f"z={self.z_range.start}..{self.z_range.stop-1}"
        )


@dataclass(frozen=True)
class RebootStep:
    on: bool
    cuboid: Cuboid

    def __str__(self) -> str:
        return f"{'on' if self.on else 'off'} {self.cuboid}"


Cube = Tuple[int, int, int]


def get_cubes(cuboid: Cuboid) -> Iterator[Cube]:
    for x in cuboid.x_range:
        for y in cuboid.y_range:
            for z in cuboid.z_range:
                yield (x, y, z)


def count_on_cubes_post_reboot(reboot_steps: List[RebootStep]) -> int:
    on_cubes: Set[Cube] = set()
    for step in reboot_steps:
        print(f"Following step: {step}, {len(on_cubes)}")
        for cube in get_cubes(step.cuboid):
            if step.on:
                on_cubes.add(cube)
            else:
                if cube in on_cubes:
                    on_cubes.remove(cube)

    return len(on_cubes)


def parse_input(lines: List[str]) -> List[RebootStep]:
    steps: List[RebootStep] = []

    def get_range(coord: str) -> range:
        start, end = map(int, coord.lstrip("xyz=").split(".."))
        return range(start, end + 1)

    for line in lines:
        step_type, coordinates = line.split(" ")
        x_range, y_range, z_range = coordinates.split(",")
        steps.append(
            RebootStep(
                step_type == "on",
                Cuboid(get_range(x_range), get_range(y_range), get_range(z_range)),
            )
        )

    return steps


def main(*args: str) -> None:
    reboot_steps: List[RebootStep] = parse_input(sys.stdin.readlines())
    print(f"Total reboot steps: {len(reboot_steps)}")

    filtered_steps: List[RebootStep] = [
        step
        for step in reboot_steps
        if all(
            map(
                lambda r: (-50 <= r.start <= 50 and -50 <= r.stop - 1 <= 50),
                [step.cuboid.x_range, step.cuboid.y_range, step.cuboid.z_range],
            )
        )
    ]

    print(f"Turned on cubes: {count_on_cubes_post_reboot(filtered_steps)}")


if __name__ == "__main__":
    main(*sys.argv[1:])
