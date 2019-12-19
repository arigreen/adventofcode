# Sum Fuel requirements
# https://adventofcode.com/2019/day/2
import fileinput
import itertools
from typing import List


def should_terminate(data: List[int], position: int) -> bool:
    return data[position] == 99


def execute_command(data: List[int], position: int) -> None:
    return


def main():
    data = list(itertools.chain.from_iterable(
        [line.strip().split(",") for line in fileinput.input()]))
    position = 0
    while not should_terminate(data, position):
        execute_command(data, position)
        position += 4
    print(data)


if __name__ == "__main__":
    main()
