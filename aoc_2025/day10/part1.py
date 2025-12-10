import argparse
from collections.abc import Generator
from functools import reduce
from itertools import chain
from itertools import combinations
from operator import xor
from pathlib import Path

import pytest

INPUT_TXT = Path(__file__).parent / "input.txt"


def parse_line(line: str) -> tuple[int, list[int], list[int]]:
    _lights, rest = line.split(" ", 1)
    _buttons, _joltage = rest.rsplit(" ", 1)

    lights = sum(
        1 << idx for idx, char in enumerate(_lights.strip("[]")) if char == "#"
    )
    buttons = [
        sum(1 << int(num) for num in button.strip("()").split(","))
        for button in _buttons.split(" ")
    ]
    joltage = [int(num) for num in _joltage.strip("{}").split(",")]

    return lights, buttons, joltage


def bfs_buttons(buttons: list[int]) -> Generator[list[int]]:
    yield from chain.from_iterable(
        combinations(buttons, num) for num in range(1, len(buttons) + 1)
    )


def compute(puzzle_input: str) -> int:
    manuals = (
        (lights, buttons)
        for lights, buttons, _ in (
            parse_line(line) for line in puzzle_input.splitlines()
        )
    )

    return sum(
        next(
            len(button_combination)
            for button_combination in bfs_buttons(buttons)
            if reduce(xor, button_combination) == lights
        )
        for lights, buttons in manuals
    )


TEST_INPUT = """\
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
"""


@pytest.mark.parametrize(
    ("input_s", "expected"),
    [
        (TEST_INPUT, 7),
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
