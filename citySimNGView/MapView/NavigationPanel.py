import pygame
from Consts import BUILDINGS_PANEL_TEXTURE


class NavigationPanel(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, size_x, size_y, game_screen):
        pygame.sprite.Sprite.__init__(self)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.size_x = size_x
        self.size_y = size_y
        self.game_screen = game_screen

        self.image = pygame.image.load(BUILDINGS_PANEL_TEXTURE)
        self.image = pygame.transform.scale(self.image, (int(self.size_x), int(self.size_y)))
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))

    def draw_navigation_panel(self):
        self.game_screen.blit(self.image, (self.pos_x, self.pos_y))