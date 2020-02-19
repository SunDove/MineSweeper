import numpy as np
import constants as C
Spaces = C.Spaces


class Engine:
    """
    Engine class responsible for handling the internal MineSweeper Game
    This includes generating the board randomly and revealing spaces
    """

    def __init__(self, width, height, bombs, gamemode="default"):
        """
        Engine constructor
        :param width: Width of the board, min and max values found in constants.py
        :param height: Height of the board, min and max values found in constants.py
        :param bombs: Number of bombs in the board, cannot exceed ratio defined in constants.py
        """
        if (bombs/(width*height)) > C.MAX_BOMB_RATIO:
            raise ValueError('Number of bombs cannot be more than {}% of the total spaces ({} bombs, {} spaces).'.format(C.MAX_BOMB_RATIO*100, bombs, width*height))

        if width < C.MIN_WIDTH or width > C.MAX_WIDTH:
            raise ValueError('Width must be within constraints {} < width < {}'.format(C.MIN_WIDTH, C.MAX_WIDTH))

        if height < C.MIN_HEIGHT or height > C.MAX_HEIGHT:
            raise ValueError('Width must be within constraints {} < height < {}'.format(C.MIN_WIDTH, C.MAX_WIDTH))

        self._width = width
        self._height = height
        self._bombs = bombs
        self._gamemode = gamemode
        self._board = self._generate_board()
        self._first_move = False
        self._flag_locs = []

    def get_width(self):
        return self._width

    def get_height(self):
        return self._height

    def get_display_board(self):
        """
        Returns the board array with flags
        """
        dboard = self._board.copy()
        for fl in self._flag_locs:
            x, y = fl
            dboard[x, y] = Spaces.FLAG

        dboard[dboard == Spaces.BOMB] = Spaces.UNKNOWN

        return dboard

    def get_real_board(self):
        """
        Returns the board array without flags, meaning with their actual spaces values
        """
        return self._board

    def toggle_flag(self, x, y):
        """
        Toggles the flag at the given (x, y) coordinate
        """
        if (x, y) in self._flag_locs:
            self._flag_locs.remove((x, y))
        else:
            if self.get_display_board()[x, y] != Spaces.UNKNOWN:
                return
            self._flag_locs.append((x, y))

    def check_location(self, x, y):
        """
        Checks the given (x, y) coordinate ie. when the user clicks a tile
        :return: False if the space was a bomb, True otherwise
        """
        if not self._first_move:
            self._check_safe_first_move(x, y)
            self._first_move = True

        if (x, y) in self._flag_locs:
            self.toggle_flag(x, y)
            return True

        s = self.get_real_board()[x, y]
        if s == Spaces.BOMB:
            return False

        if s != Spaces.UNKNOWN:
            if self.get_neighboring_space_count(x, y, Spaces.FLAG) == s.value:
                # Space is solved, click around
                return self._unsafe_check_neighbors(x, y)

        self._safe_check_location(x, y)
        return True

    def _unsafe_check_neighbors(self, x, y):
        for i in range(x-1, x+2):
            if i < 0 or i >= self._width:
                continue
            for j in range(y-1, y+2):
                if j < 0 or j >= self._height:
                    continue
                real = self.get_real_board()
                if (i, j) in self._flag_locs:
                    continue
                if real[i, j] == Spaces.BOMB:
                    return False
                if real[i, j] == Spaces.UNKNOWN:
                    nb = self._get_neighboring_bombs(i, j, True)
                    if nb == 0:
                        self._safe_check_location(i, j)
                    self._board[i, j] = Spaces(nb)
        return True

    def _check_safe_first_move(self, x, y):
        nb = self._get_neighboring_bombs(x, y)

        if nb > 0:
            self._clear_neighboring_bombs(x, y)

            empty_tiles = []

            for x in range(self._width):
                for y in range(self._height):
                    if self._board[x, y] == Spaces.UNKNOWN:
                        empty_tiles.append((x,y))
            
            n = len(empty_tiles)

            if n < nb:
                print("Unable to relocate bombs")
                return

            # numpy won't let me randomly choose from the list of tuples :(
            new_coord_indices = np.random.choice(range(n), nb, replace=False)

            for i in new_coord_indices:
                x, y = empty_tiles[i]
                self._board[x, y] = Spaces.BOMB

    def _safe_check_location(self, x, y):
        """
        Sets the board indices to the number of neighboring bombs
        If the space has 0 neighboring bombs then it will check the spaces in the N, E, W, and S directions (not diagonals)
        """
        if self._board[x, y] != Spaces.UNKNOWN:
            return
        num_bombs = self._get_neighboring_bombs(x, y, True)
        self._board[x, y] = Spaces(num_bombs)
        if num_bombs == 0:
            if x-1 >= 0:
                self._safe_check_location(x-1, y)
                if y-1 >= 0:
                    self._safe_check_location(x-1, y-1)
                if y+1 < self._height:
                    self._safe_check_location(x-1, y+1)
            if x+1 < self._width:
                self._safe_check_location(x+1, y)
                if y-1 >= 0:
                    self._safe_check_location(x+1, y-1)
                if y+1 < self._height:
                    self._safe_check_location(x+1, y+1)
            if y-1 >= 0:
                self._safe_check_location(x, y-1)
            if y+1 < self._height:
                self._safe_check_location(x, y+1)

    def _clear_neighboring_bombs(self, x, y):
        for i in range(x-1, x+2):
            if i < 0 or i >= self._width:
                continue
            for j in range(y-1, y+2):
                if j < 0 or j >= self._height:
                    continue
                self._board[i, j] = Spaces.UNKNOWN

    def get_neighboring_space_count(self, x, y, s):
        count = 0
        for i in range(x-1, x+2):
            if i < 0 or i >= self._width:
                continue
            for j in range(y-1, y+2):
                if j < 0 or j >= self._height:
                    continue
                if self.get_display_board()[i, j] == s:
                    count += 1
        return count

    def _get_neighboring_bombs(self, x, y, g2=False):
        """
        Counts the number of bombs neighboring the tile at (x, y)
        """
        ad = 2 if g2 and self._gamemode == '2' else 1
        count = 0
        for i in range(x-ad, x+ad+1):
            if i < 0 or i >= self._width:
                continue
            for j in range(y-ad, y+ad+1):
                if j < 0 or j >= self._height:
                    continue
                if self._board[i, j] == Spaces.BOMB:
                    count += 1
        return count

    def __str__(self):
        return str(self._board)

    def _generate_board(self):
        """
        Generates a random MineSweeper game
        """
        shuffle = [Spaces.BOMB]*self._bombs + [Spaces.UNKNOWN]*((self._width*self._height) - self._bombs)
        np.random.shuffle(shuffle)
        board = np.reshape(shuffle, (self._width, self._height))
        return board
