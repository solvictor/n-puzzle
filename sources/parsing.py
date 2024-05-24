from typing import List, Tuple
from io import TextIOWrapper

def deserialize_puzzle(puzzle_file: TextIOWrapper) -> List[str]:
	raw_puzzle = []
	for line in puzzle_file:
		comment = line.find('#')
		if comment != -1:
			line = line[:comment]
		line = line.strip().split()
		if line:
			raw_puzzle.extend(line)
	return raw_puzzle

def parse_puzzle(raw_puzzle: List[str]) -> Tuple[int, List[int]]:
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
