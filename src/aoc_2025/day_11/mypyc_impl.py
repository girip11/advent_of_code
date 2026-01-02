# part-1
def get_total_paths(device_conns: dict[str, list[str]], src: str, dest: str) -> int:
    total_paths: int = 0
    # stack to keep track of devices while traversing the graph
    devs: list[str] = [src]

    while len(devs) > 0:
        curr_dev = devs.pop(-1)

        if curr_dev == dest:
            total_paths += 1
            continue

        # Add its connections to the stack
        if next_devs := device_conns.get(curr_dev):
            devs.extend(next_devs)

    return total_paths


# part-2
# This works for the sample. But the puzzle input seems to have too many paths from svr to out.
def get_total_paths_with_hops(
    device_conns: dict[str, list[str]], src: str, dest: str, hops: set[str]
) -> int:
    total_paths: int = 0
    # Keeps track of all paths
    current_path: list[str] = []
    # stack to keep track of devices while traversing the graph
    devs: list[tuple[str, str | None]] = [(src, src)]

    while len(devs) > 0:
        (curr_dev, from_dev) = devs.pop(-1)

        while len(current_path) > 0 and current_path[-1] != from_dev:
            current_path.pop(-1)

        current_path.append(curr_dev)

        if curr_dev == dest:
            if hops.intersection(current_path) == hops:
                print(current_path)
                total_paths += 1
            continue

        # Add its connections to the stack
        devs.extend(
            [
                (next_dev, curr_dev)
                for next_dev in device_conns.get(curr_dev, [])
                if next_dev not in current_path
            ]
        )

    return total_paths
