import pygame
from RelativePaths import relative_textures_path
from Consts import NAV_ARROW_TEXTURE, NAV_ARROW_HEIGHT, NAV_ARROW_WIDTH, BUILDINGS_PANEL_SIZE, RESOURCES_PANEL_SIZE
from Button import Button


class NavigationArrow(Button):
    def __init__(self, width, height, pos_x, pos_y, texture_path, rotation, game_screen, direction, panel, action):
        Button.__init__(self, pos_x, pos_y, int(width), int(height), texture_path, panel, action)
        self.rotation = rotation
        self.game_screen = game_screen
        self.direction = direction

        self.image = pygame.image.load(texture_path)
        self.image = pygame.transform.rotate(self.image, rotation)
        self.image = pygame.transform.scale(self.image, (int(self.width), int(self.height)))
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))

    def draw_navigation_arrow(self):
        self.game_screen.blit(self.image, self.rect)

    def release_button(self, map_view):
        self.action(*self.args)
        self.image = pygame.image.load(self.texture)
        self.image = pygame.transform.rotate(self.image, self.rotation)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))
        self.panel.redraw_panel(map_view)