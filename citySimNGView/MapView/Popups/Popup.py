import pygame
import time
from MapView.Consts import BUILDINGS_PANEL_TEXTURE, GREEN, WHITE
from MapView.Utils import draw_text_with_wrapping


TIME_TO_APPEAR = 2
FONT_SIZE = 20


class Popup(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, sprite, width, height, surface):
        pygame.sprite.Sprite.__init__(self)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = int(width)
        self.height = int(height)
        self.sprite = sprite
        self.surface = surface

        self.timer = time.time()

        self.image = pygame.image.load(BUILDINGS_PANEL_TEXTURE)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect(midtop=(self.pos_x, self.pos_y))

        self.popup_surface = pygame.Surface.copy(self.image)

    def draw(self):
        # clean
        self.popup_surface = pygame.Surface.copy(self.image)

        if time.time() - self.timer > TIME_TO_APPEAR:
            curr_y, curr_x = 0, 0
            curr_y, widest_line = draw_text_with_wrapping(curr_x, curr_y, self.width, self.sprite.name, GREEN,
                                                          self.popup_surface, FONT_SIZE)

            # cut popup
            self.popup_surface = self.popup_surface.subsurface((0, 0, int(widest_line), int(curr_y)))

            self.rect = self.popup_surface.get_rect(midtop=(self.pos_x, self.pos_y))
            self.rect.clamp_ip(self.surface.get_rect())
            self.surface.blit(self.popup_surface, self.rect, (0, 0, self.width, int(curr_y)))
