import abc
import sys
from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Instruction:
    direction: str
    units: int


def get_instruction(input_instruction: str) -> Instruction:
    res = input_instruction.split()
    return Instruction(res[0], int(res[1]))


@dataclass
class Position:
    horizontal: int = 0
    depth: int = 0


class Submarine(abc.ABC):
    _position: Position

    def __init__(self) -> None:
        self._position = Position(0, 0)

    @property
    def position(self) -> Position:
        return self._position

    @abc.abstractmethod
    def move(self, instruction: Instruction) -> None:
        ...


class BasicSubmarine(Submarine):
    def _move_forward(self, units: int) -> None:
        self._position.horizontal += units

    def _move_up(self, units: int) -> None:
        self._position.depth -= units

    def _move_down(self, units: int) -> None:
        self._position.depth += units

    def move(self, instruction: Instruction) -> None:
        getattr(self, f"_move_{instruction.direction}")(instruction.units)


class AimedSubmarine(Submarine):
    _aim: int = 0

    def _move_forward(self, units: int) -> None:
        self._position.horizontal += units
        self._position.depth += self._aim * units

    def _move_up(self, units: int) -> None:
        self._aim -= units

    def _move_down(self, units: int) -> None:
        self._aim += units

    def move(self, instruction: Instruction) -> None:
        getattr(self, f"_move_{instruction.direction}")(instruction.units)


def compute_position_product(instructions: List[Instruction], submarine: Submarine) -> int:
    for ins in instructions:
        submarine.move(ins)
    final_position = submarine.position
    return final_position.horizontal * final_position.depth


def main(*_: str) -> None:
    instructions: List[Instruction] = list(map(get_instruction, sys.stdin.readlines()))
    # part-1
    submarine: Submarine = BasicSubmarine()
    print(compute_position_product(instructions, submarine))

    # part-2
    submarine = AimedSubmarine()
    print(compute_position_product(instructions, submarine))


if __name__ == "__main__":
    main(*sys.argv[1:])
