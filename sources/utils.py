from typing import List
from math import log10
import sys


def inversions_parity(puzzle: List[int]) -> int:
    """Get the parity of the number of inversions of a puzzle

    Args:
        puzzle (List[int]): Puzzle initial state

    Returns:
        int: Parity of number of inversions
    """

    seen = set()
    inv = 0
    for i in range(len(puzzle)):
        if i in seen:
            continue
        seen.add(i)
        j = puzzle[i]
        while j != i:
            seen.add(j)
            j = puzzle[j]
            inv ^= 1
    return inv


def is_solvable(puzzle: List[int], goal: List[int], height: int, width: int) -> bool:
    """Checks whether a given puzzle is solvable

    Args:
        puzzle (List[int]): Puzzle initial state
        goal (List[int]): Puzzle final state
        height (int): Number of rows in the puzzle
        width (int): Number of columns in the puzzle

    Returns:
        bool: Solvability of the puzzle
    """

    sy, sx = divmod(puzzle.index(0), width)
    parity_empty = (len(puzzle) ^ sy ^ sx ^ 1) & 1
    parity_puzzle = inversions_parity(puzzle)
    parity_goal = inversions_parity(goal)
    return parity_empty == (parity_puzzle ^ parity_goal)


def error(*args, **kwargs):
    """Output an error message on standard error and exit with error code"""
    print(*args, **kwargs, file=sys.stderr)
    exit(1)


def print_puzzle(puzzle: List[int], height: int, width: int, header: bool = True) -> None:
    """Print the puzzle in a convenient format

    Args:
        puzzle (List[int]): Puzzle to print
        height (int): Number of rows in the puzzle
        width (int): Number of columns in the puzzle
        header (bool, optional): Toggle header print. Defaults to True.
    """

    formatted_puzzle = ""
    element_format = "{:>" + str(int(log10(height * width) + 1)) + "}"
    for line in range(0, len(puzzle), width):
        if line:
            formatted_puzzle += '\n'
        formatted_puzzle += ' '.join(map(element_format.format, puzzle[line: line + width]))
    if header:
        print(f"Puzzle {height}x{width}")
    print(formatted_puzzle)


def print_moves(puzzle: List[int], height: int, width: int, moves: str) -> None:
    """Print a move sequence in a convenient format

    Args:
        puzzle (List[int]): Initial puzzle
        height (int): Number of rows in the puzzle
        width (int): Number of columns in the puzzle
        moves (str): Sequence of moves (^v><)
    """

    puzzle = list(puzzle)
    print_puzzle(puzzle, height, width)
    print()
    start = puzzle.index(0)
    y, x = divmod(start, width)
    for s in moves:
        ny = y + (1 if s == 'v' else -1 if s == '^' else 0)
        nx = x + (1 if s == '>' else -1 if s == '<' else 0)
        print(s)
        puzzle[ny * width + nx], puzzle[y * width + x] = puzzle[y * width + x], puzzle[ny * width + nx]
        y, x = ny, nx
        print_puzzle(puzzle, height, width, False)
        print()


def invert_moves(moves: str) -> str:
    """Change each move to the opposite one

    Args:
        moves (str): Moves to invert

    Returns:
        str: Inverted moves
    """

    inv = {'^': 'v', 'v': '^', '<': '>', '>': '<'}
    return ''.join(inv[m] for m in moves)
