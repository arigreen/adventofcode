from collections import defaultdict
from typing import DefaultDict
from typing import List

import pytest
from AOCProblem import AOCProblem


class Tree:
    def __init__(self, edges: List[List[str]]) -> None:
        self.nodes_to_children: DefaultDict[str, List[str]] = defaultdict(list)
        for edge in edges:
            parent, child = edge
            self.nodes_to_children[parent].append(child)


def parse_tree(input_lines: List[str]) -> Tree:
    edges = [line.split(")") for line in input_lines]
    return Tree(edges)


def dfs_count_orbits(node: str, tree: Tree, depth: int) -> int:
    result = (depth + 1) * len(tree.nodes_to_children[node])
    for child in tree.nodes_to_children[node]:
        result += dfs_count_orbits(child, tree, depth + 1)
    return result


class Day6(AOCProblem):
    def compute_1(self, input_lines: List[str]) -> int:
        tree = parse_tree(input_lines)
        num_orbits = dfs_count_orbits("COM", tree, 0)
        return num_orbits

    def compute_2(self, input_lines: List[str]) -> int:
        # TODO: Implement solution here!
        return 0


@pytest.mark.parametrize(
    ("input_lines", "expected"),
    (
        (["COM)A", "COM)B"], 2),
        (["COM)A", "A)B"], 3),
        (
            [
                "COM)B",
                "B)C",
                "C)D",
                "D)E",
                "E)F",
                "B)G",
                "G)H",
                "D)I",
                "E)J",
                "J)K",
                "K)L",
            ],
            42,
        ),
    ),
)
def test_1(input_lines: List[str], expected: int) -> None:
    assert Day6().compute_1(input_lines) == expected


@pytest.mark.parametrize(
    ("input_s", "expected"),
    (
        # put given test cases here
    ),
)
def test_2(input_s: str, expected: int) -> None:
    assert Day6().compute_1([input_s]) == expected


if __name__ == "__main__":
    exit(Day6().main())
