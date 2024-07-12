from typing import List


def manhattan(grid: List[int], width: int, gpos) -> int:
    res = 0
    for i, e in enumerate(grid):
        if e == 0:
            continue
        cury, curx = divmod(i, width)
        targety, targetx = gpos[e]
        res += abs(curx - targetx) + abs(cury - targety)
    return res


def euclidean(grid: List[int], width: int, gpos) -> int:
    res = 0
    for i, e in enumerate(grid):
        if e == 0:
            continue
        cury, curx = divmod(i, width)
        targety, targetx = gpos[e]
        res += (curx - targetx)**2 + (cury - targety)**2
    return res


def chebyshev(grid: List[int], width: int, gpos) -> int:
    res = 0
    for i, e in enumerate(grid):
        if e == 0:
            continue
        cury, curx = divmod(i, width)
        targety, targetx = gpos[e]
        res += max(abs(curx - targetx), abs(cury - targety))
    return res


def misplaced(grid: List[int], width: int, gpos) -> int:
    return sum(divmod(i, width) != gpos[e] for i, e in enumerate(grid) if e)


def manhattan_with_lc(grid: List[int], width: int, gpos) -> int:
    lc = 0  # Linear conflics
    return manhattan(grid, width, gpos) + 2 * lc


DEFAULT = "euclidean"
NAMES = {f.__name__: f for f in (manhattan, euclidean, misplaced, chebyshev)}
