import numpy as np
import constants as C


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
            dboard[x, y] = Spaces.FLAG
            
        return dboard

    def get_real_board(self):
        """
        Returns the board array without flags, meaning with their actual spaces values
        """
        return self._board

    def toggle_flag(self, x, y):
        if (x, y) in self._flag_locs:
            self._flag_locs.remove((x, y))
        else:
            self._flag_locs.append((x, y))

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
