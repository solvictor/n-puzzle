from collections import deque
import heapq
from . import utils


def astar(base_grid, height, width, goal, heuristic, use_g=True, use_h=True):
    """
    Get the shortest path from an initial state to a goal state using A* alogrithm

    The A* algorithm combines features of uniform-cost search and pure heuristic search to efficiently find the
    shortest path. It uses a priority queue to explore paths with the lowest estimated cost first, where the
    cost is determined by both the path length (g cost) and the heuristic estimate of the distance to the goal (h cost).

    Steps:
        1. Set the initial state as the current state.
        2. Rank all possible new moves from the current state using the heuristic and path length.
        3. Choose the best state found as the new current state.
        4. If the current state is the goal state, return the path.
        5. Otherwise, continue ranking and exploring new states.


    Args:
        base_grid (Tuple[int, ....]): Initial state
        height (int): Number of rows in the puzzle
        width (int): Number of columns in the puzzle
        goal (Tuple[int, ....]): Goal state
        heuristic (Function): Heuristic function to use
        use_g (bool, optional): Toggle g cost (length of the current path). Defaults to True.
        use_h (bool, optional): Toggle h cost (heuristic of the current grid). Defaults to True.

    Returns:
        Tuple[str, int, int]:
            - Path (str): The sequence of moves to reach the goal.
            - Time complexity (int): The number of states explored.
            - Space complexity (int): The maximum number of states held in memory at any one time.
    """

    space_complexity = 1
    time_complexity = 0
    best = ""

    gpos = [-1] * (height * width)
    for i, e in enumerate(goal):
        gpos[e] = divmod(i, width)
    gpos = tuple(gpos)

    start = base_grid.index(0)
    y, x = divmod(start, width)

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

        for ny, nx, s in utils.moves(y, x, height, width, path[-1] if path else ""):
            new_grid = list(grid)
            # Make the move
            new_grid[ny * width + nx], new_grid[y * width + x] = (
                new_grid[y * width + x],
                new_grid[ny * width + nx],
            )
            new_grid = tuple(new_grid)
            if new_grid not in seen or depth <= seen[new_grid]:
                g_cost = depth if use_g else 0
                h_cost = heuristic(new_grid, width, gpos) if use_h else 0
                heapq.heappush(heap, (h_cost + g_cost, ny, nx, new_grid, path + s))

    return best, time_complexity, space_complexity


def bd_astar(base_grid, height, width, goal, heuristic, use_g=True, use_h=True):
    """
    Get the shortest path from an initial state to a goal state using bidirectional A* alogrithm

    The bidirectional A* algorithm performs two simultaneous searches: one forward from the initial state
    and one backward from the goal state. These searches progress towards each other and meet in the middle,
    potentially reducing the search space and improving performance compared to unidirectional A*.

    Steps:
        1. Initialize both forward and backward searches with the initial and goal states as their current states.
        2. Rank all possible new moves from the current states using heuristic and path length for both searches.
        3. Select the best state found as the new current state for both searches.
        4. If the current states of the forward and backward searches meet, or if either reaches the other's initial state, return the path.
        5. Otherwise, continue ranking and exploring new states.

    Args:
        base_grid (Tuple[int, ....]): Initial state
        height (int): Number of rows in the puzzle
        width (int): Number of columns in the puzzle
        goal (Tuple[int, ....]): Goal state
        heuristic (Function): Heuristic function to use
        use_g (bool, optional): Toggle g cost (length of the current path). Defaults to True.
        use_h (bool, optional): Toggle h cost (heuristic of the current grid). Defaults to True.

    Returns:
        Tuple[str, int, int]:
            - Path (str): The sequence of moves to reach the goal.
            - Time complexity (int): The number of states explored.
            - Space complexity (int): The maximum number of states held in memory at any one time.
    """

    space_complexity = 2
    time_complexity = 0
    best = ""

    gpos = [-1] * (height * width)
    for i, e in enumerate(goal):
        gpos[e] = divmod(i, width)
    gpos = tuple(gpos)

    astart = base_grid.index(0)
    ay, ax = divmod(astart, width)

    aheap = [(0, ay, ax, base_grid, str())]
    aseen = {}

    bpos = [-1] * (height * width)
    for i, e in enumerate(base_grid):
        bpos[e] = divmod(i, width)
    bpos = tuple(bpos)

    bstart = goal.index(0)
    by, bx = divmod(bstart, width)

    bheap = [(0, by, bx, goal, str())]
    bseen = {}

    while aheap and bheap:
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
        if agrid not in aseen or len(aseen[agrid]) >= adepth:
            for ny, nx, s in utils.moves(ay, ax, height, width, apath[-1] if apath else ""):
                new_grid = list(agrid)
                new_grid[ny * width + nx], new_grid[ay * width + ax] = (
                    new_grid[ay * width + ax],
                    new_grid[ny * width + nx],
                )
                new_grid = tuple(new_grid)
                if new_grid not in aseen or len(aseen[new_grid]) >= adepth:
                    g_cost = adepth if use_g else 0
                    h_cost = heuristic(new_grid, width, gpos) if use_h else 0
                    heapq.heappush(aheap, (h_cost + g_cost, ny, nx, new_grid, apath + s))

            aseen[agrid] = apath

        # Expand path from end
        if bgrid not in bseen or len(bseen[bgrid]) >= bdepth:
            for ny, nx, s in utils.moves(by, bx, height, width, bpath[-1] if bpath else ""):
                new_grid = list(bgrid)
                new_grid[ny * width + nx], new_grid[by * width + bx] = (
                    new_grid[by * width + bx],
                    new_grid[ny * width + nx],
                )
                new_grid = tuple(new_grid)
                if new_grid not in bseen or len(bseen[new_grid]) >= bdepth:
                    g_cost = bdepth if use_g else 0
                    h_cost = heuristic(new_grid, width, bpos) if use_h else 0
                    heapq.heappush(bheap, (h_cost + g_cost, ny, nx, new_grid, bpath + s))

            bseen[bgrid] = bpath

    return best, time_complexity, space_complexity


