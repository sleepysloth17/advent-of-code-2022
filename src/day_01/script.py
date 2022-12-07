from typing import Generator, List
from ..utils.input import get_parsed_input_list


def get_per_elf_calories(file_name: str) -> Generator[int, None, None]:
    current_elf_calories: int = 0
    for value in get_parsed_input_list(
        file_name, lambda s: None if s.isspace() else int(s)
    ):
        if value is not None:
            current_elf_calories = current_elf_calories + value
        else:
            yield current_elf_calories
            current_elf_calories = 0
    yield current_elf_calories


def get_max_n_calories(file_name: str, n: int = 1) -> List[int]:
    all_calories: List[int] = [i for i in get_per_elf_calories(file_name)]
    all_calories.sort(reverse=True)
    return all_calories[0:n]


print("Part 1: ", get_max_n_calories("src/day_01/input.txt")[0])
print("Part 2: ", sum(get_max_n_calories("src/day_01/input.txt", 3)))
