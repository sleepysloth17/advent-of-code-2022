from typing import List
from ..utils.input import get_input_list


def get_register_value_list(file_name: str) -> List[int]:
    cycle_list: List[int] = [1]
    for row in get_input_list(file_name):
        cycle_list.append(cycle_list[-1])
        if row != "noop":
            cycle_list.append(cycle_list[-1] + int(row.split(" ")[1]))
    return cycle_list


def get_sum_strenghts_at(file_name: str, *cycles: int) -> int:
    cycle_list: List[int] = get_register_value_list(file_name)
    return sum(cycle_list[i - 1] * i for i in cycles)


def get_crt_display(file_name: str, crt_width: int, crt_height: int) -> str:
    crt_rows: List[str] = []
    cycle_list: List[int] = get_register_value_list(file_name)

    for y in range(crt_height):
        crt_rows.append(
            "".join(
                "#" if abs(x - cycle_list[(y * crt_width) + x]) < 2 else "."
                for x in range(crt_width)
            )
        )

    return "\n".join(crt_rows)


print(
    "Example part 1: ",
    get_sum_strenghts_at("src/day_10/example.txt", 20, 60, 100, 140, 180, 220),
)
print(
    "Part 1: ",
    get_sum_strenghts_at("src/day_10/input.txt", 20, 60, 100, 140, 180, 220),
)

print(f'Example part 2: \n{get_crt_display("src/day_10/example.txt", 40, 6)}')
print(f'Part 2: \n{get_crt_display("src/day_10/input.txt", 40, 6)}')
