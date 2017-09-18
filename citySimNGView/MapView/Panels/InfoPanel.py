from CreatorView.RelativePaths import relative_textures_path

from MapView.Consts import BUILDINGS_PANEL_TEXTURE, GREEN, RED
from MapView.Items.Button import Button
from MapView.Panels.Panel import Panel
from MapView.Utils import draw_text
from MapView.Items.Resources import resources, draw_resources_info
import pygame

DELETE_BUILDING_BUTTON_HEIGHT = 0.25
DELETE_BUILDING_BUTTON_WIDTH = 0.1
STOP_PRODUCTION_BUTTON_WIDTH = 0.1
STOP_PRODUCTION_BUTTON_HEIGHT = 0.25
SPACE = 0.1


class InfoPanel(Panel):
    """ This class represents an instance of panel containing information about selected building. """
    def __init__(self, pos_x, pos_y, width, height, surface, del_building_fun, stop_production_fun):
        """ Constructor.

        :param pos_x: x position on screen
        :param pos_y: y position on screen
        :param width: panel's width
        :param height: panel's height
        :param surface: surface on which panel should be drawn
        :param del_building_fun: function performed when delete building button is clicked
        :param stop_production_fun: function performed when stop production button is clicked
        """
        Panel.__init__(self, pos_x, pos_y, width, height, BUILDINGS_PANEL_TEXTURE, surface)
        self.curr_building = None
        self.buttons_sprites = pygame.sprite.Group()

        self.del_building_button = Button(
            self.pos_x + self.width - DELETE_BUILDING_BUTTON_WIDTH * self.width,
            self.pos_y, DELETE_BUILDING_BUTTON_WIDTH * self.width, DELETE_BUILDING_BUTTON_HEIGHT * self.height,
            relative_textures_path + 'DeleteBuilding.png', del_building_fun, self)

        self.stop_production_button = Button(
            self.pos_x + self.width - STOP_PRODUCTION_BUTTON_WIDTH * self.width,
            self.pos_y + self.height * DELETE_BUILDING_BUTTON_HEIGHT + self.height * SPACE,
            STOP_PRODUCTION_BUTTON_WIDTH * self.width, STOP_PRODUCTION_BUTTON_HEIGHT * self.height,
            relative_textures_path + 'StopProduction.png', stop_production_fun, self)

        self.buttons_sprites.add(self.del_building_button, self.stop_production_button)

    def draw(self):
        """ Draw info panel with buttons and information about currently selected building.
        Before drawing in panel it is being cleaned.
        """
        self.clean()

        if self.curr_building:

            # draw buttons
            self.panels_surface.blit(self.del_building_button.image, (self.del_building_button.rect[0] - self.pos_x,
                                                                      self.del_building_button.rect[1] - self.pos_y))
            self.panels_surface.blit(self.stop_production_button.image,
                                     (self.stop_production_button.rect[0] - self.pos_x,
                                      self.stop_production_button.rect[1] - self.pos_y))
            self.buttons_sprites.add(self.del_building_button, self.stop_production_button)

            # draw text
            curr_y = draw_text(0, 0, self.curr_building.name, GREEN, self.panels_surface)[1]
            curr_x, curr_y = draw_text(0, curr_y, 'Produces: ', GREEN, self.panels_surface)
            curr_y = draw_resources_info(self.curr_building.produces, curr_x, curr_y, self.width, self.panels_surface, 20,
                                         20)
            curr_x = draw_text(0, curr_y, 'Consumes: ', RED, self.panels_surface)[0]
            curr_y = draw_resources_info(self.curr_building.consumes, curr_x, curr_y, self.width, self.panels_surface, 20,
                                         20)

        # draw panel
        self.surface.blit(self.panels_surface, (self.pos_x, self.pos_y))

    def set_stop_production_button_texture(self):
        """ Set texture for stop production button according to building state """
        if self.curr_building.is_running:
            self.stop_production_button.set_texture(relative_textures_path + 'StopProduction.png')
        else:
            self.stop_production_button.set_texture(relative_textures_path + 'Start.png')
