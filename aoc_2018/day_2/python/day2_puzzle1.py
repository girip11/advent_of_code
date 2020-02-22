import sys
from functools import reduce
from typing import Iterable, Set, List, Tuple


def calculate_checksum(box_ids: Iterable[str]) -> int:
    """Computes and returns the checksum which is a product of the number of box 
    ids containing characters repeated exactly twice and thrice.
    
    Arguments:
        box_ids {Array[String]} -- id containing all lowercase alphabets only
    """
    char_counts: Iterable[Tuple[int, int]] = (
        _get_repeating_chars_count(id) for id in box_ids
    )

    final_count: Tuple[int, int] = reduce(
        lambda op1, op2: (op1[0] + op2[0], op1[1] + op2[1]), char_counts, (0, 0)
    )

    print(f"Final count: {final_count}")
    return final_count[0] * final_count[1]


def _get_repeating_chars_count(box_id: str) -> Tuple[int, int]:
    """Returns a tuple (twice_repeated, thrice_repeated)
    twice_repeated, thrice_repeated - 1 - atleast 1 character is repeated twice exactly
                   - 0 No character is repeated exactly twice in the id

    Arguments:
        box_id {String} -- Box id containing lowercase alphabets only 

    Returns:
        [Tuple(int, int)]
    """
    counting_bucket: List[int] = [0] * 26
    char_code_start: int = ord("a")

    for c in box_id:
        counting_bucket[(ord(c) - char_code_start)] += 1

    unique_char_counts: Set[int] = set(counting_bucket)
    return (int(2 in unique_char_counts), int(3 in unique_char_counts))


def main(*args: str):
    """
        This is the entry point.
    """
    box_ids: Iterable[str] = (id.strip() for id in sys.stdin)
    print(f"Checksum: {calculate_checksum(box_ids)}")


if __name__ == "__main__":
    main(*sys.argv)
