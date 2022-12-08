from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum
from typing import Callable, List, Optional, TypeVar
from ..utils.input import get_input_list


T = TypeVar("T")


class FileType(Enum):
    FILE = 1
    DIRECTORY = 2


class AbstractFile(ABC):
    @staticmethod
    def parse(split_line: List[str]) -> AbstractFile:
        if split_line[0] == "dir":
            return Directory(split_line[1])

        return File(split_line[1], int(split_line[0]))

    def __init__(self, fileType: FileType, name: str) -> None:
        self.parent: AbstractFile
        self.fileType = fileType
        self.children: List[AbstractFile] = []
        self.name = name

    @abstractmethod
    def add_child(self, child: AbstractFile) -> None:
        pass

    @abstractmethod
    def size(self) -> int:
        pass

    def find_first_child(
        self, callback: Callable[[AbstractFile], bool]
    ) -> Optional[AbstractFile]:
        """
        Gets first child that matches the callback, if it exists
        """

        for child in self.children:
            if callback(child):
                return child
        return None

    def iterate_down(self, callback: Callable[[AbstractFile, T], T], result: T) -> T:
        """
        Iterates down depth first and returns the result
        """

        result = callback(self, result)
        for child in self.children:
            result = child.iterate_down(callback, result)
        return result


class File(AbstractFile):
    def __init__(self, file_name: str, file_size: int) -> None:
        super().__init__(FileType.FILE, file_name)
        self.file_size = file_size

    def add_child(self, child: AbstractFile) -> None:
        pass

    def size(self) -> int:
        return self.file_size


class Directory(AbstractFile):
    def __init__(self, directory_name: str) -> None:
        super().__init__(FileType.DIRECTORY, directory_name)
        self.directory_size = 0

    def add_child(self, child: AbstractFile) -> None:
        self.children.append(child)
        child.parent = self

    # Yeah, I should really cache and update this somehow so I don't
    # continually run up and down my tree, but it runs and I can't be bothered
    def size(self) -> int:
        return sum(child.size() for child in self.children)


def handle_line(node: AbstractFile, line: str) -> AbstractFile:
    """
    Handles the current line and returns the new contextaskjdhal
    """

    split: List[str] = line.split(" ")

    if split[0] == "$":
        if split[1] == "cd":
            dir_name: str = split[2]
            match dir_name:
                case "/":
                    while node and node.name != "/":
                        node = node.parent
                    return node
                case "..":
                    return node.parent
                case _:
                    matched_child: Optional[AbstractFile] = node.find_first_child(
                        lambda child: child.name == dir_name
                    )
                    if matched_child is None:
                        raise Exception(
                            "No matching child: ", dir_name, " of ", node.name
                        )
                    return matched_child
    else:
        node.add_child(AbstractFile.parse(split))

    return node


def get_tree(file_name: str) -> AbstractFile:
    root: AbstractFile = Directory("/")
    node: AbstractFile = root

    for line in get_input_list(file_name):
        node = handle_line(node, line)

    return root


def total_all_directories_with_size_above_100000(file_name: str) -> int:
    return get_tree(file_name).iterate_down(
        lambda node, total: total + node.size()
        if node.fileType is FileType.DIRECTORY and node.size() < 100000
        else total,
        0,
    )


def find_smallest_directory_to_delete(file_name: str) -> int:
    tree: AbstractFile = get_tree(file_name)
    to_delete: int = 30000000 - (70000000 - tree.size())
    return tree.iterate_down(
        lambda node, current: node
        if node.fileType is FileType.DIRECTORY
        and node.size() < current.size()
        and node.size() >= to_delete
        else current,
        tree,
    ).size()


print("Part 1: ", total_all_directories_with_size_above_100000("src/day_07/input.txt"))
print("Part 2: ", find_smallest_directory_to_delete("src/day_07/input.txt"))
