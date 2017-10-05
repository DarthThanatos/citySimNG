import pygame
from BasicSprite import BasicSprite


class ContainerSprite(BasicSprite):
    def __init__(self, pos_x, pos_y, width, height, texture_path, popup_text, rect_point='topleft'):
        BasicSprite.__init__(self, pos_x, pos_y, width, height, texture_path, popup_text, rect_point=rect_point)
        self.all_sprites = pygame.sprite.Group()
        self.surface = pygame.Surface.copy(self.image)
