import pygame
from MapView.Consts import WHITE


class Panel(pygame.sprite.Sprite):
    """ Base class for panels """
    def __init__(self, pos_x, pos_y, width, height, texture_path, surface, name):
        """ Constructor. Initialize panel.

        :param pos_x: panel's x position
        :param pos_y: panel's y position
        :param width: panel's width (will be converted on integer)
        :param height: panel's height (will be converted on integer)
        :param texture_path: path to panel's texture
        :param surface: surface on which panel should be drawn
        """
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = int(width)
        self.height = int(height)
        self.surface = surface

        self.image = pygame.image.load(texture_path)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))

        self.panels_surface = pygame.Surface.copy(self.image)

    def draw(self):
        """ This function draws panel. """
        pass

    def clean(self):
        """ Clean panel surface. """
        self.panels_surface = pygame.Surface.copy(self.image)
