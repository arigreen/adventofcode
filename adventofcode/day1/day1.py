from typing import List

import pytest
from AOCProblem import AOCProblem


def calc_fuel_requirement(mass: int) -> int:
    return max(0, mass // 3 - 2)


def calc_fuel_requirement_repeatedly(mass: int) -> int:
    result = 0
    while mass > 0:
        fuel = calc_fuel_requirement(mass)
        result += fuel
        mass = fuel
    return result


@pytest.mark.parametrize(
    ("input", "expected"), (["12", 2], ["14", 2], ["1969", 654], ["100756", 33583],),
)
def test_1(input: str, expected: int) -> None:
    assert Day1().compute_1([input]) == expected


@pytest.mark.parametrize(
    ("input", "expected"), (["14", 2], ["1969", 966], ["100756", 50346],),
)
def test_2(input: str, expected: int) -> None:
    assert Day1().compute_2([input]) == expected


class Day1(AOCProblem):
    def compute_1(self, input_lines: List[str]) -> int:
        masses = [int(line) for line in input_lines]
        fuel_requirements = [calc_fuel_requirement(mass) for mass in masses]
        return sum(fuel_requirements)

    def compute_2(self, input_lines: List[str]) -> int:
        masses = [int(line) for line in input_lines]
        fuel_requirements = [calc_fuel_requirement_repeatedly(mass) for mass in masses]
        return sum(fuel_requirements)


if __name__ == "__main__":
    exit(Day1().main())
