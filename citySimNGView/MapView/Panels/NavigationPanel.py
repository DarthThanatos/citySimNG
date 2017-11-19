import pygame

from MapView.Consts import NAV_ARROW_WIDTH, NAV_ARROW_HEIGHT, \
    NAV_ARROW_TEXTURE, PURPLE
from MapView.Items.Button import Button
from MapView.Panels.Panel import Panel
from MapView.Utils import draw_text


class NavigationPanel(Panel):
    """ This class represents an instance of panel containing navigation items."""

    def __init__(self, pos_x, pos_y, width, height, texture_path, blit_surface,
                 action):
        """ Constructor.

        :param pos_x: x position on screen
        :param pos_y: y position on screen
        :param width: panel's width
        :param height: panel's height
        :param action: action performed when navigation arrow is clicked
        """
        Panel.__init__(self, pos_x, pos_y, width, height, texture_path,
                       blit_surface, 'Navigation Panel')
        self.action = action
        self.map_position_x = 0
        self.map_position_y = 0

        # create navigation arrows
        middle_y = self.pos_y + self.height / 2 - self.height * NAV_ARROW_HEIGHT / 2
        middle_x = self.pos_x + self.width / 2 - self.width * NAV_ARROW_WIDTH / 2
        max_x = self.pos_x + self.width - NAV_ARROW_WIDTH * self.width
        max_y = self.pos_y + self.height - NAV_ARROW_HEIGHT * self.height

        # mapping: rotation degree -> move direction
        self.arrow_direction = {
            0: 'Left',
            90: 'Down',
            180: 'Right',
            270: 'Up'
        }

        self.left_arrow = Button(self.pos_x, middle_y,
                                 self.width * NAV_ARROW_WIDTH,
                                 self.height * NAV_ARROW_HEIGHT,
                                 NAV_ARROW_TEXTURE, self.action, self,
                                 "Go left", texture_rotation=0)
        self.up_arrow = Button(middle_x, self.pos_y,
                               self.width * NAV_ARROW_HEIGHT,
                               self.height * NAV_ARROW_WIDTH,
                               NAV_ARROW_TEXTURE, self.action, self, "Go up",
                               texture_rotation=270)
        self.right_arrow = Button(max_x, middle_y,
                                  self.width * NAV_ARROW_WIDTH,
                                  self.height * NAV_ARROW_HEIGHT,
                                  NAV_ARROW_TEXTURE, self.action, self,
                                  "Go right", texture_rotation=180)
        self.down_arrow = Button(middle_x, max_y,
                                 self.width * NAV_ARROW_HEIGHT,
                                 self.height * NAV_ARROW_WIDTH,
                                 NAV_ARROW_TEXTURE, self.action, self,
                                 "Go down", texture_rotation=90)

        self.navigation_arrows_sprites = pygame.sprite.Group()
        self.navigation_arrows_sprites.add(self.left_arrow, self.right_arrow,
                                           self.up_arrow, self.down_arrow)
        self.all_sprites.add(self.navigation_arrows_sprites)

    def draw(self):
        """ Draw navigation panel with position on map and navigation arrows. Before drawing in panel it is
        being cleaned. """
        self.clean()
        draw_text(0, 0,
                  "{}:{}".format(self.map_position_x, self.map_position_y),
                  PURPLE, self.surface)
        for arrow in self.navigation_arrows_sprites:
            self.surface.blit(arrow.image, (
            arrow.rect[0] - self.pos_x, arrow.rect[1] - self.pos_y))
        self.blit_surface.blit(self.surface, (self.pos_x, self.pos_y))
