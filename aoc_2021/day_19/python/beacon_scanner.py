import functools
import itertools
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from math import cos, radians, sin, sqrt
from operator import mul
from typing import Callable, ClassVar, Dict, List, Set, Tuple


@dataclass(frozen=True, order=True)
class Vector:
    x: int = field(default_factory=int)  # pylint: disable=invalid-name
    y: int = field(default_factory=int)  # pylint: disable=invalid-name
    z: int = field(default_factory=int)  # pylint: disable=invalid-name

    _rotations: ClassVar[Dict[str, Callable[[float], List[List[int]]]]] = {
        "x": lambda r: [
            [1, 0, 0],
            [0, round(cos(r)), round(sin(r))],
            [0, -round(sin(r)), round(cos(r))],
        ],
        "y": lambda r: [
            [round(cos(r)), 0, -round(sin(r))],
            [0, 1, 0],
            [round(sin(r)), 0, round(cos(r))],
        ],
        "z": lambda r: [
            [round(cos(r)), round(sin(r)), 0],
            [-round(sin(r)), round(cos(r)), 0],
            [0, 0, 1],
        ],
    }

    def to_list(self) -> List[int]:
        return [self.x, self.y, self.z]

    def magnitude(self) -> float:
        return sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def manhattan_distance(self, other: "Vector") -> int:
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)

    def squared_distance(self, other: "Vector") -> int:
        return (self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2

    def __add__(self, other: "Vector") -> "Vector":
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: "Vector") -> "Vector":
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def translate(self, other: "Vector") -> "Vector":
        return self + other

    def rotate(self, angle: int, axis: str) -> "Vector":
        if angle == 0:
            return self
        # transposed rotation matrix
        rotation_matrix_t: List[List[int]] = Vector._rotations[axis](radians(angle))
        vec: List[int] = self.to_list()
        return Vector(*[sum(map(mul, vec, col)) for col in rotation_matrix_t])

    def scale(self, factor: int) -> "Vector":
        return Vector(self.x * factor, self.y * factor, self.z * factor)

    def __str__(self) -> str:
        return f"{self.x},{self.y},{self.z}"


@dataclass(frozen=True)
class Orientation:
    axis_order: Tuple[str, str, str] = field(default=("x", "y", "z"))
    init_sign: Tuple[int, int, int] = field(default=(1, 1, 1))
    angle: int = field(default=0)
    rotation_axis: str = field(default="x")

    def orient(self, vector: Vector) -> Vector:
        return Vector(
            self.init_sign[0] * getattr(vector, self.axis_order[0]),
            self.init_sign[1] * getattr(vector, self.axis_order[1]),
            self.init_sign[2] * getattr(vector, self.axis_order[2]),
        ).rotate(self.angle, self.rotation_axis)


@dataclass
class Scanner:
    id_: int
    beacons: Set[Vector] = field(default_factory=set)
    _position: Vector = field(default_factory=Vector, init=False)
    _orientation: Orientation = field(default_factory=Orientation, init=False)

    @property
    def orientation(self) -> Orientation:
        return self._orientation

    @property
    def position(self) -> Vector:
        return self._position

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Scanner) and self.id_ == other.id_

    def l1_distance(self, other: "Scanner") -> int:
        return self._position.manhattan_distance(other.position)

    def reorient(self, orientation: Orientation, position: Vector) -> None:
        self._orientation = orientation
        self._position = position
        self.beacons = {self._orientation.orient(beacon) + position for beacon in self.beacons}

    def __str__(self) -> str:
        beacon_positions = "".join(f"{pos}\n" for pos in self.beacons)
        return f"--- scanner {self.id_} ---\n{beacon_positions}"


