import pygame
import time
from MapView.Consts import YELLOW, RED, GOLD, LIGHT_BLUE
from MapView.Items.Resources import draw_items_info, resources
from MapView.Items.Dwellers import draw_dwellers_info
from MapView.Items.Resource import Resource
from MapView.Utils import draw_text_with_wrapping
from Popup import Popup

FONT_SIZE = 25
RESOURCE_IMAGE_WIDTH = 40
RESOURCE_IMAGE_HEIGHT = 40
MARGIN = 2
SPACE = 0.1


class BuildingsPanelPopup(Popup):
    def __init__(self, pos_x, pos_y, width, height, texture_path, building,
                 surface):
        Popup.__init__(self, pos_x, pos_y, texture_path, building, width,
                       height, surface)

        self.add_message()

    def add_message(self):
        curr_x, curr_y = MARGIN, MARGIN
        max_message_width = self.width - 2 * MARGIN

        # buildings name
        curr_y = draw_text_with_wrapping(curr_x, curr_y, max_message_width,
                                         '{}'.format(self.sprite.name),
                                         YELLOW, self.surface,
                                         FONT_SIZE)[0]

        # cost
        curr_y = \
            draw_text_with_wrapping(curr_x, curr_y, max_message_width, "Cost",
                                    GOLD, self.surface, FONT_SIZE)[0]
        curr_y = draw_items_info(self.sprite.resources_cost, curr_x, curr_y,
                                 max_message_width,
                                 self, image_width=RESOURCE_IMAGE_WIDTH,
                                 image_height=RESOURCE_IMAGE_HEIGHT,
                                 color=GOLD, space=SPACE * self.width,
                                 font_size=FONT_SIZE)[1]

        # produces
        curr_y = \
            draw_text_with_wrapping(curr_x, curr_y, max_message_width,
                                    "Produces",
                                    YELLOW, self.surface,
                                    FONT_SIZE)[0]
        curr_y = draw_items_info(self.sprite.produces, curr_x, curr_y,
                                 max_message_width, self,
                                 image_width=RESOURCE_IMAGE_WIDTH,
                                 image_height=RESOURCE_IMAGE_HEIGHT,
                                 space=SPACE * self.width,
                                 font_size=FONT_SIZE)[1]

        # consumes
        curr_y = \
            draw_text_with_wrapping(0, curr_y, max_message_width,
                                    "Consumes",
                                    RED, self.surface,
                                    FONT_SIZE)[0]
        curr_y = draw_items_info(self.sprite.consumes, curr_x, curr_y,
                                 max_message_width, self,
                                 image_width=RESOURCE_IMAGE_WIDTH,
                                 image_height=RESOURCE_IMAGE_HEIGHT,
                                 color=RED, space=SPACE * self.width,
                                 font_size=FONT_SIZE)[1]

        # required dwellers
        curr_y = draw_text_with_wrapping(0, curr_y, max_message_width,
                                         "Required dwellers",
                                         LIGHT_BLUE, self.surface,
                                         FONT_SIZE)[0]
        curr_y = draw_dwellers_info(self.sprite.dwellers_name, '{}'.format(
            self.sprite.required_dwellers),
                                    curr_x, curr_y, self,
                                    image_width=RESOURCE_IMAGE_WIDTH,
                                    image_height=RESOURCE_IMAGE_HEIGHT,
                                    color=LIGHT_BLUE,
                                    font_size=FONT_SIZE)

        self.surface = self.surface.subsurface(
            (0, 0, self.width, int(curr_y + MARGIN)))
        self.rect = self.surface.get_rect(topright=(self.pos_x, self.pos_y))
        self.rect.clamp_ip(self.blit_surface.get_rect())
