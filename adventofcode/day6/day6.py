from collections import defaultdict
from typing import DefaultDict
from typing import List
from typing import Set

import pytest
from AOCProblem import AOCProblem

Node = str


class Tree:
    def __init__(self, edges: List[List[Node]]) -> None:
        self.nodes_to_children: DefaultDict[Node, List[str]] = defaultdict(list)
        self.all_edges: DefaultDict[Node, List[Node]] = defaultdict(list)

        for edge in edges:
            parent, child = edge
            self.nodes_to_children[parent].append(child)
            self.all_edges[parent].append(child)
            self.all_edges[child].append(parent)


def parse_tree(input_lines: List[str]) -> Tree:

    edges = [line.split(")") for line in input_lines]
    return Tree(edges)


def dfs_count_orbits(node: Node, tree: Tree, depth: int) -> int:
    result = (depth + 1) * len(tree.nodes_to_children[node])
    for child in tree.nodes_to_children[node]:
        result += dfs_count_orbits(child, tree, depth + 1)
    return result


def find_shortest_path_length(tree: Tree, start: Node, end: Node) -> int:
    result = 0
    seen: Set[Node] = set()
    this_level = [start]
    next_level = []
    while this_level:
        if end in this_level:
            return max(0, result - 2)
        current = this_level.pop()
        seen.add(current)
        for next_node in tree.all_edges[current]:
            if next_node in seen:
                continue
            next_level.append(next_node)
        if not this_level:
            this_level = next_level
            next_level = []
            result += 1
    raise ValueError("There is no path for the given inputs")


def sum_of_paths(input_lines: List[str]) -> int:
    """
    For each node in the tree, find the length from that node to COM.
    Return the sum.
    Inspired by asottile's solution.
    """
    nodes_to_parents = {}
    for line in input_lines:
        parent, child = line.split(")")
        nodes_to_parents[child] = parent

    def distance_to_com(node: Node) -> int:
        distance = 0
        curr = node
        while curr != "COM":
            distance += 1
            curr = nodes_to_parents[curr]
        return distance

    return sum(distance_to_com(node) for node in nodes_to_parents)


class Day6(AOCProblem):
    def compute_1(self, input_lines: List[str]) -> int:
        tree = parse_tree(input_lines)
        num_orbits = dfs_count_orbits("COM", tree, 0)
        return num_orbits

    def compute_2(self, input_lines: List[str]) -> int:
        tree = parse_tree(input_lines)
        result = find_shortest_path_length(tree, "YOU", "SAN")
        return result


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
    assert sum_of_paths(input_lines) == expected


@pytest.mark.parametrize(
    ("input_lines", "expected"),
    (
        (["SAN)YOU"], 0),
        (["SAN)A", "A)YOU"], 0),
        (["SAN)A", "A)B", "B)YOU"], 1),
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
                "K)YOU",
                "I)SAN",
            ],
            4,
        ),
    ),
)
def test_2(input_lines: List[str], expected: int) -> None:
    assert Day6().compute_2(input_lines) == expected


if __name__ == "__main__":
    day6 = Day6()
    day6.add_alternate_1("sum_of_paths", sum_of_paths)
    exit(day6.main())
