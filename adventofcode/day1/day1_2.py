# Sum Fuel requirements
# https://adventofcode.com/2019/day/1
import argparse

import pytest
from support import timing


def calc_fuel_requirement_recursively(mass: int) -> int:
    result = 0
    while mass > 0:
        fuel = calc_fuel_requirement(mass)
        result += fuel
        mass = fuel
    return result


def calc_fuel_requirement(mass: int) -> int:
    return max(0, mass // 3 - 2)


def compute(s: str) -> int:
    masses = [int(line) for line in s.splitlines()]
    fuel_requirements = [
        calc_fuel_requirement_recursively(mass) for mass in masses]
    return sum(fuel_requirements)


@pytest.mark.parametrize(
    ('input', 'expected'),
    (
        ['14', 2],
        ['1969', 966],
        ['100756', 50346],
    ),
)
def test(input: str, expected: int) -> None:
    assert compute(input) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file')
    args = parser.parse_args()

    with open(args.data_file) as f, timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    exit(main())
