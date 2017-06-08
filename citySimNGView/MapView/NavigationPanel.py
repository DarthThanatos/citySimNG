import pygame
from Panel import Panel
from Consts import BUILDINGS_PANEL_TEXTURE, NAV_ARROW_WIDTH, NAV_ARROW_HEIGHT, NAV_ARROW_TEXTURE
from NavigationArrow import NavigationArrow


class NavigationPanel(Panel):
    def __init__(self, pos_x, pos_y, width, height, game_screen, action):
        Panel.__init__(self, pos_x, pos_y, width, height, BUILDINGS_PANEL_TEXTURE)
        self.game_screen = game_screen
        self.action = action

    def draw_panel(self):
        self.game_screen.blit(self.image, (self.pos_x, self.pos_y))

    def add_navigation_arrows(self):
        middle_y = self.pos_y + self.height / 2 - self.height * NAV_ARROW_HEIGHT / 2
        middle_x = self.pos_x + self.width / 2 - self.width * NAV_ARROW_WIDTH / 2
        max_x = self.pos_x + self.width - NAV_ARROW_WIDTH * self.width
        max_y = self.pos_y + self.height - NAV_ARROW_HEIGHT * self.height

        left_arrow = NavigationArrow(self.width * NAV_ARROW_WIDTH, self.height * NAV_ARROW_HEIGHT,
                                     self.pos_x, middle_y, NAV_ARROW_TEXTURE, 0, self.game_screen, "Left",
                                     self, self.action)
        up_arrow = NavigationArrow(self.width * NAV_ARROW_HEIGHT, self.height * NAV_ARROW_WIDTH,
                                   middle_x, self.pos_y, NAV_ARROW_TEXTURE, 270, self.game_screen, "Up", self, self.action)
        right_arrow = NavigationArrow(self.width * NAV_ARROW_WIDTH, self.height * NAV_ARROW_HEIGHT, max_x, middle_y,
                                      NAV_ARROW_TEXTURE, 180, self.game_screen, "Right", self, self.action)
        down_arrow = NavigationArrow(self.width * NAV_ARROW_HEIGHT, self.height * NAV_ARROW_WIDTH, middle_x, max_y,
                                     NAV_ARROW_TEXTURE, 90, self.game_screen, "Down", self, self.action)

        self.navigation_arrows_sprites = [left_arrow, up_arrow, right_arrow, down_arrow]
        return [left_arrow, up_arrow, right_arrow, down_arrow]

    def redraw_panel(self, map_view):
        self.draw_panel()
        for nav_arrow in self.navigation_arrows_sprites:
            nav_arrow.draw_navigation_arrow()
