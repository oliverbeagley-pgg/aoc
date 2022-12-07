from __future__ import annotations

import argparse
import os
from dataclasses import dataclass
from textwrap import dedent

import pytest

import aoc_utils

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


@dataclass
class BingoBoard:
    board: list[int]
    remaining: set[int]

    def score(self, last_number: int) -> int:
        return sum(self.remaining) * last_number

    @property
    def is_solved(self) -> bool:
        for i in range(5):
            for j in range(5):
                if self.board[i + j * 5] in self.remaining:
                    break
            else:
                return True

            for j in range(5):
                if self.board[i * 5 + j] in self.remaining:
                    break
            else:
                return True
        else:
            return False

    @classmethod
    def parse(cls, input: str) -> BingoBoard:
        board = aoc_utils.parse_numbers(input)
        return cls(board, set(board))


def compute(input: str) -> int:
    numbers, *boards = input.split("\n\n")

    number_generator = (int(s) for s in numbers.split(","))
    parsed_boards = [BingoBoard.parse(board) for board in boards]

    for number in number_generator:
        for board in parsed_boards:
            board.remaining.discard(number)
            if board.is_solved:
                return board.score(number)

    raise AssertionError


TEST_INPUT = """
    7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

    22 13 17 11  0
     8  2 23  4 24
    21  9 14 16  7
     6 10  3 18  5
     1 12 20 15 19

     3 15  0  2 22
     9 18 13 17  5
    19  8  7 25 23
    20 11 10 24  4
    14 21 16 12  6

    14 21 17 24  4
    10 16 15  9 19
    18  8 23 26 20
    22 11 13  6  5
     2  0 12  3  7
"""
TEST_INPUT = dedent(TEST_INPUT).strip()


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((TEST_INPUT, 4512),),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", nargs="?", default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(compute(f.read()))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
