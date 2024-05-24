from typing import List
import random

def generate(size: int, iterations: int = 50) -> List[int]:
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
