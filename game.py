import pygame as pg
from graphics.minesweeper import Board
from engine.engine import Engine

LEFT_CLICK = 1
RIGHT_CLICK = 3

class Game:
    """
    Interactive GUI class with no game logic
    """
    def __init__(self, engine, tile_dim=20):
        self.x_tiles = engine.get_width()
        self.y_tiles = engine.get_height()
        self.tile_dim = tile_dim
        pg.init()

        self.board = Board(self.x_tiles, self.y_tiles, tile_dim)
        self.running = True
        self.engine = engine

    def loop(self):
        """
        Render the board and handle mouse input
        :return:
        """
        accept_input = True

        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                if accept_input and event.type == pg.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    t_x, t_y = self.board.map_click(x, y)
                    button = event.button

                    if button == LEFT_CLICK:
                        is_safe = self.engine.check_location(t_y, t_x)

                        if not is_safe:
                            accept_input = False

                    elif button == RIGHT_CLICK:
                        self.engine.toggle_flag(t_y, t_x)

                    display_array = self.engine.get_display_board()
                    self.board.update_board(display_array)

            self.board.draw_screen()
        pg.quit()


if __name__ == "__main__":
    e = Engine(15, 15, 10)
    session = Game(e)
    session.loop()
