import sys
from dataclasses import dataclass, field
from typing import Callable, Dict, Iterable, List, Mapping, Set, Tuple

START_CAVE = "start"
END_CAVE = "end"


@dataclass(
    frozen=True,
)
class Cave:
    name: str
    _adjacent_caves: Set["Cave"] = field(default_factory=set, init=False, hash=False, compare=False)

    @property
    def adjacent_caves(self) -> Iterable["Cave"]:
        return sorted(self._adjacent_caves)

    def add_adjacent_cave(self, adj_cave: "Cave") -> None:
        self._adjacent_caves.add(adj_cave)

    def is_small(self) -> bool:
        return self.name.islower()

    def is_start(self) -> bool:
        return self.name == START_CAVE

    def is_end(self) -> bool:
        return self.name == END_CAVE

    def __lt__(self, other: "Cave") -> bool:
        return self.name < other.name

    def __str__(self) -> str:
        return f"{self.name} ->{','.join(map(lambda cave: cave.name, self.adjacent_caves))}"


def parse_input(lines: List[str]) -> Mapping[str, Cave]:
    caves: Dict[str, Cave] = {START_CAVE: Cave(START_CAVE), END_CAVE: Cave(END_CAVE)}

    for line in lines:
        src, dest = map(
            lambda name: caves[name] if name in caves else Cave(name), line.strip().split("-")
        )
        # bidirectional connection
        src.add_adjacent_cave(dest)
        dest.add_adjacent_cave(src)

        if src.name not in caves:
            caves[src.name] = src
        if dest.name not in caves:
            caves[dest.name] = dest

    return caves


def should_explore_cave(cave: Cave, path: List[Cave]) -> bool:
    return not cave.is_start() and (not cave.is_small() or cave not in path)


def should_explore_cave2(cave: Cave, path: List[Cave]) -> bool:
    """Allows visiting single small cave atmost twice.

    Specifically, big caves can be visited any number of times,
    a single small cave can be visited at most twice, and the
    remaining small caves can be visited at most once. However,
    the caves named start and end can only be visited
    exactly once each: once you leave the start cave, you may not
    return to it, and once you reach the end cave, the path
    must end immediately.
    """
    if cave.is_start():
        return False

    if not cave.is_small():
        return True

    # small caves only one exactly twice
    small_caves_count = {cave: path.count(cave) for cave in path if cave.is_small()}
    return small_caves_count.get(cave, 0) < 1 or max(small_caves_count.values()) < 2


def count_paths_through_caves(
    start_cave: Cave, explore_cave: Callable[[Cave, List[Cave]], bool]
) -> int:
    paths: int = 0
    nodes: List[Tuple[int, Cave]] = [(0, cave) for cave in start_cave.adjacent_caves]
    path: List[Cave] = [start_cave]

    while len(nodes) > 0:
        from_cave_idx, current_cave = nodes.pop()

        while len(path) - 1 != from_cave_idx:
            path.pop()

        if current_cave.is_end():
            paths += 1
            continue

        if not explore_cave(current_cave, path):
            continue

        current_cave_path_idx = len(path)
        caves_to_explore = [
            (current_cave_path_idx, cave)
            for cave in current_cave.adjacent_caves
            if explore_cave(cave, path)
        ]

        if len(caves_to_explore) > 0:
            path.append(current_cave)
            nodes.extend(caves_to_explore)

    return paths


def main(*_: str) -> None:
    caves: Mapping[str, Cave] = parse_input(sys.stdin.readlines())

    for cave in caves.values():
        print(cave)
    # part-1
    print(count_paths_through_caves(caves[START_CAVE], should_explore_cave))

    # # part-2
    print(count_paths_through_caves(caves[START_CAVE], should_explore_cave2))


if __name__ == "__main__":
    main(*sys.argv[1:])
