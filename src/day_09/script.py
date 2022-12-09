from __future__ import annotations
from typing import Dict, List, Tuple
from ..utils.input import get_parsed_input_list

# Looks like from the examples we have:
# - H moves
# - T goes to where H was UNLESS T is still touching H.
# We _should_ be able to do this along the whole length of the rope if
# the rope is longer than two. E.g HMT, M follows H, then T follows M.
#
# Ah, from part two it seems that it doesn't quite follow like that, RIP
# that, instead I think I need to work out the direction I need to move to be close,
# and then move there instead to reduce the distance to 1 from the max of 2 I think?


class Move:
    __move_dict: Dict[str, Tuple[int, int]] = {
        "R": (1, 0),
        "U": (0, 1),
        "L": (-1, 0),
        "D": (0, -1),
    }

    @staticmethod
    def from_row(row: str) -> Move:
        split: List[str] = row.split(" ")
        return Move(split[0], int(split[1]))

    def __init__(self, move: str, steps: int) -> None:
        self.move_vector = self.__move_dict[move]
        self.steps = steps

    def apply(self, knot_positions: List[List[Tuple[int, int]]]) -> None:
        for _ in range(self.steps):
            knot_positions[0].append(
                self.__add(knot_positions[0][-1], self.move_vector)
            )
            for i in range(1, len(knot_positions)):
                distance_from_previous_knot: Tuple[int, int] = (
                    knot_positions[i - 1][-1][0] - knot_positions[i][-1][0],
                    knot_positions[i - 1][-1][1] - knot_positions[i][-1][1],
                )
                if (
                    max(
                        abs(distance_from_previous_knot[0]),
                        abs(distance_from_previous_knot[1]),
                    )
                    > 1
                ):
                    move_direction: Tuple[int, int] = self.__get_unit_direction(
                        distance_from_previous_knot
                    )
                    knot_positions[i].append(
                        self.__add(knot_positions[i][-1], move_direction)
                    )

    def __add(self, a: Tuple[int, int], b: Tuple[int, int]) -> Tuple[int, int]:
        return (a[0] + b[0], a[1] + b[1])

    def __get_unit_direction(self, move: Tuple[int, int]) -> Tuple[int, int]:
        return (move[0] // (abs(move[0]) or 1), move[1] // (abs(move[1]) or 1))


def process_moves(file_name: str, knots: str) -> List[List[Tuple[int, int]]]:
    knot_positions: List[List[Tuple[int, int]]] = [[(0, 0)] for _ in knots]
    for move in get_parsed_input_list(file_name, Move.from_row):
        move.apply(knot_positions)
    return knot_positions


def count_unique_moves(file_name: str, knots: str, to_count: str) -> int:
    return len(set(process_moves(file_name, knots)[knots.find(to_count)]))


print("Example part 1: ", count_unique_moves("src/day_09/example.txt", "HT", "T"))
print("Part 1: ", count_unique_moves("src/day_09/input.txt", "HT", "T"))

print(
    "Example part 2: ",
    count_unique_moves("src/day_09/example_2.txt", "H123456789", "9"),
)
print("Part 2: ", count_unique_moves("src/day_09/input.txt", "H123456789", "9"))
