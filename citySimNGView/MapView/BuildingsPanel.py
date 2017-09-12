import uuid

import pygame

from Building import Building
from Button import Button
from Consts import BUILDINGS_PANEL_TEXTURE, ARROW_BUTTON_WIDTH, ARROW_BUTTON_HEIGHT, BUILDINGS_PANEL_RIGHT_ARROW_X, \
    BUILDINGS_PANEL_ARROW_Y, BUILDINGS_PANEL_LEFT_ARROW_X, BUILDING_SIZE, SPACE
from Panel import Panel
from utils.RelativePaths import relative_textures_path


class BuildingsPanel(Panel):
    def __init__(self, pos_x, pos_y, width, height, game_screen, main_panel):
        Panel.__init__(self, pos_x, pos_y, width, height, BUILDINGS_PANEL_TEXTURE)
        self.game_screen = game_screen
        self.main_panel = main_panel
        self.buildings_info = None
        self.page = 1
        self.page_buildings = {}
        self.last_page = 1

        self.right_arrow = Button(self.pos_x + BUILDINGS_PANEL_RIGHT_ARROW_X * self.width,
                                  BUILDINGS_PANEL_ARROW_Y * self.height, int(ARROW_BUTTON_WIDTH * self.width),
                                  int(ARROW_BUTTON_HEIGHT * self.height), relative_textures_path + "RightArrow.png",
                                  self, self.scroll_building_panel_right)

        self.left_arrow = Button(self.pos_x + BUILDINGS_PANEL_LEFT_ARROW_X * self.width,
                                 BUILDINGS_PANEL_ARROW_Y * self.height, int(ARROW_BUTTON_WIDTH * self.width),
                                 int(ARROW_BUTTON_HEIGHT * self.height), relative_textures_path + "LeftArrow.png",
                                 self, self.scroll_building_panel_left)

    def draw_panel(self):
        self.game_screen.blit(self.image, (self.pos_x, self.pos_y))

        self.game_screen.blit(self.right_arrow.image, self.right_arrow.rect)
        self.main_panel.right_arrow_buildings_panel = self.right_arrow

        self.game_screen.blit(self.left_arrow.image, self.left_arrow.rect)
        self.main_panel.left_arrow_buildings_panel = self.left_arrow

    def add_buildings_to_buildings_panel(self, buildings_info):
            width, height = self.game_screen.get_size()
            building_no = 0
            pos_x, pos_y = self.pos_x + SPACE, self.pos_y
            for building in buildings_info:
                # we have to go to new line
                if pos_x + BUILDING_SIZE * width > self.pos_x + self.width:
                    pos_x = self.pos_x + SPACE
                    pos_y = pos_y + BUILDING_SIZE * height + SPACE
                if pos_y + BUILDING_SIZE * height > BUILDINGS_PANEL_ARROW_Y * self.height:
                    pos_y = self.pos_y
                    self.page += 1
                    building_no = 0
                    self.last_page = self.page
                resource_cost_string = ""
                # for (resource, value) in building["resourcesCost"].iteritems():
                #     if value != 0:
                #         resource_cost_string += "{}: {} ; ".format(resource, value)
                building_sprite = Building(building["name"], uuid.uuid4().__str__(), building["texturePath"],
                                           building["resourcesCost"], building["consumes"], building["produces"], (width, height),
                                           pos=(pos_x, pos_y))
                pos_x += BUILDING_SIZE * width + SPACE
                if str(self.page) in self.page_buildings:
                    self.page_buildings[str(self.page)].append(building_sprite)
                else:
                    self.page_buildings[str(self.page)] = [building_sprite]
                building_no += 1
                # if (BUILDING_SIZE * height) * (building_no / 2 + 1) + SPACE * (building_no / 2) > BUILDINGS_PANEL_ARROW_Y * self.height:
                #     self.page += 1
                #     building_no = 0
                #     self.last_page = self.page
                # resource_cost_string = ""
                # for (resource, value) in building["resourcesCost"].iteritems():
                #     if value != 0:
                #         resource_cost_string += "{}: {} ; ".format(resource, value)
                # building_sprite = Building(building["name"], uuid.uuid4().__str__(), building["texturePath"],
                #                            resource_cost_string, building["consumes"], building["produces"], (width, height),
                #                            pos=(self.pos_x + BUILDING_SIZE * width * (building_no % 2) + (building_no % 2 + 1) * SPACE,
                #                                 BUILDING_SIZE * height * (building_no / 2) + SPACE * (building_no / 2)))
                # if str(self.page) in self.page_buildings:
                #     self.page_buildings[str(self.page)].append(building_sprite)
                # else:
                #     self.page_buildings[str(self.page)] = [building_sprite]
                # building_no += 1
            self.page = 1
            self.draw_buildings_in_buildings_panel()

    def draw_buildings_in_buildings_panel(self):
        self.main_panel.buildings_panel_sprites = pygame.sprite.Group()
        for building in self.page_buildings[str(self.page)]:
            self.game_screen.blit(building.image, (building.pos[0], building.pos[1]))
            self.main_panel.buildings_panel_sprites.add(building)

    def scroll_building_panel_right(self):
        if self.page < self.last_page:
            self.page += 1
            self.draw_panel()
            self.draw_buildings_in_buildings_panel()

    def scroll_building_panel_left(self):
        if self.page > 1:
            self.page -= 1
            self.draw_panel()
            self.draw_buildings_in_buildings_panel()

    def redraw_panel(self, map_view):
        self.draw_panel()
        self.draw_buildings_in_buildings_panel()
