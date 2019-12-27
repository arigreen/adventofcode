# Crossed Wires
# https://adventofcode.com/2019/day/3
from typing import Callable
from typing import Dict
from typing import List
from typing import NamedTuple
from typing import Optional
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
ScoringFunction = Callable[[Point, "Wire"], float]


UNIT_VEC = {
    "U": (0, 1),
    "D": (0, -1),
    "R": (1, 0),
    "L": (-1, 0),
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


def score_manhattan(point: Point, wire: Wire) -> float:
    return manhattan(point) / 2


def score_steps(point: Point, wire: Wire) -> float:
    return wire.points_to_steps[point]


def compute_generic(input_lines: List[str], scoring_fn: ScoringFunction,) -> int:
    wire1, wire2 = parse_data_from_input(input_lines)
    wire1.trace_path()
    wire2.trace_path()
    common_points = wire1.points_to_steps.keys() & wire2.points_to_steps.keys()
    return int(
        min(
            scoring_fn(point, wire1) + scoring_fn(point, wire2)
            for point in common_points
        )
    )


class Day3(AOCProblem):
    def compute_1(self, input_lines: List[str]) -> int:
        return compute_generic(input_lines, score_manhattan)

    def compute_2(self, input_lines: List[str]) -> int:
        return int(compute_generic(input_lines, score_steps))


@pytest.mark.parametrize(
    ("input_lines", "expected"),
    [
        (
            ["R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83"],
            159,
        ),
        (
            [
                "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51",
                "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7",
            ],
            135,
        ),
    ],
)
def test_1(input_lines: List[str], expected: int) -> None:
    assert Day3().compute_1(input_lines) == expected
    assert compute_1_vectorized(input_lines) == expected


@pytest.mark.parametrize(
    ("input_lines", "expected"),
    [
        (
            ["R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83"],
            610,
        ),
        (
            [
                "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51",
                "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7",
            ],
            410,
        ),
    ],
)
def test_2(input_lines: List[str], expected: int) -> None:
    assert Day3().compute_2(input_lines) == expected


# For vectorized intersection solution
class Vector(NamedTuple):
    start: Point
    direction: str
    length: int


def calculate_end(vec: Vector) -> Point:
    if vec.direction == "R":
        return (vec.start[0] + vec.length, vec.start[1])
    elif vec.direction == "L":
        return (vec.start[0] - vec.length, vec.start[1])
    elif vec.direction == "U":
        return (vec.start[0], vec.start[1] + vec.length)
    else:
        return (vec.start[0], vec.start[1] - vec.length)


def vectorize(wire: Wire) -> List[Vector]:
    """Convert a Wire to a List of Vectors."""
    vectors = []
    start = (0, 0)
    for step in wire.path:
        direction, length = step[0], int(step[1:])
        vec = Vector(start=start, direction=direction, length=length)
        vectors.append(vec)
        start = calculate_end(vec)
    return vectors


@pytest.mark.parametrize(
    ("input_line", "expected"),
    [("R75,D30", [Vector((0, 0), "R", 75), Vector((75, 0), "D", 30)],),],
)
def test_vectorize(input_line: str, expected: List[Vector]) -> None:
    wire = Wire(input_line.strip().split(","))
    assert vectorize(wire) == expected


def find_intersection(vec1: Vector, vec2: Vector) -> Optional[Point]:
    """
    Find the point that 2 vectors intersect.
    Assumes that vectors are not on the same line.
    """
    if vec1.direction in ("R", "L"):
        if vec2.direction in ("R", "L"):
            return None
        horiz, vert = vec1, vec2
    else:
        if vec2.direction in ("U", "D"):
            return None
        horiz, vert = vec2, vec1

    if vert.direction == "U":
        vert_start, vert_end = vert.start[1], vert.start[1] + vert.length
    else:
        vert_start, vert_end = vert.start[1] - vert.length, vert.start[1]

    if horiz.direction == "R":
        horiz_start, horiz_end = horiz.start[0], horiz.start[0] + horiz.length
    else:
        horiz_start, horiz_end = horiz.start[0] - horiz.length, horiz.start[0]

    x = vert.start[0]
    y = horiz.start[1]
    if x == 0 and y == 0:
        return None
    if vert_start <= y <= vert_end and horiz_start <= x <= horiz_end:
        return (x, y)
    else:
        return None


def compute_1_vectorized(input_lines: List[str]) -> int:
    wire1, wire2 = parse_data_from_input(input_lines)
    vec_1 = vectorize(wire1)
    vec_2 = vectorize(wire2)
    intersections = filter(
        None, [find_intersection(v1, v2) for v1 in vec_1 for v2 in vec_2]
    )
    return min(manhattan(point) for point in intersections)


if __name__ == "__main__":
    day3 = Day3()
    day3.add_alternate_1("vectorized", compute_1_vectorized)
    exit(day3.main())
