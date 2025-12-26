import functools
import math
import sys
from abc import ABC, abstractmethod
from copy import deepcopy
from dataclasses import dataclass
from typing import List, Optional, Tuple, cast


class SnailfishNumber(ABC):
    @abstractmethod
    def is_pair(self) -> bool:
        ...

    @abstractmethod
    def add(self, other: "SnailfishNumber") -> "SnailfishNumber":
        ...

    @abstractmethod
    def traverse_inorder(self) -> List["SnailfishNumber"]:
        ...

    @abstractmethod
    def explode(self) -> bool:
        ...

    @abstractmethod
    def split(self) -> Tuple[bool, "SnailfishNumber"]:
        ...

    @abstractmethod
    def magnitude(self) -> int:
        ...


@dataclass
class RegularNumber(SnailfishNumber):
    value: int

    def is_pair(self) -> bool:
        return False

    def add(self, other: SnailfishNumber) -> SnailfishNumber:
        return PairNumber(self, other)

    def traverse_inorder(self) -> List[SnailfishNumber]:
        return [self]

    def explode(self) -> bool:
        return False

    def split(self) -> Tuple[bool, SnailfishNumber]:
        if self.value < 10:
            return (False, self)
        funcs = [math.floor, math.ceil]
        return (True, PairNumber(*map(lambda f: RegularNumber(f(self.value / 2)), funcs)))

    def magnitude(self) -> int:
        return self.value

    def __str__(self) -> str:
        return str(self.value)


@dataclass(init=False)
class PairNumber(SnailfishNumber):
    left: SnailfishNumber
    right: SnailfishNumber

    def __init__(self, left: SnailfishNumber, right: SnailfishNumber) -> None:
        self.left = left
        self.right = right

    def is_pair(self) -> bool:
        return True

    def is_simple_pair(self) -> bool:
        return all([not self.left.is_pair(), not self.right.is_pair()])

    def add(self, other: SnailfishNumber) -> SnailfishNumber:
        return PairNumber(self, other)

    def traverse_inorder(self) -> List[SnailfishNumber]:
        numbers: List[SnailfishNumber] = [self]
        return numbers + self.left.traverse_inorder() + self.right.traverse_inorder()

    def explode(self) -> bool:
        exploded: int = 0
        while self.recursive_explode(self, 1):
            exploded += 1

        return exploded > 0

    def recursive_explode(self, root: SnailfishNumber, level: int = 0) -> bool:
        exploded: bool = False

        for number in [self.left, self.right]:
            if not exploded and number.is_pair():
                exploded = cast(PairNumber, number).recursive_explode(root, level + 1)

        if level >= 4:
            inorder_numbers: List[SnailfishNumber] = root.traverse_inorder()
            exploded = self._try_exploding(inorder_numbers)

        return exploded

    def _try_exploding(self, inorder_numbers: List[SnailfishNumber]) -> bool:
        if self.is_simple_pair():
            return False

        current_pair: PairNumber = cast(
            PairNumber, self.left if self.left.is_pair() else self.right
        )

        current_pair_pos = [
            i for i, number in enumerate(inorder_numbers) if number is current_pair
        ][0]

        def find_first_regular_number(start: int, stop: int, step: int) -> Optional[RegularNumber]:
            number: Optional[RegularNumber] = None
            for i in range(start, stop, step):
                if not inorder_numbers[i].is_pair():
                    number = cast(RegularNumber, inorder_numbers[i])
                    break
            return number

        if left := find_first_regular_number(current_pair_pos - 1, -1, -1):
            left.value += cast(RegularNumber, current_pair.left).value

        if right := find_first_regular_number(current_pair_pos + 3, len(inorder_numbers), 1):
            right.value += cast(RegularNumber, current_pair.right).value

        if current_pair is self.left:
            self.left = RegularNumber(0)
        else:
            self.right = RegularNumber(0)

        return True

    def split(self) -> Tuple[bool, SnailfishNumber]:
        split_status, self.left = self.left.split()

        if not split_status:
            split_status, self.right = self.right.split()

        return (split_status, self)

    def magnitude(self) -> int:
        return sum(num.magnitude() * scale for num, scale in [(self.left, 3), (self.right, 2)])

    def __str__(self) -> str:
        return f"[{','.join(map(str, [self.left, self.right]))}]"


@dataclass
class Line:
    line: str
    index: int = 0

    def __getitem__(self, pos: int) -> str:
        return self.line[pos]


def parse_number(line: Line) -> SnailfishNumber:
    number: PairNumber
    numbers: List[SnailfishNumber] = []
    line.index += 1
    stop: bool = False

    while not stop and line.index < len(line.line):
        i = line.index
        if line[i] == "[":
            numbers.append(parse_number(line))
            continue
        if line[i].isdigit():
            numbers.append(RegularNumber(int(line[i])))
        elif line[i] == "]":
            number = PairNumber(left=numbers[0], right=numbers[1])
            stop = True

        line.index += 1

    return number


def parse_input(lines: List[str]) -> List[SnailfishNumber]:
    return [parse_number(Line(line, 0)) for line in lines]


def reduce(number: SnailfishNumber) -> SnailfishNumber:
    split: bool = True
    while split:
        number.explode()
        split, number = number.split()

    return number


def add(op1: SnailfishNumber, op2: SnailfishNumber) -> SnailfishNumber:
    return reduce(op1.add(op2))


def perform_addition(numbers: List[SnailfishNumber]) -> SnailfishNumber:
    return functools.reduce(add, numbers)


def largest_magnitude(numbers: List[SnailfishNumber]) -> int:
    largest_magnitude: int = -1
    for number1 in numbers:
        for number2 in numbers:
            if number1 is not number2:
                current_magnitude = add(deepcopy(number1), deepcopy(number2)).magnitude()
                # print(f"{number1}{number2}{current_magnitude}")
                largest_magnitude = max(largest_magnitude, current_magnitude)

    return largest_magnitude


def main(*_: str) -> None:
    snailfish_numbers: List[SnailfishNumber] = parse_input(sys.stdin.readlines())

    for snailfish_num in snailfish_numbers:
        print(snailfish_num)

    print("======================================")
    # part-1
    result: SnailfishNumber = perform_addition([deepcopy(n) for n in snailfish_numbers])
    print(result)
    print(f"Part1 - {result.magnitude()}")

    print("======================================")
    # part-2
    print(f"Part2 - {largest_magnitude(snailfish_numbers)}")


if __name__ == "__main__":
    main(*sys.argv[1:])
