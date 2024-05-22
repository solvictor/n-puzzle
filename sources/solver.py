from argparse import ArgumentParser
from typing import List
import sys
import heapq
from collections import deque
from math import log10

def error(*args, **kwargs):
	print(*args, **kwargs, file=sys.stderr)
	exit(1)

def rinttt(puzzle, size):
	formatted_puzzle = ""
	element_format = "{:<" + str(int(log10(size * size) + 1)) + "}"
	for line in range(0, len(puzzle), size):
		if line:
			formatted_puzzle += '\n'
		formatted_puzzle += ' '.join(map(element_format.format, puzzle[line: line + size]))
	print(f"Puzzle {size}x{size}\n{formatted_puzzle}")

class Puzzle:
	def __init__(self, puzzle: List[int]) -> None:
		self.check_valid(puzzle)
		self.size = puzzle[0][0]
		self.puzzle = sum(puzzle[1:], [])
		self.solved = False
	
	def check_valid(self, puzzle) -> None:
		if not puzzle or any(not line for line in puzzle):
			raise Exception("Invalid puzzle")
		size = puzzle[0][0]
		puzzle = puzzle[1:]
		if size != len(puzzle) or any(len(line) != size for line in puzzle):
			raise Exception("Invalid puzzle")
		# TODO Dimensions are valid, add solvability check 

	def expand(self, state, h):
		f, d, y, x, puzzle = state
		possibilities = []

		for ny, nx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
			if ny < 0 or ny == self.size or nx < 0 or nx == self.size:
				continue
			updated_puzzle = list(puzzle)
			updated_puzzle[y * self.size + x], updated_puzzle[ny * self.size + nx] = updated_puzzle[ny * self.size + nx], updated_puzzle[y * self.size + x]
			possibilities.append((h(), d + 1, ny, nx, tuple(updated_puzzle)))

		return possibilities

	def solve(self, h) -> None:
		idx = self.puzzle.index(0)
		y = idx // self.size
		x = idx % self.size
		initial_state = (0, 0, y, x, tuple(self.puzzle))
		heap = deque()
		heap.append(initial_state)
		success = False

		while heap and not success:
			f, d, y, x, puzzle = state = heapq.heappop(heap)
			if all(i == e for i, e in enumerate(puzzle)): # if is_final
				success = True
			else:
				for substate in self.expand(state, h):
					heapq.heappush(heap, substate)

		if not success:
			raise Exception("Failed to solve")

	def __repr__(self) -> str:
		formatted_puzzle = ""
		element_format = "{:<" + str(int(log10(self.size * self.size) + 1)) + "}"
		for line in range(0, len(self.puzzle), self.size):
			if line:
				formatted_puzzle += '\n'
			formatted_puzzle += ' '.join(map(element_format.format, self.puzzle[line: line + self.size]))
		return f"Puzzle {self.size}x{self.size}\n{formatted_puzzle}"

def deserialize_puzzle(path: str) -> List[int]:
	raw_puzzle = []
	with open(path) as puzzle_file:
		for line in puzzle_file:
			line = line.strip()
			comment = line.find('#')
			if comment != -1:
				line = line[:comment]
			if line:
				raw_puzzle.append(list(map(int, line.split())))
	return raw_puzzle

def bad_place(state):
	f, d, y, x, puzzle = state
	return sum(i != e for i, e in enumerate(puzzle))

if __name__ == "__main__":
	parser = ArgumentParser(
                prog="n-puzzle",
                description="Solve n-puzzles"
	)

	parser.add_argument("puzzle_path", help="Path for the puzzle file")
	args = parser.parse_args()

	raw_puzzle = deserialize_puzzle(args.puzzle_path)
	puzzle = Puzzle(raw_puzzle)
	puzzle.solve(bad_place)
	print(puzzle)
	# try:
	# 	raw_puzzle = deserialize_puzzle(args.puzzle_path)
	# 	puzzle = Puzzle(raw_puzzle)
	# 	puzzle.solve(bad_place)
	# 	print(puzzle)
	# except Exception as ex:
	# 	print(f"Error: {ex}", file = sys.stderr)
	# 	exit(1)
