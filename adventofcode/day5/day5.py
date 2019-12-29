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
        if not self.input:
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
        return 0


if __name__ == "__main__":
    exit(Day5().main())
