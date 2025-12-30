import bisect
import itertools
from collections import defaultdict, deque
from collections.abc import Iterator
from dataclasses import dataclass, field
from typing import Literal

type Position = tuple[int, int]
type NodeType = Literal["S", "^", "E"]  # E for Exit


@dataclass
class Node:
    id_: int
    symbol: NodeType
    pos: Position
    neighbors: "list[Node]" = field(default_factory=list)

    def __hash__(self) -> int:
        return hash(self.id_)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Node):
            return False

        return self.id_ == other.id_

    @property
    def is_splitter(self) -> bool:
        return self.symbol == "^"

    @property
    def is_exit(self) -> bool:
        return self.symbol == "E"

    @property
    def beam_split_positions(self) -> list[Position]:
        positions: list[Position] = []
        match self.symbol:
            case "S":
                positions.append(self.pos)
            case "^":
                positions.extend([(self.pos[0], self.pos[1] - 1), (self.pos[0], self.pos[1] + 1)])
            case _:
                pass
        return positions

    @property
    def has_left_neighbor(self) -> bool:
        return any(
            (n.pos[0] > self.pos[0] and self.pos[1] - 1 == n.pos[1]) for n in self.neighbors
        )

    @property
    def has_right_neighbor(self) -> bool:
        return any(
            (n.pos[0] > self.pos[0] and self.pos[1] + 1 == n.pos[1]) for n in self.neighbors
        )


def construct_splitter_graph(manifold: list[str]) -> Node:
    rows = len(manifold)
    cols = len(manifold[0])

    node_id: Iterator[int] = itertools.count(1)
    root = Node(
        id_=next(node_id),
        symbol="S",
        pos=(0, next(idx for idx, v in enumerate(manifold[0]) if v == "S")),
    )
    nodes: deque[Node] = deque()
    nodes.append(root)
    node_positions: dict[Position, Node] = {}
    visited_nodes: set[int] = {root.id_}

    while len(nodes) > 0:
        current_node = nodes.popleft()

        for split_beam in current_node.beam_split_positions:
            if not (0 <= split_beam[1] < cols):
                continue

            for down_pos in range(split_beam[0] + 1, rows):
                if manifold[down_pos][split_beam[1]] == "^":
                    splitter_pos = (down_pos, split_beam[1])

                    if (neighbor := node_positions.get(splitter_pos)) is None:
                        neighbor = Node(id_=next(node_id), symbol="^", pos=splitter_pos)
                        node_positions[splitter_pos] = neighbor

                    current_node.neighbors.append(neighbor)
                    if neighbor.id_ not in visited_nodes:
                        nodes.append(neighbor)
                        visited_nodes.add(neighbor.id_)
                    break

        if current_node.is_splitter:
            for n in ["L", "R"]:
                neighbor_pos = None
                if n == "L":
                    if current_node.has_left_neighbor or current_node.pos[1] - 1 < 0:
                        continue
                    neighbor_pos = (rows - 1, current_node.pos[1] - 1)
                else:
                    if current_node.has_right_neighbor or current_node.pos[1] + 1 >= cols:
                        continue
                    neighbor_pos = (rows - 1, current_node.pos[1] + 1)

                if neighbor_pos is not None:
                    if (neighbor := node_positions.get(neighbor_pos)) is None:
                        neighbor = Node(id_=next(node_id), symbol="E", pos=neighbor_pos)
                        node_positions[neighbor_pos] = neighbor
                    current_node.neighbors.append(neighbor)

    return root


# part-1
def get_tachyon_beam_split_count(root: Node) -> int:
    nodes: deque[Node] = deque()
    nodes.extend(root.neighbors)

    added: set[int] = {n.id_ for n in root.neighbors}
    split_count: int = 0

    while len(nodes) > 0:
        current_node = nodes.popleft()

        if current_node.is_splitter:
            split_count += 1

            for n in current_node.neighbors:
                if n.is_splitter and n.id_ not in added:
                    nodes.append(n)
                    added.add(n.id_)

    return split_count


def get_tachyon_timelines(root: Node) -> int:
    nodes: deque[Node] = deque()
    nodes.extend(root.neighbors)
    added: set[int] = {n.id_ for n in root.neighbors}

    # Keep adding tachyon beams from upstream to downstream splitters
    node_beams: dict[Node, int] = defaultdict(int)
    node_beams[root.neighbors[0]] += 1

    # maintains splitters that have connection to the exits
    exit_nodes: dict[Node, set[Node]] = defaultdict(set)

    while len(nodes) > 0:
        current_node = nodes.popleft()

        for neighbor in current_node.neighbors:
            if neighbor.is_splitter:
                node_beams[neighbor] += node_beams[current_node]
                if neighbor.id_ not in added:
                    # without sorting, incorrect counts get added.
                    bisect.insort_left(nodes, neighbor, key=lambda e: e.pos)
                    added.add(neighbor.id_)

            if neighbor.is_exit:
                exit_nodes[neighbor].add(current_node)

    return sum(
        node_beams[splitter]
        for exit_node, splitters in exit_nodes.items()
        for splitter in splitters
    )
