from enum import Enum
from typing import List
from typing import Literal
from typing import Optional
from typing import Tuple

import pytest
from AOCProblem import AOCProblem


GOAL_RESULT = 19690720


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


ParameterMode = Literal["Position", "Immediate"]


class Program:
    def __init__(self, data: List[int]) -> None:
        self.data = data
        self.position = 0
        self.input: Optional[int] = None
        self.outputs: List[int] = []

    def set_input(self, value: int) -> None:
        self.input = value

    def read_input(self) -> int:
        if self.input is None:
            raise Exception("Attemping to read input that does not exist")
        return self.input

    @classmethod
    def parse_from_input(cls, input_line: str) -> "Program":
        data = [int(x) for x in input_line.split(",")]
        return Program(data)

    def parse_operation(self, instruction: int) -> Tuple[OpCode, List[ParameterMode]]:
        op_code = OpCode(instruction % 100)
        instruction = instruction // 100
        param_modes: List[ParameterMode] = []
        while instruction > 0:
            param_mode: ParameterMode = "Immediate" if instruction % 10 == 1 else "Position"
            param_modes.append(param_mode)
            instruction = instruction // 10
        while len(param_modes) < 4:
            param_modes.append("Position")
        return op_code, param_modes

    def output(self, value: int) -> None:
        self.outputs.append(value)

    def get_param_value(self, index: int, param_modes: List[ParameterMode]) -> int:
        value = self.data[self.position + index]
        if param_modes[index - 1] == "Position":
            value = self.data[value]
        return value

    def execute(self) -> int:
        while True:
            op_code, param_modes = self.parse_operation(self.data[self.position])
            if op_code == OpCode.ADD:
                input1 = self.get_param_value(1, param_modes)
                input2 = self.get_param_value(2, param_modes)
                self.data[self.data[self.position + 3]] = input1 + input2
                self.position += 4
            elif op_code == OpCode.MULTIPLY:
                input1 = self.get_param_value(1, param_modes)
                input2 = self.get_param_value(2, param_modes)
                self.data[self.data[self.position + 3]] = input1 * input2
                self.position += 4
            elif op_code == OpCode.SAVE:
                user_input = self.read_input()
                write_position = self.data[self.position + 1]
                self.data[write_position] = user_input
                self.position += 2
            elif op_code == OpCode.OUTPUT:
                value = self.get_param_value(1, param_modes)
                self.output(value)
                self.position += 2
            elif op_code == OpCode.JUMP_IF:
                value = self.get_param_value(1, param_modes)
                if value:
                    new_position = self.get_param_value(2, param_modes)
                    self.position = new_position
                else:
                    self.position += 3
            elif op_code == OpCode.JUMP_IF_NOT:
                value = self.get_param_value(1, param_modes)
                if not value:
                    new_position = self.get_param_value(2, param_modes)
                    self.position = new_position
                else:
                    self.position += 3
            elif op_code == OpCode.LESS_THAN:
                value1 = self.get_param_value(1, param_modes)
                value2 = self.get_param_value(2, param_modes)
                write_position = self.data[self.position + 3]
                self.data[write_position] = 1 if value1 < value2 else 0
                self.position += 4
            elif op_code == OpCode.EQUALS:
                value1 = self.get_param_value(1, param_modes)
                value2 = self.get_param_value(2, param_modes)
                write_position = self.data[self.position + 3]
                self.data[write_position] = 1 if value1 == value2 else 0
                self.position += 4
            elif op_code == OpCode.TERM:
                break
            else:
                raise Exception(f"Invalid OP_CODE {op_code}")
        return self.data[0]


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
def test_1(input_s: str, expected: int) -> None:
    program = Program.parse_from_input(input_s)
    assert program.execute() == expected


@pytest.mark.parametrize(
    ("input_s", "expected"),
    (
        ("1002,4,3,4,33", [1002, 4, 3, 4, 99]),
        ("1101,100,-1,4,0", [1101, 100, -1, 4, 99]),
    ),
)
def test_full(input_s: str, expected: List[int]) -> None:
    program = Program.parse_from_input(input_s)
    program.execute()
    assert program.data == expected


@pytest.mark.parametrize(
    ("data", "input", "expected_output"),
    (
        ([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], 1, 0),
        ([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], 8, 1),
        ([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], 7, 1),
        ([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], 8, 0),
        ([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], 9, 0),
        ([3, 3, 1108, -1, 8, 3, 4, 3, 99], 4, 0),
        ([3, 3, 1108, -1, 8, 3, 4, 3, 99], 8, 1),
        ([3, 3, 1107, -1, 8, 3, 4, 3, 99], 7, 1),
        ([3, 3, 1107, -1, 8, 3, 4, 3, 99], 8, 0),
        ([3, 3, 1107, -1, 8, 3, 4, 3, 99], 9, 0),
        ([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], 0, 0),
        ([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], 1, 1),
        ([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], 0, 0),
        ([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], 1, 1),
        (
            [
                3,
                21,
                1008,
                21,
                8,
                20,
                1005,
                20,
                22,
                107,
                8,
                21,
                20,
                1006,
                20,
                31,
                1106,
                0,
                36,
                98,
                0,
                0,
                1002,
                21,
                125,
                20,
                4,
                20,
                1105,
                1,
                46,
                104,
                999,
                1105,
                1,
                46,
                1101,
                1000,
                1,
                20,
                4,
                20,
                1105,
                1,
                46,
                98,
                99,
            ],
            7,
            999,
        ),
        (
            [
                3,
                21,
                1008,
                21,
                8,
                20,
                1005,
                20,
                22,
                107,
                8,
                21,
                20,
                1006,
                20,
                31,
                1106,
                0,
                36,
                98,
                0,
                0,
                1002,
                21,
                125,
                20,
                4,
                20,
                1105,
                1,
                46,
                104,
                999,
                1105,
                1,
                46,
                1101,
                1000,
                1,
                20,
                4,
                20,
                1105,
                1,
                46,
                98,
                99,
            ],
            8,
            1000,
        ),
        (
            [
                3,
                21,
                1008,
                21,
                8,
                20,
                1005,
                20,
                22,
                107,
                8,
                21,
                20,
                1006,
                20,
                31,
                1106,
                0,
                36,
                98,
                0,
                0,
                1002,
                21,
                125,
                20,
                4,
                20,
                1105,
                1,
                46,
                104,
                999,
                1105,
                1,
                46,
                1101,
                1000,
                1,
                20,
                4,
                20,
                1105,
                1,
                46,
                98,
                99,
            ],
            9,
            1001,
        ),
    ),
)
def test_with_input_output(data: List[int], input: int, expected_output: int) -> None:
    program = Program(data)
    program.set_input(input)
    program.execute()
    assert program.outputs == [expected_output]


class Day5(AOCProblem):
    def compute_1(self, input_lines: List[str]) -> int:
        program = Program.parse_from_input(input_lines[0])
        program.set_input(1)
        program.execute()
        outputs = program.outputs
        if any(x for x in outputs[:-1] if x != 0):
            raise Exception("Function not working correctly")
        return outputs[-1]

    def compute_2(self, input_lines: List[str]) -> int:
        program = Program.parse_from_input(input_lines[0])
        program.set_input(5)
        program.execute()
        outputs = program.outputs
        if any(x for x in outputs[:-1] if x != 0):
            raise Exception("Function not working correctly")
        return outputs[-1]


if __name__ == "__main__":
    exit(Day5().main())
