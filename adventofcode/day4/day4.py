# Day 4
# https://adventofcode.com/2019/day/4
from typing import List

import pytest
from AOCProblem import AOCProblem

# Part 1

# Find the number of values within the specified range that satisfy the
# following criteria:

# 6-digit number
# Value is within range
# Two adjacent digits are the same (e.g. 122345)
# Digits are non-decreasing going left to right

# Part 2:
# Same As Part 1, with one additional detail:
# the two adjacent matching digits are not part of a larger group
# of matching digits.
# Thus there must be at least one string of exactly 2 consecutive digits


def is_valid(x: int) -> bool:
    if x < 100000 or x > 999999:
        return False
    digits = [ch for ch in str(x)]

    # Ensure adjacent values exist
    if not any([digits[i] == digits[i + 1] for i in range(0, len(digits) - 1)]):
        return False

    # Ensure no decreasing digits
    if any([digits[i] > digits[i + 1] for i in range(0, len(digits) - 1)]):
        return False

    return True


def is_valid_2(x: int) -> bool:
    if not is_valid(x):
        return False

    # Check for string of exactly 2 consecutive chars
    digits = [ch for ch in str(x)]
    for i in range(5):
        if (
            digits[i] == digits[i + 1]
            and (i == 0 or digits[i] != digits[i - 1])
            and (i == 4 or digits[i] != digits[i + 2])
        ):
            return True

    return False


class Day4(AOCProblem):
    def compute_1(self, input_lines: List[str]) -> int:
        start, end = [int(value) for value in input_lines[0].split("-")]
        return len([x for x in range(start, end + 1) if is_valid(x)])

    def compute_2(self, input_lines: List[str]) -> int:
        start, end = [int(value) for value in input_lines[0].split("-")]
        return len([x for x in range(start, end + 1) if is_valid_2(x)])


@pytest.mark.parametrize(
    ("num", "expected"), ([111111, True], [223450, False], [123789, False],),
)
def test_1(num: int, expected: bool) -> None:
    assert is_valid(num) == expected


@pytest.mark.parametrize(
    ("num", "expected"),
    ([112233, True], [123444, False], [111122, True], [788899, True],),
)
def test_2(num: int, expected: bool) -> None:
    assert is_valid_2(num) == expected


if __name__ == "__main__":
    exit(Day4().main())
