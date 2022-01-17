import itertools
import sys
from dataclasses import dataclass, field
from operator import sub
from typing import Iterator, List, Tuple

LIGHT: str = "#"
DARK: str = "."


@dataclass
class Image:
    pixels: List[List[str]] = field(default_factory=list)
    outer: str = field(default=".")  # initially everything is dark
    _pixels_lit: int = field(default=-1, init=False)

    def size(self) -> Tuple[int, int]:
        return (len(self.pixels), len(self.pixels[0]))

    def __getitem__(self, pos: Tuple[int, int]) -> str:
        size: Tuple[int, int] = self.size()
        return (
            self.pixels[pos[0]][pos[1]]
            if 0 <= pos[0] < size[0] and 0 <= pos[1] < size[1]
            else self.outer
        )

    def __setitem__(self, pos: Tuple[int, int], value: str) -> None:
        self.pixels[pos[0]][pos[1]] = value

    @property
    def pixels_lit(self) -> int:
        if self._pixels_lit == -1:
            self._pixels_lit = sum(row.count(LIGHT) for row in self.pixels)

        return self._pixels_lit

    def display(self) -> None:
        for row in self.pixels:
            for pixel in row:
                print(pixel, end="")
            print()

    @staticmethod
    def create_blank_image(size: Tuple[int, int], outer: str) -> "Image":
        return Image([[DARK] * size[1] for _ in range(size[0])], outer)


@dataclass(frozen=True)
class ImageEnhancementAlgo:
    _algo: str

    def __len__(self) -> int:
        return len(self._algo)

    def __getitem__(self, pos: int) -> str:
        return self._algo[pos]


def pixel_window(out_pixel: Tuple[int, int], offset: int) -> List[Tuple[int, int]]:
    row_mid, col_mid = map(sub, out_pixel, [offset, offset])
    return list(itertools.product(range(row_mid - 1, row_mid + 2), range(col_mid - 1, col_mid + 2)))


def enhance_image(algo: ImageEnhancementAlgo, input_img: Image, window: int) -> Image:
    in_img_size: Tuple[int, int] = input_img.size()
    out_img_size: Tuple[int, int]

    out_img_size = (
        in_img_size[0] + window - 1,
        in_img_size[1] + window - 1,
    )

    outer: str = algo[0] if input_img.outer == DARK else algo[-1]
    output_img: Image = Image.create_blank_image(out_img_size, outer)

    for row, col in itertools.product(*map(range, out_img_size)):
        pos: Tuple[int, int] = (row, col)
        algo_pos: int = sum(
            2 ** i
            for i, pix in enumerate(reversed(pixel_window(pos, window // 2)))
            if input_img[pix] == LIGHT
        )
        output_img[pos] = algo[algo_pos]

    return output_img


def count_lit_pixels_post_enhancing(
    algo: ImageEnhancementAlgo, input_img: Image, window: int, enhance: int
) -> int:
    for _ in range(enhance):
        input_img = enhance_image(algo, input_img, window)
    return input_img.pixels_lit


def parse_input(lines: Iterator[str]) -> Tuple[ImageEnhancementAlgo, Image]:
    image_enh_algo: ImageEnhancementAlgo = ImageEnhancementAlgo(next(lines).strip())
    img: Image = Image()
    for line in lines:
        if line := line.strip():
            img.pixels.append(list(line))

    return (image_enh_algo, img)


def main(*_: str) -> None:
    img_enh_algo, input_img = parse_input(iter(sys.stdin.readlines()))
    window: int = 3
    assert len(img_enh_algo) == 512

    # part-1
    print(input_img.pixels_lit)
    print(f"Part1 - {count_lit_pixels_post_enhancing(img_enh_algo, input_img, window, 2)}")

    # part-2
    print(f"Part1 - {count_lit_pixels_post_enhancing(img_enh_algo, input_img, window, 50)}")


if __name__ == "__main__":
    main(*sys.argv[1:])
