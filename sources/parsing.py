from typing import List, Tuple
from io import TextIOWrapper

def deserialize_puzzle(puzzle_file: TextIOWrapper) -> List[str]:
	"""Extracts the puzzle from the puzzle file

	Args:
		puzzle_file (TextIOWrapper): Opened puzzle file

	Returns:
		List[str]: Lines of the puzzle file
	"""
	raw_puzzle = []
	for line in puzzle_file:
		comment = line.find('#')
		if comment != -1:
			line = line[:comment]
		line = line.strip().split()
		if line:
			raw_puzzle.extend(line)
	puzzle_file.close()
	return raw_puzzle

def parse_puzzle(raw_puzzle: List[str]) -> Tuple[int, List[int]]:
	"""Convert the 2d puzzle to a 1d grid and checks if it is valid

	Args:
		raw_puzzle (List[str]): Puzzle to parse

	Raises:
		Exception: If puzzle contains anything that is not a positive number >= 0
		Exception: If puzzle is empty
		Exception: If puzzle has invalid dimensions
		Exception: If puzzle contains invalid elements
		Exception: If puzzle has duplicates

	Returns:
		Tuple[int, List[int]]: Size and parsed puzzle
	"""
	if not all(e.isdigit() for e in raw_puzzle):
		raise Exception("Puzzle must be made of numbers only")

	if not raw_puzzle:
		raise Exception("Puzzle cannot be empty")
	
	size, *puzzle = map(int, raw_puzzle)

	if len(puzzle) != size * size:
		raise Exception(f"Invalid dimensions, expected {size}x{size}")

	invalid_elements = [e for e in puzzle if not 0 <= e < size * size]
	if invalid_elements:
		raise Exception(f"Invalid element{'s' if len(invalid_elements) > 1 else ''} found for a {size}x{size} puzzle: {invalid_elements}")

	if len(set(puzzle)) != size * size:
		raise Exception("Puzzle cannot contains duplicates")

	return size, puzzle
