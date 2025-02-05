from typing import List, Tuple
from io import TextIOWrapper


def deserialize_puzzle(puzzle_file: TextIOWrapper) -> List[List[str]]:
    """Extracts the puzzle from the puzzle file

    Args:
        puzzle_file (TextIOWrapper): Opened puzzle file

    Returns:
        List[List[str]]: Lines of the puzzle file
    """

    raw_puzzle = []
    for line in puzzle_file:
        comment = line.find("#")
        if comment != -1:
            line = line[:comment]
        line = line.split()
        if line:
            raw_puzzle.append(line)
    puzzle_file.close()
    return raw_puzzle


def parse_dimensions(header: str) -> Tuple[int, int]:
    """Get the dimensions from string formatted as either "N" or "NxM"
    with N and M positive integers

    Args:
        header (str): Dimensiosn

    Raises:
        SyntaxError: If header is bad formatted

    Returns:
        Tuple[int, int]: Height and width
    """

    try:
        height = width = header
        if header.count("x") == 1:
            height, width = header.split("x")
        assert height.isdigit() and width.isdigit()
        return int(height), int(width)
    except Exception:
        raise SyntaxError("Invalid header format. Must be N or NxM")


def parse_puzzle(raw_puzzle: List[List[str]]) -> Tuple[int, int, List[int]]:
    """Convert the 2d puzzle to a 1d grid and checks if it is valid

    Args:
        raw_puzzle (List[List[str]]): Puzzle to parse

    Raises:
        Exception: If puzzle contains anything that is not a positive number >= 0
        Exception: If puzzle is empty
        Exception: If puzzle has invalid dimensions
        Exception: If puzzle contains invalid elements
        Exception: If puzzle has duplicates

    Returns:
        Tuple[int, int, List[int]]: Size and parsed puzzle
    """

    if not raw_puzzle:
        raise Exception("Puzzle cannot be empty")

    try:
        header = raw_puzzle[0]
        assert len(header) == 1
        height, width = parse_dimensions(header[0])
    except Exception:
        raise SyntaxError("Invalid header format. Must be N or NxM")

    puzzle = sum(raw_puzzle[1:], [])
    if not all(e.isdigit() for e in puzzle):
        raise Exception("Puzzle must be made of numbers only")

    puzzle = list(map(int, puzzle))

    if len(puzzle) != height * width:
        raise Exception(f"Invalid dimensions, expected {height}x{width}")

    invalid_elements = [e for e in puzzle if not 0 <= e < height * width]
    if invalid_elements:
        raise Exception(
            f"Invalid element{'s' if len(invalid_elements) > 1 else ''} found for a {height}x{width} puzzle: {invalid_elements}"
        )

    if len(set(puzzle)) != height * width:
        raise Exception("Puzzle cannot contains duplicates")

    return height, width, puzzle
