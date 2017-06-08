from Panel import Panel
from Consts import BUILDINGS_PANEL_TEXTURE, GREEN, DELETE_BUILDING_HEIGHT, DELETE_BUILDING_WIDTH
from Utils import draw_text_with_wrapping, draw_text
from RelativePaths import relative_textures_path
from Button import Button

import pygame


class InfoPanel(Panel):
    def __init__(self, pos_x, pos_y, width, height, game_screen, del_building_fun):
        Panel.__init__(self, pos_x, pos_y, width, height, BUILDINGS_PANEL_TEXTURE)
        self.game_screen = game_screen
        self.curr_building = None

        self.del_building_button = Button(self.pos_x + self.width - DELETE_BUILDING_WIDTH * self.width, self.pos_y,
                                          int(DELETE_BUILDING_WIDTH * self.width),
                                          int(DELETE_BUILDING_HEIGHT * self.height),
                                          relative_textures_path + 'DeleteBuilding.png',
                                          self, del_building_fun)

    def draw_panel(self):
        self.game_screen.blit(self.image, (self.pos_x, self.pos_y))

    def draw_buildings_info(self, building, map_view):
        self.curr_building = building
        self.draw_panel()
        self.game_screen.blit(self.del_building_button.image, (self.pos_x + self.width - DELETE_BUILDING_WIDTH * self.width,
                              self.pos_y))
        map_view.del_button_sprite = self.del_building_button

        curr_y = draw_text(self.pos_x, self.pos_y, building.name, GREEN, self.game_screen)[1] + self.pos_y
        curr_y = map_view.resources.draw_resources_info(building.produces, self.pos_x, curr_y, self.width + self.pos_x, "Produces")
        map_view.resources.draw_resources_info(building.consumes, self.pos_x, curr_y, self.width + self.pos_x, "Consumes")

    def redraw_panel(self, map_view):
        self.draw_panel()
        if self.curr_building is not None:
            self.game_screen.blit(self.del_building_button.image, self.del_building_button.rect)
            map_view.del_button_sprite = self.del_building_button

            curr_y = draw_text(self.pos_x, self.pos_y, self.curr_building.name, GREEN, self.game_screen)[1] + self.pos_y
            curr_y = map_view.resources.draw_resources_info(self.curr_building.produces, self.pos_x, curr_y, self.width + self.pos_x,
                                                            "Produces")
            map_view.resources.draw_resources_info(self.curr_building.consumes, self.pos_x, curr_y, self.width + self.pos_x,
                                                   "Consumes")
