import numpy as np
from engine.engine import Engine
from constants import Spaces


class DataGenerator:

    def __init__(self, n_observations=10, do_gen=True):
        self._games = 0
        if do_gen:
            self._data_set = np.reshape([self._generate_one_scenerio() for k in range(n_observations)], (n_observations*10, 25)).tolist()

    def get_data_set(self):
        return self._data_set

    def _generate_one_scenerio(self):
        self._games += 1
        if self._games%1000 == 0:
            print('{:,} complete'.format(self._games))
        self._engine = Engine(12, 12, 30)
        first_move = np.floor(np.multiply(np.random.rand(1, 2), np.array([[10, 10]]))).astype(int)[0]
        self._engine.check_location(first_move[0], first_move[1])
        daters = [self._get_next_data(self._engine) for i in range(10)]
        return daters

    def _get_next_data(self, engine):
        _ = [self._make_one_board_move(engine) for i in range(np.random.randint(low=2, high=6))]
        return self._make_one_board_move(engine)

    def _make_one_board_move(self, engine):
        frontier = list(engine.get_frontier())
        index = np.random.choice(len(frontier))
        loc = frontier[index]
        ret = DataGenerator.get_data_for_space(loc[0], loc[1], self._engine)

        adj = [loc, loc]
        prev_adj = []
        #Now need to reveal random spaces adjacent to loc in the frontier
        for i in range(np.random.randint(3, 8)):
            if len(adj) == 2:
                t_adj = self._get_adjacent_frontier(frontier, prev_adj, adj[0], adj[1])
                prev_adj = adj
                adj = t_adj
            elif len(adj) == 1:
                t_adj = self._get_adjacent_frontier(frontier, prev_adj, adj[0])
                prev_adj = adj
                adj = t_adj
            if len(adj) == 0:
                # Out of spaces to make moves
                return ret
            ind = np.random.choice(len(adj))
            move = adj[ind]
            if self._engine.get_real_board()[move[0], move[1]] == Spaces.BOMB:
                self._engine.toggle_flag(move[0], move[1])
            else:
                self._engine.check_location(move[0], move[1])

        return ret

    def _get_adjacent_frontier(self, frontier, prev_adj, loc1, loc2=None):
        adj = []
        if not loc2:
            loc2 = loc1
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i==j:
                    continue
                if i == -j:
                    continue
                x = loc1[0]-i
                y = loc1[1]-j
                p = (x, y)
                if p in frontier and p not in adj and p not in prev_adj:
                    adj.append(p)
                x = loc2[0]-i
                y = loc2[1]-j
                p = (x, y)
                if p in frontier and p not in adj and p not in prev_adj:
                    adj.append(p)

        return adj

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
