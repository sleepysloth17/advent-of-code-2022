from __future__ import annotations
from typing import List
from ..utils.input import get_input_list


class Tree:
    @staticmethod
    def from_char(char: str) -> Tree:
        return Tree(int(char) + 1)

    def __init__(self, height: int) -> None:
        self.height: int = height

        # Note that the list is a list of the heights of the trees in order as if you
        # are travelling from this tree in that direction in the forest i.e closest
        # first.
        # e.g in 12345, 3.trees_right would be [4, 5] and 3.trees_left would be [2, 1].
        self.trees_left: List[int] = []
        self.trees_right: List[int] = []
        self.trees_above: List[int] = []
        self.trees_below: List[int] = []

    def is_visible(self) -> bool:
        # Just a sad note here to say that we could update the max as we go along,
        # rather than saving a list, but made the code too cluttered with the list
        # stuff I needed for part two. RIP. So much iteration.
        # Serves me right for optimizing for that rather than making this more nicely
        # extensible.
        return (
            max(
                self.height - (max(self.trees_left) if len(self.trees_left) else 0),
                self.height - (max(self.trees_right) if len(self.trees_right) else 0),
                self.height - (max(self.trees_above) if len(self.trees_above) else 0),
                self.height - (max(self.trees_below) if len(self.trees_below) else 0),
            )
            > 0
        )

    def get_scenic_score(self) -> int:
        return (
            self._get_viewing_distance_in_direction(self.trees_left)
            * self._get_viewing_distance_in_direction(self.trees_right)
            * self._get_viewing_distance_in_direction(self.trees_above)
            * self._get_viewing_distance_in_direction(self.trees_below)
        )

    def _get_viewing_distance_in_direction(self, trees: List[int]) -> int:
        distance: int = 0
        for tree in trees:
            distance += 1
            if tree >= self.height:
                break
        return max(distance, 1)


def get_input_forest(file_name: str) -> List[List[Tree]]:
    """
    For example:
    1 2
    3 4
    Becomes, [[Tree(1), Tree(2)], [Tree(3), Tree(4)]].
    I could do the first pass at this time for efficiency, but I can't be bothered.
    """

    return [[Tree.from_char(i) for i in row] for row in get_input_list(file_name)]


def run_through_forest(forest: List[List[Tree]], first_pass: bool) -> None:
    """
    Updates all the comparative height of the trees in the forest
    first_pass True means left to right, up to down
    first_pass False mean right to left, down to up

    Honestly, this made a lot more sense for part 1, with part 2 this
    is harder to read than the obvious way.
    """

    trees_vertical_list: List[List[int]] = []

    for row in forest if first_pass else forest[::-1]:
        trees_horizontal: List[int] = []
        for j, tree in enumerate(row if first_pass else row[::-1]):
            if len(row) > len(trees_vertical_list):
                trees_vertical_list.append([])

            trees_vertical: List[int] = trees_vertical_list[j]

            if first_pass:
                tree.trees_left = trees_horizontal[:]
                tree.trees_above = trees_vertical[:]
            else:
                tree.trees_right = trees_horizontal[:]
                tree.trees_below = trees_vertical[:]

            trees_vertical.insert(0, tree.height)
            trees_horizontal.insert(0, tree.height)


def get_updated_forest(file_name: str) -> List[List[Tree]]:
    forest: List[List[Tree]] = get_input_forest(file_name)
    run_through_forest(forest, True)
    run_through_forest(forest, False)
    return forest


def count_visible_trees(file_name: str) -> int:
    forest: List[List[Tree]] = get_updated_forest(file_name)
    return sum(sum(tree.is_visible() for tree in row) for row in forest)


def find_max_scenic_score(file_name: str) -> int:
    forest: List[List[Tree]] = get_updated_forest(file_name)
    return max(max(tree.get_scenic_score() for tree in row) for row in forest)


print("Example Part 1: ", count_visible_trees("src/day_08/example.txt"))
print("Part 1: ", count_visible_trees("src/day_08/input.txt"))

print("Example Part 2: ", find_max_scenic_score("src/day_08/example.txt"))
print("Part 2: ", find_max_scenic_score("src/day_08/input.txt"))
