import pygame
from RelativePaths import relative_textures_path
from Consts import NAV_ARROW_TEXTURE, NAV_ARROW_HEIGHT, NAV_ARROW_WIDTH, BUILDINGS_PANEL_SIZE, RESOURCES_PANEL_SIZE


class NavigationArrow(pygame.sprite.Sprite):
    def __init__(self, size_x, size_y, pos_x, pos_y, texture_path, rotation, game_screen, direction):
        pygame.sprite.Sprite.__init__(self)
        self.size_x = size_x
        self.size_y = size_y
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rotation = rotation
        self.game_screen = game_screen
        self.direction = direction
        self.texture_path = texture_path

        self.image = pygame.image.load(texture_path)
        self.image = pygame.transform.rotate(self.image, rotation)
        self.image = pygame.transform.scale(self.image, (int(self.size_x), int(self.size_y)))
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))

    def draw_navigation_arrow(self):
        self.game_screen.blit(self.image, (self.pos_x, self.pos_y))
