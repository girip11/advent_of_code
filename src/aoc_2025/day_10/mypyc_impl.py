import operator as op
import re
from collections.abc import Iterable
from dataclasses import dataclass, field
from functools import reduce
from typing import Final, cast

type Position = tuple[int, int]

EARLY_STOP: Final[int] = 1_000_000
INITIAL_STATE: Final[int] = 0


@dataclass
class Machine:
    target_state: str
    # This is the integer representation of the target state
    target: int = field(init=False)
    buttons: list[tuple[int, ...]]
    # This is the integer representation of the button.
    button_ids: list[int] = field(init=False)
    joltages: list[int]
    target_joltage: tuple[int, ...] = field(init=False)
    button_vectors: list[tuple[int, ...]] = field(init=False)

    def __post_init__(self) -> None:
        ind_lights = len(self.target_state) - 2

        self.target = sum(
            map(
                lambda x: op.mul(*x),
                zip(
                    (2**i for i in range(ind_lights)),
                    (0 if c == "." else 1 for c in reversed(self.target_state[1:-1])),
                    strict=True,
                ),
            )
        )

        # In a target state of 4 indicator lights, (3) should be 0001
        # 0 is the left most indicator light.
        self.button_ids = [
            reduce(
                lambda acc, v: acc | v, (1 << (ind_lights - (ind_lght + 1)) for ind_lght in button)
            )
            for button in self.buttons
        ]

        self.target_joltage = tuple(self.joltages)

        self.button_vectors = []
        n_slots = len(self.joltages)
        for button in self.buttons:
            vec = [0] * n_slots
            for idx in button:
                vec[idx] += 1
            self.button_vectors.append(tuple(vec))

    def __get_fewest_button_presses(
        self, state: int, btn_idx: int, curr_presses: int, min_presses: int
    ) -> int:
        btn = self.button_ids[btn_idx]
        current_state = state ^ btn
        curr_presses += 1

        # We can reach the target by pressing this button
        if current_state == self.target:
            return curr_presses

        # Check if we can reach the target by any of the other buttons
        if any((current_state ^ b) == self.target for b in self.button_ids if b != btn):
            return curr_presses + 1

        # we won't do better pruning. Stop exploring further
        if curr_presses >= min(10, min_presses) or current_state == INITIAL_STATE:
            # print(f"Early stopping, {curr_presses}, {current_state} {min_presses}")
            return -1

        result = -1
        for idx in range(len(self.button_ids)):
            if idx == btn_idx:
                continue

            fewest_presses = self.__get_fewest_button_presses(
                current_state, idx, curr_presses, min_presses
            )
            if fewest_presses > 0:
                min_presses = min(min_presses, fewest_presses)
                result = fewest_presses if result < 0 else min(result, fewest_presses)

            if min_presses == 2:
                break

        return result

    # part-1
    def get_fewest_button_presses(self) -> int:
        # check if a direct button exists
        if self.target in self.button_ids:
            return 1

        min_presses = 1_000_000
        for idx in range(len(self.button_ids)):
            fewest_presses = self.__get_fewest_button_presses(
                state=INITIAL_STATE,
                btn_idx=idx,
                curr_presses=0,
                min_presses=1000000,
            )
            min_presses = min(min_presses, fewest_presses)
            if min_presses == 2:
                break

        return min_presses

    def __get_fewest_joltage_button_presses(
        self,
        curr_joltage: tuple[int, ...],
        btn_idx: int,
        nj: int,
        btn_presses: int,
        min_presses: int,
    ) -> tuple[int, int]:
        if min_presses == 1:
            return (min_presses, -1)

        # Apply button press using tuple arithmetic
        btn_vec = self.button_vectors[btn_idx]
        curr_joltage = tuple(c + v for c, v in zip(curr_joltage, btn_vec, strict=True))

        # add 1 to button press
        btn_presses += 1

        # Early stopping
        # Early stopping: Check if any slot exceeded its target
        if any(c > t for c, t in zip(curr_joltage, self.target_joltage, strict=True)):
            return (min_presses, -1)

        if btn_presses >= min_presses:
            return (min_presses, -1)

        if curr_joltage == self.target_joltage:
            return (min_presses, btn_presses)

        result = -1

        for idx in range(len(self.buttons)):
            (mp, fp) = self.__get_fewest_joltage_button_presses(
                curr_joltage, idx, nj, btn_presses, min_presses
            )
            min_presses = min(min_presses, mp)
            if fp > 0:
                min_presses = min(min_presses, fp)
                result = fp if result < 0 else min(fp, result)

            if min_presses == 1:
                break

        return (min_presses, result)

    # Exhaustive search
    def get_fewest_joltage_button_presses(self) -> int:
        min_presses = 1_000_000

        for idx in range(len(self.button_ids)):
            (min_presses, fewest_presses) = self.__get_fewest_joltage_button_presses(
                curr_joltage=tuple([0] * len(self.joltages)),
                btn_idx=idx,
                nj=len(self.joltages) - 1,
                btn_presses=0,
                min_presses=min_presses,
            )
            if fewest_presses > 0:
                min_presses = min(min_presses, fewest_presses)

            if min_presses == 1:
                break

        print(min_presses)
        return min_presses


MACHINE_PATTERN = re.compile(
    r"^(?P<i>\[[.#]+\])\s*(?P<b>(?:\([\d,]+\)\s)+)\s*(?P<j>\{[\d,]+\})\s*$"
)


def parse_machines(lines: Iterable[str]) -> list[Machine]:
    machines: list[Machine] = []
    for line in lines:
        if parsed := MACHINE_PATTERN.match(line):
            target_state = cast(str, parsed.group("i"))
            buttons = [
                tuple(map(int, b.lstrip("(").rstrip(")").split(",")))
                for b in cast(str, parsed.group("b")).split(" ")
                if b
            ]
            joltages = [
                int(v) for v in cast(str, parsed.group("j")).lstrip("{").rstrip("}").split(",")
            ]
            machines.append(Machine(target_state=target_state, buttons=buttons, joltages=joltages))

    print(f"Total machines: {len(machines)}")
    return machines


def compute_fewest_button_presses(machines: list[Machine]) -> int:
    return sum(machine.get_fewest_button_presses() for machine in machines)


# This will run forever
def compute_fewest_joltage_button_presses(machines: list[Machine]) -> int:
    return sum(machine.get_fewest_joltage_button_presses() for machine in machines)
