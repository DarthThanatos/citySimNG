import pygame
from MapView.Consts import WHITE
from MapView.CustomSprites.ContainerSprite import ContainerSprite


class Panel(ContainerSprite):
    """ Base class for panels """
    def __init__(self, pos_x, pos_y, width, height, texture_path, blit_surface, name):
        """ Constructor. Initialize panel.

        :param pos_x: panel's x position
        :param pos_y: panel's y position
        :param width: panel's width (will be converted on integer)
        :param height: panel's height (will be converted on integer)
        :param texture_path: path to panel's texture
        :param blit_surface: surface on which panel should be drawn
        """
        ContainerSprite.__init__(self, pos_x, pos_y, width, height, texture_path, name)
        self.name = name
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = int(width)
        self.height = int(height)
        self.blit_surface = blit_surface

        self.all_sprites = pygame.sprite.Group()

        self.surface = pygame.Surface.copy(self.image)

    def clean(self):
        """ Clean panel surface. """
        self.surface = pygame.Surface.copy(self.image)
