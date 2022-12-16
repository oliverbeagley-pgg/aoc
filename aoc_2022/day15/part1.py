from __future__ import annotations

import argparse
import os
import re
from textwrap import dedent
from typing import TypeAlias

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")

Point: TypeAlias = tuple[int, int]


def manhattan_distance(start: Point, end: Point) -> int:
    return abs(end[0] - start[0]) + abs(end[1] - start[1])


def sensor_info(line: str) -> tuple[Point, Point]:
    line_regex = re.compile(
        r"^Sensor at x=(?P<s_x>-?\d+), y=(?P<s_y>-?\d+): "
        r"closest beacon is at x=(?P<b_x>-?\d+), y=(?P<b_y>-?\d+)$"
    )

    matches = line_regex.match(line)
    assert matches is not None

    s_x, s_y, b_x, b_y = tuple(int(v) for v in matches.groupdict().values())

    return (s_x, s_y), (b_x, b_y)


def compute(input: str, y: int = 2_000_000) -> int:

    sensor_signals = [sensor_info(line) for line in input.splitlines()]

    beacons = set()
    empty_coords = set()

    for sensor, beacon in sensor_signals:
        beacons.add(beacon)

        dist = manhattan_distance(sensor, beacon)
        x_dist = dist - abs(y - sensor[1])

        for x in range(sensor[0] - x_dist, sensor[0] + x_dist + 1):
            empty_coords.add((x, y))

    return len(empty_coords - beacons)


TEST_INPUT = """
    Sensor at x=2, y=18: closest beacon is at x=-2, y=15
    Sensor at x=9, y=16: closest beacon is at x=10, y=16
    Sensor at x=13, y=2: closest beacon is at x=15, y=3
    Sensor at x=12, y=14: closest beacon is at x=10, y=16
    Sensor at x=10, y=20: closest beacon is at x=10, y=16
    Sensor at x=14, y=17: closest beacon is at x=10, y=16
    Sensor at x=8, y=7: closest beacon is at x=2, y=10
    Sensor at x=2, y=0: closest beacon is at x=2, y=10
    Sensor at x=0, y=11: closest beacon is at x=2, y=10
    Sensor at x=20, y=14: closest beacon is at x=25, y=17
    Sensor at x=17, y=20: closest beacon is at x=21, y=22
    Sensor at x=16, y=7: closest beacon is at x=15, y=3
    Sensor at x=14, y=3: closest beacon is at x=15, y=3
    Sensor at x=20, y=1: closest beacon is at x=15, y=3
"""
TEST_INPUT = dedent(TEST_INPUT).strip()


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((TEST_INPUT, 26),),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s, 10) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", nargs="?", default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(compute(f.read()))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
