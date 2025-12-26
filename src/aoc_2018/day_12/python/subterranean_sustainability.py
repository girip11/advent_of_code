import re
import sys
from typing import Iterable, Iterator, List, Set, Tuple

PLANT = "#"
NO_PLANT = "."


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


def trim_pot_row(current_gen_pots: str, pot_offset: int, threshold: int = 2) -> Tuple[str, int]:
    # Dont leave more than the threshold number of empty pots at the left or right
    # Look for empty left pots till we reach some pot with plant
    i = 0
    while current_gen_pots[i] == NO_PLANT:
        i += 1

    if i > threshold:
        current_gen_pots = current_gen_pots[i - threshold :]
        pot_offset += i - threshold

    # Look for empty right pots till we reach some pot with plant
    i = len(current_gen_pots) - 1
    while current_gen_pots[i] == NO_PLANT:
        i -= 1

    if len(current_gen_pots) - 1 - i > threshold:
        current_gen_pots = current_gen_pots[: i + threshold + 1]

    return (current_gen_pots, pot_offset)


def compute_next_generation(
    current_gen_pots: str, plant_in_pot_rules: Set[str], pot_offset: int
) -> Tuple[str, int]:
    next_gen_pots = []

    # Expand to the left if the left most pots(2) has plant in this generation
    if PLANT in [current_gen_pots[0], current_gen_pots[1]]:
        empty_pots_to_pad = NO_PLANT * (2 if current_gen_pots[0] == PLANT else 1)
        current_gen_pots = f"{empty_pots_to_pad}{current_gen_pots}"
        pot_offset -= len(empty_pots_to_pad)

    # expand to the right if the right most pots(2) have plant in this generation
    if PLANT in [current_gen_pots[-1], current_gen_pots[-2]]:
        empty_pots_to_pad = NO_PLANT * (2 if current_gen_pots[-1] == PLANT else 1)
        current_gen_pots = f"{current_gen_pots}{empty_pots_to_pad}"

    for current_pot_with_neighbors in get_pot_slices(current_gen_pots):
        # print(current_pot_with_neighbors)
        if current_pot_with_neighbors in plant_in_pot_rules:
            next_gen_pots.append(PLANT)  # plant will be there
        else:
            next_gen_pots.append(NO_PLANT)  # no plant in next gen

    # print(f"Before trim: {''.join(next_gen_pots)}")
    current_gen_pots, pot_offset = trim_pot_row("".join(next_gen_pots), pot_offset)

    return (current_gen_pots, pot_offset)


def calc_pot_post_generations(
    generations: int, initial_state: str, plant_in_pot_rules: Set[str]
) -> Tuple[str, int]:
    current_gen_pots = initial_state
    pot_offset = 0

    # print(f"Gen: 0 --> {current_gen_pots}, {pot_offset}")
    no_change_gens = 0
    pot_offset_delta = 0
    for gen in range(1, generations + 1):
        next_gen_pots, new_pot_offset = compute_next_generation(
            current_gen_pots, plant_in_pot_rules, pot_offset
        )

        if next_gen_pots == current_gen_pots:
            no_change_gens += 1
        else:
            no_change_gens = 0

        current_gen_pots = next_gen_pots
        # positive - plants move to right
        # negative - plants move to left
        pot_offset_delta = new_pot_offset - pot_offset
        pot_offset = new_pot_offset
        # print(f"Gen: {gen} --> {current_gen_pots}, {pot_offset}")

        if no_change_gens >= 1:
            break

    if gen < generations:
        # early exit
        # adjust the pot_offset
        pot_offset += pot_offset_delta * (generations - gen)

    return (current_gen_pots, pot_offset)


def parse_input_data(input_data: List[str]) -> Tuple[str, Set[str]]:
    initial_state = read_initial_state(input_data[0])
    # print(initial_state)

    plant_in_pot_rules: Set[str] = set()

    for llcrr, pot_status in read_rules(input_data[1:]):
        if pot_status == PLANT:  # pot willhave plant in next gen
            plant_in_pot_rules.add(llcrr)

    # print(plant_in_pot_rules)

    return (initial_state, plant_in_pot_rules)


def subterranean_sustainability(
    initial_state: str, plant_in_pot_rules: Set[str], generations: int
) -> int:
    current_gen_pots, pot_offset = calc_pot_post_generations(
        generations, initial_state, plant_in_pot_rules
    )
    return sum((i + pot_offset) for i, pot in enumerate(current_gen_pots) if pot == PLANT)


def main(_: List[str]) -> None:
    input_data = sys.stdin.readlines()
    initial_state, plant_in_pot_rules = parse_input_data(input_data)

    # part-1 20 generations and part-2 5 billion generations
    for gen in [20, 50000000000]:
        pot_number_sum = subterranean_sustainability(initial_state, plant_in_pot_rules, gen)
        print(f"Sum after {gen} generations: {pot_number_sum}")


if __name__ == "__main__":
    main(sys.argv)
