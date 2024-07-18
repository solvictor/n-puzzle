from typing import List
import math


def manhattan(grid: List[int], width: int, gpos) -> float:
    res = 0
    for i, e in enumerate(grid):
        if e == 0:
            continue
        cury, curx = divmod(i, width)
        targety, targetx = gpos[e]
        res += abs(curx - targetx) + abs(cury - targety)
    return res


def euclidean(grid: List[int], width: int, gpos) -> float:
    res = 0
    for i, e in enumerate(grid):
        if e == 0:
            continue
        cury, curx = divmod(i, width)
        targety, targetx = gpos[e]
        res += math.hypot(curx - targetx, cury - targety)
    return res


def chebyshev(grid: List[int], width: int, gpos) -> float:
    res = 0
    for i, e in enumerate(grid):
        if e == 0:
            continue
        cury, curx = divmod(i, width)
        targety, targetx = gpos[e]
        res += max(abs(curx - targetx), abs(cury - targety))
    return res


def misplaced(grid: List[int], width: int, gpos) -> float:
    return sum(divmod(i, width) != gpos[e] for i, e in enumerate(grid) if e)


def manhattan_with_lc(grid: List[int], width: int, gpos) -> float:
    lc = 0  # Linear conflics
    return manhattan(grid, width, gpos) + 2 * lc

# TODO Pattern database


DEFAULT = "euclidean"
NAMES = {f.__name__: f for f in (manhattan, euclidean, misplaced, chebyshev)}
