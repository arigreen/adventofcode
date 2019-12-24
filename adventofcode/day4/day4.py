# Day 4
# https://adventofcode.com/2019/day/4
from typing import List

import pytest
from AOCProblem import AOCProblem

# Find the number of values within the specified range that satisfy the
# following criteria:

# 6-digit number
# Value is within range
# Two adjacent digits are the same (e.g. 122345)
# Digits are non-decreasing going left to right


def is_valid(x: int):
    if x < 100000 or x > 999999:
        return False
    digits = [ch for ch in str(x)]

    # Ensure adjacent values exist
    if not any([
        digits[i] == digits[i + 1]
        for i in range(0, len(digits)-1)
    ]):
        return False

    # Ensure no decreasing digits
    if any([
        digits[i] > digits[i + 1]
        for i in range(0, len(digits)-1)
    ]):
        return False

    return True


class Day4(AOCProblem):

    def compute_1(self, input_lines: List[str]) -> int:
        start, end = [int(value) for value in input_lines[0].split("-")]
        return len([x for x in range(start, end + 1) if is_valid(x)])

    def compute_2(self, input_lines: List[str]) -> int:
        # TODO: Implement solution here!
        return 0


@pytest.mark.parametrize(
    ('num', 'expected'),
    (
        [111111, True],
        [223450, False],
        [123789, False],
    ),
)
def test_1(num: int, expected: bool) -> None:
    assert is_valid(num) == expected


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        # put given test cases here
    ),
)
def test_2(input_s: str, expected: int) -> None:
    assert Day4().compute_1([input_s]) == expected


if __name__ == '__main__':
    exit(Day4().main())
