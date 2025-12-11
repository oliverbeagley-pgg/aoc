import argparse
from functools import cache
from functools import reduce
from itertools import pairwise
from itertools import permutations
from operator import mul
from pathlib import Path

import pytest

INPUT_TXT = Path(__file__).parent / "input.txt"


def compute(puzzle_input: str) -> int:
    graph = {
        root: child_s.split(" ")
        for root, child_s in (line.split(": ") for line in puzzle_input.splitlines())
    }

    @cache
    def dfs(node: str, dest: str) -> int:
        if node == dest:
            return 1

        return sum(dfs(child, dest) for child in graph.get(node, []))

    return sum(
        reduce(mul, (dfs(a, b) for a, b in pairwise(path)))
        for path in (["svr", *order, "out"] for order in permutations(["fft", "dac"]))
    )


TEST_INPUT = """\
svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out
"""


@pytest.mark.parametrize(
    ("input_s", "expected"),
    [
        (TEST_INPUT, 2),
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
