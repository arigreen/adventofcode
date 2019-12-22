import argparse

import pytest
from support import timing


def calc_fuel_requirement(mass: int) -> int:
    return max(0, mass // 3 - 2)


def compute(s: str) -> int:
    masses = [int(line) for line in s.splitlines()]
    fuel_requirements = [calc_fuel_requirement(mass) for mass in masses]
    return sum(fuel_requirements)


@pytest.mark.parametrize(
    ('input', 'expected'),
    (
        ['12', 2],
        ['14', 2],
        ['1969', 654],
        ['100756', 33583],
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
