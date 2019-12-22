import argparse

import pytest
from support import timing


def compute_1(s: str) -> int:
    # TODO: Implement solution here!
    return 0


def compute_2(s: str) -> int:
    # TODO: Implement solution here!
    return 0


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        # put given test cases here
    ),
)
def test_1(input_s: str, expected: int) -> None:
    assert compute_1(input_s) == expected


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        # put given test cases here
    ),
)
def test_2(input_s: str, expected: int) -> None:
    assert compute_2(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file')
    args = parser.parse_args()

    with open(args.data_file) as f, timing():
        print(f'Part 1: {compute_1(f.read())}')

    with open(args.data_file) as f, timing():
        print(f'Part 2: {compute_2(f.read())}')

    return 0


if __name__ == '__main__':
    exit(main())