def id_astar(base_grid, height, width, goal, heuristic):
    """
    Find the shortest path from an initial state to a goal state using the Iterative Deepening A* (IDA*) algorithm.

    The IDA* algorithm combines the concepts of iterative deepening depth-first search and A*. It performs a series
    of depth-first searches with increasing depth limits, using a heuristic to prune paths that exceed the current
    depth limit. This approach ensures completeness and optimality while using less memory than standard A*.

    Args:
        base_grid (Tuple[int, ...]): Initial state of the grid.
        height (int): Number of rows in the grid.
        width (int): Number of columns in the grid.
        goal (Tuple[int, ...]): Goal state of the grid.
        heuristic (Function): Heuristic function to estimate the distance to the goal.

    Returns:
        Tuple[str, int, int]:
            - Path (str): The sequence of moves to reach the goal.
            - Time complexity (int): The number of states explored.
            - Space complexity (int): The maximum number of states held in memory at any one time.
    """

    space_complexity = 1
    time_complexity = 0
    best = ""

    gpos = [-1] * (height * width)
    for i, e in enumerate(goal):
        gpos[e] = divmod(i, width)
    gpos = tuple(gpos)

    goal = list(goal)
    base_grid = list(base_grid)

    start = base_grid.index(0)
    sy, sx = divmod(start, width)

    max_depth = 1
    while not best:
        stack = deque([(base_grid, sy, sx, str())])

        while stack:
            grid, y, x, path = stack.popleft()

            depth = len(path)

            if grid == goal:
                best = path
                break

            time_complexity += 1
            space_complexity = max(space_complexity, len(stack))

            for ny, nx, s in utils.moves(y, x, height, width, path[-1] if path else ""):
                new_grid = grid.copy()
                new_grid[ny * width + nx], new_grid[y * width + x] = (
                    new_grid[y * width + x],
                    new_grid[ny * width + nx],
                )

                g_cost = depth
                h_cost = heuristic(new_grid, width, gpos)

                if h_cost + g_cost <= max_depth:
                    stack.append((new_grid, ny, nx, path + s))

        max_depth += 1

    return best, time_complexity, space_complexity


def id_astar_rec(base_grid, height, width, goal, heuristic):
    """
    Find the shortest path from an initial state to a goal state using the recursive Iterative Deepening A* (IDA*) algorithm.

    This function implements the IDA* algorithm recursively, which combines the principles of iterative deepening
    depth-first search and A*. It performs a series of depth-first searches with increasing depth limits, using
    a heuristic to prune paths that exceed the current depth limit. This approach ensures completeness and
    optimality while using less memory than standard A*.

    Args:
        base_grid (Tuple[int, ...]): Initial state of the grid.
        height (int): Number of rows in the grid.
        width (int): Number of columns in the grid.
        goal (Tuple[int, ...]): Goal state of the grid.
        heuristic (function): Heuristic function to estimate the distance to the goal.

    Returns:
        Tuple[str, int, int]:
            - Path (str): The sequence of moves to reach the goal.
            - Time complexity (int): The number of states explored.
            - Space complexity (int): The maximum number of states held in memory at any one time.
    """

    def search(grid, y, x, max_depth, height, width, goal, heuristic, path, gpos):
        """Perform a depth-limited search from the current state using the heuristic to prune paths."""

        if grid == goal:
            return path, 1, 0

        time_complexity = 1
        space_complexity = 1

        for ny, nx, s in utils.moves(y, x, height, width, path[-1] if path else ""):
            grid[ny * width + nx], grid[y * width + x] = grid[y * width + x], grid[ny * width + nx]

            g_cost = len(path) + 1
            h_cost = heuristic(grid, width, gpos)

            if h_cost + g_cost <= max_depth:
                solution, time, space = search(
                    grid, ny, nx, max_depth, height, width, goal, heuristic, path + s, gpos
                )
                time_complexity += time
                if solution:
                    return solution, time_complexity, space_complexity + space

            grid[ny * width + nx], grid[y * width + x] = grid[y * width + x], grid[ny * width + nx]

        return "", time_complexity, space_complexity

    space_complexity = 1
    time_complexity = 0
    best = ""

    gpos = [-1] * (height * width)
    for i, e in enumerate(goal):
        gpos[e] = divmod(i, width)
    gpos = tuple(gpos)

    goal = list(goal)
    base_grid = list(base_grid)

    start = base_grid.index(0)
    sy, sx = divmod(start, width)

    max_depth = 1
    while not best:
        best, time, space = search(
            base_grid, sy, sx, max_depth, height, width, goal, heuristic, "", gpos
        )
        time_complexity += time
        space_complexity = max(space_complexity, space)
        max_depth += 1

    return best, time_complexity, space_complexity


