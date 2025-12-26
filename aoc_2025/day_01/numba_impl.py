from numba import njit
from numba.typed import List


@njit(cache=False)
def get_steps(ins: str) -> int:
    steps: int = 0
    for idx in range(1, len(ins)):
        steps = steps * 10 + ord(ins[idx]) - ord("0")

    return steps


@njit(cache=False)
def get_password(ins: list[str], init_pos: int = 50) -> int:
    curr_pos: int = init_pos
    passwd: int = 0

    for i in ins:
        if len(i) == 0:
            continue

        dir_: str = i[0]
        steps: int = get_steps(i) % 100

        match dir_:
            case "L":
                curr_pos = (100 - (steps - curr_pos)) if steps > curr_pos else (curr_pos - steps)
            case "R":
                curr_pos = (curr_pos + steps) % 100
            case _:
                pass

        if curr_pos == 0:
            passwd += 1

    return passwd


@njit(cache=False)
def get_password_method2(ins: list[str], init_pos: int = 50) -> int:
    curr_pos: int = init_pos
    passwd: int = 0

    for i in ins:
        if len(i) == 0:
            continue

        dir_: str = i[0]
        steps: int = get_steps(i)
        passwd += steps // 100
        steps = steps % 100

        match dir_:
            case "L":
                value = curr_pos - steps
                passwd += int(value == 0)  # reached zero
                if value < 0:
                    passwd += int(curr_pos != 0)  # shouldnt have started from zero
                    curr_pos = 100 + value
                else:
                    curr_pos = value
            case "R":
                curr_pos = curr_pos + steps
                passwd += curr_pos // 100
                curr_pos = curr_pos % 100
            case _:
                pass

    return passwd


# ASCII constants
ORD_0 = 48
ORD_L = 76
ORD_R = 82


@njit(cache=False)
def get_steps_bytes(ins: bytes) -> int:
    steps: int = 0
    # Iterate bytes directly (yields integers)
    for idx in range(1, len(ins)):
        steps = steps * 10 + (ins[idx] - ORD_0)
    return steps


@njit(cache=False)
def get_password_fast(instrs: List[bytes], init_pos: int = 50) -> int:
    curr_pos: int = init_pos
    passwd: int = 0

    for ins in instrs:
        if len(ins) == 0:
            continue

        # i[0] on bytes returns an integer, no string allocation!
        dir_code: int = ins[0]
        steps: int = get_steps_bytes(ins) % 100

        if dir_code == ORD_L:
            curr_pos = (100 - (steps - curr_pos)) if steps > curr_pos else (curr_pos - steps)
        elif dir_code == ORD_R:
            curr_pos = (curr_pos + steps) % 100

        if curr_pos == 0:
            passwd += 1

    return passwd


@njit(cache=False)
def get_password_method2_fast(instrs: List[bytes], init_pos: int = 50) -> int:
    curr_pos: int = init_pos
    passwd: int = 0

    for ins in instrs:
        if len(ins) == 0:
            continue

        # i[0] on bytes returns an integer, no string allocation!
        dir_code: int = ins[0]
        steps: int = get_steps_bytes(ins)
        passwd += steps // 100
        steps = steps % 100

        if dir_code == ORD_L:
            value = curr_pos - steps
            passwd += int(value == 0)  # reached zero
            if value < 0:
                passwd += int(curr_pos != 0)  # shouldnt have started from zero
                curr_pos = 100 + value
            else:
                curr_pos = value
        elif dir_code == ORD_R:
            curr_pos = curr_pos + steps
            passwd += curr_pos // 100
            curr_pos = curr_pos % 100

    return passwd
