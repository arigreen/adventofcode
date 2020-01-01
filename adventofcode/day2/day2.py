import asyncio
from typing import List

from AOCProblem import AOCProblem
from IntCode import IntCode

Program = List[int]


def set_inputs(program: IntCode, input1: int, input2: int) -> None:
    program.data[1] = input1
    program.data[2] = input2


class Day1(AOCProblem):
    def compute_1(self, input_lines: List[str]) -> int:
        data = [int(x) for x in input_lines[0].split(",")]
        program = IntCode(data)
        set_inputs(program, 12, 2)
        asyncio.run(program.execute())
        return program.data[0]

    def compute_2(self, input_lines: List[str]) -> int:
        data = [int(x) for x in input_lines[0].split(",")]
        # Loop through all possible inputs until we find one that matches
        # expected output

        GOAL_RESULT = 19690720

        for input1 in range(100):
            for input2 in range(100):
                data_copy = data[:]
                program = IntCode(data_copy)
                set_inputs(program, input1, input2)
                asyncio.run(program.execute())
                if program.data[0] == GOAL_RESULT:
                    return input1 * 100 + input2
        return 0


if __name__ == "__main__":
    exit(Day1().main())
