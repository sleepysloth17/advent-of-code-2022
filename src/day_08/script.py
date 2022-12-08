from __future__ import annotations
from typing import List
from ..utils.input import get_input_list


class Tree:
    @staticmethod
    def from_char(char: str) -> Tree:
        return Tree(int(char) + 1)

    def __init__(self, height: int) -> None:
        self.height: int = height

        self.compare_left: int = height
        self.compare_right: int = height
        self.compare_above: int = height
        self.compare_below: int = height

        self.trees_left: List[Tree] = []
        self.trees_right: List[Tree] = []
        self.trees_above: List[Tree] = []
        self.trees_below: List[Tree] = []

    def is_visible(self) -> bool:
        return (
            max(
                self.compare_left,
                self.compare_right,
                self.compare_above,
                self.compare_below,
            )
            > 0
        )


def get_input_forest(file_name: str) -> List[List[Tree]]:
    """
    For example:
    1 2
    3 4
    Becomes, [[Tree(1), Tree(2)], [Tree(3), Tree(4)]].
    I could do the first pass at this time, but I can't be bothered.
    """

    return_list: List[List[Tree]] = []
    for row in get_input_list(file_name):
        return_list.append([Tree.from_char(i) for i in row])
    return return_list


def run_through_forest(forest: List[List[Tree]], first_pass: bool) -> None:
    """
    Updates all the comparative height of the trees in the forest
    first_pass True means left to right, up to down
    first_pass False mean right to left, down to up
    """

    trees_vertical_list: List[List[Tree]] = []
    max_vertical_list: List[int] = []

    for row in forest if first_pass else forest[::-1]:
        trees_horizontal: List[Tree] = []
        max_horizontal: int = 0
        for j, tree in enumerate(row if first_pass else row[::-1]):
            if len(row) > len(max_vertical_list):
                max_vertical_list.append(0)
                trees_vertical_list.append([])

            # This is part 2
            trees_vertical: List[Tree] = trees_vertical_list[j]

            if first_pass:
                tree.trees_left = trees_horizontal[:]
                tree.trees_above = trees_vertical[:]
            else:
                tree.trees_right = trees_horizontal[:]
                tree.trees_below = trees_vertical[:]

            trees_vertical.append(tree)
            trees_horizontal.append(tree)

            # Below was for part 1
            max_vertical: int = max_vertical_list[j]

            if first_pass:
                tree.compare_left = tree.height - max_horizontal
                tree.compare_above = tree.height - max_vertical
            else:
                tree.compare_right = tree.height - max_horizontal
                tree.compare_below = tree.height - max_vertical

            if tree.height > max_vertical:
                max_vertical_list[j] = tree.height
            if tree.height > max_horizontal:
                max_horizontal = tree.height


def count_visible_trees(file_name: str) -> int:
    forest: List[List[Tree]] = get_input_forest(file_name)
    run_through_forest(forest, True)
    run_through_forest(forest, False)
    for row in forest:
        print(i.trees_above for i in row)
    return sum(sum(tree.is_visible() for tree in row) for row in forest)


print("Example Part 1: ", count_visible_trees("src/day_08/example.txt"))
# print("Part 1: ", count_visible_trees("src/day_08/input.txt"))