def get_orientations() -> List[Orientation]:
    # Watching from +ve x axis makes x as x, y as y and z as z
    # Watching from +ve y axis makes y as x, z as y and x as z
    # Watching from +ve z axis makes z as x, x as y and y as z
    # Watching from -ve x axis makes -x as x, -y as y and z as z
    # Watching from -ve y axis makes -y as x, -z as y and x as z
    # Watching from -ve z axis makes -z as x, -y as y and x as z
    axis_orders: List[Tuple[str, str, str]] = [("x", "y", "z"), ("y", "z", "x"), ("z", "x", "y")]
    signs: List[Tuple[int, int, int]] = [(1, 1, 1), (-1, -1, 1)]
    return [
        Orientation(axis_order, sign, angle)
        for axis_order, sign in itertools.product(axis_orders, signs)  # 6 facings
        for angle in [0, 90, 180, 270]  # 4 rotations
    ]


def get_position_and_orientation(sc1: Scanner, sc2: Scanner) -> Tuple[Orientation, Vector]:
    result: Tuple[Orientation, Vector]
    orientations: List[Orientation] = get_orientations()
    diff_vectors: Dict[Vector, int]

    for orientation in orientations:
        diff_vectors = defaultdict(int)
        reoriented_beacons: List[Vector] = [orientation.orient(beacon) for beacon in sc2.beacons]

        for beacon1 in sc1.beacons:
            for beacon2 in reoriented_beacons:
                diff_vectors[(beacon1 - beacon2)] += 1

        if max(diff_vectors.values()) >= 12:
            sc2_pos = max(diff_vectors.keys(), key=lambda vec: diff_vectors[vec])
            result = (orientation, sc2_pos)
            print("Overlapping", result, sc1.id_, sc2.id_)
            break

    assert result is not None

    return result


def does_scanners_overlap(sc1: Scanner, sc2: Scanner) -> bool:
    distances: Dict[int, List[Tuple[Vector, Vector]]] = defaultdict(list)

    for bc1, bc2 in itertools.combinations(sc1.beacons, 2):
        distances[bc1.squared_distance(bc2)].append((bc1, bc2))

    for bc1, bc2 in itertools.combinations(sc2.beacons, 2):
        distances[bc1.squared_distance(bc2)].append((bc1, bc2))

    return sum(1 for _, pairs in distances.items() if len(pairs) == 2) >= 66


def compute_scanner_positions(scanners: List[Scanner]) -> List[Scanner]:
    scanners_to_explore: List[Scanner] = [scanners[0]]
    computed: Set[int] = {scanners[0].id_}

    while len(scanners_to_explore) > 0:
        current_scanner: Scanner = scanners_to_explore.pop(0)

        for unexp_scanner in (sc for sc in scanners if sc.id_ not in computed):
            # print(current_scanner.id_, unexp_scanner.id_)
            if does_scanners_overlap(current_scanner, unexp_scanner):
                unexp_scanner.reorient(
                    *get_position_and_orientation(current_scanner, unexp_scanner)
                )
                computed.add(unexp_scanner.id_)
                scanners_to_explore.append(unexp_scanner)

    assert len(computed) == len(scanners)
    return scanners


def find_total_beacons(scanners: List[Scanner]) -> int:
    unique_beacons: Set[Vector] = functools.reduce(
        lambda s1, s2: s1.union(s2),
        (sc.beacons for sc in compute_scanner_positions(scanners)),
        set(),
    )
    return len(unique_beacons)


def largest_manhattan_distance(scanners: List[Scanner]) -> int:
    return max(sc1.l1_distance(sc2) for sc1, sc2 in itertools.combinations(scanners, 2))


def parse_beacon_positions(lines: List[str]) -> List[Scanner]:
    scanners: List[Scanner] = []

    for line in lines:
        if "scanner" in line:
            id_: int = int(line.replace("---", "").replace("scanner", "").strip())
            scanners.append(Scanner(id_))
        else:
            if line := line.strip():
                x, y, z = map(int, line.split(","))  # pylint: disable=invalid-name
                scanners[-1].beacons.add(Vector(x, y, z))

    return scanners


def main(*_: str) -> None:
    scanners: List[Scanner] = parse_beacon_positions(sys.stdin.readlines())
    # part-1
    print(f"Part1 - {find_total_beacons(scanners)}")

    # part-2
    print(f"Part1 - {largest_manhattan_distance(scanners)}")


if __name__ == "__main__":
    main(*sys.argv[1:])
