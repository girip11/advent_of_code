import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from heapq import heappop, heappush, nsmallest
from typing import Dict, Iterator, List, Mapping, Tuple


def main(*_: str) -> None:
    raw_instructions = sys.stdin.readlines()
    path_taken = computer_instructions_traversal_order(iter(raw_instructions))
    print(f"Path Taken:{path_taken}")

    # part 2
    # time_spent: int = compute_traversal_duration(iter(raw_instructions), 2)
    time_spent: int = compute_traversal_duration(iter(raw_instructions), 5)
    print(f"total time spent:{time_spent}")


# part 1
def computer_instructions_traversal_order(raw_instructions: Iterator[str]) -> str:
    prerequisite_map, dependency_graph = get_dependency_graph(raw_instructions)

    # part 1
    path_taken: str = ""
    for root in get_root_elements(prerequisite_map):
        path_taken += traverse_instructions(root, prerequisite_map, dependency_graph)

    return path_taken


# TODO: Work with one way dependency graph instead of two maps.
def get_dependency_graph(
    raw_instructions: Iterator[str],
) -> Tuple[Dict[str, List[str]], Dict[str, List[str]]]:
    prerequisite_map: Dict[str, List[str]] = defaultdict(list)
    dependency_graph: Dict[str, List[str]] = defaultdict(list)

    for prereq_step, dependent_step in get_instructions(raw_instructions):
        heappush(prerequisite_map[dependent_step], prereq_step)
        # simple access creates an entry in the list
        if prereq_step not in prerequisite_map:
            prerequisite_map[prereq_step]  # pylint: disable=pointless-statement
        dependency_graph[prereq_step].append(dependent_step)

    return (prerequisite_map, dependency_graph)


def get_instructions(raw_instructions: Iterator[str]) -> Iterator[Tuple[str, str]]:
    pattern = re.compile(r"Step\s+([A-Z]).*step\s+([A-Z]).*", re.RegexFlag.DOTALL)

    for line in raw_instructions:
        match = re.match(pattern, line)
        if match and len(match.groups()) == 2:
            matches = match.groups()
            yield (matches[0], matches[1])


def get_root_elements(prerequisite_map: Mapping[str, List[str]]) -> List[str]:
    root_nodes: List[str] = []  # heap

    for key, value in prerequisite_map.items():
        if len(value) == 0:
            heappush(root_nodes, key)

    # print(root_nodes)
    return root_nodes


def traverse_instructions(
    root: str,
    prerequisite_map: Dict[str, List[str]],
    dependency_graph: Dict[str, List[str]],
) -> str:
    # this is a min heap, sorts by ascending order
    steps_to_complete: List[str] = []
    current: str = root
    path: str = ""

    while True:
        path += current
        # print(current, end="")

        for next_step in dependency_graph[current]:
            prerequisites = prerequisite_map[next_step]
            prerequisites.remove(current)
            if prerequisites == []:
                heappush(steps_to_complete, next_step)

        if steps_to_complete == []:
            break

        current = heappop(steps_to_complete)

    return path


# part 2
def compute_traversal_duration(raw_instructions: Iterator[str], workers: int) -> int:
    prerequisite_map, dependency_graph = get_dependency_graph(raw_instructions)

    return traverse_instructions_per_second(
        get_root_elements(prerequisite_map), prerequisite_map, dependency_graph, workers
    )


@dataclass
class Work:
    MISSING = ""  # pylint: disable=invalid-name
    step: str = MISSING
    work_left: int = 0

    def is_valid_step(self) -> bool:
        return self.step != Work.MISSING

    def is_work_completed(self) -> bool:
        return self.work_left == 0

    def decrement_work(self, completed_units: int) -> None:
        if self.work_left != 0:
            self.work_left -= completed_units


# returns the seconds for completion
def traverse_instructions_per_second(
    root_steps: List[str],
    prerequisite_map: Dict[str, List[str]],
    dependency_graph: Dict[str, List[str]],
    workers: int,
) -> int:
    current_workers_work: List[Work] = [Work()] * workers

    for i, step in enumerate(root_steps):
        current_workers_work[i] = Work(step, (ord(step) - ord("A") + 61))

    print(current_workers_work)

    time_spent: int = 0
    steps_available: List[str] = []
    work_completed: List[Work] = []

    while not all(map(lambda work: work.is_work_completed(), current_workers_work)):
        completed_work: int = nsmallest(
            1,
            current_workers_work,
            key=lambda work: work.work_left if work.is_valid_step() else sys.maxsize,
        )[0].work_left

        # print(completed_work)
        time_spent += completed_work

        # deduct completed work and note down completed steps
        for work in current_workers_work:
            if work.is_valid_step():
                work.decrement_work(completed_work)
                if work.is_work_completed():
                    heappush(work_completed, work)

        # print(work_completed)

        # look for new available steps based on completed steps
        for _ in range(len(work_completed)):
            work = heappop(work_completed)
            for next_step in dependency_graph[work.step]:
                prerequisites = prerequisite_map[next_step]
                prerequisites.remove(work.step)

                if prerequisites == []:
                    heappush(steps_available, next_step)

        # print(steps_available)

        # check if we can assign the work to workers
        for i in range(workers):
            if current_workers_work[i].is_work_completed():
                if steps_available:
                    next_step = heappop(steps_available)
                    current_workers_work[i] = Work(next_step, (ord(next_step) - ord("A") + 61))
                else:
                    current_workers_work[i] = Work()

    return time_spent


if __name__ == "__main__":
    main(*sys.argv)
