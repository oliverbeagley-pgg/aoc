import argparse
import os
from string import ascii_letters
from textwrap import dedent

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


priority = {letter: priority for priority, letter in enumerate(ascii_letters, 1)}


def compute(input: str) -> str:
    boxes, instructions = input.split("\n\n")

    last_line = boxes.splitlines()[-1]
    n_stacks = len(last_line.replace(" ", ""))
    stacks: list[list[str]] = [[] for _ in range(n_stacks)]

    for line in boxes.splitlines()[:-1]:
        for idx, val in enumerate(line[1::4]):
            if not val.isspace():
                stacks[idx].append(val)

    for stack in stacks:
        stack.reverse()

    for instruction in instructions.splitlines():
        _, n_boxes_s, _, target_s, _, destination_s = instruction.split()
        n_boxes, target, destination = int(n_boxes_s), int(target_s), int(destination_s)

        boxes_to_move = stacks[target - 1][-n_boxes:]
        del stacks[target - 1][-n_boxes:]
        stacks[destination - 1].extend(boxes_to_move)

    return "".join(stack[-1] for stack in stacks if len(stack) != 0)


TEST_INPUT = """
        [D]
    [N] [C]
    [Z] [M] [P]
     1   2   3

    move 1 from 2 to 1
    move 3 from 1 to 3
    move 2 from 2 to 1
    move 1 from 1 to 2
"""
TEST_INPUT = dedent(TEST_INPUT).rstrip()


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((TEST_INPUT, "MCD"),),
)
def test(input_s: str, expected: str) -> None:
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
