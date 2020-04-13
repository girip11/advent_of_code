import sys
from functools import reduce
from typing import Dict, List, Iterable, MutableMapping, Tuple


class Direction:
    NORTH: str = "^"
    SOUTH: str = "v"
    EAST: str = ">"
    WEST: str = "<"


def present_to_house(
    direction: str,
    cur_loc: Tuple[int, int],
    visited_house_coordinates: MutableMapping[Tuple[int, int], int],
) -> Tuple[int, int]:
    new_loc: Tuple[int, int]
    if direction == Direction.NORTH:
        # moves north
        new_loc = (cur_loc[0], cur_loc[1] + 1)
    elif direction == Direction.SOUTH:
        # moves south
        new_loc = (cur_loc[0], cur_loc[1] - 1)
    elif direction == Direction.EAST:
        # moves east
        new_loc = (cur_loc[0] + 1, cur_loc[1])
    elif direction == Direction.WEST:
        # moves west
        new_loc = (cur_loc[0] - 1, cur_loc[1])
    else:
        raise ValueError(f"{direction} is not a valid direction")

    if new_loc not in visited_house_coordinates:
        visited_house_coordinates[new_loc] = 1
    else:
        visited_house_coordinates[new_loc] += 1

    return new_loc


# part 1
def houses_gifted_by_santa(navigation: Iterable[str]) -> int:
    visited_house_coordinates: Dict[Tuple[int, int], int] = {(0, 0): 1}

    # Moves through the map
    reduce(
        lambda cur_loc, direction: present_to_house(direction, cur_loc, visited_house_coordinates),
        navigation,
        (0, 0),
    )

    return len(visited_house_coordinates.keys())


def is_santas_turn(turn_number: int) -> bool:
    return turn_number % 2 == 0


# part 2
def houses_gifted_by_santa_and_robot(navigation: Iterable[str]) -> int:
    visited_house_coordinates: Dict[Tuple[int, int], int] = {(0, 0): 2}
    santa_cur_loc: Tuple[int, int] = (0, 0)
    robot_santa_cur_loc: Tuple[int, int] = (0, 0)

    turns: int = 0

    # Moves through the map
    for direction in navigation:
        if is_santas_turn(turns):
            santa_cur_loc = present_to_house(direction, santa_cur_loc, visited_house_coordinates)
        else:
            robot_santa_cur_loc = present_to_house(
                direction, robot_santa_cur_loc, visited_house_coordinates
            )
        turns += 1

    return len(visited_house_coordinates.keys())


def main(_: List[str]) -> None:
    """
        This is the entry point.
    """
    navigation: str = sys.stdin.read().strip()
    print(f"Houses with multiple gifts: {houses_gifted_by_santa(navigation)}")
    print(f"Houses with multiple gifts: {houses_gifted_by_santa_and_robot(navigation)}")


if __name__ == "__main__":
    main(sys.argv)
