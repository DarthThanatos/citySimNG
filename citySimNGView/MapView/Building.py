import pygame
from Consts import BUILDING_SIZE, DEFAULT_BUILDING_TEXTURE


class Building(pygame.sprite.Sprite):
    def __init__(self, name, id, resources_cost, texture, game_screen_size, pos):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.id = id
        self.resources_cost = resources_cost
        self.texture = texture
        self.game_screen_size = game_screen_size
        self.pos = pos

        width, height = self.game_screen_size
        try:
            self.image = pygame.image.load(self.texture)
        except Exception:
            self.texture = DEFAULT_BUILDING_TEXTURE
            self.image = pygame.image.load(self.texture)
        self.image = pygame.transform.scale(self.image, (int(width * BUILDING_SIZE),
                                                         int(height * BUILDING_SIZE)))
        self.rect = self.image.get_rect(topleft=(pos[0], pos[1]))
