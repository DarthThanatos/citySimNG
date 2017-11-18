import pygame
import time
from MapView.Items.Button import Button
from MapView.Consts import BUILDINGS_PANEL_TEXTURE

Y_POSITIONS = {
    "0": 400,
    "1": 350,
    "2": 300,
    "3": 250,
    "4": 200
}

HINT_WIDTH = 0.05
HINT_HEIGHT = 0.05

class ClosedHintModal(Button):
    def __init__(self, width, height, game_board, hints, expand_hint_modal,
                 id):
        Button.__init__(self, 0, Y_POSITIONS[str(id)], width, height,
                        BUILDINGS_PANEL_TEXTURE, expand_hint_modal,
                        game_board, "Hint")
        self.id = id
        self.game_board = game_board
        self.hints = hints
        self.need_update = False

    def draw(self):
        self.game_board.blit(self.image, self.rect)

    def update(self):
        self.id -= 1
        self.pos_y = Y_POSITIONS[str(self.id)]
        self.load_texture()
        self.set_rect()