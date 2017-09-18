import pygame
from CreatorView.RelativePaths import relative_textures_path
from MapView.Utils import calculate_text_size, draw_text
from MapView.Consts import GREEN, RESOURCES_SPACE

DEFAULT_RESOURCE_TEXTURE = relative_textures_path + "DefaultBuilding.jpg"
RESOURCE_SIZE = 0.03
WHITE = (255, 255, 255)


class Resource(pygame.sprite.Sprite):
    """ This class represents an instance of resource. """
    def __init__(self, name, texture_path):
        """ Constructor.

        :param name: resources's name
        :param texture_path: path to resource's texture
        """
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.texture_path = texture_path

        try:
            self.image = pygame.image.load(self.texture_path)
        except Exception:
            self.texture_path = DEFAULT_RESOURCE_TEXTURE
            self.image = pygame.image.load(self.texture_path)
        self.image.set_colorkey(WHITE)
