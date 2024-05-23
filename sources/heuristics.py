from typing import List

# TODO May not be admissible
def manhattan(grid: List[int], size: int, goal: List[int]) -> int:
	res = 0
	coords = {}
	for i, e in enumerate(goal):
		coords[e] = (i // size, i % size)
	for i, e in enumerate(grid):
		cury = i // size
		curx = i % size
		targety, targetx = coords[e]
		res += abs(curx - targetx) + abs(cury - targety)
	return res

# TODO May not be admissible
def squared(grid: List[int], size: int, goal: List[int]) -> int:
	res = 0
	coords = {}
	for i, e in enumerate(goal):
		coords[e] = (i // size, i % size)
	for i, e in enumerate(grid):
		cury = i // size
		curx = i % size
		targety, targetx = coords[e]
		res += (curx - targetx)**2 + (cury - targety)**2
	return res

# TODO May not be admissible
def misplaced(grid: List[int], size: int, goal: List[int]) -> int:
	return sum(a != b for a, b in zip(grid, goal))