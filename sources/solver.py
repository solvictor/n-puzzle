import heapq
import utils


def astar(base_grid, size, goal, heuristic):
    space_complexity = 0
    time_complexity = 0

    start = base_grid.index(0)
    y, x = divmod(start, size)

    heap = [(0, y, x, base_grid, str())]
    seen = set()
    best = ""

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

        for ny, nx, s in ((y + 1, x, 'v'), (y - 1, x, '^'), (y, x + 1, '>'), (y, x - 1, '<')):
            if 0 <= ny < size and 0 <= nx < size:
                new_grid = list(grid)
                # Make the move
                new_grid[ny * size + nx], new_grid[y * size + x] = new_grid[y * size + x], new_grid[ny * size + nx]
                new_grid = tuple(new_grid)
                if not new_grid in seen:
                    heapq.heappush(heap, (heuristic(new_grid, size, goal) + depth, ny, nx, new_grid, path + s))

    return best, time_complexity, space_complexity


def bdastar(base_grid, size, goal, heuristic):
    space_complexity = 0
    time_complexity = 0
    best = ""

    astart = base_grid.index(0)
    ay, ax = divmod(astart, size)

    aheap = [(0, ay, ax, base_grid, str())]
    aseen = {}

    bstart = goal.index(0)
    by, bx = divmod(bstart, size)

    bheap = [(0, by, bx, goal, str())]
    bseen = {}

    while aheap or bheap:
        ah, ay, ax, agrid, apath = heapq.heappop(aheap)
        bh, by, bx, bgrid, bpath = heapq.heappop(bheap)

        adepth = len(apath)
        bdepth = len(bpath)

        if agrid in bseen:
            best = apath + utils.invert_moves(bseen[agrid][::-1])
            break

        if bgrid in aseen:
            best = aseen[bgrid] + utils.invert_moves(bpath[::-1])
            break

        if agrid == goal:
            best = apath
            break

        if bgrid == base_grid:
            best = utils.invert_moves(bpath[::-1])
            break

        if agrid == bgrid:
            best = apath + utils.invert_moves(bpath[::-1])
            break

        time_complexity += 1
        space_complexity = max(space_complexity, len(aheap) + len(bheap))

        # Expand path from start
        if not agrid in aseen or len(aseen[agrid]) >= len(apath):
            for ny, nx, s in ((ay + 1, ax, 'v'), (ay - 1, ax, '^'), (ay, ax + 1, '>'), (ay, ax - 1, '<')):
                if 0 <= ny < size and 0 <= nx < size:
                    new_grid = list(agrid)
                    new_grid[ny * size + nx], new_grid[ay * size + ax] = new_grid[ay * size + ax], new_grid[ny * size + nx]
                    new_grid = tuple(new_grid)
                    if not new_grid in aseen:
                        heapq.heappush(aheap, (heuristic(new_grid, size, goal) + adepth, ny, nx, new_grid, apath + s))

            aseen[agrid] = apath

        # Expand path from end
        if not bgrid in bseen or len(bseen[bgrid]) >= len(bpath):
            for ny, nx, s in ((by + 1, bx, 'v'), (by - 1, bx, '^'), (by, bx + 1, '>'), (by, bx - 1, '<')):
                if 0 <= ny < size and 0 <= nx < size:
                    new_grid = list(bgrid)
                    new_grid[ny * size + nx], new_grid[by * size + bx] = new_grid[by * size + bx], new_grid[ny * size + nx]
                    new_grid = tuple(new_grid)
                    if not new_grid in bseen:
                        heapq.heappush(bheap, (heuristic(goal, size, new_grid) + bdepth, ny, nx, new_grid, bpath + s))

            bseen[bgrid] = bpath

    return best, time_complexity, space_complexity


DEFAULT = "astar"
NAMES = {f.__name__: f for f in (astar, bdastar)}
