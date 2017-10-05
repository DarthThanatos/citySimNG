import pygame
import time
from MapView.Consts import BUILDINGS_PANEL_TEXTURE, GREEN, WHITE
from MapView.Utils import draw_text_with_wrapping
from MapView.CustomSprites.ContainerSprite import ContainerSprite


TIME_TO_APPEAR = 1
FONT_SIZE = 20


class Popup(ContainerSprite):
    def __init__(self, pos_x, pos_y, sprite, width, height, blit_surface):
        ContainerSprite.__init__(self, pos_x, pos_y, width, height, BUILDINGS_PANEL_TEXTURE, 'Popup',
                                 rect_point='midtop')
        self.sprite = sprite
        self.blit_surface = blit_surface

        self.timer = time.time()

    def draw(self):
        # clean
        self.load_texture(rect_point='midtop')
        self.surface = pygame.Surface.copy(self.image)
        if time.time() - self.timer > TIME_TO_APPEAR:
            curr_y, curr_x = 0, 0
            curr_y, widest_line = draw_text_with_wrapping(curr_x, curr_y, self.width, self.sprite.popup_text, GREEN,
                                                          self.surface, FONT_SIZE)

            # cut popup
            self.surface = self.surface.subsurface((0, 0, int(widest_line), int(curr_y)))

            self.rect = self.surface.get_rect(midtop=(self.pos_x, self.pos_y))
            self.rect.clamp_ip(self.blit_surface.get_rect())
            self.blit_surface.blit(self.surface, self.rect, (0, 0, self.width, int(curr_y)))
