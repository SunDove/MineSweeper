import pygame as pg
from graphics.board import Board
from engine.engine import Engine
from engine.aiengine import AIEngine
import argparse

LEFT_CLICK = 1
RIGHT_CLICK = 3


class Game:
    """
    Interactive GUI class with no game logic
    """
    def __init__(self, engine, tile_dim=50):
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
                        is_safe = self.engine.check_location(t_x, t_y)

                        if not is_safe:
                            accept_input = False

                    elif button == RIGHT_CLICK:
                        self.engine.toggle_flag(t_x, t_y)

                    if accept_input:
                        display_array = self.engine.get_display_board()
                        self.board.update_board(display_array)
                    else:
                        self.board.update_board(self.engine.get_real_board())

            self.board.draw_screen()
        pg.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-width', action='store', dest='width', type=int, default=15)
    parser.add_argument('-height', action='store', dest='height', type=int, default=15)
    parser.add_argument('-bombs', action='store', dest='bombs', type=int, default=50)
    parser.add_argument('-gamemode', action='store', dest='gamemode', type=str, default='default')
    parser.add_argument('-datagen', action='store_true', dest='datagen', default=False)
    args = parser.parse_args()
    if args.datagen:
        AIEngine().generate_data()
    else:
        e = Engine(args.width, args.height, args.bombs, args.gamemode)
        session = Game(e)
        session.loop()
