import pygame as pg
from constants import Spaces


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
        :param value: Spaces enum value of the tile
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
        """
        Set the enum value of the tile
        :param val_enum:
        :return:
        """
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
        :return:
        """
        self.text_surface = self.font.render(str(self.value), False, (255, 255, 255))
