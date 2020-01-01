import asyncio
import copy
import itertools
from typing import Any
from typing import Coroutine
from typing import List

import pytest
from AOCProblem import AOCProblem
from int_code import IntCode


@pytest.mark.parametrize(
    ("data", "expected"),
    (
        (
            #
            # 15 <- phase_ordering
            # 16 <- last_output
            # MULTIPLY last_output * 10 and store in 16
            # ADD to phase_ordering and store in 15
            #
            [3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0],
            43210,
        ),
        (
            [
                3,
                23,
                3,
                24,
                1002,
                24,
                10,
                24,
                1002,
                23,
                -1,
                23,
                101,
                5,
                23,
                23,
                1,
                24,
                23,
                23,
                4,
                23,
                99,
                0,
                0,
            ],
            54321,
        ),
        (
            [
                3,
                31,
                3,
                32,
                1002,
                32,
                10,
                32,
                1001,
                31,
                -2,
                31,
                1007,
                31,
                0,
                33,
                1002,
                33,
                7,
                33,
                1,
                33,
                31,
                31,
                1,
                32,
                31,
                31,
                4,
                31,
                99,
                0,
                0,
                0,
            ],
            65210,
        ),
    ),
)
def test_1(data: List[int], expected: int) -> None:
    result = asyncio.run(solve_1(data))
    assert result == expected


@pytest.mark.parametrize(
    ("data", "expected"),
    (
        #
        # 15 <- phase_ordering
        # 16 <- last_output
        # MULTIPLY last_output * 10 and store in 16
        # ADD to phase_ordering and store in 15
        #
        (
            [
                3,
                26,
                1001,
                26,
                -4,
                26,
                3,
                27,
                1002,
                27,
                2,
                27,
                1,
                27,
                26,
                27,
                4,
                27,
                1001,
                28,
                -1,
                28,
                1005,
                28,
                6,
                99,
                0,
                0,
                5,
            ],
            139629729,
        ),
    ),
)
def test_2(data: List[int], expected: int) -> None:
    result = asyncio.run(solve_2(data))
    assert result == expected


async def run_program_repeatedly(
    data: List[int], ordering: List[int], should_amplify: bool
) -> int:  # create 5 programs
    queues = []
    num_programs = len(ordering)
    for i in range(num_programs):
        queue: asyncio.Queue[int] = asyncio.Queue()
        queue.put_nowait(ordering[i])
        queues.append(queue)

    # append output queue for final program
    if should_amplify:
        queues.append(queues[0])
    else:
        queues.append(asyncio.Queue())

    programs = [
        IntCode(copy.copy(data), queues[i], queues[i + 1]) for i in range(num_programs)
    ]
    # initial input
    queues[0].put_nowait(0)

    tasks = [prog.execute() for prog in programs]

    async def run_all(tasks: List[Coroutine[Any, Any, int]]) -> None:
        await asyncio.gather(*tasks)

    await run_all(tasks)
    return await queues[-1].get()


async def solve_1(data: List[int]) -> int:
    results = [
        await run_program_repeatedly(data, list(ordering), False)
        for ordering in itertools.permutations(range(5))
    ]
    return max(results)


async def solve_2(data: List[int]) -> int:
    results = [
        await run_program_repeatedly(data, list(ordering), True)
        for ordering in itertools.permutations(range(5, 10))
    ]
    return max(results)


class Day7(AOCProblem):
    def compute_1(self, input_lines: List[str]) -> int:
        data = [int(x) for x in input_lines[0].split(",")]
        return asyncio.run(solve_1(data))

    def compute_2(self, input_lines: List[str]) -> int:
        data = [int(x) for x in input_lines[0].split(",")]
        return asyncio.run(solve_2(data))


if __name__ == "__main__":
    exit(Day7().main())
