import heapq
import itertools
import math
import operator as op
from functools import reduce
from typing import cast

type Position = tuple[int, int, int]

type JBoxDistance = tuple[Position, Position, float]


class Circuit:
    def __init__(self, id_: int) -> None:
        self.id_ = id_
        self.j_boxes: set[Position] = set()

    def __hash__(self) -> int:
        return hash(self.id_)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Circuit):
            return False
        return self.id_ == other.id_

    def __contains__(self, j_box: Position) -> bool:
        return j_box in self.j_boxes

    def __len__(self) -> int:
        return len(self.j_boxes)

    @property
    def size(self) -> int:
        return len(self)

    def add_connection(self, con: tuple[Position, Position]) -> None:
        for j_box in con:
            self.j_boxes.add(j_box)

    def merge(self, circuit: "Circuit") -> "Circuit":
        self.j_boxes = self.j_boxes.union(circuit.j_boxes)
        return self


def compute_distance(jb1: Position, jb2: Position) -> float:
    return round(
        math.sqrt(
            sum(map(lambda x: x**2, (op.sub(c1, c2) for (c1, c2) in zip(jb1, jb2, strict=True))))
        ),
        3,
    )


class CircuitManager:
    def __init__(self, j_boxes: list[Position]) -> None:
        self.j_boxes = j_boxes
        self.circuits: dict[int, Circuit] = {}
        self.__node_circuits: dict[Position, int] = {}
        self.__id_counter = itertools.count(1)
        self.__distances: list[JBoxDistance] = [
            (i, j, compute_distance(i, j)) for i, j in itertools.combinations(j_boxes, 2)
        ]

    @property
    def n_j_boxes(self) -> int:
        return len(self.j_boxes)

    @property
    def distances(self) -> list[JBoxDistance]:
        return self.__distances

    def get_n_closest_pairs(self, n: int) -> list[JBoxDistance]:
        return heapq.nsmallest(n, self.__distances, key=lambda e: e[2])

    def add_jbox_connection(self, conn: JBoxDistance) -> Circuit | None:
        c1_id = self.__node_circuits.get(conn[0])
        c2_id = self.__node_circuits.get(conn[1])
        circuit: Circuit | None = None

        if c1_id is None and c2_id is None:
            circuit = Circuit(id_=next(self.__id_counter))
            self.circuits[circuit.id_] = circuit
        elif (c1_id is not None and c2_id is None) or (c1_id is None and c2_id is not None):
            circuit_id = cast(int, c1_id if c1_id is not None else c2_id)
            circuit = self.circuits[circuit_id]
        elif c1_id is not None and c2_id is not None:
            if c1_id == c2_id:
                circuit = self.circuits[c1_id]
            else:
                circuit1 = self.circuits[c1_id]
                circuit2 = self.circuits[c2_id]
                circuit = circuit1.merge(circuit2)
                for node in circuit2.j_boxes:
                    self.__node_circuits[node] = circuit.id_
                self.circuits.pop(c2_id)

        if circuit is not None:
            circuit.add_connection((conn[0], conn[1]))
            self.__node_circuits[conn[0]] = circuit.id_
            self.__node_circuits[conn[1]] = circuit.id_

        return circuit

    def get_n_largests_circuits(self, n: int) -> list[Circuit]:
        return heapq.nlargest(n, list(self.circuits.values()), key=lambda c: c.size)


# part-1
def get_circuit_size(circuit_mgr: CircuitManager, n_closest_pairs: int) -> int:
    for closest_pair in circuit_mgr.get_n_closest_pairs(n=n_closest_pairs):
        # print(closest_pair)
        circuit_mgr.add_jbox_connection(closest_pair)

    return reduce(op.mul, (c.size for c in circuit_mgr.get_n_largests_circuits(n=3)), 1)


# part-2
def get_farthest_junction_boxes(circuit_mgr: CircuitManager) -> int:
    for closest_pair in sorted(circuit_mgr.distances, key=lambda e: e[2]):
        # print(closest_pair)
        if circuit := circuit_mgr.add_jbox_connection(closest_pair):
            if circuit.size == circuit_mgr.n_j_boxes:
                return closest_pair[0][0] * closest_pair[1][0]

    raise ValueError("No connection found that unifies all junctions boxes into single circuit.")
