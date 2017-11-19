import pygame
from BasicSprite import BasicSprite


class ContainerSprite(BasicSprite):
    """ This class represents an instance of container sprite -
    sprite containing other sprites."""
    def __init__(self, pos_x, pos_y, width, height, texture_path, popup_text,
                 blit_surface, texture_rotation=0, rect_point='topleft'):
        """ Constructor.

        :param pos_x: x position [px]
        :param pos_y: y position [px]
        :param width: width [px] -> will be cast to integer
        :param height: height [px] -> will be cast to integer
        :param texture_path: path to texture
        :param popup_text: text displayed in popup
        :param rect_point: keyword argument used to get image rect
        """
        BasicSprite.__init__(self, pos_x, pos_y, width, height, texture_path,
                             popup_text, texture_rotation=texture_rotation,
                             rect_point=rect_point)

        self.all_sprites = pygame.sprite.Group()
        self.surface = pygame.Surface.copy(self.image)
        self.blit_surface = blit_surface

    def draw(self, surface=None):
        """ This function draws container sprite. """
        self.blit_surface.blit(self.surface, self.rect)

    def clean(self):
        """ Clean panel surface. """
        self.surface = pygame.Surface.copy(self.image)