import argparse
from pathlib import Path

import numpy as np
import pytest
from scipy.optimize import linprog

INPUT_TXT = Path(__file__).parent / "input.txt"


def parse_line(line: str) -> tuple[int, list[list[int]], list[int]]:
    _lights, *_buttons, _joltage = line.split(" ")

    lights = sum(
        1 << idx for idx, char in enumerate(_lights.strip("[]")) if char == "#"
    )
    buttons = [
        [int(num) for num in button.strip("()").split(",")] for button in _buttons
    ]
    joltage = [int(num) for num in _joltage.strip("{}").split(",")]

    return lights, buttons, joltage


def solve(buttons: list[list[int]], joltage: list[int]) -> int:
    A = np.zeros(shape=(len(joltage), len(buttons)))  # noqa: N806
    for j, button in enumerate(buttons):
        for i in button:
            A[i, j] = 1

    b = joltage
    c = [1] * len(buttons)

    return int(linprog(c=c, A_eq=A, b_eq=b, integrality=1).fun)


def compute(puzzle_input: str) -> int:
    manuals = (
        (buttons, joltage)
        for _, buttons, joltage in (
            parse_line(line) for line in puzzle_input.splitlines()
        )
    )

    return sum(solve(buttons, joltage) for buttons, joltage in manuals)


TEST_INPUT = """\
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
"""


@pytest.mark.parametrize(
    ("input_s", "expected"),
    [
        (TEST_INPUT, 33),
    ],
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
