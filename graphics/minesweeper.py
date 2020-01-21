import pygame as pg
import random

LEFT_CLICK = 1
RIGHT_CLICK = 3


class Game:
    """
    Interactive GUI class with no game logic
    """
    def __init__(self, x_tiles, y_tiles, tile_dim=20):
        """
        Game session constructor
        :param x_tiles: Number of tiles in the x dimension
        :param y_tiles: Number of tiles in the y dimension
        :param tile_dim: Width/height of the tiles in pixels
        """
        self.x_tiles = x_tiles
        self.y_tiles = y_tiles
        self.tile_dim = tile_dim
        pg.init()

        self.board = Board(x_tiles, y_tiles, tile_dim)
        self.running = True

    def loop(self):
        """
        Render the board and handle mouse input
        :return:
        """
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    t_x, t_y = self.board.map_click(x, y)
                    button = event.button

                    if button == LEFT_CLICK:
                        (running, _) = self.board.check_tile(t_x, t_y)

                    elif button == RIGHT_CLICK:
                        self.board.toggle_flag(t_x, t_y)

            self.board.draw_screen()
        pg.quit()

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
                    Tile(x, y, color, tile_dim, 0, self.font, has_bomb=False)
                dark = not dark

    def set_tile(self, x, y, has_bomb, num_neighbors):
        """
        Change the parameters of the tile at (x, y)
        :param x:
        :param y:
        :param has_bomb:
        :param num_neighbors:
        :return:
        """
        self.tiles[(x, y)].has_bomb = has_bomb
        self.tiles[(x,y)].n_bombs = num_neighbors

    def map_click(self, x, y):
        """
        Translates mouse coordinate clicks into grid coordinates
        :param x: x coordinate of the mouse click
        :param y: y coordinate of the mouse click
        :return: (int, int) x and y coordinates of the clicked tile in grid coordinates
        """
        return (x // self.tile_dim, y // self.tile_dim)

    def draw_screen(self):
        """
        Renders the board
        :return:
        """
        self.screen.fill((255,255,255))

        for tile in self.tiles.values():
            tile.draw(self.screen)

        pg.display.flip()

    def toggle_flag(self, tile_x, tile_y):
        """
        Toggle minesweeper flag for the tile at (tile_x, tile_y)
        :param tile_x:
        :param tile_y:
        :return: True if the tile is flagged else False
        """
        return self.tiles[(tile_x, tile_y)].toggle_flag()

    def check_tile(self, tile_x, tile_y):
        """
        Check the tile at (tile_x, tile_y) for a bomb
        :param tile_x:
        :param tile_y:
        :return: (boolean, int) True if tile has a bomb, number of neighbors with bombs
        """
        return self.tiles[(tile_x, tile_y)].check_tile()

class Tile:
    """
    Represents a square on the minesweeper grid
    """

    def __init__(self, x, y, color, width, num_bombs, font, has_bomb=False):
        """
        Tile constructor
        :param x: x coordinate on screen
        :param y: y coordinate on screen
        :param color: Default tile color
        :param width: tile width and height
        :param num_bombs: Number of neighbors with bombs
        :param font: Font object; only passed to the object for optimization
        :param has_bomb: True if the tile contains a bomb else False
        """
        self.width = width
        self.x = x
        self.y = y
        self.rect = pg.rect.Rect(self.x, self.y, self.width, self.width)
        self.color = color
        self.DEFAULT_COLOR = color
        self.active = True
        self.flagged = False
        self.has_bomb = has_bomb
        self.n_bombs = num_bombs
        self.font = font
        self.text_surface = self.font.render("", False, (255, 255, 255))

    def draw(self, screen):
        """
        Draw the tile in screen
        :param screen:
        :return:
        """
        pg.draw.rect(screen, self.color, self.rect)
        screen.blit(self.text_surface, (self.x, self.y))

    def _update_text(self, text):
        """
        Update the text rendered on the tile
        :param text:
        :return:
        """
        self.text_surface = self.font.render(text, False, (255,255,255))

    def toggle_flag(self):
        """
        Toggle flagged
        :return: True if the tile has been flagged
        """
        if self.active:
            self.flagged = not self.flagged

            if self.flagged:
                self.color = (0,0,255)
                self._update_text("?")
            else:
                self._update_text("")
                self.color = self.DEFAULT_COLOR

        return self.flagged

    def check_tile(self):
        """
        Check the tile for a bomb
        :return: (boolean, int) True if tile has a bomb else False, count of neighbors with bombs
        """
        if not self.active:
            return (self.has_bomb, self.n_bombs)

        self.active = False


        if self.has_bomb:
            self.color = (255,0,0)
            self._update_text("*")
        else:
            self._update_text(str(self.n_bombs))
            self.color = (0,0,0)
        return (self.has_bomb, self.n_bombs)

if __name__ == '__main__':
    session = Game(15,15)
    session.loop()