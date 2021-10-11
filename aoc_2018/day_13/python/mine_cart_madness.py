# I do need to maintain each cart's position and what turn it will take at intersection

import abc
import sys
from dataclasses import dataclass, field
from typing import ClassVar, Dict, List, Mapping, NamedTuple, Optional, Tuple


class Location(NamedTuple):
    x: int
    y: int


class Direction:
    LEFT: ClassVar[str] = "<"
    RIGHT: ClassVar[str] = ">"
    UP: ClassVar[str] = "^"
    DOWN: ClassVar[str] = "v"

    _flip_config: ClassVar[Dict[str, str]] = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}

    @staticmethod
    def flip(dir_: str) -> str:
        return Direction._flip_config[dir_]


@dataclass
class TrackCell:
    symbol: str
    carts: int = field(default=0, init=False)


@dataclass(frozen=True)
class Track:
    cells: List[List[TrackCell]] = field(default_factory=list, init=False)

    def print_track(self) -> None:
        print("Displaying the track")
        for row in self.cells:
            for col in row:
                if col.carts == 0:
                    print(col.symbol, end="")
                else:
                    print("C", end="")
            print()


class CartMovement(abc.ABC):
    @abc.abstractmethod
    def move(self, cart_dir: str, cart_inters: Optional[int] = None) -> str:
        pass


class HorizontalMovement(CartMovement):
    def move(self, cart_dir: str, cart_inters: Optional[int] = None) -> str:
        return cart_dir


class VerticalMovement(CartMovement):
    def move(self, cart_dir: str, cart_inters: Optional[int] = None) -> str:
        return cart_dir


class TurnMovement(CartMovement):
    _forward_slash_turn_movement = {
        Direction.LEFT: Direction.DOWN,
        Direction.RIGHT: Direction.UP,
        Direction.UP: Direction.RIGHT,
        Direction.DOWN: Direction.LEFT,
    }

    def __init__(self, turn_type: str) -> None:
        self._turn_type = turn_type

    def move(self, cart_dir: str, cart_inters: Optional[int] = None) -> str:
        res = self._forward_slash_turn_movement[cart_dir]
        return res if self._turn_type == "/" else Direction.flip(res)


class IntersectionMovement(CartMovement):
    INTERSECTION_TURNS = ["L", "S", "R"]

    LEFT_TURN_CONFIG = {
        Direction.UP: Direction.LEFT,
        Direction.DOWN: Direction.RIGHT,
        Direction.LEFT: Direction.DOWN,
        Direction.RIGHT: Direction.UP,
    }

    def move(self, cart_dir: str, cart_inters: Optional[int] = None) -> str:
        turn_dir = IntersectionMovement.INTERSECTION_TURNS[(cart_inters or 0) % 3]

        if turn_dir == "S":
            return cart_dir

        # it could be left or right
        res = IntersectionMovement.LEFT_TURN_CONFIG[cart_dir]
        return res if turn_dir == "L" else Direction.flip(res)


class Cart:
    direction: str  # can be <, >, v or ^
    position: Location
    turns: int = 0

    def __init__(self, direction: str, position: Location) -> None:
        self.direction = direction
        self.position = position

    @staticmethod
    def is_cart(symbol: str) -> bool:
        return symbol in "<>^v"

    def __str__(self) -> str:
        return f"Cart: {self.direction}, position: {self.position}"

    def move(self, current_track_symbol: str, track_movement: Mapping[str, CartMovement]) -> None:
        dir_: str = track_movement[current_track_symbol].move(self.direction, self.turns)

        if current_track_symbol == "+":
            self.turns += 1

        if dir_ == Direction.UP:
            self.move_up()
        elif dir_ == Direction.DOWN:
            self.move_down()
        elif dir_ == Direction.LEFT:
            self.move_left()
        else:
            self.move_right()

    def move_left(self) -> None:
        if self.direction != "<":
            self.direction = "<"
        self.position = Location(self.position.x, self.position.y - 1)

    def move_right(self) -> None:
        if self.direction != ">":
            self.direction = ">"
        self.position = Location(self.position.x, self.position.y + 1)

    def move_up(self) -> None:
        if self.direction != "^":
            self.direction = "^"
        self.position = Location(self.position.x - 1, self.position.y)

    def move_down(self) -> None:
        if self.direction != "v":
            self.direction = "v"
        self.position = Location(self.position.x + 1, self.position.y)


