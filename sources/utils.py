from typing import List, Tuple
import sys


# TODO Check if solvable
def is_solvable(puzzle: List[int], size: int) -> bool:
	return True

def error(*args, **kwargs):
	print(*args, **kwargs, file=sys.stderr)
	exit(1)

def get_goal(size: int) -> Tuple[int, ...]:
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

	return tuple(goal)
