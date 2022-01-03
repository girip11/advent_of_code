import sys
from dataclasses import dataclass
from typing import List


@dataclass
class BitCounter:
    zero: int = 0
    one: int = 0

    def most_common_bit(self, on_equal: int = 0) -> int:
        if self.zero == self.one:
            return on_equal
        return 0 if self.zero > self.one else 1

    def least_common_bit(self, on_equal: int = 0) -> int:
        if self.zero == self.one:
            return on_equal

        return 0 if self.zero < self.one else 1


def compute_rate(positionwise_bit_counters: List[BitCounter], rate_type: str) -> int:
    rate = 0
    attr = "most_common_bit" if rate_type == "gamma" else "least_common_bit"

    for idx, counter in enumerate(reversed(positionwise_bit_counters)):
        rate += getattr(counter, attr)() * (2 ** idx)

    print(rate)
    return rate


def compute_gamma_rate(positionwise_bit_counters: List[BitCounter]) -> int:
    return compute_rate(positionwise_bit_counters, "gamma")


def compute_epsilon_rate(positionwise_bit_counters: List[BitCounter]) -> int:
    return compute_rate(positionwise_bit_counters, "epsilon")


def compute_positionwise_bit_count(diagnostics: List[str]) -> List[BitCounter]:
    positionwise_bit_counters: List[BitCounter] = [BitCounter() for _ in range(len(diagnostics[0]))]

    for num in diagnostics:
        for pos, bit in enumerate(num):
            counter = positionwise_bit_counters[pos]
            if bit == "0":
                counter.zero += 1
            else:
                counter.one += 1

    return positionwise_bit_counters


def compute_power_consumption(diagnostics: List[str]) -> int:
    positionwise_bit_counters: List[BitCounter] = compute_positionwise_bit_count(diagnostics)
    return compute_gamma_rate(positionwise_bit_counters) * compute_epsilon_rate(
        positionwise_bit_counters
    )


def compute_o2_co2_rating(
    diagnostics: List[str], positionwise_bit_counters: List[BitCounter], gas_type: str
) -> int:
    current_vals = diagnostics
    current_counters = positionwise_bit_counters
    attr = "most_common_bit" if gas_type == "o2" else "least_common_bit"
    on_equal = 1 if gas_type == "o2" else 0

    for pos, _ in enumerate(current_counters):
        common_bit = getattr(current_counters[pos], attr)(on_equal=on_equal)
        current_vals = [num for num in current_vals if int(num[pos]) == common_bit]
        current_counters = compute_positionwise_bit_count(current_vals)
        # print(current_vals)

        if len(current_vals) == 1:
            break

    return int(current_vals[0], 2)


def compute_o2_generator_rating(
    diagnostics: List[str], positionwise_bit_counters: List[BitCounter]
) -> int:
    return compute_o2_co2_rating(diagnostics, positionwise_bit_counters, "o2")


def compute_co2_scrubber_rating(
    diagnostics: List[str], positionwise_bit_counters: List[BitCounter]
) -> int:
    return compute_o2_co2_rating(diagnostics, positionwise_bit_counters, "co2")


def compute_life_support_rating(diagnostics: List[str]) -> int:
    positionwise_bit_counters: List[BitCounter] = compute_positionwise_bit_count(diagnostics)

    return compute_o2_generator_rating(
        diagnostics, positionwise_bit_counters
    ) * compute_co2_scrubber_rating(diagnostics, positionwise_bit_counters)


def main(*_: str) -> None:
    diagnostics: List[str] = list(map(lambda diag: diag.strip(), sys.stdin.readlines()))
    # part-1
    print(compute_power_consumption(diagnostics))

    # part-2
    print(compute_life_support_rating(diagnostics))


if __name__ == "__main__":
    main(*sys.argv[1:])
