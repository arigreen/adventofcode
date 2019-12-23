# Crossed Wires
# https://adventofcode.com/2019/day/3
import argparse
from typing import List
from typing import Set
from typing import Tuple

import pytest
from support import timing

# General Approach
# For each wire, maintain a set of points that are in its path
# Take the intersection of the points for the 2 wires, and choose
# the point with the smallest Manhattan Distance from the origin
# that appears in both paths

Path = List[str]
Point = Tuple[int, int]


class Wire:

    def __init__(self, path: Path):
        self.path = path
        self.points: Set[Point] = set()

    def trace_path(self) -> None:
        current = (0, 0)
        for step in self.path:
            dir = step[0]
            amount = int(step[1:])
            if dir == 'U':
                for x in range(amount):
                    current = (current[0], current[1]+1)
                    self.points.add(current)
            elif dir == 'D':
                for x in range(amount):
                    current = (current[0], current[1]-1)
                    self.points.add(current)
            elif dir == 'L':
                for x in range(amount):
                    current = (current[0]-1, current[1])
                    self.points.add(current)
            elif dir == 'R':
                for x in range(amount):
                    current = (current[0]+1, current[1])
                    self.points.add(current)


def parse_data_from_input(input_s: str) -> List[Wire]:
    lines = input_s.splitlines()
    if len(lines) != 2:
        raise Exception("Invalid input")
    return [Wire(line.strip().split(",")) for line in lines]


def manhattan(point: Point) -> int:
    return abs(point[0]) + abs(point[1])


def solve_part_1(wire1: Wire, wire2: Wire) -> int:
    wire1.trace_path()
    wire2.trace_path()
    common_points = wire1.points & wire2.points
    return min(manhattan(point) for point in common_points)


def solve_part_2() -> str:
    return '-1'


def compute_1(s: str) -> int:
    wires = parse_data_from_input(s)
    if len(wires) != 2:
        raise Exception("Unexpected input")
    wire1, wire2 = wires
    wire1.trace_path()
    wire2.trace_path()
    common_points = wire1.points & wire2.points
    return min(manhattan(point) for point in common_points)


def compute_2(s: str) -> int:
    # TODO: Implement solution here!
    return 0


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    [
        (
            'R75,D30,R83,U83,L12,D49,R71,U7,L72\n'
            'U62,R66,U55,R34,D71,R55,D58,R83',
            159,
        ),
        (
            'R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51\n'
            'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7',
            135,
        ),
    ],
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
