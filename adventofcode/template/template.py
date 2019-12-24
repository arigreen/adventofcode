from typing import List

import pytest
from AOCProblem import AOCProblem


class DAY_CLASS(AOCProblem):

    def compute_1(self, input_lines: List[str]) -> int:
        # TODO: Implement solution here!
        return 0

    def compute_2(self, input_lines: List[str]) -> int:
        # TODO: Implement solution here!
        return 0


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        # put given test cases here
    ),
)
def test_1(input_s: str, expected: int) -> None:
    assert DAY_CLASS().compute_1([input_s]) == expected


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        # put given test cases here
    ),
)
def test_2(input_s: str, expected: int) -> None:
    assert DAY_CLASS().compute_1([input_s]) == expected


if __name__ == '__main__':
    exit(DAY_CLASS().main())
