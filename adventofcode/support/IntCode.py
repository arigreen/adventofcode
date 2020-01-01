import asyncio
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
        input_queue: "asyncio.Queue[int]" = None,
        output_queue: "asyncio.Queue[int]" = None,
    ) -> None:
        self.data = data
        self.original_data = copy.copy(self.data)
        self.position = 0
        self.finished = False
        self.input_queue = input_queue
        self.output_queue = output_queue

    def restore(self) -> None:
        self.data = copy.copy(self.original_data)
        self.position = 0
        self.finished = False

    async def read_input(self) -> int:
        if not self.input_queue:
            raise NotImplementedError("No input queue")
        result = await self.input_queue.get()
        return result
        return await self.input_queue.get()

    async def write_output(self, value: int) -> None:
        if not self.output_queue:
            raise NotImplementedError("No output queue")
        await self.output_queue.put(value)

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

    async def execute(self) -> int:
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
                    user_input = await self.read_input()
                except NoInputException:
                    return -1

                write_position = self.data[self.position + 1]
                self.data[write_position] = user_input
                self.position += 2
            elif op_code == OpCode.OUTPUT:
                value = self.get_parameter(1)
                await self.write_output(value)
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
        ("1,9,10,3,2,3,11,0,99,30,40,50", 3500),
        ("1,0,0,0,99", 2),
        ("2,3,0,3,99", 2),
        ("2,4,4,5,99,0", 2),
        ("1,1,1,4,99,5,6,0,99", 30),
    ),
)
def test_pos_0(input_s: str, expected: int) -> None:
    data = [int(x) for x in input_s.split(",")]
    program = IntCode(data)
    asyncio.run(program.execute())
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
    program = IntCode(data)
    asyncio.run(program.execute())
    assert program.data == expected
