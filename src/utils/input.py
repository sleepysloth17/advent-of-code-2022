from typing import Callable, Generator, TypeVar

T = TypeVar("T")


def get_parsed_input_list(
    file_name: str, parsing_func: Callable[[str], T]
) -> Generator[T, None, None]:
    """
    Goes through the input file, runs the parsing func on it and outputs the
    result
    """

    for line in get_input_list(file_name):
        yield parsing_func(line)


def get_input_list(file_name: str) -> Generator[str, None, None]:
    """
    Goes through the input file and outputs each line as it reaches it
    """

    with open(file_name) as input_file:
        for line in input_file:
            yield line
