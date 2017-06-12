import pygame
from Consts import WHITE


class Panel(pygame.sprite.Sprite):

    def __init__(self, pos_x, pos_y, width, height, texture):
        pygame.sprite.Sprite.__init__(self)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height

        self.image = pygame.image.load(texture)
        self.image = pygame.transform.scale(self.image, (int(self.width), int(self.height)))  # scale needs integers
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))

    def draw_panel(self):
        pass

    def redraw_panel(self, map_view):
        pass
