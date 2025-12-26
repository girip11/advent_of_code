from aoc_2021.day_16.python.packet_decoder import Packet, compute_version_sum, parse_transmission


def test_compute_version_sum() -> None:
    input_ = {
        "A0016C880162017C3686B18A3D4780": 31,
        "C0015000016115A2E0802F182340": 23,
        "620080001611562C8802118E34": 12,
        "8A004A801A8002F478": 16,
    }

    for hex_msg, version_sum in input_.items():
        packet: Packet = parse_transmission(hex_msg)
        assert compute_version_sum(packet) == version_sum


def test_evaluate() -> None:
    input_ = {
        "C200B40A82": 3,
        "04005AC33890": 54,
        "880086C3E88112": 7,
        "CE00C43D881120": 9,
        "D8005AC2A8F0": 1,
        "F600BC2D8F": 0,
        "9C005AC2F8F0": 0,
        "9C0141080250320F1802104A08": 1,
    }

    for hex_msg, result in input_.items():
        packet: Packet = parse_transmission(hex_msg)
        assert packet.evaluate() == result
