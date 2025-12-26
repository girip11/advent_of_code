from collections.abc import Generator
from typing import Literal, cast

type Direction = Literal["L", "R"]


def get_instruction(ins: list[str]) -> Generator[tuple[Direction, int]]:
    for i in ins:
        if len(i) > 0:
            yield (cast(Direction, i[0]), int(i[1:]))


def get_password(ins: list[str], init_pos: int = 50) -> int:
    curr_pos: int = init_pos
    passwd: int = 0
    for dir_, steps in get_instruction(ins):
        steps = steps % 100
        match dir_:
            case "L":
                curr_pos = (100 - (steps - curr_pos)) if steps > curr_pos else (curr_pos - steps)
            case "R":
                curr_pos = (curr_pos + steps) % 100

        if curr_pos == 0:
            passwd += 1

    return passwd


# Count all ticks leading to 0
def get_password_method2(ins: list[str], init_pos: int = 50) -> int:
    curr_pos: int = init_pos
    passwd: int = 0
    for dir_, steps in get_instruction(ins):
        passwd += steps // 100
        steps = steps % 100

        match dir_:
            case "L":
                value = curr_pos - steps
                passwd += int(value == 0)  # reached zero
                if value < 0:
                    passwd += int(curr_pos != 0)  # shouldnt have started from zero
                    curr_pos = value % 100
                else:
                    curr_pos = value
            case "R":
                curr_pos = curr_pos + steps
                passwd += curr_pos // 100
                curr_pos = curr_pos % 100

    return passwd
