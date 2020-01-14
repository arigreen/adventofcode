import textwrap
from collections import Counter
from typing import List

import pytest
from AOCProblem import AOCProblem


class Day8(AOCProblem):
    def compute_1(self, input_lines: List[str]) -> int:
        return solve_part_1(input_lines[0], 25, 6)

    def compute_2(self, input_lines: List[str]) -> int:
        # TODO: Implement solution here!
        return 0


def solve_part_1(image: str, width: int, height: int) -> int:
    layer_length = width * height
    if layer_length <= 0:
        raise ValueError("Invalid width and height")
    if len(image) % layer_length > 0:
        raise ValueError("Image is wrong size")
    layers = textwrap.wrap(image, layer_length)

    num_zeros_layers = [(Counter(layer)["0"], layer) for layer in layers]
    min_layer = min(num_zeros_layers)[1]
    c = Counter(min_layer)
    return c["1"] * c["2"]


@pytest.mark.parametrize(
    ("input_s", "width", "height", "expected"),
    (
        ("123456789012", 3, 2, 1),
        ("123451789012", 3, 2, 2),
        ("111111789012", 3, 2, 0),
        ("111222789012", 3, 2, 9),
    ),
)
def test_1(input_s: str, width: int, height: int, expected: int) -> None:
    assert solve_part_1(input_s, width, height) == expected


@pytest.mark.parametrize(
    ("input_s", "expected"),
    (
        # put given test cases here
    ),
)
def test_2(input_s: str, expected: int) -> None:
    assert Day8().compute_1([input_s]) == expected


if __name__ == "__main__":
    exit(Day8().main())
