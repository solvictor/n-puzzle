import heapq
import utils


def astar(base_grid, height, width, goal, heuristic):
    space_complexity = 0
    time_complexity = 0
    best = ""

    start = base_grid.index(0)
    y, x = divmod(start, width)

    gpos = [-1] * (height * width)
    for i, e in enumerate(goal):
        gpos[e] = divmod(i, width)
    gpos = tuple(gpos)

    heap = [(0, y, x, base_grid, str())]
    seen = set()

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
            if 0 <= ny < height and 0 <= nx < width:
                new_grid = list(grid)
                # Make the move
                new_grid[ny * width + nx], new_grid[y * width + x] = new_grid[y * width + x], new_grid[ny * width + nx]
                new_grid = tuple(new_grid)
                if not new_grid in seen:
                    heapq.heappush(heap, (heuristic(new_grid, width, gpos) + depth, ny, nx, new_grid, path + s))

    return best, time_complexity, space_complexity


def bdastar(base_grid, height, width, goal, heuristic):
    space_complexity = 0
    time_complexity = 0
    best = ""

    astart = base_grid.index(0)
    ay, ax = divmod(astart, width)

    gpos = [-1] * (height * width)
    for i, e in enumerate(goal):
        gpos[e] = divmod(i, width)
    gpos = tuple(gpos)

    aheap = [(0, ay, ax, base_grid, str())]
    aseen = {}

    bstart = goal.index(0)
    by, bx = divmod(bstart, width)

    bpos = [-1] * (height * width)
    for i, e in enumerate(base_grid):
        bpos[e] = divmod(i, width)
    bpos = tuple(bpos)

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
        if not agrid in aseen:
            for ny, nx, s in ((ay + 1, ax, 'v'), (ay - 1, ax, '^'), (ay, ax + 1, '>'), (ay, ax - 1, '<')):
                if 0 <= ny < height and 0 <= nx < width:
                    new_grid = list(agrid)
                    new_grid[ny * width + nx], new_grid[ay * width + ax] = new_grid[ay * width + ax], new_grid[ny * width + nx]
                    new_grid = tuple(new_grid)
                    if not new_grid in aseen:
                        heapq.heappush(aheap, (heuristic(new_grid, width, gpos) + adepth, ny, nx, new_grid, apath + s))

            aseen[agrid] = apath

        # Expand path from end
        if not bgrid in bseen:
            for ny, nx, s in ((by + 1, bx, 'v'), (by - 1, bx, '^'), (by, bx + 1, '>'), (by, bx - 1, '<')):
                if 0 <= ny < height and 0 <= nx < width:
                    new_grid = list(bgrid)
                    new_grid[ny * width + nx], new_grid[by * width + bx] = new_grid[by * width + bx], new_grid[ny * width + nx]
                    new_grid = tuple(new_grid)
                    if not new_grid in bseen:
                        heapq.heappush(bheap, (heuristic(new_grid, width, bpos) + bdepth, ny, nx, new_grid, bpath + s))

            bseen[bgrid] = bpath

    return best, time_complexity, space_complexity


DEFAULT = "astar"
NAMES = {f.__name__: f for f in (astar, bdastar)}
