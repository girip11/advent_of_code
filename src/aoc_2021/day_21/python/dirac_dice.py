import itertools
import sys
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Dict, Iterator, List, Tuple


@dataclass
class Player:
    id_: int
    pos: int
    score: int = field(default=0)

    def advance(self, moves: int) -> None:
        self.pos = ((self.pos + moves) % 10) or 10
        self.score += self.pos


class NSidedDice:
    def __init__(self, sides: int) -> None:
        self._dice_roller: Iterator[int] = itertools.cycle(range(1, sides + 1))

    def roll(self) -> int:
        return sum(next(self._dice_roller) for _ in range(3))


def play_for_win(players: List[Player], winning_score: int) -> Tuple[int, Player, Player]:
    turns: int = 0
    dice: NSidedDice = NSidedDice(100)
    winner: int

    for player in itertools.cycle(players):
        player.advance(dice.roll())
        turns += 1

        if player.score >= winning_score:
            winner = player.id_ - 1
            break

    return (turns, players[winner], players[winner - 1])


@dataclass
class Game:
    players: List[Player]
    current: int
    universes: int

    def update(self, moves: int, universes: int, winning_score: int) -> bool:
        self.players[self.current].advance(moves)
        self.universes *= universes
        current_player = self.current
        self.current = (self.current + 1) % 2
        return self.players[current_player].score >= winning_score

    def clone(self) -> "Game":
        return Game(deepcopy(self.players), self.current, self.universes)


DICE_SCORES_FREQUENCY: Dict[int, int] = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}


# Runs for long, not the best of solutions. But this is what I was able to come up with
def find_most_winning_player(players: List[Player], winning_score: int) -> Tuple[int, int]:
    plays: List[Game] = [Game(players, 0, 1)]
    wins: List[int] = [0] * len(players)

    while plays:
        game: Game = plays.pop()
        print(wins)
        # current player rolls the dice thrice
        # With each roll universe splits and hence 27 outcomes
        for score, universes in DICE_SCORES_FREQUENCY.items():
            cur_game = game.clone()
            if cur_game.update(score, universes, winning_score):
                wins[game.current] += cur_game.universes
            else:
                plays.append(cur_game)

    print(wins)
    return (max([0, 1], key=lambda i: wins[i]) + 1, max(wins))


def parse_input(lines: List[str]) -> List[Player]:
    return [Player(id_, int(line.split(":")[-1].strip())) for id_, line in enumerate(lines, 1)]


def main(*_: str) -> None:
    players: List[Player] = parse_input(sys.stdin.readlines())
    print(players)

    # part-1
    turns, winner, loser = play_for_win(deepcopy(players), 1000)
    print(turns, winner, loser)
    print(f"Part1 - {(turns * 3) * loser.score}")

    # part-2
    print(f"Part2 - {find_most_winning_player(players, 21)}")


if __name__ == "__main__":
    main(*sys.argv[1:])
