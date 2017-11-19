import uuid

import pygame
from CreatorView.RelativePaths import relative_textures_path

from MapView.Consts import ARROW_BUTTON_WIDTH, ARROW_BUTTON_HEIGHT, \
    GREEN
from MapView.Items.PanelBuilding import PanelBuilding
from MapView.Items.Button import Button
from MapView.Panels.Panel import Panel
from MapView.Utils import draw_text_with_wrapping_and_centering

BUILDING_HEIGHT = 0.15
BUILDING_WIDTH = 0.45
SPACE = 0.1
ARROW_Y = 0.85
LEFT_ARROW_X = 0.1
RIGHT_ARROW_X = 0.6
BUILDINGS_POPUP_WIDTH = 0.7


class BuildingsPanel(Panel):
    """ This class represents an instance of panel containing buildings. """

    def __init__(self, pos_x, pos_y, width, height, texture_path, blit_surface,
                 domestic_buildings_data, industrial_buildings_data,
                 resources_panel_pos_y, resources_panel_height):
        """ Constructor.

        :param pos_x: x position on screen
        :param pos_y: y position on screen
        :param width: panel's width
        :param height: panel's height
        :param blit_surface: surface on which panel should be drawn
        :param buildings_data: information about buildings available in game
        """
        Panel.__init__(self, pos_x, pos_y, width, height, texture_path,
                       blit_surface, 'Buildings Panel')
        self.domestic_buildings_data = domestic_buildings_data
        self.industrial_buildings_data = industrial_buildings_data
        self.buildings = {}
        self.buildings_sprites = pygame.sprite.Group()
        self.curr_page = 1
        self.last_page = 1
        self.page_buildings = {}

        self.create_scrolling_arrows()
        self.init_buildings_pages(resources_panel_pos_y,
                                  resources_panel_height,
                                  domestic_buildings_data,
                                  industrial_buildings_data)

    def draw(self):
        """ Draw buildings panel with arrows for changing pages and buildings
        from current page. Before drawing in panel it is being cleaned. """
        self.clean()

        # draw arrows
        self.surface.blit(self.right_arrow.image,
                          (self.right_arrow.rect[0] - self.pos_x,
                           self.right_arrow.rect[1] - self.pos_y))
        self.surface.blit(self.left_arrow.image,
                          (self.left_arrow.rect[0] - self.pos_x,
                           self.left_arrow.rect[1] - self.pos_y))

        # draw buildngs
        self.draw_buildings_in_buildings_panel()

        # blit panel
        self.blit_surface.blit(self.surface, (self.pos_x, self.pos_y))

    def parse_buildings_data(self, resources_panel_pos_y,
                             resources_panel_height,
                             buildings_data, buildings_type):
        """ Parse information about buildings available in game sent by model
        - split buildings into pages and create sprite for each building. """
        curr_x, curr_y = 0, self.get_header_height(buildings_type)
        for building in buildings_data:
            # we have to go to next line
            if curr_x + BUILDING_WIDTH * self.width > self.width:
                curr_x = 0
                curr_y = curr_y + BUILDING_HEIGHT * self.height + \
                         SPACE * self.width

            # we have to go to next page
            if curr_y + BUILDING_HEIGHT * self.height > ARROW_Y * self.height:
                curr_y = 0.1 * self.height
                self.curr_page += 1
                self.last_page = self.curr_page

            building_sprite = PanelBuilding(building.getName(),
                                            uuid.uuid4().__str__(),
                                            building.getTexturePath(),
                                            building.getType(),
                                            building.getResourcesCost(),
                                            building.getConsumes(),
                                            building.getProduces(),
                                            building.getDwellersAmount(),
                                            building.getDwellersName(),
                                            curr_x + self.pos_x,
                                            curr_y + self.pos_y,
                                            BUILDING_WIDTH * self.width,
                                            BUILDING_HEIGHT * self.height,
                                            building.isEnabled())

            self.buildings[building.getName()] = building_sprite

            building_sprite.popup = building_sprite.create_popup(
                self.pos_x,
                resources_panel_pos_y + resources_panel_height,
                BUILDINGS_POPUP_WIDTH * self.width,
                self.height,
                self.texture_path,
                self.blit_surface)

            curr_x += BUILDING_WIDTH * self.width + SPACE * self.width

            if str(self.curr_page) in self.page_buildings:
                self.page_buildings[str(self.curr_page)].append(
                    building_sprite)
            else:
                self.page_buildings[str(self.curr_page)] = [building_sprite]

    def draw_buildings_in_buildings_panel(self):
        """ Draw buildings from current page. """
        # blit header message
        panel_header_message = '{} buildings'.format(
            self.page_buildings[str(self.curr_page)][0].type)
        curr_y = draw_text_with_wrapping_and_centering(0, 0, self.width,
                                                       panel_header_message,
                                                       self.surface, GREEN)

        # blit buildings
        for building in self.page_buildings[str(self.curr_page)]:
            building.draw(self.surface, building.pos_x - self.pos_x,
                          building.pos_y - self.pos_y)

    def scroll_building_panel_right(self):
        """ Go to next page with buildings. """
        if self.curr_page < self.last_page:
            self.curr_page += 1
            self.update_buildings_sprites()

    def scroll_building_panel_left(self):
        """ Go to previous page with buildings. """
        if self.curr_page > 1:
            self.curr_page -= 1
            self.update_buildings_sprites()

    def enable_buildings(self, buildings):
        for building in buildings:
            self.buildings[building].is_enabled = True

    def get_header_height(self, buildings_type):
        header_message = '{} buildings'.format(buildings_type)
        return draw_text_with_wrapping_and_centering(0, 0, self.width,
                                                     header_message,
                                                     self.surface, GREEN,
                                                     blit=False)

    def create_scrolling_arrows(self):
        self.right_arrow = Button(RIGHT_ARROW_X * self.width + self.pos_x,
                                  ARROW_Y * self.height + self.pos_y,
                                  ARROW_BUTTON_WIDTH * self.width,
                                  ARROW_BUTTON_HEIGHT * self.height,
                                  relative_textures_path + "RightArrow.png",
                                  self.scroll_building_panel_right,
                                  self,
                                  "Go to the next page")

        self.left_arrow = Button(self.pos_x + LEFT_ARROW_X * self.width,
                                 self.pos_y + ARROW_Y * self.height,
                                 ARROW_BUTTON_WIDTH * self.width,
                                 ARROW_BUTTON_HEIGHT * self.height,
                                 relative_textures_path + "LeftArrow.png",
                                 self.scroll_building_panel_left,
                                 self,
                                 "Go to the previous page")

        self.all_sprites.add(self.right_arrow, self.left_arrow)

    def init_buildings_pages(self, resources_panel_pos_y,
                             resources_panel_height, domestic_buildings_data,
                             industrial_buildings_data):

        # parse domestic buildings data
        self.parse_buildings_data(resources_panel_pos_y,
                                  resources_panel_height,
                                  domestic_buildings_data,
                                  'Domestic')

        # for industrial buildings start new page
        if len(domestic_buildings_data) > 0:
            self.curr_page += 1

        # parse industrial buildings data
        self.parse_buildings_data(resources_panel_pos_y,
                                  resources_panel_height,
                                  industrial_buildings_data,
                                  'Industrial')

        # set last and current page
        self.last_page = self.curr_page
        self.curr_page = 1

        # update sprites according to current page
        self.update_buildings_sprites()

    def update_buildings_sprites(self):
        self.all_sprites.remove(self.buildings_sprites)
        self.buildings_sprites.empty()
        self.buildings_sprites = pygame.sprite.Group(
            [building_sprite for building_sprite in
             self.page_buildings[str(self.curr_page)]])
        self.all_sprites.add(self.buildings_sprites)
