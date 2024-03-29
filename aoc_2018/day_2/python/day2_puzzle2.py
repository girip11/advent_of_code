import sys
from itertools import combinations
from typing import Iterable, List, Optional


def find_common_letters(box_ids: List[str]) -> Optional[str]:
    """Returns the common letters from the correct box ids.
    Two boxes form the correct combination, if the ids differ by exactly a single character.
    Arguments:
        box_ids {list} -- Sequence of box ids
    Returns:
        [String]
    """
    common_letters: Optional[str] = None

    for id1, id2 in combinations(box_ids, 2):
        common_letters = _get_common_letters(id1, id2)

        if (len(id1) - len(common_letters)) == 1:
            print(f"Id1: {id1}, Id2: {id2}")
            break

        common_letters = None

    return common_letters


def _get_common_letters(box_id1: str, box_id2: str) -> str:
    """Returns common letters in the box ids
    Arguments:
        box_id1 {String}
        box_id2 {String}
    Returns:
        [String]
    """
    # I can iterate through both the string and find out the diff in one iteration only.
    # below logic is O(n), n - min(length(boxid1), length(boxid2))
    common_letters: Iterable[str] = map(
        lambda e: e[0] if e[0] == e[1] else "", zip(box_id1, box_id2)
    )
    return "".join(common_letters)


def main(*_: str) -> None:
    """
    This is the entry point.
    """
    box_ids: List[str] = [box_id.strip() for box_id in sys.stdin]
    print(f"Checksum: {find_common_letters(box_ids)}")


if __name__ == "__main__":
    main(*sys.argv)
