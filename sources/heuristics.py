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

    # Lines conflicts
    for i, e in enumerate(grid):
        y, x = divmod(i, width)
        if e == 0:
            continue
        ty, tx = gpos[e]
        for k in range(x):
            p = grid[y * width + k]
            if p == 0:
                continue
            ky, kx = gpos[p]
            if ky == ty == y and kx > tx:
                lc += 1

    # Columns conflicts
    for i, e in enumerate(grid):
        y, x = divmod(i, width)
        if e == 0:
            continue
        ty, tx = gpos[e]
        for k in range(y):
            p = grid[k * width + x]
            if p == 0:
                continue
            ky, kx = gpos[p]
            if kx == tx == x and ky > ty:
                lc += 1

    return manhattan(grid, width, gpos) + 2 * lc


def best(grid: List[int], width: int, gpos) -> float:
    return max(heuristic(grid, width, gpos) for heuristic in (euclidean, misplaced, chebyshev, manhattan_with_lc))


# TODO Pattern database
DEFAULT = "euclidean"
NAMES = {f.__name__: f for f in (manhattan, euclidean, misplaced, chebyshev, manhattan_with_lc, best)}
