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
        type=int,
        help="Generate a random puzzle of size NxN",
        metavar="N"
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
        size, puzzle = parsing.parse_puzzle(raw_puzzle)
    else:
        size = args.generate
        puzzle = generator.generate(size)

    heuristic = heuristics.NAMES[args.heuristic]
    algorithm = solver.NAMES[args.algorithm]
    goal = generator.make_goal(size)

    # TODO Check for solvability
    if not utils.is_solvable(puzzle, goal, size):
        utils.error("Puzzle is not solvable")

    utils.print_puzzle(puzzle, size)
    # utils.print_puzzle(goal, size)

    print()
    start = time.time()
    solution, time_complexity, space_complexity = algorithm(tuple(puzzle), size, tuple(goal), heuristic)
    end = time.time()

    print(f"Solution found in {end - start:.5}s using {args.algorithm}")
    print("Heuristic:", args.heuristic)
    print("Moves:", len(solution))
    print("Time Complexity:", time_complexity)
    print("Space Complexity:", space_complexity)

    # utils.print_moves(puzzle, size, solution)
    if args.visualize:
        visualizer.start(puzzle, size, solution)
