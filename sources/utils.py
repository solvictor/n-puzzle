from typing import List, Tuple
import sys


# TODO Check if solvable
def is_solvable(puzzle: List[int], size: int) -> bool:
	"""Checks whether a given puzzle is solvable

	Args:
		puzzle (List[int]): Puzzle
		size (int): Number of rows/columns in the puzzle

	Returns:
		bool: Solvability of the puzzle
	"""
	return True

def error(*args, **kwargs):
	"""Output an error message on standart error and exit with error code"""
	print(*args, **kwargs, file=sys.stderr)
	exit(1)
