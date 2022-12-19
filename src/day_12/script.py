from __future__ import annotations
from typing import Dict, List, Literal
from ..utils.input import get_input_list


class Square:
    def __init__(self, elevation: str, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.elevation = elevation
        self.elevation_value = self.__get_elevation_value(elevation)
        self.path: List[Square] = [self]

    def __get_elevation_value(self, elevation: str) -> int:
        match elevation:
            case "S":
                return ord("a")
            case "E":
                return ord("z")
        return ord(elevation)

    def equals(self, other: Square) -> bool:
        return self.x == other.x and self.y == other.y

    def get_options(self, height_map: List[List[Square]]) -> List[Square]:
        """
        Returns a list of neighbours that we can move to:
        1. correct elevation
        2. not already in our path
        3. has no path or a longer path to it
        4. we are not already at the end
        """

        if self.elevation == "E":
            return []

        dimensions: Dict[str, int] = {
            "height": len(height_map),
            "width": len(height_map[0]),
        }

        options: List[Square] = []
        for direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_x, new_y = (self.x + direction[0], self.y + direction[1])
            if (
                new_x > -1
                and new_x < dimensions["width"]
                and new_y > -1
                and new_y < dimensions["height"]
            ):
                neighbour: Square = height_map[new_y][new_x]
                if (
                    self.__can_move_to(neighbour)
                    and self.__has_no_or_longer_path(neighbour)
                    and not self.__is_already_in_path(neighbour)
                ):
                    options.append(neighbour)

        return options

    def __can_move_to(self, other: Square) -> bool:
        return (
            self.elevation_value >= other.elevation_value
            or other.elevation_value - self.elevation_value == 1
        )

    # honestly, I should probably not search the path everytime and do something
    # with a visited boolean, but eh
    def __is_already_in_path(self, other: Square) -> bool:
        return any(s.equals(other) for s in self.path)

    def __has_no_or_longer_path(self, other: Square) -> bool:
        return len(other.path) == 1 or len(other.path) > len(self.path) + 1

    def handle_move_to(self, other: Square) -> None:
        other.path = self.path[:] + [other]


def get_height_map(file_name: str) -> List[List[Square]]:
    return_list: List[List[Square]] = []

    for y, row in enumerate(get_input_list(file_name)):
        new_row: List[Square] = []
        return_list.append(new_row)
        for x, col in enumerate(row):
            new_row.append(Square(col, x, y))

    return return_list


def find_start_or_end(
    height_map: List[List[Square]], elevation: Literal["E", "S"]
) -> Square:
    for row in height_map:
        for square in row:
            if square.elevation == elevation:
                return square
    raise Exception("Yeah, couldn't find that")


def find_shortest_path_to_end(file_name: str) -> List[Square]:
    height_map: List[List[Square]] = get_height_map(file_name)
    walk_to_end(height_map, [find_start_or_end(height_map, "S")])
    return find_start_or_end(height_map, "E").path


# gonna be lazy here and unparse every time and not do anything cool
def find_shortest_path_length_from_any_a(file_name: str) -> int:
    lengths: List[int] = []
    for y, row in enumerate(get_input_list(file_name)):
        for x, col in enumerate(row):
            if col == "a" or col == "S":
                height_map: List[List[Square]] = get_height_map(file_name)
                found_path_to_E: bool = walk_to_end(height_map, [height_map[y][x]])
                if found_path_to_E:
                    lengths.append(len(find_start_or_end(height_map, "E").path))
    return sorted(lengths)[0] - 1


def walk_to_end(height_map: List[List[Square]], squares: List[Square]) -> bool:
    """
    BFS for a path from the squares to E, will return True if a path has been found,
    else False
    """

    if not len(squares):
        return False

    new_squares: List[Square] = []
    for square in squares:
        if square.elevation == "E":
            return True
        for option in square.get_options(height_map):
            square.handle_move_to(option)
            new_squares.append(option)
    return walk_to_end(height_map, new_squares)


print(
    "Example part 1: ",
    len(find_shortest_path_to_end("src/day_12/example.txt")) - 1,
)
print(
    "Part 1: ",
    len(find_shortest_path_to_end("src/day_12/input.txt")) - 1,
),

print(
    "Example part 2: ",
    find_shortest_path_length_from_any_a("src/day_12/example.txt"),
)
print(
    "Part 2: ",
    find_shortest_path_length_from_any_a("src/day_12/input.txt"),
),
