import argparse
import os
from textwrap import dedent

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")

moves = {
    "A": "rock",
    "B": "paper",
    "C": "scissors",
    "X": "rock",
    "Y": "paper",
    "Z": "scissors",
}
scores = {
    "rock": 1,
    "paper": 2,
    "scissors": 3,
}
wins = {
    "rock": "scissors",
    "paper": "rock",
    "scissors": "paper",
}


def compute(input: str) -> int:
    games = ([moves[move] for move in game.split()] for game in input.splitlines())
    n = 0
    for game in games:
        them, us = game
        n += scores[us]

        if them == us:
            n += 3
        elif wins[them] != us:
            n += 6
        else:
            pass

    return n


TEST_INPUT = """
    A Y
    B X
    C Z
"""
TEST_INPUT = dedent(TEST_INPUT).strip()


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((TEST_INPUT, 15),),
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
