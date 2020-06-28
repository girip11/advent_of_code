import re
import sys
from dataclasses import dataclass, field
from typing import Iterable, List, Optional, Tuple


def main(*_: str) -> None:
    license_numbers: List[int] = [int(num) for num in re.findall(r"\d+", sys.stdin.readline())]

    root = get_nodes(license_numbers, start=0)

    if root:
        # part1
        print(get_metadata_sum(root))
        # part2
        print(get_root_node_value(root))


@dataclass
class TreeNode:
    children_count: int
    metadata_count: int
    metadata_span: Tuple[int, int] = field(init=False)
    child_nodes: List["TreeNode"] = field(default_factory=list, init=False)
    metadata_entries: List[int] = field(default_factory=list, init=False)

    def add_metadata_span(self, span: Tuple[int, int]) -> None:
        self.metadata_span = span

    def add_metadata_entries(self, metadata_entries: Iterable[int]) -> None:
        self.metadata_entries.extend(metadata_entries)

    def add_child_node(self, child_node: "TreeNode") -> None:
        self.child_nodes.append(child_node)


def get_nodes(license_numbers: List[int], start: int = 0) -> Optional[TreeNode]:
    """Returns the root of the tree formed from the license numbers array

    Args:
        license_numbers (List[int]): [description]
        start (int, optional): [description]. Defaults to 0.
    """
    # handling corner cases. These cases won't be hit on recursive calls
    # unless the data is corrupted
    if license_numbers == [] or len(license_numbers) < (start + 1):
        return None

    children_count = license_numbers[start]
    metadata_count = license_numbers[start + 1]

    node = TreeNode(children_count, metadata_count)
    start += 2

    for _ in range(children_count):
        child_node = get_nodes(license_numbers, start)
        if child_node is not None:
            node.add_child_node(child_node)
            start = child_node.metadata_span[1]

    node.add_metadata_span((start, start + metadata_count))
    if metadata_count > 0:
        node.add_metadata_entries(license_numbers[start : (start + metadata_count)])

    return node


def get_metadata_sum(root: TreeNode) -> int:
    metadata_sum = sum(root.metadata_entries)

    for child in root.child_nodes:
        metadata_sum += get_metadata_sum(child)

    return metadata_sum


def get_root_node_value(root: TreeNode) -> int:

    # base case
    if root.children_count == 0:
        return 0 if root.metadata_count == 0 else sum(root.metadata_entries)

    root_node_value = 0

    child_node_values = [get_root_node_value(child) for child in root.child_nodes]

    for entry in root.metadata_entries:
        # metadata entries start from 1 while array index start from 0
        index = entry - 1
        if index < root.children_count:
            root_node_value += child_node_values[index]

    return root_node_value


if __name__ == "__main__":
    main(*sys.argv)
