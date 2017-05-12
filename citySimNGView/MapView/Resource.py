import pygame
from RelativePaths import relative_textures_path

DEFAULT_RESOURCE_TEXTURE = relative_textures_path + "DefaultBuilding.jpg"
RESOURCE_SIZE = 0.03
WHITE = (255, 255, 255)


class Resource(pygame.sprite.Sprite):
    def __init__(self, name, texture_path, game_screen):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.texture_path = texture_path
        self.game_screen = game_screen

        width, height = self.game_screen.get_size()
        try:
            self.image = pygame.image.load(self.texture_path)
        except Exception:
            self.texture_path = DEFAULT_RESOURCE_TEXTURE
            self.image = pygame.image.load(self.texture_path)
        self.image = self.image.convert_alpha()
        self.image.set_colorkey(WHITE)
        self.image = pygame.transform.scale(self.image, (int(width * RESOURCE_SIZE),
                                                         int(height * RESOURCE_SIZE)))
