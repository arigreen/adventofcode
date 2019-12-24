import argparse
from typing import List

from utils import timing


class AOCProblem:

    def compute_1(self, input_lines: List[str]) -> int:
        raise NotImplementedError("Part 1 not implemented!")

    def compute_2(self, input_lines: List[str]) -> int:
        raise NotImplementedError("Part 2 not implemented!")

    def parse_input(self) -> List[str]:
        parser = argparse.ArgumentParser()
        parser.add_argument('data_file')
        args = parser.parse_args()

        with open(args.data_file) as f:
            input_s = f.read()
        return input_s.splitlines()

    def main(self) -> int:
        input_lines = self.parse_input()
        with timing():
            print(f'Part 1: {self.compute_1(input_lines)}')

        with timing():
            print(f'Part 2: {self.compute_2(input_lines)}')

        return 0
