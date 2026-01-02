import itertools
from collections import defaultdict, deque
from functools import reduce


# I had to find the levels at which each device exist so that I can use the levels
# to prune the path between each hop
def get_device_levels(out_conn: dict[str, list[str]], src: str, dest: str) -> dict[str, int]:
    device_levels: dict[str, int] = defaultdict(int)
    device_levels[src] = 1
    # stack to keep track of devices while traversing the graph
    devs: deque[str] = deque([src])

    while len(devs) > 0:
        curr_dev = devs.popleft()

        if curr_dev == dest:
            continue

        # Add its connections to the stack
        curr_level = device_levels[curr_dev]
        next_level = curr_level + 1
        for next_dev in out_conn.get(curr_dev, []):
            if next_dev not in device_levels:
                device_levels[next_dev] = next_level
                devs.append(next_dev)

    return device_levels


def get_total_paths(
    device_conns: dict[str, list[str]], device_levels: dict[str, int], src: str, dest: str
) -> int:
    total_paths: int = 0
    # stack to keep track of devices while traversing the graph
    devs: list[str] = [src]

    while len(devs) > 0:
        curr_dev = devs.pop(-1)

        if curr_dev == dest:
            total_paths += 1
            continue

        # Add its connections to the stack only upto level of the destination
        # This has the limitation of connection back from the next level nodes.
        if device_levels[curr_dev] <= device_levels[dest]:
            if next_devs := device_conns.get(curr_dev):
                devs.extend(next_devs)

    return total_paths


# part-1
def get_total_paths_between_src_dest(
    device_conns: dict[str, list[str]], device_levels: dict[str, int], src: str, dest: str
) -> int:
    return get_total_paths(device_conns, device_levels, src, dest)


# Without levels, the input node connections are huge to be traversed.
# Maybe full traversal with memoization can be a solution.
# suppose src, two hops and dest
# we compute paths from src to hop1, hop1 to hop2 and hop2 to dest
# This makes the computation feasible within few seconds.
def get_total_paths_between_src_dest_with_hops(
    device_conns: dict[str, list[str]],
    device_levels: dict[str, int],
    src: str,
    dest: str,
    hops: set[str],
) -> int:
    return reduce(
        lambda acc, paths: acc * paths,
        (
            get_total_paths(device_conns, device_levels, *pair)
            for pair in itertools.pairwise(
                [src, *sorted(hops, key=lambda h: device_levels[h]), dest]
            )
        ),
        1,
    )
