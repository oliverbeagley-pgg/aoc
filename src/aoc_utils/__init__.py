import argparse
import os
import re

import requests

HERE = os.path.dirname(os.path.abspath(__file__))


def _get_cookies() -> dict[str, str]:
    with open(os.path.join(HERE, "../../.env")) as f:
        return {"Cookie": f.read().strip()}


def get_input(year: int, day: int) -> str:
    url = f"https://adventofcode.com/{year}/day/{day}/input"
    request = requests.get(url, headers=_get_cookies())

    return request.content.decode()


def get_year_day() -> tuple[int, int]:
    cwd = os.getcwd()

    day = os.path.basename(cwd)
    year = os.path.basename(os.path.dirname(cwd))

    day_prefix = "day"
    aoc_prefix = "aoc_"

    if not day.startswith(day_prefix) or not year.startswith(aoc_prefix):
        raise AssertionError(f"unexpected working dir: {cwd}")

    return int(year[len(aoc_prefix) :]), int(day[len(day_prefix) :])


def download_input() -> int:
    parser = argparse.ArgumentParser()
    parser.parse_args()

    input = get_input(*get_year_day())

    with open("input.txt", "w") as f:
        f.write(input)

    lines = input.splitlines()
    if len(lines) > 10:
        for line in lines[:10]:
            print(line)
    else:
        print(lines[0][:80])

    print("...")

    raise SystemExit(0)


def send_answer(year: int, day: int, part: int, answer: int) -> str:
    url = f"https://adventofcode.com/{year}/day/{day}/answer"
    payload = {"level": part, "answer": answer}

    response = requests.post(url=url, headers=_get_cookies(), data=payload)

    return response.content.decode()


WRONG = re.compile(r"That's not the right answer.*?\.")
RIGHT = "That's the right answer!"
ALREADY_DONE = re.compile(r"You don't seem to be solving.*\?")
TOO_RECENT = re.compile(r"You gave an answer too recently.*left to wait\.")


def submit_solution() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--part", type=int, required=True)
    parser.add_argument("answer", nargs="?", type=int, default=0)

    args = parser.parse_args()

    year, day = get_year_day()
    contents = send_answer(year, day, args.part, args.answer)

    if RIGHT in contents:
        print(RIGHT)
        raise SystemExit(0)

    for error in (WRONG, ALREADY_DONE, TOO_RECENT):

        match = error.search(contents)
        if match:
            print(match[0])
            raise SystemExit(1)

    print("Unhandled response")
    print(contents)
    raise SystemExit(1)


def parse_numbers(s: str) -> list[int]:
    return [int(x) for x in s.split()]


def parse_number_comma(s: str) -> list[int]:
    return [int(x) for x in s.split(",")]
