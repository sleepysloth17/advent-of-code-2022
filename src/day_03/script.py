from functools import reduce
from typing import Dict, List, Tuple
from ..utils.input import get_input_list, get_parsed_input_list

priorities: Dict[str, int] = {}
for i, char in enumerate("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", 1):
    priorities[char] = i


def parse(s: str) -> Tuple[str, str, str]:
    """
    Returns a tuple of form (first_half, second_half, common_letters)
    """

    half: int = len(s) // 2
    first_half: str = s[:half]
    second_half: str = s[half:]
    return (first_half, second_half, get_common_letter(first_half, second_half))


def get_common_letter(*strs: str) -> str:
    return "".join(reduce(lambda a, b: set(a).intersection(set(b)), strs))


def sum_priorities(file_name: str) -> int:
    return sum(
        priorities[value[2]] for value in get_parsed_input_list(file_name, parse)
    )


def sum_priorities_part_2(file_name: str) -> int:
    lines: List[str] = [value for value in get_input_list(file_name)]
    return sum(
        priorities[get_common_letter(lines[i], lines[i + 1], lines[i + 2])]
        for i in range(0, len(lines), 3)
    )


print("Part 1: ", sum_priorities("src/day_03/input.txt"))
print("Part 2: ", sum_priorities_part_2("src/day_03/input.txt"))
