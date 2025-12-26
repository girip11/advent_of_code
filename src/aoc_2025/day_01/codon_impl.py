import codon


@codon.jit
def get_password(ins: list[str], init_pos: int = 50) -> int:
    curr_pos: int = init_pos
    passwd: int = 0
    for i in ins:
        if len(i) == 0:
            continue
        dir_, steps = (i[0], int(i[1:]))
        steps = steps % 100
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


# Count all ticks leading to 0
@codon.jit
def get_password_method2(ins: list[str], init_pos: int = 50) -> int:
    curr_pos: int = init_pos
    passwd: int = 0
    for i in ins:
        if len(i) == 0:
            continue
        dir_, steps = (i[0], int(i[1:]))
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
