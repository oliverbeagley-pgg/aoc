import argparse
from collections import defaultdict
from functools import partial
from functools import total_ordering
from pathlib import Path

import pytest

import aoc_utils

INPUT_TXT = Path(__file__).parent / "input.txt"


def check_update(update: list[str], rules: dict[str, set[str]]) -> bool:
    return all(
        update[after_page_idx] in rules[page]
        for idx, page in enumerate(update)
        for after_page_idx in range(idx + 1, len(update))
    )


@total_ordering
class PageSortKey:
    def __init__(self, page: str, rule_set: dict[str, set[str]]) -> None:
        self.page = page
        self.rule_set = rule_set

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PageSortKey):
            return NotImplemented
        return False

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, PageSortKey):
            return NotImplemented
        return other.page in self.rule_set[self.page]


def compute(puzzle_input: str) -> int:
    rules_, updates_ = puzzle_input.split("\n\n")
    rules = (s.split("|") for s in rules_.splitlines())
    updates = (s.split(",") for s in updates_.splitlines())

    rule_set = defaultdict(set)
    for before, after in rules:
        rule_set[before].add(after)

    return sum(
        int(
            sorted(update, key=partial(PageSortKey, rule_set=rule_set))[
                len(update) // 2
            ]
        )
        for update in updates
        if not check_update(update, rule_set)
    )


TEST_INPUT = """\
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""


@pytest.mark.parametrize(
    ("input_s", "expected"),
    [
        (TEST_INPUT, 123),
    ],
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", nargs="?", default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, aoc_utils.timing():
        print(compute(f.read()))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
