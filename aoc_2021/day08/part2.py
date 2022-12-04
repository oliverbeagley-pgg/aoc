import argparse
import os
from textwrap import dedent

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


def compute(input: str) -> int:
    numbers = input.splitlines()

    total = 0
    for line in numbers:
        start, end = line.split(" | ")
        starts = ["".join(sorted(number)) for number in start.split()]
        ends = ["".join(sorted(number)) for number in end.split()]
        digits = {*starts, *ends}

        n_to_seg: dict[int, str] = {}

        (n_to_seg[1],) = (seg for seg in digits if len(seg) == 2)
        (n_to_seg[4],) = (seg for seg in digits if len(seg) == 4)
        (n_to_seg[7],) = (seg for seg in digits if len(seg) == 3)
        (n_to_seg[8],) = (seg for seg in digits if len(seg) == 7)

        s6 = {seg for seg in digits if len(seg) == 6}
        (n_to_seg[6],) = (seg for seg in s6 if len(set(seg) & set(n_to_seg[1])) == 1)
        (n_to_seg[9],) = (seg for seg in s6 if len(set(seg) & set(n_to_seg[4])) == 4)
        (n_to_seg[0],) = s6 - {n_to_seg[6], n_to_seg[9]}

        s5 = {seg for seg in digits if len(seg) == 5}
        (n_to_seg[3],) = (seg for seg in s5 if len(set(seg) & set(n_to_seg[1])) == 2)
        (n_to_seg[5],) = (seg for seg in s5 if len(set(seg) & set(n_to_seg[6])) == 5)
        (n_to_seg[2],) = s5 - {n_to_seg[3], n_to_seg[5]}

        seg_to_n = {v: str(k) for k, v in n_to_seg.items()}

        total += int("".join(seg_to_n[end] for end in ends))

    return total


# spell-checker: disable
TEST_INPUT = """
    be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
    edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
    fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
    fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
    aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
    fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
    dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
    bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
    egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
    gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
"""  # noqa: E501
# spell-checker: enable
TEST_INPUT = dedent(TEST_INPUT).strip()


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((TEST_INPUT, 61229),),
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
