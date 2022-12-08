from __future__ import annotations

import argparse
import os
from functools import cached_property
from textwrap import dedent
from typing import NamedTuple

import pytest

INPUT_TXT = os.path.join(os.path.dirname(__file__), "input.txt")


class Directory:
    def __init__(self, name: str, parent: Directory | None) -> None:
        self.name = name
        self.parent = parent
        self.children: dict[str, Directory] = {}
        self.files: list[File] = []

    def mkdir(self, name: str) -> None:
        self.children[name] = Directory(name=name, parent=self)

    def cd(self, name: str) -> Directory:
        if name == "..":
            assert self.parent is not None
            pwd = self.parent
        else:
            pwd = self.children[name]

        return pwd

    def touch(self, name: str, size: int) -> None:
        self.files.append(File(name, size))

    @cached_property
    def size(self) -> int:
        file_sizes = sum(file.size for file in self.files)
        directory_sizes = sum(directory.size for directory in self.children.values())

        return file_sizes + directory_sizes


class File(NamedTuple):
    name: str
    size: int


def parse_stdin(stdin: list[str]) -> Directory:
    root_directory = Directory("/", parent=None)
    pwd = root_directory

    for line in stdin:
        if line.startswith("$"):
            _, *cmd = line.split()

            if cmd[0] == "cd":
                pwd = root_directory if cmd[1] == "/" else pwd.cd(cmd[1])
            else:
                continue

        else:
            start, end = line.split()
            if start == "dir":
                pwd.mkdir(end)
            else:
                pwd.touch(end, int(start))

    return root_directory


def walk(directory: Directory, accumulator: list[File]) -> None:
    accumulator.append(File(directory.name, directory.size))

    for dir in directory.children.values():
        walk(dir, accumulator)


def compute(input: str) -> int:
    root_directory = parse_stdin(input.splitlines())

    file_info: list[File] = []
    walk(root_directory, file_info)

    return sum(file.size for file in file_info if file.size <= 100000)


TEST_INPUT = """
    $ cd /
    $ ls
    dir a
    14848514 b.txt
    8504156 c.dat
    dir d
    $ cd a
    $ ls
    dir e
    29116 f
    2557 g
    62596 h.lst
    $ cd e
    $ ls
    584 i
    $ cd ..
    $ cd ..
    $ cd d
    $ ls
    4060174 j
    8033020 d.log
    5626152 d.ext
    7214296 k
"""
TEST_INPUT = dedent(TEST_INPUT).strip()


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((TEST_INPUT, 95437),),
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
