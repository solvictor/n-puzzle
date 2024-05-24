from argparse import ArgumentParser, FileType
from typing import List, Tuple, Optional
from math import log10
import heuristics
import generator
import parsing
import utils
import heapq

def print_puzzle(puzzle, size, header = True):
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
	best = []

	while heap:
		h, y, x, grid, path = heapq.heappop(heap)
		depth = len(path)

		if grid in seen:
			continue

		if grid == goal:
			best = path
			break

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
	
	print(f"{time_complexity = }\n{space_complexity = }")
	return best

def biastar_solve(base_grid, size, goal, heuristic):
	space_complexity = 0
	time_complexity = 0
	best = []

	start = base_grid.index(0)
	ay = start // size
	ax = start % size

	aheap = [(0, ay, ax, base_grid, [])]
	aseen = {}

	bstart = goal.index(0)
	by = bstart // size
	bx = bstart % size

	bheap = [(0, by, bx, goal, [])]
	bseen = {}

	while aheap:
		h, ay, ax, agrid, apath = heapq.heappop(aheap)
		bh, by, bx, bgrid, bpath = heapq.heappop(bheap)

		adepth = len(apath)
		bdepth = len(bpath)

		if agrid in bseen:
			print("agrid in bseen", len(apath), len(bseen[agrid]))
			best = apath + bseen[agrid]
			break

		if bgrid in aseen:
			print("bgrid in aseen", len(bpath), len(aseen[bgrid]))
			best = aseen[bgrid] + bpath[::-1]
			break

		if agrid == goal:
			best = apath
			break

		if bgrid == base_grid:
			best = bpath
			break

		time_complexity += 1
		space_complexity = max(space_complexity, len(aheap) + len(bheap))

		# Expand path from start
		if not agrid in aseen:
			for i, (ny, nx) in enumerate(((ay + 1, ax), (ay - 1, ax), (ay, ax + 1), (ay, ax - 1))):
				if 0 <= ny < size and 0 <= nx < size:
					new_grid = list(agrid)
					new_grid[ny * size + nx], new_grid[ay * size + ax] = new_grid[ay * size + ax], new_grid[ny * size + nx]
					new_grid = tuple(new_grid)
					if not new_grid in aseen:
						heapq.heappush(aheap, (heuristic(new_grid, size, goal) + adepth, ny, nx, new_grid, apath + [(ny, nx, "v^><"[i])]))

			aseen[agrid] = apath

		# Expand path from end
		if not bgrid in bseen:
			for i, (ny, nx) in enumerate(((by + 1, bx), (by - 1, bx), (by, bx + 1), (by, bx - 1))):
				if 0 <= ny < size and 0 <= nx < size:
					new_grid = list(bgrid)
					new_grid[ny * size + nx], new_grid[by * size + bx] = new_grid[by * size + bx], new_grid[ny * size + nx]
					new_grid = tuple(new_grid)
					if not new_grid in bseen:
						heapq.heappush(bheap, (heuristic(goal, size, new_grid) + bdepth, ny, nx, new_grid, bpath + [(ny, nx, "v^><"[i])]))

			bseen[bgrid] = bpath
	
	print(f"{time_complexity = }\n{space_complexity = }")
	return best


if __name__ == "__main__":
	parser = ArgumentParser(
		prog="n-puzzle",
		description="Solve n-puzzles"
	)

	group = parser.add_mutually_exclusive_group(required=True)
	group.add_argument(
		"-g",
		"--generate",
		type=int,
		help="Generate a random puzzle of size NxN",
		metavar="N"
	)
	group.add_argument(
		"puzzle_path",
		nargs="?",
		type=FileType('r'),
		default=None,
		help="Path for the puzzle file"
	)

	args = parser.parse_args()

	if args.generate is None:
		raw_puzzle = parsing.deserialize_puzzle(args.puzzle_path)
		size, puzzle = parsing.parse_puzzle(raw_puzzle)
		# TODO Check for solvability
		if not utils.is_solvable(puzzle, size):
			utils.error("Puzzle is not solvable")
	else:
		size = args.generate
		if size < 2:
			utils.error(f"Cannot generate a puzzle of {size}x{size}")
		puzzle = generator.generate(size)
	goal = generator.make_goal(size)
	print_puzzle(puzzle, size)
	print()
	solution = astar_solve(tuple(puzzle), size, tuple(goal), heuristics.squared)
	print(f"{len(solution) = }")
	# for y, x, s in solution:
	# 	print(y, x, s)
	# print_moves(puzzle, size, solution)

