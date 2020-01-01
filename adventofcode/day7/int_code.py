import copy
from enum import Enum
from typing import List

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


class IntCode:
    def __init__(
        self,
        data: List[int],
        #        input_fn: Callable[[], int]=None,
        #        output_fn: Callable[[int], None]=None,
    ) -> None:
        self.data = data
        self.original_data = copy.copy(self.data)
        self.position = 0
        self.finished = False
        #        self.input_fn = input_fn
        #        self.output_fn = output_fn
        self.inputs: List[int] = []
        self.outputs: List[int] = []

    def restore(self) -> None:
        self.data = copy.copy(self.original_data)
        self.position = 0
        self.finished = False
        self.inputs = []
        self.outputs = []

    def read_input(self) -> int:
        if not self.inputs:
            raise NoInputException()
        return self.inputs.pop(0)

    def write_output(self, value: int) -> None:
        self.outputs.append(value)

    def set_input(self, value: int) -> None:
        self.inputs.append(value)

    @classmethod
    def parse_from_input(cls, input_line: str) -> "IntCode":
        data = [int(x) for x in input_line.split(",")]
        return IntCode(data)

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

    def execute(self) -> int:
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
                try:
                    user_input = self.read_input()
                except NoInputException:
                    return -1

                write_position = self.data[self.position + 1]
                self.data[write_position] = user_input
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
                self.finished = True
                break
            else:
                raise NotImplementedError(op_code)
        return self.data[0]


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
