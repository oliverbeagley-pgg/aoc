import argparse
import os
from collections import deque
from textwrap import dedent

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def compute(input: str) -> int:
    queue: deque[str] = deque(maxlen=4)
    for idx, val in enumerate(input.strip(), 1):
        queue.append(val)

        if len(set(queue)) == queue.maxlen:
            return idx

    raise AssertionError("Should not run")


TEST_INPUT = """
    mjqjpqmgbljsphdztnvjfqwrcgsmlb
"""
TEST_INPUT = dedent(TEST_INPUT).strip()


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((TEST_INPUT, 7),),
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
