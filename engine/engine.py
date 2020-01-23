import numpy as np
import constants as C
Spaces = C.Spaces


class Engine:
    """
    Engine class responsible for handling the internal MineSweeper Game
    This includes generating the board randomly and revealing spaces
    """

    def __init__(self, width, height, bombs):
        """
        Engine constructor
        :param width: Width of the board, min and max values found in constants.py
        :param height: Height of the board, min and max values found in constants.py
        :param bombs: Number of bombs in the board, cannot exceed ratio defined in constants.py
        """
        if (bombs/(width*height)) > C.MAX_BOMB_RATIO:
            raise ValueError('Number of bombs cannot be more than half of the total spaces ({} bombs, {} spaces).'.format(bombs, width*height))

        if width < C.MIN_WIDTH or width > C.MAX_WIDTH:
            raise ValueError('Width must be within constraints {} < width < {}'.format(C.MIN_WIDTH, C.MAX_WIDTH))

        if height < C.MIN_HEIGHT or height > C.MAX_HEIGHT:
            raise ValueError('Width must be within constraints {} < height < {}'.format(C.MIN_WIDTH, C.MAX_WIDTH))

        self._width = width
        self._height = height
        self._bombs = bombs
        self._board = self._generate_board()
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
        if (x, y) in self._flag_locs:
            self.toggle_flag(x, y)
            return True

        s = self.get_real_board()[x, y]
        if s == Spaces.BOMB:
            return False

        self._safe_check_location(x, y)
        return True

    def _safe_check_location(self, x, y):
        """
        Sets the board indices to the number of neighboring bombs
        If the space has 0 neighboring bombs then it will check the spaces in the N, E, W, and S directions (not diagonals)
        """
        if self._board[x, y] != Spaces.UNKNOWN:
            return
        num_bombs = self._get_neighboring_bombs(x, y)
        self._board[x, y] = Spaces(num_bombs)
        if num_bombs == 0:
            if x-1 >= 0:
                self._safe_check_location(x-1, y)
            if x+1 < self._width:
                self._safe_check_location(x+1, y)
            if y-1 >= 0:
                self._safe_check_location(x, y-1)
            if y+1 < self._height:
                self._safe_check_location(x, y+1)

    def _get_neighboring_bombs(self, x, y):
        """
        Counts the number of bombs neighboring the tile at (x, y)
        """
        count = 0
        for i in range(x-1, x+2):
            if i < 0 or i >= self._width:
                continue
            for j in range(y-1, y+2):
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
