import argparse
from pathlib import Path

import pytest

INPUT_TXT = Path(__file__).parent / "input.txt"


def is_bad_code(id_str: str) -> bool:
    if len(id_str) % 2 != 0:
        return False

    midpoint = len(id_str) // 2
    return id_str[:midpoint] == id_str[midpoint:]


def compute(puzzle_input: str) -> int:
    ids = [line.split("-") for line in puzzle_input.split(",")]

    bad_ids = [
        id_
        for id_pair in ids
        for id_ in range(int(id_pair[0]), int(id_pair[1]) + 1)
        if is_bad_code(str(id_))
    ]

    return sum(bad_ids)


TEST_INPUT = """\
11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124
"""


@pytest.mark.parametrize(
    ("input_s", "expected"),
    [
        (TEST_INPUT, 1227775554),
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
