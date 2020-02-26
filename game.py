import pygame as pg
import operator
import json
from graphics.board import Board
from engine.engine import Engine
from engine.aiengine import AIEngine
from engine.datagen import DataGenerator
import argparse

LEFT_CLICK = 1
RIGHT_CLICK = 3


class Game:
    """
    Interactive GUI class with no game logic
    """
    def __init__(self, engine, tile_dim=50, gametype='normal', aiengine=None):
        self.x_tiles = engine.get_width()
        self.y_tiles = engine.get_height()
        self.tile_dim = tile_dim
        pg.init()

        self.board = Board(self.x_tiles, self.y_tiles, tile_dim)
        self.running = True
        self.engine = engine
        self.gametype = gametype
        self.aiengine = aiengine

        self.show_heatmap = False
        self.accept_input = True

    def do_normal_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if self.accept_input and event.type == pg.MOUSEBUTTONDOWN:
                x, y = event.pos
                t_x, t_y = self.board.map_click(x, y)
                button = event.button

                if button == LEFT_CLICK:
                    is_safe = self.engine.check_location(t_x, t_y)

                    if not is_safe:
                        self.accept_input = False

                elif button == RIGHT_CLICK:
                    self.engine.toggle_flag(t_x, t_y)

                if self.accept_input:
                    display_array = self.engine.get_display_board()
                    self.board.update_board(display_array)
                else:
                    self.board.update_board(self.engine.get_real_board())

        self.board.draw_screen()

    def do_aitest_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if self.accept_input and event.type == pg.MOUSEBUTTONDOWN:
                x, y = event.pos
                t_x, t_y = self.board.map_click(x, y)
                button = event.button

                if button == LEFT_CLICK:
                    self.accept_input = self.engine.check_location(t_x, t_y)

                if button == RIGHT_CLICK:
                    space_data = DataGenerator.get_data_for_space(t_x, t_y, self.engine, self.x_tiles, self.y_tiles, False)
                    features = self.aiengine.vectorize_data([space_data])['x']
                    pred = self.aiengine.get_prediction(features)

            if self.accept_input and event.type == pg.KEYDOWN:
                if pg.key.get_mods() & pg.KMOD_SHIFT:
                    self.accept_input = self._toggle_heatmap()

        if not self.show_heatmap:
            display_array = self.engine.get_display_board()
            if self.accept_input:
                self.board.update_board(display_array)
            else:
                self.board.update_board(self.engine.get_real_board())

        self.board.draw_screen()

    def _toggle_heatmap(self):
        self.show_heatmap = not self.show_heatmap
        front = self.engine.get_frontier()
        if self.show_heatmap:
            for x, y in front:
                space_data = DataGenerator.get_data_for_space(x, y, self.engine, self.x_tiles, self.y_tiles)
                features = self.aiengine.vectorize_data([space_data])['x']
                pred = self.aiengine.get_prediction(features)
                self.board.toggle_tile_heatmap(x, y, pred)
        else:
            preds = {}
            for x, y in front:
                space_data = DataGenerator.get_data_for_space(x, y, self.engine, self.x_tiles, self.y_tiles)
                features = self.aiengine.vectorize_data([space_data])['x']
                pred = self.aiengine.get_prediction(features)
                preds[(x, y)] = pred[0][1]
                self.board.toggle_tile_heatmap(x, y)
            shmove = max(preds, key=lambda key: abs(0.5-(preds[key]+0.01)))
            print(shmove, preds[shmove])
            if preds[shmove] <= 0.5:
                return self.engine.check_location(shmove[0], shmove[1])
            else:
                self.engine.toggle_flag(shmove[0], shmove[1])

            display_array = self.engine.get_display_board()
            self.board.update_board(display_array)
        return True

    def loop(self):
        """
        Render the board and handle mouse input
        :return:
        """
        while self.running:
            if self.gametype == 'normal':
                self.do_normal_loop()
            elif self.gametype == 'aitest':
                self.do_aitest_loop()

        pg.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-width', action='store', dest='width', type=int, default=15)
    parser.add_argument('-height', action='store', dest='height', type=int, default=15)
    parser.add_argument('-bombs', action='store', dest='bombs', type=int, default=50)
    parser.add_argument('-gamemode', action='store', dest='gamemode', type=str, default='default')
    parser.add_argument('-datagen', action='store', dest='datagen', type=int, default=0)
    parser.add_argument('-vectorize', action='store', dest='vectorize', default=None)
    parser.add_argument('-ai', action='store', dest='ai', default=None)
    args = parser.parse_args()

    if args.datagen:
        AIEngine().generate_data(args.datagen)
    # Adding this hook for debugging purposes
    if args.vectorize:
        AIEngine().vectorize_json(args.vectorize)
    if args.ai:
        data = {}
        try:
            with open('vectorizeddataset.json', 'r') as f:
                data = json.loads(f.read())
        except:
            raise ValueError('Missing training data, please run game.py with -datagen and -vectorize flags')
        if not data['x'] or not data['y']:
            raise ValueError('Missing training data, please run game.py with -datagen and -vectorize flags')
        aie = AIEngine()
        if args.ai == 'DTC':
            aie.train_decision_tree([data['x'], data['y']])
            e = Engine(args.width, args.height, args.bombs, args.gamemode)
            session = Game(e, 50, 'aitest', aie)
            session.loop()
        else:
            raise ValueError('Unknown classifier type {}'.format(args.ai))
    else:
        e = Engine(args.width, args.height, args.bombs, args.gamemode)
        session = Game(e)
        session.loop()
