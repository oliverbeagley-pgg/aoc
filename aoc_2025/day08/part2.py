import argparse
from dataclasses import dataclass
from itertools import combinations
from math import dist
from pathlib import Path
from typing import NamedTuple
from typing import Self

import pytest

INPUT_TXT = Path(__file__).parent / "input.txt"


class Point(NamedTuple):
    x: int
    y: int
    z: int

    def distance(self, other: Self) -> float:
        return dist(self, other)

    @classmethod
    def from_string(cls, s: str) -> Self:
        x, y, z = map(int, s.split(","))
        return cls(x, y, z)


@dataclass
class Circuit:
    junctions: set[Point]

    def merge(self, other: "Circuit") -> None:
        self.junctions |= other.junctions

    def contains_junction(self, junction: Point) -> bool:
        return junction in self.junctions


def compute(puzzle_input: str) -> int:
    junction_boxes = [Point.from_string(line) for line in puzzle_input.splitlines()]

    queue = sorted(
        combinations(junction_boxes, 2),
        reverse=True,
        key=lambda jb: jb[0].distance(jb[1]),
    )

    circuits = [Circuit({junction_box}) for junction_box in junction_boxes]
    while queue:
        box_1, box_2 = queue.pop()

        for circuit in circuits:
            if circuit.contains_junction(box_1):
                circuit_1 = circuit
            if circuit.contains_junction(box_2):
                circuit_2 = circuit

        if circuit_1 != circuit_2:
            circuit_1.merge(circuit_2)
            circuits.remove(circuit_2)

        if len(circuits) == 1:
            return box_1.x * box_2.x

    msg = "Could not connect all junction boxes"
    raise ValueError(msg)


TEST_INPUT = """\
162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689
"""


@pytest.mark.parametrize(
    ("input_s", "expected"),
    [
        (TEST_INPUT, 25272),
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
