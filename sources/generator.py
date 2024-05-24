from typing import List
import random
import utils

def generate(size: int, iterations: int = 10000) -> List[int]:
	"""Generate a random solvable size x size puzzle

	Args:
		size (int): Number of rows/columns in the puzzle
		iterations (int, optional): Number of times the puzzle is shuffled. Defaults to 10000.

	Returns:
		List[int]: A random puzzle
	"""

	if size < 2:
		utils.error(f"Cannot generate a puzzle of {size}x{size}")

	def swap_empty(puzzle, idx):
		poss = []
		if idx % size > 0:
			poss.append(idx - 1)
		if idx % size < size - 1:
			poss.append(idx + 1)
		if idx / size > 0 and idx - size >= 0:
			poss.append(idx - size)
		if idx / size < size - 1:
			poss.append(idx + size)
		swi = random.choice(poss)
		puzzle[idx] = puzzle[swi]
		puzzle[swi] = 0
		return swi

	puzzle = make_goal(size)
	zero_idx = puzzle.index(0)
	for _ in range(iterations):
		zero_idx = swap_empty(puzzle, zero_idx)

	return puzzle

def make_goal(size: int) -> List[int]:
	"""Generate a goal (solved) size x size puzzle

	Args:
		size (int): Number of rows/columns in the puzzle

	Returns:
		List[int]: Goal puzzle
	"""
	goal = [0] * (size * size)
	y = x = 0
	dy, dx = 0, 1

	for i in range(size * size - 1):
		goal[y * size + x] = i + 1
		ny, nx = y + dy, x + dx
		if ny < 0 or ny == size or nx < 0 or nx == size or goal[ny * size + nx]:
			dy, dx = dx, -dy
		y += dy
		x += dx

	return goal
