import uuid

import pygame
from CreatorView.RelativePaths import relative_textures_path

from MapView.Consts import BUILDINGS_PANEL_TEXTURE, ARROW_BUTTON_WIDTH, ARROW_BUTTON_HEIGHT, SPACE, GREEN
from MapView.Items.Building import Building
from MapView.Items.Button import Button
from MapView.Panels.Panel import Panel


BUILDING_HEIGHT = 0.15
BUILDING_WIDTH = 0.4
ARROW_Y = 0.85
LEFT_ARROW_X = 0.1
RIGHT_ARROW_X = 0.6


class BuildingsPanel(Panel):
    """ This class represents an instance of panel containing buildings. """
    def __init__(self, pos_x, pos_y, width, height, blit_surface, buildings_data):
        """ Constructor.

        :param pos_x: x position on screen
        :param pos_y: y position on screen
        :param width: panel's width
        :param height: panel's height
        :param blit_surface: surface on which panel should be drawn
        :param buildings_data: information about buildings available in game
        """
        Panel.__init__(self, pos_x, pos_y, width, height, BUILDINGS_PANEL_TEXTURE, blit_surface, 'Buildings Panel')
        self.buildings_data = buildings_data
        self.buildings_sprites = pygame.sprite.Group()
        self.curr_page = 1
        self.last_page = 1
        self.page_buildings = {}

        self.right_arrow = Button(RIGHT_ARROW_X * self.width + self.pos_x, ARROW_Y * self.height + self.pos_y,
                                  ARROW_BUTTON_WIDTH * self.width, ARROW_BUTTON_HEIGHT * self.height,
                                  relative_textures_path + "RightArrow.png", self.scroll_building_panel_right, self,
                                  "Go to the next page")
        self.left_arrow = Button(self.pos_x + LEFT_ARROW_X * self.width, self.pos_y + ARROW_Y * self.height,
                                 ARROW_BUTTON_WIDTH * self.width, ARROW_BUTTON_HEIGHT * self.height,
                                 relative_textures_path + "LeftArrow.png", self.scroll_building_panel_left, self,
                                 "Go to the previous page")
        self.all_sprites.add(self.right_arrow, self.left_arrow)

        self.parse_buildings_data()

    def draw(self):
        """ Draw buildings panel with arrows for changing pages and buildings from current page.
        Before drawing in panel it is being cleaned. """
        self.clean()
        self.surface.blit(self.right_arrow.image, (self.right_arrow.rect[0] - self.pos_x,
                                                          self.right_arrow.rect[1] - self.pos_y))
        self.surface.blit(self.left_arrow.image, (self.left_arrow.rect[0] - self.pos_x,
                                                         self.left_arrow.rect[1] - self.pos_y))
        self.draw_buildings_in_buildings_panel()
        self.blit_surface.blit(self.surface, (self.pos_x, self.pos_y))

    def parse_buildings_data(self):
        """ Parse information about buildings available in game sent by model - split buildings into pages and
        create sprite for each building. """
        curr_x, curr_y = 0, 0
        for building in self.buildings_data:
            # we have to go to next line
            if curr_x + BUILDING_WIDTH * self.width > self.width:
                curr_x = 0
                curr_y = curr_y + BUILDING_HEIGHT * self.height + SPACE

            # we have to go to next page
            if curr_y + BUILDING_HEIGHT * self.height > ARROW_Y * self.height:
                curr_y = 0
                self.curr_page += 1
                self.last_page = self.curr_page

            building_sprite = Building(building.getName(), uuid.uuid4().__str__(), building.getTexturePath(),
                                       building.getResourcesCost(), building.getConsumes(), building.getProduces(),
                                       curr_x + self.pos_x, curr_y + self.pos_y, BUILDING_WIDTH * self.width,
                                       BUILDING_HEIGHT * self.height)
            self.all_sprites.add(building_sprite)
            curr_x += BUILDING_WIDTH * self.width + SPACE
            if str(self.curr_page) in self.page_buildings:
                self.page_buildings[str(self.curr_page)].append(building_sprite)
            else:
                self.page_buildings[str(self.curr_page)] = [building_sprite]
        self.curr_page = 1

    def draw_buildings_in_buildings_panel(self):
        """ Draw buildings from current page. """
        self.buildings_sprites = pygame.sprite.Group()
        for building in self.page_buildings[str(self.curr_page)]:
            building.draw(self.surface, building.pos_x - self.pos_x, building.pos_y - self.pos_y)
            self.buildings_sprites.add(building)

    def scroll_building_panel_right(self):
        """ Go to next page with buildings. """
        if self.curr_page < self.last_page:
            self.curr_page += 1

    def scroll_building_panel_left(self):
        """ Go to previous page with buildings. """
        if self.curr_page > 1:
            self.curr_page -= 1
