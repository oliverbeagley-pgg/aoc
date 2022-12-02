import argparse
import os
from textwrap import dedent

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def compute(input: str) -> int:
    plan = input.splitlines()

    horiztonal = 0
    depth = 0
    aim = 0
    for command in plan:
        direction, number_s = command.split()
        number = int(number_s)

        match direction:
            case "forward":
                horiztonal += number
                depth += aim * number
            case "down":
                aim += number
            case "up":
                aim -= number

    return horiztonal * depth


TEST_INPUT = """
    forward 5
    down 5
    forward 8
    up 3
    down 8
    forward 2
"""
TEST_INPUT = dedent(TEST_INPUT).strip()


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((TEST_INPUT, 900),),
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
