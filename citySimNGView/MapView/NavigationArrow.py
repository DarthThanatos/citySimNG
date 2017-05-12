import pygame
from RelativePaths import relative_textures_path


class NavigationArrow(pygame.sprite.Sprite):
    def __init__(self, size_x, size_y, pos_x, pos_y, texture_path, rotation, game_screen, direction):
        pygame.sprite.Sprite.__init__(self)
        self.size_x = size_x
        self.size_y = size_y
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.texture_path = texture_path
        self.rotation = rotation
        self.game_screen = game_screen
        self.direction = direction

        image = pygame.image.load(relative_textures_path + 'LeftArrow.png')
        image = pygame.transform.rotate(image, rotation)
        image = pygame.transform.scale(image, (int(self.size_x), int(self.size_y)))
        self.rect = image.get_rect(topleft=(self.pos_x, self.pos_y))
        self.game_screen.blit(image, (self.pos_x, self.pos_y))
