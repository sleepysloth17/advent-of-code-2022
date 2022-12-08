# I have been shamed by a meme into this, and yes it was a lot easier to use dicts


from typing import Dict, Generator, List, Optional, Tuple
from ..utils.input import get_parsed_input_list

part_1_dict: Dict[str, Dict[str, int]] = {
    "A": {
        "X": 4,
        "Y": 8,
        "Z": 3,
    },
    "B": {
        "X": 1,
        "Y": 5,
        "Z": 9,
    },
    "C": {
        "X": 7,
        "Y": 2,
        "Z": 6,
    },
}

part_2_dict: Dict[str, Dict[str, int]] = {
    "A": {
        "X": 3,
        "Y": 4,
        "Z": 8,
    },
    "B": {
        "X": 1,
        "Y": 5,
        "Z": 9,
    },
    "C": {
        "X": 2,
        "Y": 6,
        "Z": 7,
    },
}


def row_parser(row: str) -> Optional[Tuple[str, str]]:
    if not row:
        return None

    split: List[str] = row.split(" ")
    return (split[0], split[1])


def get_each_row_result(
    file_name: str, score_dict: Dict[str, Dict[str, int]]
) -> Generator[int, None, None]:
    for value in get_parsed_input_list(file_name, row_parser):
        if value is not None:
            yield score_dict[value[0]][value[1]]


def sum_results(file_name: str, score_dict: Dict[str, Dict[str, int]]) -> int:
    return sum(score for score in get_each_row_result(file_name, score_dict))


print(
    "Part 1: ",
    sum_results("src/day_02/input.txt", part_1_dict),
)
print(
    "Part 2: ",
    sum_results("src/day_02/input.txt", part_2_dict),
)
