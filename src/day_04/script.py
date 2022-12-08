from typing import List, Set, Tuple
from ..utils.input import get_parsed_input_list


def parse_range(s: str) -> Tuple[int, int]:
    split: List[str] = s.split("-")
    return (int(split[0]), int(split[1]))


def parse_row(s: str) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    split: List[str] = s.split(",")
    return (parse_range(split[0]), parse_range(split[1]))


def one_contains_another(range_a: Tuple[int, int], range_b: Tuple[int, int]) -> bool:
    """
    Returns True if one of the given ranges fully contains the other
    """

    a: Set[int] = set(range(range_a[0], range_a[1] + 1))
    b: Set[int] = set(range(range_b[0], range_b[1] + 1))
    intersection: Set[int] = a.intersection(b)

    return a == intersection or b == intersection


def overlap(range_a: Tuple[int, int], range_b: Tuple[int, int]) -> bool:
    """
    Returns True if there is any overlap
    """

    a: Set[int] = set(range(range_a[0], range_a[1] + 1))
    b: Set[int] = set(range(range_b[0], range_b[1] + 1))

    return len(a.intersection(b)) > 0


def get_total_contains(file_name: str) -> int:
    return sum(
        one_contains_another(value[0], value[1])
        for value in get_parsed_input_list(file_name, parse_row)
    )


def get_total_overlap(file_name: str) -> int:
    return sum(
        overlap(value[0], value[1])
        for value in get_parsed_input_list(file_name, parse_row)
    )


print("Part 1: ", get_total_contains("src/day_04/input.txt"))
print("Part 2: ", get_total_overlap("src/day_04/input.txt"))
