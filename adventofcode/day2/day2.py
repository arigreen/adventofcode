# Sum Fuel requirements
# https://adventofcode.com/2019/day/2
import copy
import fileinput
import itertools
from typing import List


Data = List[int]

GOAL_RESULT = 19690720


class OP_CODES:
    ADD = 1
    MULTIPLY = 2
    TERM = 99


def should_terminate(data: List[int], position: int) -> bool:
    return data[position] == OP_CODES.TERM


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


def parse_data_from_input(lines: List[str]) -> Data:
    strings = list(itertools.chain.from_iterable(
        [line.strip().split(",") for line in lines]))
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


def solve_part_1(data: Data) -> int:
    data = restore_gravity_assist(data)
    result = execute_program(data)
    return result


def solve_part_2(data: Data) -> str:
    # Loop through all possible inputs until we find one that matches expected
    # output
    for input1 in range(100):
        for input2 in range(100):
            data_copy = copy.deepcopy(data)
            set_inputs(data_copy, input1, input2)
            result = execute_program(data_copy)
            if result == GOAL_RESULT:
                return f'{input1}{input2}'
    return '-1'


def main():
    input = fileinput.input()
    data = parse_data_from_input(input)

    result_1 = solve_part_1(data)
    result_2 = solve_part_2(data)

    print(f"Part 1: {result_1}")
    print(f"Part 2: {result_2}")


if __name__ == "__main__":
    main()
