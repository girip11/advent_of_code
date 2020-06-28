import re
import sys
from typing import List, Sequence, Tuple


def main(*_: str) -> None:
    license_numbers: List[int] = [
        int(num) for num in re.findall(r"\d+", sys.stdin.readline())
    ]
    metadata_sum = get_metadata_sum(license_numbers)
    print(metadata_sum)


def get_metadata_sum(license_numbers: List[int]) -> int:
    metadata_sum = 0
    metadata_indices = get_metadata_indices(license_numbers, start=0)

    for entry in metadata_indices:
        metadata_sum += sum(license_numbers[entry[0] : entry[1]])

    return metadata_sum


def get_metadata_indices(
    license_numbers: List[int], start: int = 0
) -> Sequence[Tuple[int, int]]:
    """Returns the metadata indices range in the license numbers array

    Args:
        license_numbers (List[int]): [description]
        start (int, optional): [description]. Defaults to 0.

    Returns:
        Sequence[Tuple[int, int]]: [description]
    """
    # handling corner cases. These cases won't be hit on recursive calls
    # unless the data is corrupted
    if license_numbers == [] or len(license_numbers) < (start + 1):
        return []

    children_count = license_numbers[start]
    metadata_count = license_numbers[start + 1]
    # print(children_count, metadata_count)

    start += 2

    children_metadata_indices: List[Tuple[int, int]] = []

    for _ in range(children_count):
        metadata_span = get_metadata_indices(license_numbers, start)
        children_metadata_indices.extend(metadata_span)
        start = metadata_span[-1][1]

    children_metadata_indices.append((start, start + metadata_count))

    return children_metadata_indices


if __name__ == "__main__":
    main(*sys.argv)
