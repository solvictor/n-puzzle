from typing import List
from math import log10
import sys


def inversions(puzzle: List[int], goal: List[int], size: int) -> int:
    """Get the number of inversions of a puzzle

    Args:
        puzzle (List[int]): Puzzle initial state
        goal (List[int]): Puzzle final state
        size (int): Number of rows/columns in the puzzle

    Returns:
        int: Number of inmversions
    """
    return 0


# TODO Check if solvable
def is_solvable(puzzle: List[int], goal: List[int], size: int) -> bool:
    """Checks whether a given puzzle is solvable

    Args:
        puzzle (List[int]): Puzzle initial state
        goal (List[int]): Puzzle final state
        size (int): Number of rows/columns in the puzzle

    Returns:
        bool: Solvability of the puzzle
    """
    return True
    inv = inversions(puzzle, goal, size)
    if size & 1:
        return inv & 1 == 0
    starty = puzzle.index(0) // size
    return inv & 1 != starty & 1


def error(*args, **kwargs):
    """Output an error message on standart error and exit with error code"""
    print(*args, **kwargs, file=sys.stderr)
    exit(1)


def print_puzzle(puzzle, size, header=True):
    formatted_puzzle = ""
    element_format = "{:>" + str(int(log10(size * size) + 1)) + "}"
    for line in range(0, len(puzzle), size):
        if line:
            formatted_puzzle += '\n'
        formatted_puzzle += ' '.join(map(element_format.format, puzzle[line: line + size]))
    if header:
        print(f"Puzzle {size}x{size}")
    print(formatted_puzzle)


def print_moves(puzzle, size, moves):
    puzzle = list(puzzle)
    print_puzzle(puzzle, size)
    print()
    start = puzzle.index(0)
    y, x = divmod(start, size)
    for ny, nx, s in moves:
        print(s)
        puzzle[ny * size + nx], puzzle[y * size + x] = puzzle[y * size + x], puzzle[ny * size + nx]
        y, x = ny, nx
        print_puzzle(puzzle, size, False)
        print()
