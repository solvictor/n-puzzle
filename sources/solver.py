from argparse import ArgumentParser
import parsing
import utils
from typing import List, Tuple, Optional
import heapq
from math import log10
import heuristics

def print_puzzle(puzzle, size, header = True):
	formatted_puzzle = ""
	element_format = "{:<" + str(int(log10(size * size) + 1)) + "}"
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
	y = start // size
	x = start % size
	for ny, nx, s in moves:
		print(s)
		puzzle[ny * size + nx], puzzle[y * size + x] = puzzle[y * size + x], puzzle[ny * size + nx]
		y, x = ny, nx
		print_puzzle(puzzle, size, header = False)
		print()

def astar_solve(base_grid, size, goal, heuristic):
	space_complexity = 0
	time_complexity = 0

	start = base_grid.index(0)
	y = start // size
	x = start % size

	heap = [(0, y, x, base_grid, [])]
	seen = set()

	while heap:
		h, y, x, grid, path = heapq.heappop(heap)
		depth = len(path)

		if grid in seen:
			continue

		if grid == goal:
			return path

		time_complexity += 1
		space_complexity = max(space_complexity, len(heap))

		seen.add(grid)

		for i, (ny, nx) in enumerate(((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1))):
			if 0 <= ny < size and 0 <= nx < size:
				new_grid = list(grid)
				# Make the move
				new_grid[ny * size + nx], new_grid[y * size + x] = new_grid[y * size + x], new_grid[ny * size + nx]
				new_grid = tuple(new_grid)
				if not new_grid in seen:
					heapq.heappush(heap, (heuristic(new_grid, size, goal) + depth, ny, nx, new_grid, path + [(ny, nx, "v^><"[i])]))

	return []

if __name__ == "__main__":
	parser = ArgumentParser(
				prog="n-puzzle",
				description="Solve n-puzzles"
	)

	parser.add_argument("puzzle_path", help="Path for the puzzle file")
	args = parser.parse_args()

	raw_puzzle = parsing.deserialize_puzzle(args.puzzle_path)
	# TODO Check for solvability
	size, puzzle = parsing.parse_puzzle(raw_puzzle)
	if utils.is_solvable(puzzle, size):
		goal = utils.get_goal(size)
		print_puzzle(puzzle, size)
		print()
		solution = astar_solve(tuple(puzzle), size, goal, heuristics.squared)
		print(f"{len(solution) = }")
		# for y, x, s in solution:
		# 	print(y, x, s)
		print_moves(puzzle, size, solution)
	else:
		utils.error("Grid is not solvable")
