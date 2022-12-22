from enum import Enum
from functools import cmp_to_key, reduce
from typing import Generator, List, Optional, Tuple, Union, cast
from itertools import zip_longest
from ..utils.input import get_parsed_input_list


Packet = List[Union[int, "Packet"]]


class PacketState(Enum):
    RIGHT_ORDER = -1
    WRONG_ORDER = 1
    CONTINUE = 0


# eval felt like cheating
def parse_packet_from_row(row: str) -> Optional[Packet]:
    if not len(row):
        return None
    packet_list: List[Packet] = []
    row_length: int = len(row)
    i = 0
    while i < row_length:
        char: str = row[i]
        match char:
            case "[":
                packet_list.append([])
            case "]":
                if len(packet_list) > 1:
                    packet_list[-2].append(packet_list.pop())
            case ",":
                pass
            case _:
                new_int: str = char
                while row[i + 1].isdigit():
                    i += 1
                    new_int += row[i]
                packet_list[-1].append(int(new_int))
        i += 1
    return packet_list[-1]


def get_packet_pairs(file_name: str) -> Generator[Tuple[Packet, Packet], None, None]:
    packets: List[Packet] = []
    for row in get_parsed_input_list(file_name, parse_packet_from_row):
        if row is None:
            yield (packets.pop(0), packets.pop(0))
        else:
            assert row is not None
            packets.append(row)
    if len(packets):
        yield (packets.pop(0), packets.pop(0))


def compare(left: Union[int, "Packet"], right: Union[int, "Packet"]) -> PacketState:
    if isinstance(left, int):
        if isinstance(right, int):
            # left and right is int
            left_int: int = int(left)
            right_int: int = int(right)
            if left_int < right_int:
                return PacketState.RIGHT_ORDER
            elif left_int == right_int:
                return PacketState.CONTINUE
            return PacketState.WRONG_ORDER
        else:
            # left is int and right is list
            return compare([left], right)
    elif isinstance(right, list):
        # left is list, right is list
        for pair in zip_longest(left, right):
            if pair[0] == None:
                return PacketState.RIGHT_ORDER
            elif pair[1] == None:
                return PacketState.WRONG_ORDER

            compare_result: PacketState = compare(pair[0], pair[1])
            if compare_result != PacketState.CONTINUE:
                return compare_result

        return PacketState.CONTINUE
    # left is list, right is int
    return compare(left, [right])


def sum_correct_indices(file_name: str) -> int:
    return sum(
        (i + 1 if compare(p[0], p[1]) == PacketState.RIGHT_ORDER else 0)
        for i, p in enumerate(get_packet_pairs(file_name))
    )


def comparator(a: Packet, b: Packet) -> int:
    return compare(a, b).value


def sort_with_extra_packets_and_find_location(
    file_name: str, *extra_packets: Packet
) -> int:
    sorted_packets: List[Packet] = sorted(
        [packet for pair in get_packet_pairs(file_name) for packet in pair]
        + [p for p in extra_packets],
        key=cmp_to_key(comparator),
    )
    return reduce(
        lambda a, b: a * b,
        [
            entry[0] if entry[1] in extra_packets else 1
            for entry in enumerate(sorted_packets, 1)
        ],
    )


print("Example part 1:", sum_correct_indices("src/day_13/example.txt"))
print("Part 1:", sum_correct_indices("src/day_13/input.txt"))

print(
    "Example part 2:",
    sort_with_extra_packets_and_find_location("src/day_13/example.txt", [[2]], [[6]]),
)
print(
    "Part 2:",
    sort_with_extra_packets_and_find_location("src/day_13/input.txt", [[2]], [[6]]),
)
