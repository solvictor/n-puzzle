from argparse import ArgumentParser, FileType
import heuristics
import generator
import parsing
import utils
import solver
import visualizer
import time


if __name__ == "__main__":
    parser = ArgumentParser(
        prog="n-puzzle",
        description="Solve n-puzzles"
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-g",
        "--generate",
        type=str,
        help="Generate a random puzzle of size NxN or NxM"
    )
    group.add_argument(
        "puzzle_path",
        nargs="?",
        type=FileType('r'),
        default=None,
        help="Path for the puzzle file"
    )

    parser.add_argument(
        "--visualize",
        help="Visualize the solution with a window",
        action="store_true"
    )
    parser.add_argument(
        "--speed",
        help="Change visualizer speed",
        type=int,
        default=5
    )
    parser.add_argument(
        "--algorithm",
        type=str,
        help=f"Choose the solver algorithm. Defaults to {solver.DEFAULT}.",
        choices=solver.NAMES,
        default=solver.DEFAULT
    )
    parser.add_argument(
        "--heuristic",
        type=str,
        help=f"Choose the heuristic function. Defaults to {heuristics.DEFAULT}.",
        choices=heuristics.NAMES,
        default=heuristics.DEFAULT
    )

    args = parser.parse_args()

    if args.generate is None:
        raw_puzzle = parsing.deserialize_puzzle(args.puzzle_path)
        height, width, puzzle = parsing.parse_puzzle(raw_puzzle)
    else:
        height, width = parsing.parse_dimensions(args.generate)
        puzzle = generator.generate(height, width)

    heuristic = heuristics.NAMES[args.heuristic]
    algorithm = solver.NAMES[args.algorithm]
    goal = generator.make_goal(height, width)

    if not utils.is_solvable(puzzle, goal, height, width):
        utils.error("Puzzle is not solvable")

    utils.print_puzzle(puzzle, height, width)
    # utils.print_puzzle(goal, size)

    print()
    start = time.time()
    solution, time_complexity, space_complexity = algorithm(tuple(puzzle), height, width, tuple(goal), heuristic)
    end = time.time()

    print(f"Solution found in {end - start:.3f}s using {args.algorithm}")
    print("Heuristic:", args.heuristic)
    print("Moves:", len(solution))
    print("Time Complexity:", time_complexity)
    print("Space Complexity:", space_complexity)

    # utils.print_moves(puzzle, size, solution)
    if args.visualize:
        visualizer.start(puzzle, height, width, solution, args.speed)
