import itertools
import sys
from dataclasses import dataclass
from typing import Iterable, Iterator, List, Tuple


@dataclass(frozen=True)
class Instruction:
    x_delta: int
    y_delta: int
    z_divisor: int

    def compute(self, digit: int, z_reg: int) -> int:
        w_reg: int = digit
        result: int = z_reg // self.z_divisor
        if (z_reg % 26 + self.x_delta) != w_reg:
            result = (26 * result) + w_reg + self.y_delta

        return result


@dataclass(frozen=True)
class Monad:
    instructions: List[Instruction]

    def validate(self, model_number: Iterable[int]) -> bool:
        z_reg: int = 0
        for ins, digit in zip(self.instructions, model_number):
            z_reg = ins.compute(digit, z_reg)
        return z_reg == 0


@dataclass(frozen=True)
class SimplifiedInstruction:
    matching_inst_y_delta: int
    curr_inst_x_delta: int

    def generate_pairs(self, digit_range: range) -> Iterator[Tuple[int, int]]:
        for w_match_inst in digit_range:
            w_curr: int = w_match_inst + self.matching_inst_y_delta + self.curr_inst_x_delta
            if 1 <= w_curr <= 9:
                yield (w_match_inst, w_curr)


DigitPlaces = Tuple[int, int]


def simplify_instructions(
    instructions: List[Instruction],
) -> List[Tuple[DigitPlaces, SimplifiedInstruction]]:

    y_delta_stack: List[Tuple[int, int]] = []
    simplified_instructions: List[Tuple[DigitPlaces, SimplifiedInstruction]] = []

    for cur_inst_num, inst in enumerate(instructions):
        if inst.z_divisor == 26:
            prev_inst_num, y_delta = y_delta_stack.pop()
            digit_places: DigitPlaces = (prev_inst_num, cur_inst_num)
            simplified_instructions.append(
                (digit_places, SimplifiedInstruction(y_delta, inst.x_delta))
            )
        else:
            y_delta_stack.append((cur_inst_num, inst.y_delta))

    return simplified_instructions


def generate_valid_model_numbers(
    instructions: List[Instruction], digit_range: range
) -> Iterator[List[int]]:
    simplified_instructions: List[
        Tuple[DigitPlaces, SimplifiedInstruction]
    ] = simplify_instructions(instructions)

    digit_places: List[int] = list(itertools.chain(*[dp for dp, _ in simplified_instructions]))
    model_digit_generators: List[Iterator[Tuple[int, int]]] = [
        simp_inst.generate_pairs(digit_range) for _, simp_inst in simplified_instructions
    ]

    for model_number in itertools.product(*model_digit_generators):
        number: List[int] = [0] * 14
        for pos, digit in zip(digit_places, itertools.chain(*list(model_number))):
            number[pos] = digit

        yield number


def find_largest_model_number(monad: Monad) -> List[int]:
    return next(generate_valid_model_numbers(monad.instructions, range(9, 0, -1)))


def find_smallest_model_number(monad: Monad) -> List[int]:
    return next(generate_valid_model_numbers(monad.instructions, range(1, 10)))


def parse_input(lines: List[str]) -> Monad:
    instructions: List[Instruction] = []

    for i in (i for i, ins in enumerate(lines) if ins.startswith("inp")):
        z_divisor = int(lines[i + 4].strip().split(" ")[-1])
        x_delta = int(lines[i + 5].strip().split(" ")[-1])
        y_delta = int(lines[i + 15].strip().split(" ")[-1])
        instructions.append(Instruction(x_delta, y_delta, z_divisor))

    return Monad(instructions)


def main(*_: str) -> None:
    input_lines = sys.stdin.readlines()
    monad: Monad = parse_input(input_lines)

    # part-1
    largest_valid_model_number = find_largest_model_number(monad)
    assert monad.validate(largest_valid_model_number)
    print("".join(map(str, largest_valid_model_number)))

    # part-2
    smallest_valid_model_number = find_smallest_model_number(monad)
    assert monad.validate(smallest_valid_model_number)
    print("".join(map(str, smallest_valid_model_number)))


if __name__ == "__main__":
    main(*sys.argv[1:])
