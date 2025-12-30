from collections import deque
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

    @property
    def is_splitter(self) -> bool:
        return self.symbol == "^"

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

    node_id = 0
    root = Node(
        id_=node_id,
        symbol="S",
        pos=(0, next(idx for idx, v in enumerate(manifold[0]) if v == "S")),
    )
    nodes: deque[Node] = deque()
    nodes.append(root)
    splitter_positions: dict[Position, Node] = {}
    visited_nodes: set[int] = {root.id_}

    while len(nodes) > 0:
        current_node = nodes.popleft()

        for split_beam in current_node.beam_split_positions:
            if not (0 <= split_beam[1] < cols):
                continue

            for down_pos in range(split_beam[0] + 1, rows):
                if manifold[down_pos][split_beam[1]] == "^":
                    splitter_pos = (down_pos, split_beam[1])

                    if splitter_pos in splitter_positions:
                        neighbor = splitter_positions[splitter_pos]
                    else:
                        node_id += 1
                        neighbor = Node(id_=node_id, symbol="^", pos=splitter_pos)
                        splitter_positions[splitter_pos] = neighbor

                    current_node.neighbors.append(neighbor)
                    if neighbor.id_ not in visited_nodes:
                        nodes.append(neighbor)
                        visited_nodes.add(neighbor.id_)
                    break

        if current_node.is_splitter:
            if not current_node.has_left_neighbor and current_node.pos[1] - 1 >= 0:
                node_id += 1
                current_node.neighbors.append(
                    Node(id_=node_id, symbol="E", pos=(rows - 1, current_node.pos[1] - 1))
                )
            if not current_node.has_right_neighbor and current_node.pos[1] + 1 < cols:
                node_id += 1
                current_node.neighbors.append(
                    Node(id_=node_id, symbol="E", pos=(rows - 1, current_node.pos[1] + 1))
                )

    return root


# part-1
# def get_tachyon_beam_split_count(manifold: list[str]) -> int:
#     split_count: int = 0
#     rows = len(manifold)
#     cols = len(manifold[0])
#     start_pos: tuple[int, int] = (0, next(idx for idx, v in enumerate(manifold[0]) if v == "S"))
#     beams: deque[tuple[int, int]] = deque()
#     beams.append(start_pos)
#     unique_beams: set[tuple[int, int]] = set()
#     # multiple beams can reach the same splitter, but count once
#     activated_splitters: set[tuple[int, int]] = set()

#     while len(beams) > 0:
#         current_beam = beams.popleft()

#         for down_pos in range(current_beam[0] + 1, rows):
#             if manifold[down_pos][current_beam[1]] == "^":
#                 for new_beam in [(down_pos, current_beam[1] - 1), (down_pos, current_beam[1] + 1)]:
#                     if 0 <= new_beam[1] < cols and new_beam not in unique_beams:
#                         beams.append(new_beam)
#                         unique_beams.add(new_beam)

#                 splitter_pos = (down_pos, current_beam[1])
#                 if splitter_pos not in activated_splitters:
#                     activated_splitters.add(splitter_pos)
#                     split_count += 1

#                 print(
#                     f"Beam: {current_beam}, Splitter: {(down_pos, current_beam[1])}, count: {split_count}"
#                 )
#                 break

#     return split_count


# part-1
def get_tachyon_beam_split_count(root: Node) -> int:
    nodes: deque[Node] = deque()
    nodes.extend(root.neighbors)
    visited: set[int] = set()
    added: set[int] = set()
    split_count: int = 0

    while len(nodes) > 0:
        current_node = nodes.popleft()
        # print(
        #     f"{current_node.id_}, {current_node.symbol}, {current_node.pos}, {[n.pos for n in current_node.neighbors if n.is_splitter]}"
        # )

        if current_node.is_splitter and current_node.id_ not in visited:
            visited.add(current_node.id_)
            split_count += 1

            for n in current_node.neighbors:
                if n.is_splitter and n.id_ not in added:
                    nodes.append(n)
                    added.add(n.id_)

    return split_count


# part-2
def get_tachyon_timelines(root: Node) -> int:
    root_splitter = root.neighbors[0]

    def get_downstream_timelines(node: Node) -> int:
        # print(f"{node.id_},{node.pos}, {node.symbol}, {len(node.neighbors)}")

        if node.symbol == "E":
            return 1
        return sum(get_downstream_timelines(n) for n in node.neighbors)

    return get_downstream_timelines(root_splitter)
