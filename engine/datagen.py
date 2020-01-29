import numpy as np
from engine.engine import Engine
from constants import Spaces


class DataGenerator:

    def __init__(self, n_observations=10):
        self._data_set = [self._generate_one_scenerio() for k in range(n_observations)]

    def get_data_set(self):
        return self._data_set

    def _generate_one_scenerio(self):
        self._engine = Engine(10, 10, 15)
        first_move = np.floor(np.multiply(np.random.rand(1, 2), np.array([[10, 10]]))).astype(int)[0]
        self._engine.check_location(first_move[0], first_move[1])
        loc = self._get_random_unknown_loc(self._engine)
        daters = []
        board = self._engine.get_display_board()
        rboard = self._engine.get_real_board()
        for i in range(-1, 2):
            x = loc[0] + i
            if x < 0 or x >= 10:
                daters.append("Edge")
                continue
            for j in range(-1, 2):
                y = loc[1] + j
                if y < 0 or y >= 10:
                    daters.append("Edge")
                    continue
                if i == 0 and j == 0:
                    daters.append(str(rboard[x, y] == Spaces.BOMB))
                else:
                    daters.append(str(board[x, y]))

        return daters

    def _get_random_unknown_loc(self, engine):
        board = engine.get_display_board()
        not_valid = True
        new_coords = [-1, -1]
        while not_valid:
            new_coords = np.floor(np.multiply(np.random.rand(1, 2), np.array([[10, 10]]))).astype(int)[0]
            all_unknown = True
            for i in range(-1, 2):
                if not all_unknown:
                    break
                x = new_coords[0] + i
                if x < 0 or x >= 10:
                    continue
                for j in range(-1, 2):
                    if not all_unknown:
                        break
                    y = new_coords[1] + j
                    if y < 0 or y >= 10:
                        continue
                    if board[x, y] != Spaces.UNKNOWN:
                        all_unknown = False
            if not all_unknown:
                not_valid = False
                break
        return new_coords
