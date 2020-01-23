import pygame as pg
from constants import Spaces

LEFT_CLICK = 1
RIGHT_CLICK = 3

class Board:

    """
    Contains a grid of tiles.
    Manages tile state and draws grid
    """

    def __init__(self, x_tiles, y_tiles, tile_dim=20):
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
        WHITE = (255, 255, 255)

        self.tiles = {}
        dark = False

        # TODO: Add a different method of assigning bombs to tiles?
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
        y_dim, x_dim = board_array.shape

        for x in range(x_dim):
            for y in range(y_dim):
                self.tiles[(x, y)].set_value(board_array[y, x])

    def draw_screen(self):
        """
        Renders the board
        :return:
        """
        self.screen.fill((255,255,255))

        for tile in self.tiles.values():
            tile.draw(self.screen)

        pg.display.flip()


class Tile:
    """
    Represents a square on the minesweeper grid
    """

    def __init__(self, x, y, color, width, font, value):
        """
        Tile constructor
        :param x: x coordinate on screen
        :param y: y coordinate on screen
        :param color: Default tile color
        :param width: tile width and height
        :param font: Font object; only passed to the object for optimization
        """

        self.width = width
        self.x = x
        self.y = y
        self.rect = pg.rect.Rect(self.x, self.y, self.width, self.width)
        self.color = (155, 155, 155)
        self.stroke = 1
        self.DEFAULT_COLOR = color
        self.active = True
        self.font = font
        self.text_surface = self.font.render("", False, (255, 255, 255))
        self.value = value

    def set_value(self, val_enum):
        self.value = val_enum
        self._update_text_surface()

        if val_enum != Spaces.UNKNOWN:
            self.stroke = 0
        else:
            self.stroke = 1

    def draw(self, screen):
        """
        Draw the tile in screen
        :param screen:
        :return:
        """
        pg.draw.rect(screen, self.color, self.rect, self.stroke)
        screen.blit(self.text_surface, (self.x, self.y))

    def _update_text_surface(self):
        """
        Update the text rendered on the tile
        :param tile_enum:
        :return:
        """
        self.text_surface = self.font.render(str(self.value), False, (255, 255, 255))
