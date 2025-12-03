import argparse
from pathlib import Path

import pytest

INPUT_TXT = Path(__file__).parent / "input.txt"


def argmax(bank: str) -> int:
    return max(range(len(bank)), key=bank.__getitem__)


def best_jolt(bank: str) -> int:
    largest_first_battery_idx = argmax(bank[:-1])

    largest_first_battery = bank[largest_first_battery_idx]
    largest_second_battery = max(bank[largest_first_battery_idx + 1 :])

    return int(f"{largest_first_battery}{largest_second_battery}")


def compute(puzzle_input: str) -> int:
    banks = puzzle_input.splitlines()

    return sum(best_jolt(bank) for bank in banks)


TEST_INPUT = """\
987654321111111
811111111111119
234234234234278
818181911112111
"""


@pytest.mark.parametrize(
    ("input_s", "expected"),
    [
        (TEST_INPUT, 357),
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
