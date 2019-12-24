# Crossed Wires
# https://adventofcode.com/2019/day/3
from typing import Dict
from typing import List
from typing import Tuple

import pytest
from AOCProblem import AOCProblem

# General Approach
# For each wire, maintain a set of points that are in its path
# Take the intersection of the points for the 2 wires, and choose
# the point with the smallest Manhattan Distance from the origin
# that appears in both paths

Path = List[str]
Point = Tuple[int, int]


UNIT_VEC = {
    'U': (0, 1),
    'D': (0, -1),
    'R': (1, 0),
    'L': (-1, 0),
}


def add_points(p1: Point, p2: Point) -> Point:
    return (p1[0] + p2[0], p1[1] + p2[1])


class Wire:

    def __init__(self, path: Path):
        self.path = path
        self.points_to_steps: Dict[Point, int] = {}

    def trace_path(self) -> None:
        current = (0, 0)
        total_steps = 0
        for step in self.path:
            direction, amount = step[0], int(step[1:])
            step_vector = UNIT_VEC[direction]
            for _ in range(amount):
                total_steps += 1
                current = add_points(current, step_vector)
                if current not in self.points_to_steps:
                    self.points_to_steps[current] = total_steps


def parse_data_from_input(input_lines: List[str]) -> List[Wire]:
    if len(input_lines) != 2:
        raise Exception("Invalid input")
    return [Wire(line.strip().split(",")) for line in input_lines]


def manhattan(point: Point) -> int:
    return abs(point[0]) + abs(point[1])


class Day3(AOCProblem):

    def compute_1(self, input_lines: List[str]) -> int:
        wire1, wire2 = parse_data_from_input(input_lines)
        wire1.trace_path()
        wire2.trace_path()
        common_points = (
            wire1.points_to_steps.keys() & wire2.points_to_steps.keys()
        )
        return min(manhattan(point) for point in common_points)

    def compute_2(self, input_lines: List[str]) -> int:
        wire1, wire2 = parse_data_from_input(input_lines)
        wire1.trace_path()
        wire2.trace_path()
        common_points = (
            wire1.points_to_steps.keys() & wire2.points_to_steps.keys()
        )
        return min(
            wire1.points_to_steps[point] + wire2.points_to_steps[point]
            for point in common_points
        )


@pytest.mark.parametrize(
    ('input_lines', 'expected'),
    [
        (
            ['R75,D30,R83,U83,L12,D49,R71,U7,L72',
                'U62,R66,U55,R34,D71,R55,D58,R83'],
            159,
        ),
        (
            ['R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51',
             'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7'],
            135,
        ),
    ],
)
def test_1(input_lines: List[str], expected: int) -> None:
    assert Day3().compute_1(input_lines) == expected


@pytest.mark.parametrize(
    ('input_lines', 'expected'),
    [
        (
            ['R75,D30,R83,U83,L12,D49,R71,U7,L72',
                'U62,R66,U55,R34,D71,R55,D58,R83'],
            610,
        ),
        (
            ['R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51',
             'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7'],
            410,
        ),
    ],
)
def test_2(input_lines: List[str], expected: int) -> None:
    assert Day3().compute_2(input_lines) == expected


if __name__ == '__main__':
    exit(Day3().main())