def greedy(base_grid, height, width, goal, heuristic):
    """
    Find the shortest path from an initial state to a goal state using the Greedy Best-First Search algorithm.

    This function utilizes the A* algorithm but considers only the heuristic cost (h cost) without the path length
    (g cost), effectively making it a Greedy Best-First Search.

    Args:
        base_grid (Tuple[int, ...]): Initial state of the grid.
        height (int): Number of rows in the grid.
        width (int): Number of columns in the grid.
        goal (Tuple[int, ...]): Goal state of the grid.
        heuristic (Function): Heuristic function to estimate the distance to the goal.

    Returns:
        Tuple[str, int, int]:
            - Path (str): The sequence of moves to reach the goal.
            - Time complexity (int): The number of states explored.
            - Space complexity (int): The maximum number of states held in memory at any one time.
    """

    return astar(base_grid, height, width, goal, heuristic, use_g=False, use_h=True)


def uniform_cost(base_grid, height, width, goal, heuristic):
    """
    Find the shortest path from an initial state to a goal state using the Uniform Cost Search algorithm.

    This function utilizes the A* algorithm but considers only the path length (g cost) without the heuristic cost
    (h cost), effectively making it a Uniform Cost Search.

    Args:
        base_grid (Tuple[int, ...]): Initial state of the grid.
        height (int): Number of rows in the grid.
        width (int): Number of columns in the grid.
        goal (Tuple[int, ...]): Goal state of the grid.
        heuristic (Function): Heuristic function to estimate the distance to the goal.

    Returns:
        Tuple[str, int, int]:
            - Path (str): The sequence of moves to reach the goal.
            - Time complexity (int): The number of states explored.
            - Space complexity (int): The maximum number of states held in memory at any one time.
    """

    return astar(base_grid, height, width, goal, heuristic, use_g=True, use_h=False)


def bd_greedy(base_grid, height, width, goal, heuristic):
    """
    Find the shortest path from an initial state to a goal state using the Bidirectional Greedy Best-First Search algorithm.

    This function utilizes the bidirectional A* algorithm but considers only the heuristic cost (h cost) without the path length
    (g cost), effectively making it a Bidirectional Greedy Best-First Search.

    Args:
        base_grid (Tuple[int, ...]): Initial state of the grid.
        height (int): Number of rows in the grid.
        width (int): Number of columns in the grid.
        goal (Tuple[int, ...]): Goal state of the grid.
        heuristic (Function): Heuristic function to estimate the distance to the goal.

    Returns:
        Tuple[str, int, int]:
            - Path (str): The sequence of moves to reach the goal.
            - Time complexity (int): The number of states explored.
            - Space complexity (int): The maximum number of states held in memory at any one time.
    """

    return bd_astar(base_grid, height, width, goal, heuristic, use_g=False, use_h=True)


def bd_uniform_cost(base_grid, height, width, goal, heuristic):
    """
    Find the shortest path from an initial state to a goal state using the Bidirectional Uniform Cost Search algorithm.

    This function utilizes the bidirectional A* algorithm but considers only the path length (g cost) without the heuristic cost
    (h cost), effectively making it a Bidirectional Uniform Cost Search.

    Args:
        base_grid (Tuple[int, ...]): Initial state of the grid.
        height (int): Number of rows in the grid.
        width (int): Number of columns in the grid.
        goal (Tuple[int, ...]): Goal state of the grid.
        heuristic (Function): Heuristic function to estimate the distance to the goal.

    Returns:
        Tuple[str, int, int]:
            - Path (str): The sequence of moves to reach the goal.
            - Time complexity (int): The number of states explored.
            - Space complexity (int): The maximum number of states held in memory at any one time.
    """

    return bd_astar(base_grid, height, width, goal, heuristic, use_g=True, use_h=False)


def line_by_line(base_grid, height, width, goal, heuristic):
    raise NotImplementedError("")


DEFAULT = "greedy"
NAMES = {
    f.__name__: f
    for f in (
        astar,
        greedy,
        uniform_cost,
        id_astar,
        id_astar_rec,
        bd_astar,
        bd_greedy,
        bd_uniform_cost,
        line_by_line,
    )
}
