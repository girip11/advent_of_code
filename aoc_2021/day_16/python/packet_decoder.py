import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from functools import reduce
from operator import eq, gt, lt, mul
from typing import List, cast

VERSION_BITS = 3
TYPE_BITS = 3
LENGTH_BIT = 1


class Packet(ABC):
    version: int
    type_: int

    def __init__(self, version: int, type_: int) -> None:
        self.version = version
        self.type_ = type_

    @abstractmethod
    def evaluate(self) -> int:
        ...


class OperatorPacket(Packet):
    subpackets: List[Packet]

    def __init__(self, version: int, type_: int) -> None:
        self.subpackets = []
        super().__init__(version, type_)

    def evaluate(self) -> int:
        if self.type_ == 0:
            return sum(subpacket.evaluate() for subpacket in self.subpackets)
        elif self.type_ == 1:
            return reduce(mul, (subpacket.evaluate() for subpacket in self.subpackets), 1)
        elif self.type_ == 2:
            return min(subpacket.evaluate() for subpacket in self.subpackets)
        elif self.type_ == 3:
            return max(subpacket.evaluate() for subpacket in self.subpackets)
        elif self.type_ == 5:
            return 1 if gt(self.subpackets[0].evaluate(), self.subpackets[1].evaluate()) else 0
        elif self.type_ == 6:
            return 1 if lt(self.subpackets[0].evaluate(), self.subpackets[1].evaluate()) else 0
        elif self.type_ == 7:
            return 1 if eq(self.subpackets[0].evaluate(), self.subpackets[1].evaluate()) else 0
        else:
            return 0


@dataclass
class LiteralPacket(Packet):
    value: int

    def __init__(self, version: int, type_: int, value: int) -> None:
        self.value = value
        super().__init__(version, type_)

    def evaluate(self) -> int:
        return self.value


@dataclass
class ParseIndex:
    index: int = field(default_factory=int, init=False)


def parse_version(bin_msg: str, index: ParseIndex) -> int:
    current_idx = index.index
    version: int = int(bin_msg[current_idx : current_idx + VERSION_BITS], base=2)
    index.index += VERSION_BITS
    return version


def parse_type(bin_msg: str, index: ParseIndex) -> int:
    current_idx = index.index
    type_: int = int(bin_msg[current_idx : current_idx + TYPE_BITS], base=2)
    index.index += TYPE_BITS
    return type_


def parse_literal_value(bin_msg: str, index: ParseIndex) -> int:
    current_val: str = "1"
    result: List[str] = []
    while current_val[0] == "1":
        current_val = bin_msg[index.index : index.index + 5]
        index.index += 5
        result.append(current_val[1:])

    return int("".join(result), base=2)


def parse_subpacket_bits_length(bin_msg: str, index: ParseIndex) -> int:
    subpacket_bit_length = int(bin_msg[index.index : index.index + 15], base=2)
    index.index += 15
    return subpacket_bit_length


def parse_subpacket_count(bin_msg: str, index: ParseIndex) -> int:
    subpacket_count = int(bin_msg[index.index : index.index + 11], base=2)
    index.index += 11
    return subpacket_count


def parse_operator_packet(bin_msg: str, index: ParseIndex) -> List[Packet]:
    packet_length_type: int = int(bin_msg[index.index], base=2)
    index.index += 1

    if packet_length_type == 0:
        subpackets: List[Packet] = []
        bit_length = parse_subpacket_bits_length(bin_msg, index)
        before_parsing = index.index

        while index.index - before_parsing < bit_length:
            subpackets.append(parse_packet(bin_msg, index))

        # bits_parsed = index.index - index_before
        # # skip the rest as padding
        # index.index += bit_length - bits_parsed
        return subpackets

    return [parse_packet(bin_msg, index) for _ in range(parse_subpacket_count(bin_msg, index))]


LITERAL_PACKET = 4


def parse_packet(bin_msg: str, index: ParseIndex) -> Packet:
    version = parse_version(bin_msg, index)
    type_ = parse_type(bin_msg, index)

    if type_ == LITERAL_PACKET:
        return LiteralPacket(version, type_, parse_literal_value(bin_msg, index))

    packet = OperatorPacket(version, type_)
    packet.subpackets.extend(parse_operator_packet(bin_msg, index))

    return packet


def hex_to_binary(bits_msg: str) -> str:
    hex_binary_mapping = {
        "0": "0000",
        "1": "0001",
        "2": "0010",
        "3": "0011",
        "4": "0100",
        "5": "0101",
        "6": "0110",
        "7": "0111",
        "8": "1000",
        "9": "1001",
        "A": "1010",
        "B": "1011",
        "C": "1100",
        "D": "1101",
        "E": "1110",
        "F": "1111",
    }
    return "".join(hex_binary_mapping[hex_bit] for hex_bit in bits_msg)


def parse_transmission(bits_transmission: str) -> Packet:
    binary_msg: str = hex_to_binary(bits_transmission)
    parse_index: ParseIndex = ParseIndex()
    print(binary_msg)

    return parse_packet(binary_msg, parse_index)


def compute_version_sum(packet: Packet) -> int:
    if isinstance(packet, LiteralPacket):
        return packet.version

    subpackets_version_sum = sum(
        compute_version_sum(pkt) for pkt in cast(OperatorPacket, packet).subpackets
    )
    return packet.version + subpackets_version_sum


def main(*_: str) -> None:
    bits_msg: str = sys.stdin.readline().strip()
    packet: Packet = parse_transmission(bits_msg)

    # print(packet.value)

    # for packet in packet.subpackets:
    #     print(packet.value)

    # part-1
    # if packet:
    print(compute_version_sum(packet))

    # part-2
    print(packet.evaluate())


if __name__ == "__main__":
    main(*sys.argv[1:])
