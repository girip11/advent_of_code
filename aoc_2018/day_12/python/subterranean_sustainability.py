import re
import sys
from typing import Iterable, Iterator, List, Set, Tuple


def read_initial_state(init_state: str) -> str:
    return init_state.replace("initial state:", "").strip()


def read_rules(rules: Iterable[str]) -> Iterator[Tuple[str, str]]:
    """Read the rules for growing plants in the pot.

    Rules are of the form "...## => #"

    Parameters
    ----------
    rules : Iterable[str]

    Yields
    -------
    Iterator[Tuple[str, str]]
    """
    pattern: re.Pattern = re.compile(r"([.|#]{5})\s=>\s([.|#]{1})")
    for rule in rules:
        if len(rule) > 0:
            match = pattern.match(rule)
            if match is not None:
                llcrr, pot_status = match.groups()
                yield (llcrr, pot_status)


def get_pot_slices(pots: str) -> Iterator[str]:
    """Note: No other pots currently contain plants. So default is '.'

    Pot slices follow the pattern LLCRR. Two to the left and two to the right of
    the current pot.
    """
    last_pot = len(pots)

    for pot_num in range(0, last_pot):
        # current pot is the left most pot
        # add additional pots to its left
        if pot_num in [0, 1]:
            yield ".."[pot_num:] + pots[: pot_num + 3]
        elif pot_num in [last_pot - 2, last_pot - 1]:
            # current pot is the right most pot
            # so add additional pots to the right
            yield pots[pot_num - 2 :] + ".."[last_pot - pot_num - 1 :]
        else:
            yield pots[pot_num - 2 : pot_num + 3]


def compute_next_generation(
    current_gen_pots: str, plant_in_pot_rules: Set[str], pot_offset: int
) -> Tuple[str, int]:
    next_gen_pots = []

    # Expand to the left by 2 if the left most pots(2) has plant in this generation
    if current_gen_pots[0] == "#" or current_gen_pots[1] == "#":
        current_gen_pots = f"..{current_gen_pots}"
        pot_offset -= 2

    # expand to the right by 2  if the right most pots(2) have plant in this generation
    if current_gen_pots[-1] == "#" or current_gen_pots[-1] == "#":
        current_gen_pots = f"{current_gen_pots}.."

    for current_pot_with_neighbors in get_pot_slices(current_gen_pots):
        # print(current_pot_with_neighbors)
        if current_pot_with_neighbors in plant_in_pot_rules:
            next_gen_pots.append("#")  # plant will be there
        else:
            next_gen_pots.append(".")  # no plant in next gen

    return ("".join(next_gen_pots), pot_offset)


def calc_pot_number_sum(generations: int, initial_state: str, plant_in_pot_rules: Set[str]) -> int:
    current_gen_pots = initial_state
    pot_offset = 0

    print(f"Gen: 0 --> {current_gen_pots}")
    for gen in range(1, generations + 1):
        current_gen_pots, pot_offset = compute_next_generation(
            current_gen_pots, plant_in_pot_rules, pot_offset
        )
        print(f"Gen: {gen} --> {current_gen_pots}")

    print(pot_offset)

    return sum((i + pot_offset) for i, pot in enumerate(current_gen_pots) if pot == "#")


def parse_input_data(input_data: List[str]) -> Tuple[str, Set[str]]:
    initial_state = read_initial_state(input_data[0])
    print(initial_state)

    plant_in_pot_rules: Set[str] = set()

    for llcrr, pot_status in read_rules(input_data[1:]):
        if pot_status == "#":  # pot willhave plant in next gen
            plant_in_pot_rules.add(llcrr)

    print(plant_in_pot_rules)

    return (initial_state, plant_in_pot_rules)


def subterranean_sustainability_part1(input_data: List[str], generations: int) -> int:
    initial_state, plant_in_pot_rules = parse_input_data(input_data)
    return calc_pot_number_sum(generations, initial_state, plant_in_pot_rules)


def main(_: List[str]) -> None:
    generations = 20
    pot_number_sum = subterranean_sustainability_part1(sys.stdin.readlines(), generations)
    print(pot_number_sum)


if __name__ == "__main__":
    main(sys.argv)
