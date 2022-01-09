import sys
from collections import defaultdict
from typing import Dict, List, Mapping, Tuple


def parse_input(lines: List[str]) -> Tuple[str, Dict[str, str]]:
    polymer_template: str = lines[0].strip()
    insertion_rules: Dict[str, str] = {}
    for line in lines[2:]:
        key, value = line.split("->")
        insertion_rules[key.strip()] = value.strip()

    return (polymer_template, insertion_rules)


def mce_lce_difference(
    current_template: str, insertion_rules: Mapping[str, str], steps: int
) -> int:
    polymer_pairs: Dict[str, int] = defaultdict(int)
    pair: str = ""

    for i in range(0, len(current_template) - 1):
        pair = current_template[i : i + 2]
        polymer_pairs[pair] += 1

    last_inserted_pair: str = pair

    for _ in range(steps):
        new_polymer_pairs: Dict[str, int] = defaultdict(int)
        for polymer_pair, count in polymer_pairs.items():
            p1: str = polymer_pair[0]  # pylint: disable=invalid-name
            p3: str = polymer_pair[1]  # pylint: disable=invalid-name
            p2: str = insertion_rules[f"{p1}{p3}"]  # pylint: disable=invalid-name
            for pair in [f"{p1}{p2}", f"{p2}{p3}"]:
                new_polymer_pairs[pair] += count

            if polymer_pair == last_inserted_pair:
                last_inserted_pair = f"{p2}{p3}"

        polymer_pairs = new_polymer_pairs

    element_counts: Dict[str, int] = defaultdict(int)
    for pair, count in polymer_pairs.items():
        if pair == last_inserted_pair:
            element_counts[pair[1]] += 1
        element_counts[pair[0]] += count

    print(element_counts)

    return max(element_counts.values()) - min(element_counts.values())


def main(*_: str) -> None:
    polymer_template, insertion_rules = parse_input(sys.stdin.readlines())
    print(polymer_template)
    print(insertion_rules)

    # part-1
    print(mce_lce_difference(polymer_template, insertion_rules, 10))

    # part-2
    print(mce_lce_difference(polymer_template, insertion_rules, 40))


if __name__ == "__main__":
    main(*sys.argv[1:])