def move_cart_on_track(
    track: Track, track_movement: Mapping[str, CartMovement], cart: Cart
) -> Cart:
    current_track_cell: TrackCell = track.cells[cart.position.x][cart.position.y]
    current_track_cell.carts -= 1

    cart.move(current_track_cell.symbol, track_movement)

    moved_track_cell: TrackCell = track.cells[cart.position.x][cart.position.y]
    moved_track_cell.carts += 1

    return cart


def arrange_carts(carts: List[Cart]) -> List[Cart]:
    carts.sort(key=lambda c: c.position)
    return carts


# part-1
def find_first_crash(
    track: Track, track_movement: Mapping[str, CartMovement], carts: List[Cart]
) -> Location:
    ticks = 0

    crash_location: Optional[Location] = None

    while crash_location is None:
        for cart in arrange_carts(carts):
            cart = move_cart_on_track(track, track_movement, cart)

            moved_track_cell: TrackCell = track.cells[cart.position.x][cart.position.y]
            if moved_track_cell.carts > 1:
                crash_location = cart.position
                break
        else:
            ticks += 1
        # track.print_track()

    # print(ticks)

    return crash_location


# part-2
def find_last_cart_location(
    track: Track, track_movement: Mapping[str, CartMovement], carts: List[Cart]
) -> Location:
    ticks = 0

    while len(carts) > 1:
        crashed_carts = []

        for i, cart in enumerate(arrange_carts(carts)):
            cart = move_cart_on_track(track, track_movement, cart)
            moved_track_cell: TrackCell = track.cells[cart.position.x][cart.position.y]

            if moved_track_cell.carts > 1:
                crashed_carts.append(i)
                for idx, neighbor in enumerate(carts):
                    if idx != i and cart.position == neighbor.position:
                        crashed_carts.append(idx)

        ticks += 1

        # remove the carts from the track
        for idx in crashed_carts:
            track_cell: TrackCell = track.cells[carts[idx].position[0]][carts[idx].position[1]]
            track_cell.carts -= 1

        # remove the carts from the carts list
        carts = [cart for idx, cart in enumerate(carts) if idx not in crashed_carts]

        # print(crashed_carts)
        # track.print_track()

    # print(ticks)

    if len(carts) == 0:
        raise Exception("All carts crashed")

    return carts[0].position


def _print_map(input_track: List[List[str]]) -> None:
    for row in input_track:
        for col in row:
            print(col, end="")
        print()


def _load_input_track(input_track: List[List[str]]) -> Track:
    cart_track = Track()
    for row in input_track:
        cart_track.cells.append([])
        for sym in row:
            track_cell = TrackCell(sym)
            if Cart.is_cart(sym):
                track_cell.carts += 1
            cart_track.cells[-1].append(track_cell)

    return cart_track


def _get_carts_from_track(input_track: Track) -> List[Cart]:
    carts: List[Cart] = []
    for row_num, row in enumerate(input_track.cells):
        for col_num, cell in enumerate(row):
            if Cart.is_cart(cell.symbol):
                carts.append(Cart(cell.symbol, Location(row_num, col_num)))

    return carts


# this assumes carts are currently not placed on intersections or corners
def _get_clean_track(track: Track) -> Track:
    for row in track.cells:
        for cell in row:
            if cell.symbol in "<>":
                cell.symbol = "-"
            elif cell.symbol in "v^":
                cell.symbol = "|"
    return track


def get_tracks_and_carts(input_track: List[List[str]]) -> Tuple[Track, List[Cart]]:
    loaded_input_track = _load_input_track(input_track)
    carts = _get_carts_from_track(loaded_input_track)
    clean_track = _get_clean_track(loaded_input_track)

    return (clean_track, carts)


def track_movement_config() -> Mapping[str, CartMovement]:
    return {
        "-": HorizontalMovement(),
        "|": VerticalMovement(),
        "/": TurnMovement("/"),
        "\\": TurnMovement("\\"),
        "+": IntersectionMovement(),
    }


def main(_: List[str]) -> None:
    input_track: List[List[str]] = [list(line.strip("\n")) for line in sys.stdin.readlines()]
    _print_map(input_track)

    track_movement = track_movement_config()

    track, carts = get_tracks_and_carts(input_track)
    loc = find_first_crash(track, track_movement, carts)
    print(f"{loc.y},{loc.x}")

    track, carts = get_tracks_and_carts(input_track)
    loc = find_last_cart_location(track, track_movement, carts)
    print(f"{loc.y},{loc.x}")


if __name__ == "__main__":
    main(sys.argv)
