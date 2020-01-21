import pygame as pg

LEFT_CLICK = 1
RIGHT_CLICK = 3

class Game:

    def __init__(self, x_tiles, y_tiles, tile_dim=20):
        self.x_tiles = x_tiles
        self.y_tiles = y_tiles
        self.tile_dim = tile_dim
        pg.init()

        self.board = Board(x_tiles, y_tiles, tile_dim)
        self.running = True

    def loop(self):
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    # print(event)
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

    def __init__(self, xTiles, yTiles, tileDim=20):
        self.screen_width = tileDim * xTiles
        self.screen_height = tileDim * yTiles
        self.tile_dim = tileDim
        # self.font = pg.font.SysFont(None, self.tile_dim)
        self.font = pg.font.Font(pg.font.get_default_font(), self.tile_dim)

        self.screen = pg.display.set_mode([self.screen_width, self.screen_height])
        pg.display.set_caption("Minesweeper")

        GREY = (155, 155, 155)
        WHITE = (255, 255, 255)

        self.tiles = {}
        dark = False

        for x in range(0, self.screen_width, tileDim):
            for y in range(0, self.screen_height, tileDim):
                color = GREY if dark else WHITE
                print(color)
                self.tiles[(x // tileDim, y // tileDim)] = Tile(x, y, color, tileDim, 3, self.font, has_bomb=True)
                dark = not dark

    def map_click(self, x, y):
        return (x // self.tile_dim, y // self.tile_dim)

    def draw_screen(self):
        self.screen.fill((255,255,255))

        for tile in self.tiles.values():
            tile.draw(self.screen)

        pg.display.flip()

    def toggle_flag(self, tileX, tileY):
        self.tiles[(tileX, tileY)].toggle_flag()

    def check_tile(self, tileX, tileY):
        return self.tiles[(tileX, tileY)].check_tile()

class Tile:

    def __init__(self, x, y, color, width, num_bombs, font, has_bomb=False):
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
        pg.draw.rect(screen, self.color, self.rect)
        screen.blit(self.text_surface, (self.x, self.y))

    def _update_text(self, text):
        self.text_surface = self.font.render(text, False, (255,255,255))

    def toggle_flag(self):
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