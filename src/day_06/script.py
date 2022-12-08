from ..utils.input import get_input_list
from itertools import islice


def get_datastream_from_file(file_name: str) -> str:
    return list(islice(get_input_list(file_name), 1))[0]


def find_position_of_marker(datastream: str, chunk_size: int) -> int:
    current_chunk: str = datastream[:chunk_size]
    for i, char in enumerate(datastream[chunk_size:], chunk_size):
        if len(set(current_chunk)) == len(current_chunk):
            return i
        else:
            current_chunk = current_chunk[1:] + char

    return 0


print("Example 1: ", find_position_of_marker("bvwbjplbgvbhsrlpgdmjqwftvncz", 4))
print("Example 2: ", find_position_of_marker("nppdvjthqldpwncqszvftbrmjlhg", 4))
print("Example 3: ", find_position_of_marker("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 4))
print("Example 4: ", find_position_of_marker("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 4))

print(
    "Part 1: ",
    find_position_of_marker(get_datastream_from_file("src/day_06/input.txt"), 4),
)
print(
    "Part 2: ",
    find_position_of_marker(get_datastream_from_file("src/day_06/input.txt"), 14),
)
