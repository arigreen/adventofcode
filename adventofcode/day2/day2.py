import itertools
from typing import List

import pytest
from AOCProblem import AOCProblem

Program = List[int]

GOAL_RESULT = 19690720


def execute_command(program: List[int], position: int) -> None:
    if program[position] == OP_CODES.ADD:
        input1 = program[program[position+1]]
        input2 = program[program[position+2]]
        program[program[position+3]] = input1 + input2
    elif program[position] == OP_CODES.MULTIPLY:
        input1 = program[program[position+1]]
        input2 = program[program[position+2]]
        program[program[position+3]] = input1 * input2
    else:
        raise Exception("Unexpected opcode {}".format(program[position]))


class OP_CODES:
    ADD = 1
    MULTIPLY = 2
    TERM = 99


def should_terminate(program: List[int], position: int) -> bool:
    return program[position] == OP_CODES.TERM


def parse_program_from_input(input_lines: List[str]) -> Program:
    strings = list(itertools.chain.from_iterable(
        [line.strip().split(",") for line in input_lines]))
    program = [int(x) for x in strings]
    return program


def set_inputs(program, input1, input2) -> None:
    program[1] = input1
    program[2] = input2


def restore_gravity_assist(program: Program) -> None:
    set_inputs(program, 12, 2)


def execute_program(program: Program) -> int:
    position = 0
    while not should_terminate(program, position):
        execute_command(program, position)
        position += 4
    return program[0]


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        ('1,9,10,3,2,3,11,0,99,30,40,50', 3500),
        ('1,0,0,0,99', 2),
        ('2,3,0,3,99', 2),
        ('2,4,4,5,99,0', 2),
        ('1,1,1,4,99,5,6,0,99', 30),
    ),
)
def test_1(input_s: str, expected: int) -> None:
    assert execute_program(parse_program_from_input([input_s])) == expected


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        # put given test cases here
    ),
)
def test_2(input_s: str, expected: int) -> None:
    pass


class Day1(AOCProblem):

    def compute_1(self, input_lines: List[str]) -> int:
        program = parse_program_from_input(input_lines)
        restore_gravity_assist(program)
        return execute_program(program)

    def compute_2(self, input_lines: List[str]) -> int:
        program = parse_program_from_input(input_lines)
        # Loop through all possible inputs until we find one that matches
        # expected output
        for input1 in range(100):
            for input2 in range(100):
                program_copy = program[:]
                set_inputs(program_copy, input1, input2)
                result = execute_program(program_copy)
                if result == GOAL_RESULT:
                    return input1 * 100 + input2
        return 0


if __name__ == '__main__':
    exit(Day1().main())
