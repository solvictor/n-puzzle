from typing import List
import random
import utils


def generate(height: int, width: int, iterations: int = 10000) -> List[int]:
    """Generate a random solvable size x size puzzle

    Args:
        height (int): Number of rows in the puzzle
        width (int): Number of columns in the puzzle
        iterations (int, optional): Number of times the puzzle is shuffled. Defaults to 10000.

    Returns:
        List[int]: A random puzzle
    """

    if height * width < 1:
        utils.error(f"Cannot generate a puzzle of {height}x{width}")
    elif height * width == 1:
        return [0]

    def swap_empty(puzzle, idx):
        poss = []
        if idx % width > 0:
            poss.append(idx - 1)
        if idx % width < width - 1:
            poss.append(idx + 1)
        if idx // width > 0:
            poss.append(idx - width)
        if idx // width < height - 1:
            poss.append(idx + width)
        swi = random.choice(poss)
        puzzle[idx] = puzzle[swi]
        puzzle[swi] = 0
        return swi

    puzzle = make_goal(height, width)
    zero_idx = puzzle.index(0)
    for _ in range(iterations):
        zero_idx = swap_empty(puzzle, zero_idx)

    return puzzle


def make_goal(height: int, width: int) -> List[int]:
    """Generate a goal (solved) height x width puzzle

    Args:
        height (int): Number of rows in the puzzle
        width (int): Number of columns in the puzzle

    Returns:
        List[int]: Goal puzzle
    """

    goal = [0] * (height * width)
    y = x = 0
    dy, dx = 0, 1

    for i in range(height * width - 1):
        goal[y * width + x] = i + 1
        ny, nx = y + dy, x + dx
        if ny < 0 or ny == height or nx < 0 or nx == width or goal[ny * width + nx]:
            dy, dx = dx, -dy
        y += dy
        x += dx

    return goal
