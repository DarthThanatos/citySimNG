from RelativePaths import relative_textures_path
import pygame

BUILDING_SIZE = 0.05
DEFAULT_BUILDING_TEXTURE = relative_textures_path + "DefaultBuilding.jpg"


class Building(pygame.sprite.Sprite):
    def __init__(self, name, id, resources_cost, texture, game_screen, pos=()):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.id = id
        self.resources_cost = resources_cost
        self.texture = texture
        self.game_screen = game_screen
        self.pos = pos

        width, height = self.game_screen.get_size()
        try:
            self.image = pygame.image.load(self.texture)
        except Exception:
            self.texture = DEFAULT_BUILDING_TEXTURE
            self.image = pygame.image.load(self.texture)
        self.image = pygame.transform.scale(self.image, (int(width * BUILDING_SIZE),
                                                         int(height * BUILDING_SIZE)))
        self.rect = self.image.get_rect(topleft=(pos[0], pos[1]))
