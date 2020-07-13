import itertools
import re
import sys
from dataclasses import dataclass, field
from typing import ClassVar, Iterator, List, Tuple


def main(*_: str) -> None:
    players, marbles = parse_input(sys.stdin.readline())

    # part 1
    highest_score: int = get_highest_score(players, marbles)
    print(f"Highest score: {highest_score}")


def parse_input(game_input: str) -> Tuple[int, int]:
    players, marbles = tuple(map(int, re.findall(r"\d+", game_input)))
    print(f"Players: {players}, marbles: {marbles}")
    return (players, marbles)


def get_highest_score(players: int, marbles: int) -> int:
    player_scores: List[int] = [0] * players
    marble_game: MarbleGame = MarbleGame()
    players_turn = get_current_player(players)

    for marble_value in range(1, marbles + 1):
        current_player = next(players_turn)
        # print(f"Marble {marble_value} placed by player {current_player + 1}")
        score_obtained = marble_game.place_marble(marble_value)
        player_scores[current_player] += score_obtained

    return max(player_scores)


def get_current_player(players: int) -> Iterator[int]:
    yield from itertools.cycle(range(players))


@dataclass
class Marble:
    MAGIC_NUMBER: ClassVar[int] = 23  # pylint: disable=invalid-name

    value: int
    prev_pos: "Marble" = field(init=False)
    next_pos: "Marble" = field(init=False)

    def __post_init__(self) -> None:
        self.next_pos = self
        self.prev_pos = self

    def is_magic_marble(self) -> bool:
        return self.value % Marble.MAGIC_NUMBER == 0


# This is a circular doubly linked list
class MarbleGame:
    MAGIC_MARBLE_POSITION_SHIFT: ClassVar[int] = 7

    def __init__(self):
        self._current_marble = Marble(0)

    def place_marble(self, marble_value: int) -> int:
        """Places marble of given value in the game
        and returns the points accumulated

        Args:
            marble (int)

        Returns:
            int: Score by placing the marble in the game
        """
        marble = Marble(marble_value)
        return (
            self._handle_magic_marble(marble)
            if marble.is_magic_marble()
            else self._place_marble(marble)
        )

    def _handle_magic_marble(self, marble: Marble) -> int:
        score: int = marble.value

        # take the 7th marble in anticlockwise direction
        current_marble = self._current_marble
        for _ in range(MarbleGame.MAGIC_MARBLE_POSITION_SHIFT):
            current_marble = current_marble.prev_pos

        # print(f"Marble_to_remove: {current_marble.value}")
        score += current_marble.value
        self._remove_marble(current_marble)
        self._current_marble = current_marble.next_pos
        return score

    def _remove_marble(self, marble_to_remove: Marble) -> None:
        marble_to_remove.prev_pos.next_pos = marble_to_remove.next_pos
        marble_to_remove.next_pos.prev_pos = marble_to_remove.prev_pos

    def _place_marble(self, marble: Marble) -> int:
        # place the current marble between 1 and 2 of current marble
        one: Marble = self._current_marble.next_pos
        two: Marble = one.next_pos
        marble.prev_pos = one
        marble.next_pos = two
        one.next_pos = marble
        two.prev_pos = marble
        self._current_marble = marble

        return 0


if __name__ == "__main__":
    main(*sys.argv)
