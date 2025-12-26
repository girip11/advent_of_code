from aoc_2021.day_2.python.dive import (
    AimedSubmarine,
    BasicSubmarine,
    Instruction,
    compute_position_product,
)

instructions = [
    Instruction("forward", 5),
    Instruction("down", 5),
    Instruction("forward", 8),
    Instruction("up", 3),
    Instruction("down", 8),
    Instruction("forward", 2),
]


def test_basic_submarine_movement() -> None:
    assert compute_position_product(instructions, BasicSubmarine()) == 150


def test_aimed_submarine_movement() -> None:
    assert compute_position_product(instructions, AimedSubmarine()) == 900
