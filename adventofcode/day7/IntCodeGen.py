import copy
from enum import Enum
from typing import Generator
from typing import List
from typing import Optional

import pytest

# from typing import Callable


class NoInputException(Exception):
    pass


class OpCode(Enum):
    ADD = 1
    MULTIPLY = 2
    SAVE = 3
    OUTPUT = 4
    JUMP_IF = 5
    JUMP_IF_NOT = 6
    LESS_THAN = 7
    EQUALS = 8
    TERM = 99


class ParameterMode(Enum):
    POSITION = 0
    IMMEDIATE = 1


class IntCodeGen:
    """IntCode as a generator"""

    def __init__(self, data: List[int],) -> None:
        self.data = data
        self.original_data = copy.copy(self.data)
        self.position = 0
        self.inputs: List[int] = []
        self.outputs: List[int] = []

    def restore(self) -> None:
        self.data = copy.copy(self.original_data)
        self.position = 0
        self.inputs = []
        self.outputs = []

    def read_input(self) -> Generator[Optional[int], int, int]:
        if self.inputs:
            result = self.inputs.pop(0)
        else:
            output_value = self.outputs.pop(0) if self.outputs else None
            result = yield output_value
        return result

    def write_output(self, value: int) -> None:
        self.outputs.append(value)

    def current_operation(self) -> OpCode:
        return OpCode(self.data[self.position] % 100)

    def get_parameter(self, index: int) -> int:
        param_mode = ParameterMode(self.data[self.position] // 10 ** (1 + index) % 10)
        if param_mode == ParameterMode.POSITION:
            return self.data[self.data[self.position + index]]
        elif param_mode == ParameterMode.IMMEDIATE:
            return self.data[self.position + index]
        else:
            raise NotImplementedError(param_mode)

    def execute(self) -> Generator[Optional[int], int, None]:
        while True:
            op_code = self.current_operation()
            if op_code == OpCode.ADD:
                input1 = self.get_parameter(1)
                input2 = self.get_parameter(2)
                self.data[self.data[self.position + 3]] = input1 + input2
                self.position += 4
            elif op_code == OpCode.MULTIPLY:
                input1 = self.get_parameter(1)
                input2 = self.get_parameter(2)
                self.data[self.data[self.position + 3]] = input1 * input2
                self.position += 4
            elif op_code == OpCode.SAVE:
                input_value = yield from self.read_input()
                write_position = self.data[self.position + 1]
                self.data[write_position] = input_value
                self.position += 2
            elif op_code == OpCode.OUTPUT:
                value = self.get_parameter(1)
                self.write_output(value)
                self.position += 2
            elif op_code == OpCode.JUMP_IF:
                value = self.get_parameter(1)
                if value:
                    new_position = self.get_parameter(2)
                    self.position = new_position
                else:
                    self.position += 3
            elif op_code == OpCode.JUMP_IF_NOT:
                value = self.get_parameter(1)
                if not value:
                    new_position = self.get_parameter(2)
                    self.position = new_position
                else:
                    self.position += 3
            elif op_code == OpCode.LESS_THAN:
                value1 = self.get_parameter(1)
                value2 = self.get_parameter(2)
                write_position = self.data[self.position + 3]
                self.data[write_position] = 1 if value1 < value2 else 0
                self.position += 4
            elif op_code == OpCode.EQUALS:
                value1 = self.get_parameter(1)
                value2 = self.get_parameter(2)
                write_position = self.data[self.position + 3]
                self.data[write_position] = 1 if value1 == value2 else 0
                self.position += 4
            elif op_code == OpCode.TERM:
                output_value = self.outputs[0] if self.outputs else -1
                yield output_value
                return
            else:
                raise NotImplementedError(op_code)


@pytest.mark.parametrize(
    ("input_s", "expected"),
    (
        ("1,9,10,3,2,3,11,0,99,30,40,50", 3500),
        ("1,0,0,0,99", 2),
        ("2,3,0,3,99", 2),
        ("2,4,4,5,99,0", 2),
        ("1,1,1,4,99,5,6,0,99", 30),
    ),
)
def test_pos_0(input_s: str, expected: int) -> None:
    data = [int(x) for x in input_s.split(",")]
    program = IntCodeGen(data)
    program.execute()
    assert program.data[0] == expected


@pytest.mark.parametrize(
    ("input_s", "expected"),
    (
        ("1002,4,3,4,33", [1002, 4, 3, 4, 99]),
        ("1101,100,-1,4,0", [1101, 100, -1, 4, 99]),
    ),
)
def test_full(input_s: str, expected: List[int]) -> None:
    data = [int(x) for x in input_s.split(",")]
    program = IntCodeGen(data)
    program.execute()
    assert program.data == expected
