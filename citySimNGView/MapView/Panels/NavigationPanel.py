import pygame

from MapView.Consts import NAV_PANEL_TEX, NAV_ARROW_WIDTH, NAV_ARROW_HEIGHT, NAV_ARROW_TEXTURE, PURPLE
from MapView.Items.NavigationArrow import NavigationArrow
from MapView.Panels.Panel import Panel
from MapView.Utils import draw_text


class NavigationPanel(Panel):
    """ This class represents an instance of panel containing navigation items."""
    def __init__(self, pos_x, pos_y, width, height, surface, action):
        """ Constructor.

        :param pos_x: x position on screen
        :param pos_y: y position on screen
        :param width: panel's width
        :param height: panel's height
        :param action: action performed when navigation arrow is clicked
        """
        Panel.__init__(self, pos_x, pos_y, width, height, NAV_PANEL_TEX, surface, 'Naigation Panel')
        self.action = action
        self.map_position_x = 0
        self.map_position_y = 0

        # create navigation arrows
        middle_y = self.pos_y + self.height / 2 - self.height * NAV_ARROW_HEIGHT / 2
        middle_x = self.pos_x + self.width / 2 - self.width * NAV_ARROW_WIDTH / 2
        max_x = self.pos_x + self.width - NAV_ARROW_WIDTH * self.width
        max_y = self.pos_y + self.height - NAV_ARROW_HEIGHT * self.height

        self.left_arrow = NavigationArrow(self.pos_x, middle_y, self.width * NAV_ARROW_WIDTH,
                                          self.height * NAV_ARROW_HEIGHT, NAV_ARROW_TEXTURE, 0, "Left", self,
                                          self.action)
        self.up_arrow = NavigationArrow(middle_x, self.pos_y, self.width * NAV_ARROW_HEIGHT,
                                        self.height * NAV_ARROW_WIDTH, NAV_ARROW_TEXTURE, 270, "Up", self, self.action)
        self.right_arrow = NavigationArrow(max_x, middle_y, self.width * NAV_ARROW_WIDTH,
                                           self.height * NAV_ARROW_HEIGHT, NAV_ARROW_TEXTURE, 180, "Right", self,
                                           self.action)
        self.down_arrow = NavigationArrow(middle_x, max_y, self.width * NAV_ARROW_HEIGHT, self.height * NAV_ARROW_WIDTH,
                                          NAV_ARROW_TEXTURE, 90, "Down", self, self.action)

        self.navigation_arrows_sprites = pygame.sprite.Group()
        self.navigation_arrows_sprites.add(self.left_arrow, self.right_arrow, self.up_arrow, self.down_arrow)

    def draw(self):
        """ Draw navigation panel with position on map and navigation arrows. Before drawing in panel it is
        being cleaned. """
        self.clean()
        draw_text(0, 0, "{}:{}".format(self.map_position_x, self.map_position_y), PURPLE, self.panels_surface)
        for arrow in self.navigation_arrows_sprites:
            self.panels_surface.blit(arrow.image, (arrow.rect[0] - self.pos_x, arrow.rect[1] - self.pos_y))
        self.surface.blit(self.panels_surface, (self.pos_x, self.pos_y))
