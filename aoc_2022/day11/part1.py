from __future__ import annotations

import argparse
import math
import os
from collections.abc import Callable
from functools import partial
from textwrap import dedent
from typing import NamedTuple

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


class Monkey(NamedTuple):
    items: list[int]
    operation: Callable[[int], int]
    test: int
    true_target: int
    false_target: int


def add(old: int, value: int) -> int:
    return old + value


def multiply(old: int, value: int) -> int:
    return old * value


def square(old: int) -> int:
    return old * old


def compute(input: str) -> int:
    monkeys: list[Monkey] = []
    for monkey_s in input.split("\n\n"):
        (
            _,
            starting_s,
            operation_s,
            test_s,
            true_target_s,
            false_target_s,
        ) = monkey_s.splitlines()

        starting = [int(s) for s in starting_s.split(": ")[1].split(", ")]

        if "old * old" in operation_s:
            operation = square
        elif "+" in operation_s:
            operation = partial(add, value=int(operation_s.split()[-1]))
        else:
            operation = partial(multiply, value=int(operation_s.split()[-1]))

        test = int(test_s.split()[-1])

        true = int(true_target_s.split()[-1])
        false = int(false_target_s.split()[-1])

        monkeys.append(Monkey(starting, operation, test, true, false))

    seen = [0] * len(monkeys)
    for _ in range(20):
        for idx, monkey in enumerate(monkeys):
            for item in monkey.items:
                seen[idx] += 1

                item = monkey.operation(item) // 3
                if item % monkey.test == 0:
                    monkeys[monkey.true_target].items.append(item)
                else:
                    monkeys[monkey.false_target].items.append(item)

            monkey.items.clear()

    seen.sort()

    return math.prod(seen[-2:])


TEST_INPUT = """
    Monkey 0:
    Starting items: 79, 98
    Operation: new = old * 19
    Test: divisible by 23
        If true: throw to monkey 2
        If false: throw to monkey 3

    Monkey 1:
    Starting items: 54, 65, 75, 74
    Operation: new = old + 6
    Test: divisible by 19
        If true: throw to monkey 2
        If false: throw to monkey 0

    Monkey 2:
    Starting items: 79, 60, 97
    Operation: new = old * old
    Test: divisible by 13
        If true: throw to monkey 1
        If false: throw to monkey 3

    Monkey 3:
    Starting items: 74
    Operation: new = old + 3
    Test: divisible by 17
        If true: throw to monkey 0
        If false: throw to monkey 1
"""
TEST_INPUT = dedent(TEST_INPUT).strip()


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((TEST_INPUT, 10605),),
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
