import sys
from typing import Iterable, List, Optional, Set, Tuple


def _trigger_polymer_reaction(
    polymer_seq: str, ignore_types: Optional[Tuple[str, str]] = None
) -> str:
    polymer_stack: List[str] = []
    tos: int = -1
    prev_polyunit: Optional[str] = None

    for polyunit in polymer_seq:
        if ignore_types is not None and polyunit in ignore_types:
            continue

        prev_polyunit = (tos >= 0 and polymer_stack[tos]) or None

        if prev_polyunit and abs(ord(prev_polyunit) - ord(polyunit)) == 32:
            polymer_stack.pop()
            tos -= 1
            # print(f"Polymer units {polyunit} and {prev_polyunit} reacted")
        else:
            polymer_stack.append(polyunit)
            tos += 1

    return "".join(polymer_stack)


def _distinct_polymer_types(polymer_seq: Iterable[str]) -> Set[str]:
    return set(map(str.lower, polymer_seq))


# part 1
def polymer_units_after_reaction(polymer_seq: str) -> int:
    polymer_seq_post_reaction: str = _trigger_polymer_reaction(polymer_seq)
    # print(f"Final polymer units after reaction: {polymer_seq_post_reaction}")
    return len(polymer_seq_post_reaction)


# part 2
def find_best_polymer_reaction(polymer_seq: str) -> int:
    polymer_types: Set[str] = _distinct_polymer_types(polymer_seq)
    best_seq_len: int = len(polymer_seq) + 1
    current_seq_len: int = 0

    for skip in polymer_types:
        polymer_seq_post_reaction: str = _trigger_polymer_reaction(
            polymer_seq, (skip.lower(), skip.upper())
        )

        # print(f"Final polymer units after reaction: {polymer_seq_post_reaction}")
        current_seq_len = len(polymer_seq_post_reaction)
        if current_seq_len < best_seq_len:
            print(
                f"Best seq len changed from {best_seq_len} to {current_seq_len} by removing {skip} type units"
            )
            best_seq_len = current_seq_len

    return best_seq_len


def main(*_: str) -> None:
    polymer_seq: str = sys.stdin.read().strip()
    print(f"Polymer Seq length post reaction: {polymer_units_after_reaction(polymer_seq)}")
    print(f"Length of best possible reaction sequence: {find_best_polymer_reaction(polymer_seq)}")


if __name__ == "__main__":
    main(*sys.argv)
