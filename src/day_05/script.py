from __future__ import annotations
from re import Pattern, findall, compile
from typing import List, Optional
from ..utils.input import get_input_list, get_parsed_input_list


class Move:
    _move_row_regex: Pattern = compile("^move \\d+ from \\d+ to \\d+$")

    @staticmethod
    def parse(row: str) -> Optional[Move]:
        """
        Parses a move from a row of the form move 1 from 2 to 1
        """

        if not Move._move_row_regex.match(row):
            return None

        numbers: List[str] = findall("\d+", row)

        return Move(int(numbers[0]), int(numbers[1]) - 1, int(numbers[2]) - 1)

    def __init__(self, total: int, from_stack: int, to_stack: int) -> None:
        self.total = total
        self.from_stack = from_stack
        self.to_stack = to_stack

    def apply(self, boxes: List[str], chunked: bool) -> None:
        index: int = -self.total
        if chunked:
            boxes[self.to_stack] += boxes[self.from_stack][index:]
            boxes[self.from_stack] = boxes[self.from_stack][:index]
        else:
            boxes[self.to_stack] += boxes[self.from_stack][-1 : index - 1 : -1]
            boxes[self.from_stack] = boxes[self.from_stack][:index]


def get_boxes(file_name: str) -> List[str]:
    """
    Gets the boxes e.g
        [D]
    [N] [C]
    [Z] [M] [P]
     1   2   3
    becomes [ZN, MCD, P]
    """

    boxes: List[str] = []

    for line in get_input_list(file_name):
        if line.replace(" ", "").isnumeric():
            break
        column: int = 0
        for i in range(0, len(line), 4):
            letter: str = line[i + 1].strip()
            if len(boxes) < column + 1:
                boxes.append(letter)
            else:
                boxes[column] = letter + boxes[column]
            column += 1

    return boxes


def apply_moves(file_name: str, chunked: bool) -> List[str]:
    boxes: List[str] = get_boxes(file_name)
    for move in get_parsed_input_list(file_name, Move.parse):
        if move is not None:
            move.apply(boxes, chunked)
    return boxes


def get_top_of_all_stacks_after_moves(file_name: str, chunked: bool) -> str:
    return "".join(
        stack[len(stack) - 1] if len(stack) else ""
        for stack in apply_moves(file_name, chunked)
    )


print(get_top_of_all_stacks_after_moves("src/day_05/input.txt", False))
print(get_top_of_all_stacks_after_moves("src/day_05/input.txt", True))
