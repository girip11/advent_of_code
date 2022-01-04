import sys
from dataclasses import dataclass
from typing import Dict, List, Set, Tuple


@dataclass(init=False)
class BingoBoard:
    numbers: List[List[int]]
    _row_tracker: List[int]
    _column_tracker: List[int]
    _marked: Set[int]
    _num_pos: Dict[int, Tuple[int, int]]
    _recently_marked: int

    def __init__(self, numbers: List[List[int]]) -> None:
        self.numbers = numbers
        # print(numbers)
        self._num_pos = {}
        for rowno, row in enumerate(self.numbers):
            for colno, value in enumerate(row):
                # assume all numbers in a board will be unique
                self._num_pos[value] = (rowno, colno)

        self._row_tracker = [5] * 5
        self._column_tracker = [5] * 5
        self._marked = set()

    def mark(self, number: int) -> bool:
        # add count to row and column.
        if number not in self._num_pos:
            return False

        self._recently_marked = number
        self._marked.add(number)
        rowno, colno = self._num_pos[number]
        self._row_tracker[rowno] -= 1
        self._column_tracker[colno] -= 1

        return True

    def check_for_win(self) -> bool:
        rowno, colno = self._num_pos[self._recently_marked]
        return self._row_tracker[rowno] == 0 or self._column_tracker[colno] == 0

    def calculate_score(self) -> int:
        unmarked_sum: int = 0
        for num in self._num_pos.keys():
            if num not in self._marked:
                unmarked_sum += num

        print(unmarked_sum, self._recently_marked)
        return unmarked_sum * self._recently_marked


def compute_first_winning_board_score(numbers: List[int], boards: List[BingoBoard]) -> int:
    for number in numbers:
        for board in boards:
            if board.mark(number) and board.check_for_win():
                return board.calculate_score()

    return -1


def compute_last_winning_board_score(numbers: List[int], boards: List[BingoBoard]) -> int:
    for number in numbers:
        winning_boards = set()
        for idx, board in enumerate(boards):
            if board.mark(number) and board.check_for_win():
                if len(boards) > 1:
                    winning_boards.add(idx)
                else:
                    return board.calculate_score()

        # filter the winning boards for next number
        boards = [board for i, board in enumerate(boards) if i not in winning_boards]

    return -1


def parse_input(lines: List[str]) -> Tuple[List[int], List[List[List[int]]]]:
    random_bingo_numbers = [int(num) for num in lines[0].strip().split(",")]

    bingo_boards: List[List[List[int]]] = []
    board: List[List[int]] = []
    for line in lines[2:]:
        line = line.strip()
        if len(line) == 0:
            bingo_boards.append(board)
            board = []
        else:
            row: List[int] = [int(num) for num in line.split()]
            board.append(row)
    bingo_boards.append(board)

    return (random_bingo_numbers, bingo_boards)


def main(*_: str) -> None:
    random_bingo_numbers, boards = parse_input(sys.stdin.readlines())
    bingo_boards = [BingoBoard(board) for board in boards]
    # part-1
    print(compute_first_winning_board_score(random_bingo_numbers, bingo_boards))

    bingo_boards = [BingoBoard(board) for board in boards]
    # part-2
    print(compute_last_winning_board_score(random_bingo_numbers, bingo_boards))


if __name__ == "__main__":
    main(*sys.argv[1:])
