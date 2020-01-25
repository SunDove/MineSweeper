import pygame as pg
from constants import Spaces
from graphics.tile import Tile


class Board:

    """
    Contains a grid of tiles.
    Manages tile state and draws grid
    """

    def __init__(self, x_tiles, y_tiles, tile_dim=40):
        """
        Game board constructor
        :param x_tiles:
        :param y_tiles:
        :param tile_dim:
        """
        self.screen_width = tile_dim * x_tiles
        self.screen_height = tile_dim * y_tiles
        self.tile_dim = tile_dim
        # self.font = pg.font.SysFont(None, self.tile_dim)
        self.font = pg.font.Font(pg.font.get_default_font(), self.tile_dim)

        self.screen = pg.display.set_mode([self.screen_width, self.screen_height])
        pg.display.set_caption("Minesweeper")

        GREY = (155, 155, 155)
        WHITE = (200, 200, 200)

        self.tiles = {}
        dark = False

        for x in range(0, self.screen_width, tile_dim):
            for y in range(0, self.screen_height, tile_dim):
                color = GREY if dark else WHITE
                self.tiles[(x // tile_dim, y // tile_dim)] = \
                    Tile(x, y, color, tile_dim, self.font, Spaces.UNKNOWN)
                dark = not dark

    def map_click(self, x, y):
        """
        Translates mouse coordinate clicks into grid coordinates
        :param x: x coordinate of the mouse click
        :param y: y coordinate of the mouse click
        :return: (int, int) x and y coordinates of the clicked tile in grid coordinates
        """
        return (x // self.tile_dim, y // self.tile_dim)

    def update_board(self, board_array):
        """
        Update the board using the 2D display array from the engine
        :param board_array:
        :return:
        """
        y_dim, x_dim = board_array.shape

        for x in range(x_dim):
            for y in range(y_dim):
                self.tiles[(y, x)].set_value(board_array[y, x])

    def draw_screen(self):
        """
        Renders the board
        :return:
        """
        self.screen.fill((255,255,255))

        for tile in self.tiles.values():
            tile.draw(self.screen)

        pg.display.flip()
