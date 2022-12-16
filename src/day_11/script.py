from __future__ import annotations
from functools import reduce
from re import findall
from typing import Callable, List
from ..utils.input import get_input_list


def get_numbers(to_parse: str) -> List[int]:
    return [int(i) for i in findall("\\d+", to_parse)]


class Monkey:
    @staticmethod
    def from_rows(rows: List[str]) -> Monkey:
        return Monkey(
            get_numbers(rows[0]),
            Monkey.__get_operation(rows[1]),
            get_numbers(rows[2])[0],
            get_numbers(rows[3])[0],
            get_numbers(rows[4])[0],
        )

    @staticmethod
    def __get_operation(row: str) -> Callable[[int], int]:
        arithmetic_side: str = row.split(" = ")[1]

        if "*" in row:
            args: List[str] = arithmetic_side.split(" * ")
            if args[1] == "old":
                return lambda i: i * i
            return lambda i: i * int(args[1])

        modifier = int(arithmetic_side.split(" + ")[1])
        return lambda i: i + modifier

    def __init__(
        self,
        items: List[int],
        operation: Callable[[int], int],
        divisor: int,
        monkey_if_true: int,
        monkey_if_false: int,
    ) -> None:
        self.inspections = 0
        self.items = items
        self.operation = operation
        self.divisor = divisor
        self.monkey_if_false = monkey_if_false
        self.monkey_if_true = monkey_if_true

    def handle_turn(
        self, monkeys: List[Monkey], worry_function: Callable[[int], int]
    ) -> None:
        while len(self.items) > 0:
            self.inspections += 1
            new_worry = worry_function(self.operation(self.items.pop(0)))
            monkeys[
                self.monkey_if_false
                if new_worry % self.divisor
                else self.monkey_if_true
            ].items.append(new_worry)


def get_monkeys(file_name: str) -> List[Monkey]:
    monkeys: List[Monkey] = []
    new_monkey: List[str] = []
    for row in get_input_list(file_name):
        if row.startswith("Monkey"):
            add_monkey(monkeys, new_monkey)
            new_monkey = []
        elif row:
            new_monkey.append(row)
    add_monkey(monkeys, new_monkey)
    return monkeys


def add_monkey(monkeys: List[Monkey], new_monkey: List[str]) -> None:
    if len(new_monkey) == 5:
        monkeys.append(Monkey.from_rows(new_monkey))


def monkey_business(monkeys: List[Monkey]) -> int:
    return reduce(
        lambda x, y: x * y,
        sorted(
            map(
                lambda m: m.inspections,
                monkeys,
            )
        )[-2:],
    )


def handle_rounds_part_1(file_name: str, number_of_rounds: int) -> List[Monkey]:
    monkeys: List[Monkey] = get_monkeys(file_name)
    for _ in range(number_of_rounds):
        for monkey in monkeys:
            monkey.handle_turn(monkeys, lambda w: w // 3)
    return monkeys


def handle_rounds_part_2(file_name: str, number_of_rounds: int) -> List[Monkey]:
    monkeys: List[Monkey] = get_monkeys(file_name)
    div: int = reduce(lambda a, b: a * b, map(lambda m: m.divisor, monkeys))
    for _ in range(number_of_rounds):
        for monkey in monkeys:
            monkey.handle_turn(monkeys, lambda w: w % div)
    return monkeys


print(
    "Example part 1: ",
    monkey_business(handle_rounds_part_1("src/day_11/example.txt", 20)),
)
print("Part 1: ", monkey_business(handle_rounds_part_1("src/day_11/input.txt", 20)))

print(
    "Example part 2: ",
    monkey_business(handle_rounds_part_2("src/day_11/example.txt", 10000)),
)
print(
    "Part 2: ",
    monkey_business(handle_rounds_part_2("src/day_11/input.txt", 10000)),
)
