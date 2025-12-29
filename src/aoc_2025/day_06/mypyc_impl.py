import itertools
import operator
import re
from collections.abc import Iterable
from functools import reduce

NUMBER_PATTERN = re.compile(r"(\d+|[*+])")


# part-1
def get_math_homework_result(lines: Iterable[str]) -> int:
    result: int = 0
    for problem in zip(
        *[NUMBER_PATTERN.findall(line) for entry in lines if (line := entry.strip())],
        strict=True,
    ):
        numbers = map(int, problem[:-1])
        if problem[-1] == "+":
            # print(problem, sum(numbers))
            result += sum(numbers)
        elif problem[-1] == "*":
            # print(problem, reduce(operator.mul, numbers, 1))
            result += reduce(operator.mul, numbers, 1)

    return result


NUMBER_PATTERN2 = re.compile(r"(\d+|[*+])\s")


# part-2
def get_math_homework_result_part2(lines: list[str]) -> int:
    result: int = 0
    op_indices = [i for i, s in enumerate(lines[-1]) if s == "*" or s == "+"]
    op_indices.append(-1)

    for problem in zip(
        *[
            [
                line[start : (end - 1) if end != -1 else end]
                for start, end in itertools.pairwise(op_indices)
            ]
            for line in lines
            if len(line.strip()) > 0
        ],
        strict=True,
    ):
        numbers = [
            sum(
                digit * (10**idx)
                for idx, digit in enumerate(map(int, filter(str.isdigit, reversed(digits))))
            )
            for digits in zip(*problem[:-1], strict=True)
        ]

        op = problem[-1].strip()
        if op == "+":
            # print(problem, sum(numbers))
            result += sum(numbers)
        elif op == "*":
            # print(problem, reduce(operator.mul, numbers, 1))
            result += reduce(operator.mul, numbers, 1)

    return result
