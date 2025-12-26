import sys
from dataclasses import dataclass
from itertools import product
from typing import List, Optional, Set, Tuple

Point = Tuple[int, int, int]


@dataclass(frozen=True, eq=True)
class Cuboid:
    x_range: range
    y_range: range
    z_range: range

    @property
    def volume(self) -> int:
        return len(self.x_range) * len(self.y_range) * len(self.z_range)

    @property
    def vertices(self) -> List[Point]:
        return list(
            product(
                [self.x_range.start, self.x_range.stop - 1],
                [self.y_range.start, self.y_range.stop - 1],
                [self.z_range.start, self.z_range.stop - 1],
            )
        )

    def __contains__(self, point: Point) -> bool:
        x, y, z = point  # pylint: disable=invalid-name
        return x in self.x_range and y in self.y_range and z in self.z_range

    def does_enclose(self, other: "Cuboid") -> bool:
        return all(v in self for v in other.vertices)

    def does_overlap(self, other: "Cuboid") -> Optional["Cuboid"]:
        def find_intersecting_range(first: range, second: range) -> Optional[range]:
            intersecting_range: Optional[range]
            if second.start in first:
                intersecting_range = range(
                    second.start,
                    min(first.stop, second.stop, key=lambda i: abs(i - second.start)),
                )
            elif second.stop - 1 in first:
                intersecting_range = range(
                    min(first.start, second.start, key=lambda i: abs(second.stop - i)),
                    second.stop,
                )
            else:
                intersecting_range = None

            return intersecting_range

        x_range = find_intersecting_range(self.x_range, other.x_range) or find_intersecting_range(
            other.x_range, self.x_range
        )
        y_range = find_intersecting_range(self.y_range, other.y_range) or find_intersecting_range(
            other.y_range, self.y_range
        )
        z_range = find_intersecting_range(self.z_range, other.z_range) or find_intersecting_range(
            other.z_range, self.z_range
        )

        if x_range and y_range and z_range:
            return Cuboid(x_range, y_range, z_range)

        return None

    def _get_non_overlapping_ranges(self, axis: str, overlap_range: range) -> List[range]:
        nonoverlapping_ranges: List[range] = []
        this_range: range = getattr(self, f"{axis}_range")

        assert overlap_range.start in this_range or overlap_range.stop - 1 in this_range

        # complete overlap of the axis
        if this_range == overlap_range:
            return nonoverlapping_ranges

        if this_range.start == overlap_range.start:
            nonoverlapping_ranges.append(range(overlap_range.stop, this_range.stop))
        elif this_range.stop == overlap_range.stop:
            nonoverlapping_ranges.append(range(this_range.start, overlap_range.start))
        else:
            # overlap is enclosed within this_range
            # this will lead to nonoverlap on either sides of the overlapping range
            nonoverlapping_ranges.extend(
                [
                    range(this_range.start, overlap_range.start),
                    range(overlap_range.stop, this_range.stop),
                ]
            )

        return nonoverlapping_ranges

    def split(self, overlap_region: "Cuboid") -> List["Cuboid"]:
        split_regions: List[Cuboid] = []
        for x_range in self._get_non_overlapping_ranges("x", overlap_region.x_range):
            split_regions.append(Cuboid(x_range, self.y_range, self.z_range))

        for y_range in self._get_non_overlapping_ranges("y", overlap_region.y_range):
            split_regions.append(Cuboid(overlap_region.x_range, y_range, self.z_range))

        for z_range in self._get_non_overlapping_ranges("z", overlap_region.z_range):
            split_regions.append(Cuboid(overlap_region.x_range, overlap_region.y_range, z_range))

        return split_regions

    def __str__(self) -> str:
        return (
            f"x={self.x_range.start}..{self.x_range.stop-1},"
            + f"y={self.y_range.start}..{self.y_range.stop-1},"
            + f"z={self.z_range.start}..{self.z_range.stop-1}"
        )


@dataclass(frozen=True)
class RebootStep:
    on: bool  # pylint: disable=invalid-name
    cuboid: Cuboid

    def __str__(self) -> str:
        return f"{'on' if self.on else 'off'} {self.cuboid}"


def process_on_step(on_regions: Set[Cuboid], on_region: Cuboid) -> None:
    if len(on_regions) > 0:
        for reg in on_regions:
            if reg.does_enclose(on_region):
                return

        for cur_region in list(on_regions):
            if on_region.does_enclose(cur_region):
                on_regions.remove(cur_region)
            elif overlap_reg := cur_region.does_overlap(on_region):
                # when overlapping existing regions should be split to exclude the overlap of
                # on_region
                on_regions.remove(cur_region)
                for reg in cur_region.split(overlap_reg):
                    on_regions.add(reg)
            else:
                ...
                # print(f"{cur_region} neither encloses/overlaps with {on_region}")

    on_regions.add(on_region)


def process_off_step(on_regions: Set[Cuboid], off_region: Cuboid) -> None:
    """Turns off cubes on the grid.

    Algorithm
    ==========
    1. off_region can enclose an on_region. In that can remove the on_region
    2. off_region is inside on_region, split the on_region
    3. off_region overlaps with on_region, split the on_region
    4. No overlap, on_region remains untouched

    When split, remove the on_region and add the split regions to on_regions set.
    Parameters
    ----------
    on_regions : Set[Cuboid]
    off_region : Cuboid
    """
    for on_region in list(on_regions):
        if off_region.does_enclose(on_region):
            on_regions.remove(on_region)
        elif on_region.does_enclose(off_region):
            on_regions.remove(on_region)
            for reg in on_region.split(off_region):
                on_regions.add(reg)
        elif overlap_region := on_region.does_overlap(off_region):
            on_regions.remove(on_region)
            for reg in on_region.split(overlap_region):
                on_regions.add(reg)
        else:
            ...


def turned_on_cubes(on_regions: Set[Cuboid]) -> int:
    return sum(region.volume for region in on_regions)


def count_on_cubes_post_reboot(reboot_steps: List[RebootStep]) -> int:
    on_regions: Set[Cuboid] = set()  # non-overlapping regions
    for step in reboot_steps:
        # print(f"Following step: {step}, {turned_on_cubes(on_regions)}")
        if step.on:
            process_on_step(on_regions, step.cuboid)
        else:
            process_off_step(on_regions, step.cuboid)

    return turned_on_cubes(on_regions)


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


def main(*_: str) -> None:
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

    # part-1
    print(f"1. Turned on cubes: {count_on_cubes_post_reboot(filtered_steps)}")

    # part-2
    print(f"2. Turned on cubes: {count_on_cubes_post_reboot(reboot_steps)}")


if __name__ == "__main__":
    main(*sys.argv[1:])
