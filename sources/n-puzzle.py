from argparse import ArgumentParser, FileType
import heuristics
import generator
import parsing
import utils
import solver


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

	args = parser.parse_args()

	if args.generate is None:
		raw_puzzle = parsing.deserialize_puzzle(args.puzzle_path)
		size, puzzle = parsing.parse_puzzle(raw_puzzle)
		# TODO Check for solvability
		if not utils.is_solvable(puzzle, size):
			utils.error("Puzzle is not solvable")
	else:
		size = args.generate
		puzzle = generator.generate(size)
	goal = generator.make_goal(size)
	utils.print_puzzle(puzzle, size)
	print()
	solution = solver.astar_solve(tuple(puzzle), size, tuple(goal), heuristics.squared)
	print(f"{len(solution) = }")
	# for y, x, s in solution:
	# 	print(y, x, s)
	# print_moves(puzzle, size, solution)
