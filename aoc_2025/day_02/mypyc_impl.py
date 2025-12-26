import itertools
from collections.abc import Generator
from functools import cache


def get_next_invalid_prd_id(start_prd_id: str, end_prd_id: str, n_repeat: int) -> Generator[str]:
    seq_start = start_prd_id[0 : len(start_prd_id) // n_repeat]
    start_prd_id_val = int(start_prd_id)
    end_prd_id_val = int(end_prd_id)

    for i in itertools.count(int(seq_start)):
        next_prd_id = "".join(itertools.repeat(str(i), n_repeat))
        next_prd_id_val = int(next_prd_id)
        if start_prd_id_val <= next_prd_id_val <= end_prd_id_val:
            # print(f"S: {start_prd_id}, V:{next_prd_id}, E:{end_prd_id}")
            yield next_prd_id
        elif next_prd_id_val > end_prd_id_val:
            break

    return


def get_invalid_prd_ids(
    start_prd_id: str, end_prd_id: str, *, n_repeats: set[int]
) -> Generator[int]:
    start_digits_n = len(start_prd_id)
    end_digits_n = len(end_prd_id)

    for n_repeat in n_repeats:
        # find sequences that can repeat `n_repeat` times
        # ex: 500 - 600, n_repeat = 2
        if start_digits_n % n_repeat != 0 and end_digits_n % n_repeat != 0:
            continue

        curr_start_prd_id = start_prd_id
        curr_end_prd_id = end_prd_id

        if start_digits_n % n_repeat != 0 and end_digits_n % n_repeat == 0:
            # start cannot be pattern that can be repeated n_repeat times
            # ex: 50000 - 200000, n_repeat = 3
            curr_start_prd_id = str(10 ** (end_digits_n - 1))

        if end_digits_n % n_repeat != 0 and start_digits_n % n_repeat == 0:
            # end cannot be pattern that can be repeated n_repeat times
            # ex: 500 - 2000, n_repeat = 3
            curr_end_prd_id = str((10**start_digits_n) - 1)

        yield from map(int, get_next_invalid_prd_id(curr_start_prd_id, curr_end_prd_id, n_repeat))


def get_prd_id_ranges(prd_id_ranges: str) -> Generator[tuple[str, str]]:
    for prd_id_range in prd_id_ranges.split(","):
        start_end_range = prd_id_range.split("-")
        yield (start_end_range[0], start_end_range[1])


# part-1
def get_invalid_prd_ids_sum(prd_id_ranges: str) -> int:
    return sum(
        itertools.chain(
            *[
                get_invalid_prd_ids(start, end, n_repeats={2})
                for (start, end) in get_prd_id_ranges(prd_id_ranges)
            ]
        )
    )


@cache
def get_n_repeats(digit_len: int) -> set[int]:
    return {int(digit_len / i) for i in range(1, (digit_len // 2) + 1) if digit_len % i == 0}


# part-2: Look for sequences that can repeat multiple times
def get_invalid_prd_ids_sum_multi_seq_len_repeats(prd_id_ranges: str) -> int:
    return sum(
        set(
            itertools.chain(
                *[
                    get_invalid_prd_ids(
                        start,
                        end,
                        n_repeats=get_n_repeats(len(start)).union(get_n_repeats(len(end))),
                    )
                    for (start, end) in get_prd_id_ranges(prd_id_ranges)
                ]
            )
        )
    )
