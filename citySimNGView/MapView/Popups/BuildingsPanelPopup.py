import pygame
import time
from MapView.Consts import BUILDINGS_PANEL_TEXTURE, GREEN, WHITE
from MapView.Items.Resources import draw_resources_info, resources
from MapView.Items.Resource import Resource
from MapView.Utils import draw_text_with_wrapping
from Popup import Popup


FONT_SIZE = 25
RESOURCE_IMAGE_WIDTH = 20
RESOURCE_IMAGE_HEIGHT = 20
MARGIN = 2


class BuildingsPanelPopup(Popup):
    def __init__(self, pos_x, pos_y, width, height, building, surface):
        Popup.__init__(self, pos_x, pos_y, building, width, height, surface)

        self.add_message()

    def add_message(self):
        curr_x, curr_y = MARGIN, MARGIN
        max_message_width = self. width - 2 * MARGIN

        # buildings name
        curr_y = draw_text_with_wrapping(curr_x, curr_y,  max_message_width, self.sprite.name, GREEN, self.surface,
                                         FONT_SIZE)[0]

        # cost
        curr_y = draw_text_with_wrapping(curr_x, curr_y,  max_message_width, "Cost", GREEN, self.surface, FONT_SIZE)[0]
        curr_y = draw_resources_info(self.sprite.resources_cost, curr_x, curr_y,  max_message_width,
                                     self, image_width=RESOURCE_IMAGE_WIDTH, image_height=RESOURCE_IMAGE_HEIGHT)

        # produces
        curr_y = draw_text_with_wrapping(curr_x, curr_y, max_message_width, "Produces", GREEN, self.surface,
                                         FONT_SIZE)[0]
        curr_y = draw_resources_info(self.sprite.produces, curr_x, curr_y,  max_message_width, self,
                                     image_width=RESOURCE_IMAGE_WIDTH, image_height=RESOURCE_IMAGE_HEIGHT)

        # consumes
        curr_y = draw_text_with_wrapping(0, curr_y,  max_message_width, "Consumes", GREEN, self.surface,
                                         FONT_SIZE)[0]
        curr_y = draw_resources_info(self.sprite.consumes, curr_x, curr_y,  max_message_width, self,
                                     image_width=RESOURCE_IMAGE_WIDTH, image_height=RESOURCE_IMAGE_HEIGHT)

        self.surface = self.surface.subsurface((0, 0, self.width, int(curr_y + MARGIN)))
        self.rect = self.surface.get_rect(topright=(self.pos_x, self.pos_y))
        self.rect.clamp_ip(self.blit_surface.get_rect())
