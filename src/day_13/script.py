# from __future__ import annotations
from typing import Generator, List, Optional, Tuple, Union
from ..utils.input import get_parsed_input_list


Packet = List[Union[int, "Packet"]]


def parse_packet_from_row(row: str) -> Optional[Packet]:
    if not len(row):
        return None
    parent_packet: Optional[Packet] = None
    current_packet: Optional[Packet] = None
    for char in row:
        match char:
            case "[":
                if current_packet:
                    parent_packet = current_packet
                    current_packet = []
                    parent_packet.append(current_packet)
                else:
                    current_packet = []
                    # parent_packet = current_packet
                continue
            case "]":
                assert current_packet is not None
                if parent_packet:
                    # parent_packet.append(current_packet)
                    current_packet = parent_packet
                continue
            case ",":
                continue
            case _:
                assert current_packet is not None
                current_packet.append(int(char))
                continue
    return current_packet


def get_packet_pairs(file_name: str) -> Generator[Tuple[Packet, Packet], None, None]:
    packets: List[Packet] = []
    for row in get_parsed_input_list(file_name, parse_packet_from_row):
        if row is None:
            yield (packets.pop(0), packets.pop(0))
        else:
            assert row is not None
            packets.append(row)


for p in get_packet_pairs("src/day_13/example.txt"):
    print(p)
