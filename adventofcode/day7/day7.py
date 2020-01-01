import copy
import itertools
from typing import List

import pytest
from AOCProblem import AOCProblem
from int_code import IntCode


@pytest.mark.parametrize(
    ("data", "expected"),
    (
        (
            #
            # 15 <- phase_ordering
            # 16 <- last_output
            # MULTIPLY last_output * 10 and store in 16
            # ADD to phase_ordering and store in 15
            #
            [3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0],
            43210,
        ),
        (
            [
                3,
                23,
                3,
                24,
                1002,
                24,
                10,
                24,
                1002,
                23,
                -1,
                23,
                101,
                5,
                23,
                23,
                1,
                24,
                23,
                23,
                4,
                23,
                99,
                0,
                0,
            ],
            54321,
        ),
        (
            [
                3,
                31,
                3,
                32,
                1002,
                32,
                10,
                32,
                1001,
                31,
                -2,
                31,
                1007,
                31,
                0,
                33,
                1002,
                33,
                7,
                33,
                1,
                33,
                31,
                31,
                1,
                32,
                31,
                31,
                4,
                31,
                99,
                0,
                0,
                0,
            ],
            65210,
        ),
    ),
)
def test_1(data: List[int], expected: int) -> None:
    assert solve_1(data) == expected


@pytest.mark.parametrize(
    ("data", "expected"),
    (
        #
        # 15 <- phase_ordering
        # 16 <- last_output
        # MULTIPLY last_output * 10 and store in 16
        # ADD to phase_ordering and store in 15
        #
        (
            [
                3,
                26,
                1001,
                26,
                -4,
                26,
                3,
                27,
                1002,
                27,
                2,
                27,
                1,
                27,
                26,
                27,
                4,
                27,
                1001,
                28,
                -1,
                28,
                1005,
                28,
                6,
                99,
                0,
                0,
                5,
            ],
            139629729,
        ),
    ),
)
def test_2(data: List[int], expected: int) -> None:
    assert solve_2(data) == expected


@pytest.mark.parametrize(
    ("input_s", "expected"),
    (
        ("1002,4,3,4,33", [1002, 4, 3, 4, 99]),
        ("1101,100,-1,4,0", [1101, 100, -1, 4, 99]),
    ),
)
def test_full(input_s: str, expected: List[int]) -> None:
    program = IntCode.parse_from_input(input_s)
    program.execute()
    assert program.data == expected


def run_program_repeatedly(program: IntCode, ordering: List[int]) -> int:
    last_output = 0
    # create 5 programs
    for x in ordering:
        program.restore()
        program.set_input(x)
        program.set_input(last_output)
        program.execute()
        last_output = program.outputs[-1]
        program.restore()
    return last_output


def solve_1(data: List[int]) -> int:
    program = IntCode(data)
    return max(
        run_program_repeatedly(program, list(ordering))
        for ordering in itertools.permutations(range(5))
    )


def run_program_repeatedly_2(program: IntCode, ordering: List[int]) -> int:
    program.restore()

    # create 5 programs
    prog1 = program
    prog2 = copy.deepcopy(program)
    prog3 = copy.deepcopy(program)
    prog4 = copy.deepcopy(program)
    prog5 = copy.deepcopy(program)
    all_programs = [prog1, prog2, prog3, prog4, prog5]
    prog1.set_input(ordering[0])
    prog2.set_input(ordering[1])
    prog3.set_input(ordering[2])
    prog4.set_input(ordering[3])
    prog5.set_input(ordering[4])
    prog1.set_input(0)

    while True:
        if all(prog.finished for prog in all_programs):
            break
        prog1.execute()

        prog2.set_input(prog1.outputs[-1])
        prog2.execute()

        prog3.set_input(prog2.outputs[-1])
        prog3.execute()
        prog4.set_input(prog3.outputs[-1])
        prog4.execute()
        prog5.set_input(prog4.outputs[-1])
        prog5.execute()
        prog1.set_input(prog5.outputs[-1])

    return prog5.outputs[-1]


def solve_2(data: List[int]) -> int:
    program = IntCode(data)
    return max(
        run_program_repeatedly_2(program, list(ordering))
        for ordering in itertools.permutations(range(5, 10))
    )


class Day7(AOCProblem):
    def compute_1(self, input_lines: List[str]) -> int:
        data = [int(x) for x in input_lines[0].split(",")]
        return solve_1(data)

    def compute_2(self, input_lines: List[str]) -> int:
        data = [int(x) for x in input_lines[0].split(",")]
        return solve_2(data)


if __name__ == "__main__":
    exit(Day7().main())
