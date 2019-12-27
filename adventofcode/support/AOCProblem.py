import argparse
from typing import Callable
from typing import List
from typing import NamedTuple

from utils import timing


class AlternateSolution(NamedTuple):
    name: str
    fn: Callable[[List[str]], int]


class AOCProblem:
    def __init__(self) -> None:
        self._alternate_solutions_1: List[AlternateSolution] = []
        self._alternate_solutions_2: List[AlternateSolution] = []

    def compute_1(self, input_lines: List[str]) -> int:
        raise NotImplementedError("Part 1 not implemented!")

    def compute_2(self, input_lines: List[str]) -> int:
        raise NotImplementedError("Part 2 not implemented!")

    def parse_input(self) -> List[str]:
        parser = argparse.ArgumentParser()
        parser.add_argument("data_file")
        args = parser.parse_args()

        with open(args.data_file) as f:
            input_s = f.read()
        return input_s.splitlines()

    def add_alternate_1(self, name: str, fn: Callable[[List[str]], int]) -> None:
        self._alternate_solutions_1.append(AlternateSolution(name, fn))

    def main(self) -> int:
        input_lines = self.parse_input()
        with timing():
            print(f"Part 1 (original): {self.compute_1(input_lines)}")

        for name, fn in self._alternate_solutions_1:
            with timing():
                print(f"Part 1 ({name}): {fn(input_lines)}")

        with timing():
            print(f"Part 2: {self.compute_2(input_lines)}")

        return 0
