import argparse
import copy
import itertools
from typing import List

import pytest
from support import timing


Data = List[int]

GOAL_RESULT = 19690720


def execute_command(data: List[int], position: int) -> None:
    if data[position] == OP_CODES.ADD:
        input1 = data[data[position+1]]
        input2 = data[data[position+2]]
        data[data[position+3]] = input1 + input2
    elif data[position] == OP_CODES.MULTIPLY:
        input1 = data[data[position+1]]
        input2 = data[data[position+2]]
        data[data[position+3]] = input1 * input2
    else:
        raise Exception("Unexpected opcode {}".format(data[position]))


class OP_CODES:
    ADD = 1
    MULTIPLY = 2
    TERM = 99


def should_terminate(data: List[int], position: int) -> bool:
    return data[position] == OP_CODES.TERM


def parse_data_from_input(input_s: str) -> Data:
    strings = list(itertools.chain.from_iterable(
        [line.strip().split(",") for line in input_s.splitlines()]))
    data = [int(x) for x in strings]
    return data


def set_inputs(data, input1, input2) -> None:
    data[1] = input1
    data[2] = input2


def restore_gravity_assist(data: Data) -> Data:
    modified = copy.deepcopy(data)
    set_inputs(modified, 12, 2)
    return modified


def execute_program(data: Data) -> int:
    position = 0
    while not should_terminate(data, position):
        execute_command(data, position)
        position += 4
    return data[0]


def compute_1(s: str) -> int:
    data = parse_data_from_input(s)
    data = restore_gravity_assist(data)
    return execute_program(data)


def compute_2(s: str) -> int:
    data = parse_data_from_input(s)
    # Loop through all possible inputs until we find one that matches expected
    # output
    for input1 in range(100):
        for input2 in range(100):
            data_copy = copy.deepcopy(data)
            set_inputs(data_copy, input1, input2)
            result = execute_program(data_copy)
            if result == GOAL_RESULT:
                return input1 * 100 + input2
    return 0


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
    assert execute_program(parse_data_from_input(input_s)) == expected


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
