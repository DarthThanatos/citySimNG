import pygame
import time
from MapView.Consts import BUILDINGS_PANEL_TEXTURE, GREEN, WHITE
from MapView.Items.Resources import draw_resources_info
from MapView.Utils import draw_text_with_wrapping
from Popup import Popup


FONT_SIZE = 25
RESOURCE_IMAGE_WIDTH = 20
RESOURCE_IMAGE_HEIGHT = 20


class BuildingsPanelPopup(Popup):
    def __init__(self, pos_x, pos_y, width, height, building, surface):
        Popup.__init__(self, pos_x, pos_y, building, width, height, surface)

    def draw(self):
        # clean
        self.popup_surface = pygame.Surface.copy(self.image)

        curr_x, curr_y = 0, 0

        # buildings name
        curr_y = draw_text_with_wrapping(curr_x, curr_y, self.width, self.sprite.name, GREEN, self.popup_surface,
                                         FONT_SIZE)[0]

        # cost
        curr_y = draw_text_with_wrapping(curr_x, curr_y, self.width, "Cost", GREEN, self.popup_surface, FONT_SIZE)[0]
        curr_y = draw_resources_info(self.sprite.resources_cost, curr_x, curr_y, self.width, self.popup_surface,
                                     RESOURCE_IMAGE_WIDTH, RESOURCE_IMAGE_HEIGHT)

        # produces
        curr_y = draw_text_with_wrapping(curr_x, curr_y, self.width, "Produces", GREEN, self.popup_surface, FONT_SIZE)[0]
        curr_y = draw_resources_info(self.sprite.produces, curr_x, curr_y, self.width, self.popup_surface,
                                     RESOURCE_IMAGE_WIDTH, RESOURCE_IMAGE_HEIGHT)

        # consumes
        curr_y = draw_text_with_wrapping(0, curr_y, self.width, "Consumes", GREEN, self.popup_surface, FONT_SIZE)[0]
        curr_y = draw_resources_info(self.sprite.consumes, curr_x, curr_y, self.width, self.popup_surface,
                                     RESOURCE_IMAGE_WIDTH, RESOURCE_IMAGE_HEIGHT)

        self.popup_surface = self.popup_surface.subsurface((0, 0, self.width, int(curr_y)))
        self.rect = self.popup_surface.get_rect(topright=(self.pos_x, self.pos_y))
        self.rect.clamp_ip(self.surface.get_rect())
        self.surface.blit(self.popup_surface, self.rect, (0, 0, self.width, int(curr_y)))



