from pathlib import Path

from aoc_2021.day_20.python.trench_map import count_lit_pixels_post_enhancing, parse_input


def test_unique_beacons() -> None:
    for file, res in [("simple_input.txt", 35), ("simple_input2.txt", 5326)]:
        algo, img = parse_input(
            iter((Path(__file__).parent.parent / file).read_text().strip().split("\n"))
        )
        assert count_lit_pixels_post_enhancing(algo, img, 3, 2) == res
