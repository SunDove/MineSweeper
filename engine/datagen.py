import numpy as np
from engine.engine import Engine
from constants import Spaces


class DataGenerator:

    def __init__(self, n_observations=10, do_gen=True):
        if do_gen:
            self._data_set = [self._generate_one_scenerio() for k in range(n_observations)]

    def get_data_set(self):
        return self._data_set

    def _generate_one_scenerio(self):
        self._engine = Engine(10, 10, 15)
        first_move = np.floor(np.multiply(np.random.rand(1, 2), np.array([[10, 10]]))).astype(int)[0]
        self._engine.check_location(first_move[0], first_move[1])
        loc = self._get_random_unknown_loc(self._engine)
        daters = DataGenerator.get_data_for_space(loc[0], loc[1], self._engine)
        return daters

    def _get_random_unknown_loc(self, engine):
        frontier = list(engine.get_frontier())
        index = np.random.choice(len(frontier))
        return frontier[index]

    def get_data_for_space(l1, l2, engine, maxx=10, maxy=10, random_flag=True):
        daters = []
        board = engine.get_display_board()
        rboard = engine.get_real_board()
        for i in range(-2, 3):
            x = l1 + i
            for j in range(-2, 3):
                y = l2 + j
                if y < 0 or y >= maxy or x < 0 or x >= maxx:
                    daters.append("Edge")
                else:
                    if i == 0 and j == 0:
                        daters.append(str(rboard[x, y] == Spaces.BOMB))
                    else:
                        if rboard[x, y] == Spaces.BOMB and random_flag and np.random.uniform(0, 1.0)<0.3:
                            daters.append(repr(Spaces.FLAG))
                        else:
                            daters.append(repr(board[x, y]))
        return daters
