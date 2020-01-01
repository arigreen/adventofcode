import asyncio
from typing import List

import pytest
from AOCProblem import AOCProblem
from IntCode import IntCode


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
    all_output = asyncio.run(get_all_outputs_from_input(data, input))
    assert all_output == [expected_output]


async def get_all_outputs_from_input(data: List[int], input: int) -> List[int]:
    input_queue: asyncio.Queue[int] = asyncio.Queue()
    output_queue: asyncio.Queue[int] = asyncio.Queue()
    program = IntCode(data, input_queue, output_queue)
    input_queue.put_nowait(input)
    await program.execute()
    # There are many values, the last is what we care about
    values = []
    for x in range(output_queue.qsize()):
        values.append(output_queue.get_nowait())
    return values


def solve_with_input_output(data: List[int], input: int) -> int:
    all_output = asyncio.run(get_all_outputs_from_input(data, input))
    if any(x for x in all_output[:-1] if x != 0):
        raise Exception("Function not working correctly")
    return all_output[-1]


class Day5(AOCProblem):
    def compute_1(self, input_lines: List[str]) -> int:
        data = [int(x) for x in input_lines[0].split(",")]
        return solve_with_input_output(data, 1)

    def compute_2(self, input_lines: List[str]) -> int:
        data = [int(x) for x in input_lines[0].split(",")]
        return solve_with_input_output(data, 5)


if __name__ == "__main__":
    exit(Day5().main())
