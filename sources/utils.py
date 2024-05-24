from typing import List, Tuple
import sys


# TODO Check if solvable
def is_solvable(puzzle: List[int], size: int) -> bool:
	return True

def error(*args, **kwargs):
	print(*args, **kwargs, file=sys.stderr)
	exit(1)
