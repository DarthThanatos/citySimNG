import pygame
from MapView.Items.Button import Button

Y_POSITIONS = {
    "0": 0.7,
    "1": 0.62,
    "2": 0.54,
    "3": 0.46,
    "4": 0.38
}

HINT_WIDTH = 0.05
HINT_HEIGHT = 0.05

class ClosedHintModal(Button):
    def __init__(self, game_board_height, width, height, texture_path,
                 game_board, hints, expand_hint_modal, id):
        Button.__init__(self, 0, game_board_height * Y_POSITIONS[str(id)],
                        width, height, texture_path, expand_hint_modal,
                        game_board, "Hint")
        self.id = id
        self.game_board = game_board
        self.game_board_height = game_board_height
        self.hints = hints
        self.need_update = False

    def draw(self):
        self.game_board.blit(self.image, self.rect)

    def update(self):
        self.id -= 1
        self.pos_y = int(self.game_board_height * Y_POSITIONS[str(self.id)])
        self.load_texture()
        self.set_rect()
