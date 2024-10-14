from keras.api import Sequential, Input
from keras.api.layers import Dense
from . import generator, solver, heuristics
from typing import List
from tqdm import tqdm
import numpy as np


MODEL = None


def generate_dataset(goal: List[int], height: int, width: int, size: int):
    data = []
    for _ in tqdm(range(size)):
        puzzle = tuple(generator.generate(height, width, goal, 1000))
        path, _, _ = solver.id_astar_rec(puzzle, height, width, goal, heuristics.manhattan_with_lc)
        puzzle = list(puzzle)
        start = puzzle.index(0)
        y, x = divmod(start, width)
        for i, s in enumerate(path):
            data.append((puzzle.copy(), len(path) - i))
            ny = y + (1 if s == 'v' else -1 if s == '^' else 0)
            nx = x + (1 if s == '>' else -1 if s == '<' else 0)
            puzzle[ny * width + nx], puzzle[y * width + x] = puzzle[y * width + x], puzzle[ny * width + nx]
            y, x = ny, nx
        data.append((puzzle.copy(), 0))
    return data


def create_model(height: int, width: int) -> Sequential:
    model = Sequential()

    model.add(Input(shape=(height * width,)))

    model.add(Dense(128, activation='relu'))
    model.add(Dense(256, activation='relu'))
    model.add(Dense(128, activation='relu'))

    model.add(Dense(1))

    model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])
    return model


def train(model: Sequential, goal: List[int], height: int, width: int):
    N_GRIDS = 50
    print(f"Generating dataset with {N_GRIDS} grids...")
    dataset = generate_dataset(goal, height, width, N_GRIDS)
    puzzles = np.array([puzzle for puzzle, _ in dataset])
    moves = np.array([n_moves for _, n_moves in dataset])


    print("Training the model...")
    history = model.fit(puzzles, moves, 
                        validation_split=0.1,
                        epochs=200, 
                        batch_size=32)
    print("Done")
    return history
