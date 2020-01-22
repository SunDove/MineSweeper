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

    def get_width(self):
        return self._width

    def get_height(self):
        return self._height

    def get_board(self):
        return self._board

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
