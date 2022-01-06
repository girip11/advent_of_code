import sys
from dataclasses import dataclass
from typing import Dict, List, Mapping, Set

DIGIT_DISPLAY_MAPPING = {2: 1, 3: 7, 4: 4, 7: 8}


@dataclass(frozen=True)
class Entry:
    unique_signals: List[str]
    output: List[str]

    def __post_init__(self) -> None:
        self.unique_signals.sort(key=len)

    def decode_digit_mapping(self) -> Mapping[str, int]:
        digit_mapping: Dict[str, int] = {}
        ref_mapping: Mapping[int, str] = self._decode_1478(digit_mapping)

        self._decode_069(digit_mapping, ref_mapping)
        self._decode_235(digit_mapping, ref_mapping)

        return digit_mapping

    def _decode_1478(self, digit_mapping: Dict[str, int]) -> Dict[int, str]:
        # first find 1,4,7,8
        for idx in [0, 1, 2, -1]:
            signal = self.unique_signals[idx]
            digit_mapping["".join(sorted(signal))] = DIGIT_DISPLAY_MAPPING[len(signal)]

        return {v: k for k, v in digit_mapping.items()}

    def _decode_069(self, digit_mapping: Dict[str, int], ref_mapping: Mapping[int, str]) -> None:
        eight_signal = set(ref_mapping[8])
        one_signal = set(ref_mapping[1])
        four_signal = set(ref_mapping[4])

        # look for signals of length 6 in sorted list
        for idx in [6, 7, 8]:
            signal = "".join(sorted(self.unique_signals[idx]))
            diff = "".join(eight_signal - set(signal))
            if diff in one_signal:
                digit_mapping[signal] = 6
            elif diff in four_signal:
                digit_mapping[signal] = 0
            else:
                digit_mapping[signal] = 9

    def _decode_235(self, digit_mapping: Dict[str, int], ref_mapping: Mapping[int, str]) -> None:
        eight_signal = set(ref_mapping[8])
        one_signal = set(ref_mapping[1])
        four_signal = set(ref_mapping[4])

        # look for signals of length 5 in sorted list
        for idx in [3, 4, 5]:
            signal = "".join(sorted(self.unique_signals[idx]))
            diff: Set[str] = eight_signal - set(signal)
            if len(diff.intersection(one_signal)) == 0:
                digit_mapping[signal] = 3
            else:
                if len(diff.intersection(four_signal)) == len(diff):
                    digit_mapping[signal] = 2
                else:
                    digit_mapping[signal] = 5


def parse_input(lines: List[str]) -> List[Entry]:
    entries: List[Entry] = []
    for line in lines:
        signals, output = map(lambda s: s.strip(), line.split("|"))
        entries.append(Entry(signals.split(" "), output.split(" ")))

    return entries


def count_1478_in_output(entries: List[Entry]) -> int:
    count = 0
    for entry in entries:
        for value in entry.output:
            if len(value) in DIGIT_DISPLAY_MAPPING:
                count += 1

    return count


def decode_output_digits(entries: List[Entry]) -> int:
    result = 0

    for entry in entries:
        digit_mapping: Mapping[str, int] = entry.decode_digit_mapping()
        # print(digit_mapping)
        value = 0
        for out_signal in entry.output:
            out_signal = "".join(sorted(out_signal))
            value = value * 10 + digit_mapping[out_signal]

        result += value

    return result


def main(*_: str) -> None:
    entries: List[Entry] = parse_input(sys.stdin.readlines())

    print(entries)
    # part-1
    print(count_1478_in_output(entries))

    # part-2
    print(decode_output_digits(entries))


if __name__ == "__main__":
    main(*sys.argv[1:])
