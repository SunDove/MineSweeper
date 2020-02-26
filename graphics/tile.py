import pygame as pg
import numpy as np
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
        self.color = (200, 200, 200)
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
            self.color = (200, 200, 200)
        else:
            self.color = (200, 200, 200)
            self.stroke = 1

    def rgb(self, minimum, maximum, value):
        minimum, maximum = float(minimum), float(maximum)
        ratio = 2 * (value-minimum) / (maximum - minimum)
        b = int(max(0, 255*(1 - ratio)))
        r = int(max(0, 255*(ratio - 1)))
        g = 255 - b - r
        return r, g, b

    def toggle_heatmap(self, pred=None):
        if pred is not None:
            r, g, b = self.rgb(0, 1, pred[0][1])
            self.stroke = 2
            self.color = (r, g, b)
        else:
            self.stroke = 1
            self.color = (200, 200, 200)

    def draw(self, screen):
        """
        Draw the tile in screen
        :param screen:
        :return:
        """
        if self.stroke == 1:
            pg.draw.rect(screen, self.color, self.rect, 0)
            width = max(self.width*.1, 5)
            pg.draw.rect(screen, tuple(np.add(self.color, (55, 55, 55))), pg.rect.Rect(self.x, self.y, self.width-width, width), 0)
            pg.draw.rect(screen, tuple(np.add(self.color, (55, 55, 55))), pg.rect.Rect(self.x, self.y, width, self.width-width), 0)
            pg.draw.rect(screen, tuple(np.subtract(self.color, (25, 25, 25))), pg.rect.Rect(self.x, self.y+self.width-width, self.width, width), 0)
            pg.draw.rect(screen, tuple(np.subtract(self.color, (25, 25, 25))), pg.rect.Rect(self.x+self.width-width, self.y, width, self.width), 0)
        elif self.stroke == 0:
            pg.draw.rect(screen, tuple(np.subtract(self.color, (55, 55, 55))), self.rect, 0)
            width = max(self.width*.01, 2)
            pg.draw.rect(screen, tuple(np.subtract(self.color, (150, 150, 150))), pg.rect.Rect(self.x-width, self.y-width, self.width, width), 0)
            pg.draw.rect(screen, tuple(np.subtract(self.color, (150, 150, 150))), pg.rect.Rect(self.x-width, self.y-width, width, self.width), 0)
            pg.draw.rect(screen, tuple(np.subtract(self.color, (150, 150, 150))), pg.rect.Rect(self.x, self.y+self.width-width, self.width, width), 0)
            pg.draw.rect(screen, tuple(np.subtract(self.color, (150, 150, 150))), pg.rect.Rect(self.x+self.width-width, self.y, width, self.width), 0)
        elif self.stroke == 2:
            pg.draw.rect(screen, self.color, self.rect, 0)
            width = max(self.width*.1, 5)
            pg.draw.rect(screen, tuple(np.clip(np.add(self.color, (55, 55, 55)), 0, 255)), pg.rect.Rect(self.x, self.y, self.width-width, width), 0)
            pg.draw.rect(screen, tuple(np.clip(np.add(self.color, (55, 55, 55)), 0, 255)), pg.rect.Rect(self.x, self.y, width, self.width-width), 0)
            pg.draw.rect(screen, tuple(np.clip(np.subtract(self.color, (25, 25, 25)), 0, 255)), pg.rect.Rect(self.x, self.y+self.width-width, self.width, width), 0)
            pg.draw.rect(screen, tuple(np.clip(np.subtract(self.color, (25, 25, 25)), 0, 255)), pg.rect.Rect(self.x+self.width-width, self.y, width, self.width), 0)

        screen.blit(self.text_surface, (self.x, self.y))

    def _update_text_surface(self):
        """
        Update the text rendered on the tile
        :return:
        """
        num = self.value.value
        color = (255, 255, 255)
        if num > 0 and num <9:
            diffr = diffg = diffb = 0
            third = 255/3
            if num%3 == 0:
                diffr += 1
            elif num%3 == 1:
                diffg += 1
            else:
                diffb += 1
            if num<3:
                diffr += 2
            elif num<6:
                diffg += 2
            else:
                diffb += 2

            color = (255 - diffr*third, 255-diffg*third, 255-diffb*third)

        self.text_surface = self.font.render(str(self.value), False, color)
