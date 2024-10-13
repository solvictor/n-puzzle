<h1 align="center"><u>n-puzzle</u></h1>
42 Algorithm project that solve n-puzzle

## Requirements

`python >= 3.9`

## Usage

```sh
git clone https://github.com/solvictor/n-puzzle
cd n-puzzle
pip install -r requirements.txt
python3 n-puzzle.py -h
```

## Features
- **Algorithms**
  - [x] A*
  - [x] Uniform-Cost Search
  - [x] Greedy Search
  - [x] Iterative deepening A*
  - [x] Bidirectionnal A*
  - [x] Bidirectionnal Uniform-Cost Search
  - [x] Bidirectionnal Greedy Search
- **Heuristics**
  - [x] Misplaced count
  - [x] Manhattan distance
  - [x] Euclidean distance
  - [x] Chebyshev distance
  - [x] Manhattan with linear conflicts
  - [ ] Pattern database
- **Generator**
  - [x] Generate `N x M` valid random grids
  - [x] Generate `N x M` spiral goals
- **Visualizer**
  - [x] Visualize `N x M` grids being solved
  - [x] Change move speed
- **Misc**
  - [x] Custom goal handling
  - [x] Display computing time, space and time complexities, solution size and moves
  - [x] Solvability check
  - [x] Support for multiple input algorithms (executed in a row)
  - [x] Ranking on multiple algorithms
  - [x] CTRL-C Handling
  - [x] Verbose option (display every state of the puzzle between start and solution)
