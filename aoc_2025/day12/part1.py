import argparse
from pathlib import Path

import pytest

INPUT_TXT = Path(__file__).parent / "input.txt"


def parse_region(region: str) -> tuple[int, list[int]]:
    dimensions_, requirements_ = region.split(": ")
    width, height = (int(num) for num in dimensions_.split("x"))
    requirements = [int(num) for num in requirements_.split(" ")]

    return (width * height), requirements


def has_enough_space(
    region: tuple[int, list[int]],
    areas: list[int],
    dead_space_factor: float = 1.0,
) -> bool:
    region_area, reqs = region

    shape_area = sum(req * area for req, area in zip(reqs, areas, strict=True))

    return shape_area * dead_space_factor <= region_area


def compute(puzzle_input: str) -> int:
    shapes_ = puzzle_input.split("\n\n")

    regions = (parse_region(line) for line in shapes_.pop().splitlines())
    areas = [shape.count("#") for shape in shapes_]

    dead_space_factor = 1.2
    return sum(has_enough_space(region, areas, dead_space_factor) for region in regions)


TEST_INPUT = """\
0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2
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
