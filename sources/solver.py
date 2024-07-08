import heapq


def astar(base_grid, size, goal, heuristic):
    space_complexity = 0
    time_complexity = 0

    start = base_grid.index(0)
    y, x = divmod(start, size)

    heap = [(0, y, x, base_grid, [])]
    seen = set()
    best = []

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

        for i, (ny, nx) in enumerate(((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1))):
            if 0 <= ny < size and 0 <= nx < size:
                new_grid = list(grid)
                # Make the move
                new_grid[ny * size + nx], new_grid[y * size + x] = new_grid[y * size + x], new_grid[ny * size + nx]
                new_grid = tuple(new_grid)
                if not new_grid in seen:
                    heapq.heappush(heap, (heuristic(new_grid, size, goal) + depth, ny, nx, new_grid, path + [(ny, nx, "v^><"[i])]))

    return best, time_complexity, space_complexity


# TODO Fix
def biastar(base_grid, size, goal, heuristic):
    space_complexity = 0
    time_complexity = 0
    best = []

    start = base_grid.index(0)
    ay, ax = divmod(start, size)

    aheap = [(0, ay, ax, base_grid, [])]
    aseen = {}

    bstart = goal.index(0)
    by, bx = divmod(bstart, size)

    bheap = [(0, by, bx, goal, [])]
    bseen = {}

    while aheap:
        h, ay, ax, agrid, apath = heapq.heappop(aheap)
        bh, by, bx, bgrid, bpath = heapq.heappop(bheap)

        adepth = len(apath)
        bdepth = len(bpath)

        if bgrid == base_grid:
            print("bgrid == base_grid")
            best = bpath[::-1]
            break

        if agrid == goal:
            print("agrid == goal")
            best = apath
            break


        time_complexity += 1
        space_complexity = max(space_complexity, len(aheap) + len(bheap))

        # Expand path from start
        if not agrid in aseen:
            for i, (ny, nx) in enumerate(((ay + 1, ax), (ay - 1, ax), (ay, ax + 1), (ay, ax - 1))):
                if 0 <= ny < size and 0 <= nx < size:
                    new_grid = list(agrid)
                    new_grid[ny * size + nx], new_grid[ay * size + ax] = new_grid[ay * size + ax], new_grid[ny * size + nx]
                    new_grid = tuple(new_grid)
                    if not new_grid in aseen:
                        heapq.heappush(aheap, (heuristic(new_grid, size, goal) + adepth, ny, nx, new_grid, apath + [(ny, nx, "v^><"[i])]))

            aseen[agrid] = apath

        # Expand path from end
        if not bgrid in bseen:
            for i, (ny, nx) in enumerate(((by + 1, bx), (by - 1, bx), (by, bx + 1), (by, bx - 1))):
                if 0 <= ny < size and 0 <= nx < size:
                    new_grid = list(bgrid)
                    new_grid[ny * size + nx], new_grid[by * size + bx] = new_grid[by * size + bx], new_grid[ny * size + nx]
                    new_grid = tuple(new_grid)
                    if not new_grid in bseen:
                        heapq.heappush(bheap, (heuristic(goal, size, new_grid) + bdepth, ny, nx, new_grid, bpath + [(ny, nx, "v^><"[i])]))

            bseen[bgrid] = bpath

    return best, time_complexity, space_complexity


DEFAULT = "astar"
NAMES = {f.__name__: f for f in (astar, biastar)}
