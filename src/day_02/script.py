from __future__ import annotations
from enum import Enum
from typing import Callable, Generator, List, Optional
from ..utils.input import get_parsed_input_list


class Move(Enum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

    @staticmethod
    def from_opponent(value: str) -> Move:
        match value:
            case "A":
                return Move.ROCK
            case "B":
                return Move.PAPER
            case _:
                return Move.SCISSORS

    @staticmethod
    def from_us(value: str) -> Move:
        match value:
            case "X":
                return Move.ROCK
            case "Y":
                return Move.PAPER
            case _:
                return Move.SCISSORS

    @staticmethod
    def from_us_part_2(opponent: Move, value: str) -> Move:
        match value:
            case "X":  # lose
                return Move((opponent.value + 1) % 3 + 1)
            case "Y":  # draw
                return opponent
            case _:  # win
                return Move((opponent.value + 3) % 3 + 1)


class RockPaperSissorsRow:
    @staticmethod
    def from_row(row: str) -> Optional[RockPaperSissorsRow]:
        if row.isspace():
            return None
        split_row: List[str] = row.split(" ")
        return RockPaperSissorsRow(
            Move.from_opponent(split_row[0]), Move.from_us(split_row[1])
        )

    @staticmethod
    def from_row_part_2(row: str) -> Optional[RockPaperSissorsRow]:
        if row.isspace():
            return None
        split_row: List[str] = row.split(" ")
        opponent: Move = Move.from_opponent(split_row[0])
        return RockPaperSissorsRow(
            opponent, Move.from_us_part_2(opponent, split_row[1])
        )

    def __init__(self, opponent: Move, us: Move) -> None:
        self.opponent = opponent
        self.us = us

    def get_score(self) -> int:
        return self.us.value + ((self.us.value - self.opponent.value + 1) % 3) * 3


def get_each_row_result(
    file_name: str, row_parser: Callable[[str], Optional[RockPaperSissorsRow]]
) -> Generator[int, None, None]:
    for value in get_parsed_input_list(file_name, row_parser):
        if value is not None:
            yield value.get_score()


def sum_score(
    file_name: str, row_parser: Callable[[str], Optional[RockPaperSissorsRow]]
) -> int:
    return sum([i for i in get_each_row_result(file_name, row_parser)])


print(
    "Part 1: ",
    sum_score("src/day_02/input.txt", RockPaperSissorsRow.from_row),
)
print(
    "Part 2: ",
    sum_score("src/day_02/input.txt", RockPaperSissorsRow.from_row_part_2),
)
