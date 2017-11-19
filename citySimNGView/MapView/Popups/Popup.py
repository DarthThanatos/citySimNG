import pygame
import time
from MapView.Consts import GREEN, WHITE
from MapView.Utils import draw_text_with_wrapping
from MapView.CustomSprites.ContainerSprite import ContainerSprite


TIME_TO_APPEAR = 1
FONT_SIZE = 25
MARGIN = 0.03


class Popup(ContainerSprite):
    def __init__(self, pos_x, pos_y, texture_path, sprite, width, height,
                 blit_surface):
        ContainerSprite.__init__(self, pos_x, pos_y, width, height,
                                 texture_path, 'Popup',
                                 blit_surface, rect_point='midtop')
        self.sprite = sprite
        self.add_message()
        self.timer = time.time()

    def add_message(self):
        curr_y, curr_x = MARGIN * self.height, MARGIN * self.width
        max_message_width = self.width - 2 * MARGIN * self.width
        draw_result = draw_text_with_wrapping(
            curr_x, curr_y, max_message_width, self.sprite.popup_text,
            GREEN, self.surface, FONT_SIZE)
        curr_y, widest_line = draw_result[0], draw_result[1]

        # cut popup
        self.surface = self.surface.subsurface(
            (0, 0, int(widest_line + MARGIN * self.width),
             int(curr_y + MARGIN * self.height)))

        self.rect = self.surface.get_rect(midtop=(self.pos_x, self.pos_y))
        self.rect.clamp_ip(self.blit_surface.get_rect())

    def draw(self):
        if time.time() - self.timer > TIME_TO_APPEAR:
            self.rect.clamp_ip(self.blit_surface.get_rect())
            self.blit_surface.blit(self.surface, self.rect)
