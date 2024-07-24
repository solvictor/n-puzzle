from argparse import ArgumentParser, FileType
import heuristics
import visualizer
import generator
import parsing
import solver
import signal
import utils
import time
import sys


if __name__ == "__main__":
    parser = ArgumentParser(
        prog="n-puzzle",
        description="Solve n-puzzles."
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-g",
        "--generate",
        metavar='N',
        type=str,
        help="Generate a random puzzle of size NxN or NxM."
    )
    group.add_argument(
        "puzzle",
        nargs="?",
        type=FileType('r'),
        default=None,
        help="Path for the puzzle file."
    )

    parser.add_argument(
        "--goal",
        metavar="GOAL_PATH",
        type=FileType('r'),
        default=None,
        help="Path for the goal file. Defaults to spiral pattern."
    )
    parser.add_argument(
        "--verbose",
        help="Print each state of the puzzle from start to solution.",
        action="store_true"
    )
    parser.add_argument(
        "--visualize",
        help="Visualize the solution with a window.",
        action="store_true"
    )
    parser.add_argument(
        "--speed",
        help="Change visualizer speed. Defaults to 5.",
        type=int,
        default=5
    )
    parser.add_argument(
        "--algorithm",
        type=str,
        help=f"Choose the solver algorithm(s). Defaults to {solver.DEFAULT}.",
        choices=solver.NAMES,
        default=[solver.DEFAULT],
        nargs='+'
    )
    parser.add_argument(
        "--heuristic",
        type=str,
        help=f"Choose the heuristic function(s). Defaults to {heuristics.DEFAULT}.",
        choices=heuristics.NAMES,
        default=[heuristics.DEFAULT],
        nargs='+'
    )

    args = parser.parse_args()

    try:
        signal.signal(signal.SIGINT, lambda *_: (print("\033[2Dn-puzzle: error: computation ended by user."), exit(1)))

        if args.generate is None:
            raw_puzzle = parsing.deserialize_puzzle(args.puzzle)
            height, width, puzzle = parsing.parse_puzzle(raw_puzzle)
        else:
            height, width = parsing.parse_dimensions(args.generate)
            puzzle = generator.generate(height, width)

        if args.goal is None:
            goal = generator.make_goal(height, width)
        else:
            raw_goal = parsing.deserialize_puzzle(args.goal)
            gheight, gwidth, goal = parsing.parse_puzzle(raw_goal)
            if gheight != height or gwidth != width:
                raise RuntimeError("Invalid goal dimensions")

        if not utils.is_solvable(puzzle, goal, width):
            raise RuntimeError("Puzzle is not solvable")

        utils.print_puzzle(puzzle, height, width)
        # utils.print_puzzle(goal, size)

        scores = {}

        for algo_name in args.algorithm:
            algorithm = solver.NAMES[algo_name]
            for heur_name in args.heuristic:
                heuristic = heuristics.NAMES[heur_name]

                print()
                print(f"Searching for a solution using {algo_name} algorithm and {heur_name} heuristic.")
                start = time.time()
                solution, time_complexity, space_complexity = algorithm(tuple(puzzle), height, width, tuple(goal), heuristic)
                end = time.time()

                scores[(algo_name, heur_name)] = (end - start, len(solution), time_complexity, space_complexity)

                print(f"Solution of {len(solution)} moves found in {end - start:.3f}s")
                print("Time Complexity:", time_complexity)
                print("Space Complexity:", space_complexity)
                print("Moves:", *solution if solution else (None,))

                if args.verbose:
                    utils.print_moves(puzzle, height, width, solution)

                if args.visualize:
                    visualizer.start(puzzle, height, width, solution, args.speed)

        if len(args.algorithm) > 1 or len(args.heuristic) > 1:
            categories = (
                ("Time", "s"),
                ("Moves", " moves"),
                ("Time Complexity", " operations"),
                ("Space Complexity", " maximum simultaneous states")
            )

            print("\n――――― Ranking ―――――")
            for i, (category, unit) in enumerate(categories):
                best_algo, best_heur = best = min(scores, key=lambda s: scores[s][i])
                best_scores = scores[best]
                bests = [algo for algo, stats in scores.items() if stats[i] == best_scores[i]]
                print(f"Best algorithm by {category}: {', '.join(algo + (f' ({heur})' if len(args.heuristic) > 1 else '') for algo, heur in bests)} ({best_scores[i]}{unit})")

    except Exception as ex:
        print(f"n-puzzle: {ex.__class__.__name__}: {ex}", file=sys.stderr)
        exit(1)
