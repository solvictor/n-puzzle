import heapq
import utils


def moves(y, x, height, width):
    return (
        (ny, nx, s) 
        for ny, nx, s in ((y + 1, x, 'v'), (y - 1, x, '^'), (y, x + 1, '>'), (y, x - 1, '<')) 
        if 0 <= ny < height and 0 <= nx < width
        )


def astar(base_grid, height, width, goal, heuristic, use_g=True, use_h=True):
    space_complexity = 1
    time_complexity = 0
    best = ""

    start = base_grid.index(0)
    y, x = divmod(start, width)

    gpos = [-1] * (height * width)
    for i, e in enumerate(goal):
        gpos[e] = divmod(i, width)
    gpos = tuple(gpos)

    heap = [(0, y, x, base_grid, str())]
    seen = {}

    while heap:
        h, y, x, grid, path = heapq.heappop(heap)
        depth = len(path)

        if grid == goal:
            best = path
            break

        if grid in seen and seen[grid] < depth:
            continue

        seen[grid] = depth

        time_complexity += 1
        space_complexity = max(space_complexity, len(heap) + len(seen))


        for ny, nx, s in moves(y, x, height, width):
            new_grid = list(grid)
            # Make the move
            new_grid[ny * width + nx], new_grid[y * width + x] = new_grid[y * width + x], new_grid[ny * width + nx]
            new_grid = tuple(new_grid)
            if not new_grid in seen or depth <= seen[new_grid]:
                g_cost = depth if use_g else 0
                h_cost = heuristic(new_grid, width, gpos) if use_h else 0
                heapq.heappush(heap, (h_cost + g_cost, ny, nx, new_grid, path + s))

    return best, time_complexity, space_complexity


def bd_astar(base_grid, height, width, goal, heuristic, use_g=True, use_h=True):
    space_complexity = 2
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
        space_complexity = max(space_complexity, len(aheap) + len(bheap) + len(aseen) + len(bseen))

        # Expand path from start
        if not agrid in aseen:
            for ny, nx, s in moves(ay, ax, height, width):
                new_grid = list(agrid)
                new_grid[ny * width + nx], new_grid[ay * width + ax] = new_grid[ay * width + ax], new_grid[ny * width + nx]
                new_grid = tuple(new_grid)
                if not new_grid in aseen:
                    g_cost = adepth if use_g else 0
                    h_cost = heuristic(new_grid, width, gpos) if use_h else 0
                    heapq.heappush(aheap, (h_cost + g_cost, ny, nx, new_grid, apath + s))

            aseen[agrid] = apath

        # Expand path from end
        if not bgrid in bseen:
            for ny, nx, s in moves(by, bx, height, width):
                new_grid = list(bgrid)
                new_grid[ny * width + nx], new_grid[by * width + bx] = new_grid[by * width + bx], new_grid[ny * width + nx]
                new_grid = tuple(new_grid)
                if not new_grid in bseen:
                    g_cost = bdepth if use_g else 0
                    h_cost = heuristic(new_grid, width, bpos) if use_h else 0
                    heapq.heappush(bheap, (h_cost + g_cost, ny, nx, new_grid, bpath + s))

            bseen[bgrid] = bpath

    return best, time_complexity, space_complexity


def greedy(base_grid, height, width, goal, heuristic):
    return astar(base_grid, height, width, goal, heuristic, use_g=False, use_h=True)


def uniform_cost(base_grid, height, width, goal, heuristic):
    return astar(base_grid, height, width, goal, heuristic, use_g=True, use_h=False)


def bd_greedy(base_grid, height, width, goal, heuristic):
    return bd_astar(base_grid, height, width, goal, heuristic, use_g=False, use_h=True)


def bd_uniform_cost(base_grid, height, width, goal, heuristic):
    return bd_astar(base_grid, height, width, goal, heuristic, use_g=True, use_h=False)


# TODO Ida abd bd-Ida solvers

DEFAULT = "astar"
NAMES = {f.__name__: f for f in (astar, greedy, uniform_cost, bd_astar, bd_greedy, bd_uniform_cost)}
