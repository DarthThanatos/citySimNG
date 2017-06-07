from Panel import Panel
from Consts import BUILDINGS_PANEL_TEXTURE, GREEN, DELETE_BUILDING_HEIGHT, DELETE_BUILDING_WIDTH
from Utils import draw_text_with_wrapping, draw_text
from RelativePaths import relative_textures_path

import pygame


class InfoPanel(Panel):
    def __init__(self, pos_x, pos_y, width, height, game_screen):
        Panel.__init__(self, pos_x, pos_y, width, height, BUILDINGS_PANEL_TEXTURE)
        self.game_screen = game_screen
        self.curr_building = None

        self.delete_icon_image = pygame.image.load(relative_textures_path + 'DeleteBuilding.png')
        self.delete_icon_image = pygame.transform.scale(self.delete_icon_image, (int(DELETE_BUILDING_WIDTH * self.width),
                                                                                 int(DELETE_BUILDING_HEIGHT * self.height)))

        self.delete_icon_rect = self.delete_icon_image.get_rect(
            topleft=(self.pos_x + self.width - DELETE_BUILDING_WIDTH * self.width,
                     self.pos_y))

    def draw_panel(self):
        self.game_screen.blit(self.image, (self.pos_x, self.pos_y))

    def draw_buildings_info(self, building, map_view):
        self.curr_building = building
        self.draw_panel()
        self.game_screen.blit(self.delete_icon_image, (self.pos_x + self.width - DELETE_BUILDING_WIDTH * self.width,
                                                       self.pos_y))
        map_view.del_button_sprite = self.delete_icon_rect

        # TODO: same code as in resources panel
        for (resource, value) in building.produces.iteritems():
            if value != 0:
                image = map_view.resources_panel.resources[resource].image
                self.game_screen.blit(image, (self.pos_x, self.pos_y))
                draw_text(self.pos_x + image.get_size()[0], self.pos_y, "{}".format(value), GREEN, self.game_screen)
        #
        # building_info = "{} \n " \
        #                 "{} \n " \
        #                 "{} \n " \
        #                 "{} \n ".format(building.name, building.produces, building.consumes, building.resources_cost)
        # draw_text_with_wrapping(self.pos_x, self.pos_y, self.pos_x + self.width, building_info, GREEN, self.game_screen)

